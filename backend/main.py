from fastapi import FastAPI, File, UploadFile, HTTPException, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse  
from pydantic import BaseModel
import numpy as np
import librosa
import torch
import torchaudio
import random
import threading
import tempfile
import tensorflow as tf
from tensorflow.keras.models import load_model
from dotenv import load_dotenv
import os
from supabase import create_client
from postgrest.exceptions import APIError
import uuid
import traceback
import matplotlib.pyplot as plt
from fastapi.staticfiles import StaticFiles
import re
import matplotlib as mpl
from datetime import datetime, timedelta
from pydantic import BaseModel
import subprocess
import shutil
from mutagen.id3 import ID3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
import json
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

supabase_auth = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    )
}

class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str
    confirmPassword: str
    username: str
    firstName: str
    lastName: str

class YoutubeRequest(BaseModel):
    link: str
    userId: str | None = None

model = None
model_ready = False

SR = 22050
TARGET_RMS = 0.1
N_FFT = 2048
HOP = 512
N_MELS = 128
TARGET_TIME = 345
global_mean = 1.0557609
global_std = 0.16382909

def detect_source(link: str) -> str:
    host = urlparse(link).netloc.lower()
    if "youtube.com" in host or "youtu.be" in host:
        return "youtube"
    if "suno.com" in host or "suno.ai" in host:
        return "suno"
    return "unknown"

def _extract_suno_info(song_url: str):
    resp = requests.get(song_url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    audio_url = None
    title = None
    thumbnail_url = None

    og_audio = soup.find("meta", property="og:audio")
    if og_audio and og_audio.get("content"):
        audio_url = og_audio["content"]

    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        title = og_title["content"]

    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        thumbnail_url = og_image["content"]

    if not audio_url:
        match = re.search(r'https://cdn\d*\.suno\.(?:ai|com)/[a-f0-9\-]+\.mp3', html)
        if match:
            audio_url = match.group(0)

    if not title and soup.title:
        title = soup.title.string

    if not audio_url:
        raise ValueError("Tidak menemukan URL audio dari halaman Suno")

    return audio_url, (title or "suno_song"), thumbnail_url


def download_suno_song(link: str, temp_dir: str):
    """
    Download lagu dari link Suno, convert ke WAV, dan ambil thumbnail.
    Return: (wav_path, title, thumbnail_bytes, thumbnail_mime)
    """
    audio_url, title, thumbnail_url = _extract_suno_info(link)

    mp3_path = os.path.join(temp_dir, "source.mp3")
    with requests.get(audio_url, headers=HEADERS, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(mp3_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    wav_path = os.path.join(temp_dir, "source.wav")
    subprocess.run(
        ["ffmpeg", "-y", "-i", mp3_path, wav_path],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    thumbnail_bytes = None
    thumbnail_mime = "image/jpeg"
    if thumbnail_url:
        try:
            img_resp = requests.get(thumbnail_url, headers=HEADERS, timeout=20)
            img_resp.raise_for_status()
            thumbnail_bytes = img_resp.content
            content_type = img_resp.headers.get("Content-Type")
            if content_type:
                thumbnail_mime = content_type
        except requests.RequestException:
            pass

    return wav_path, title, thumbnail_bytes, thumbnail_mime

mel_transform = torchaudio.transforms.MelSpectrogram(
    sample_rate=SR,
    n_fft=N_FFT,
    hop_length=HOP,
    n_mels=N_MELS,
    f_min=30,
    f_max=8000,
    power=2.0
)

db_transform = torchaudio.transforms.AmplitudeToDB(
    stype="power",
    top_db=80
)

def process_slice(y_slice):
    y_slice = torch.tensor(y_slice, dtype=torch.float32)

    if y_slice.dim() == 1:
        y_slice = y_slice.unsqueeze(0)

    mel = mel_transform(y_slice)
    mel_db = db_transform(mel)

    mel_norm = (mel_db + 80) / 80

    return mel_norm.squeeze(0).numpy().astype(np.float32)


def fix_length(x):
    if x.shape[2] > TARGET_TIME:
        x = x[:, :, :TARGET_TIME]

    if x.shape[2] < TARGET_TIME:
        pad = TARGET_TIME - x.shape[2]

        x = np.pad(
            x,
            ((0,0), (0,0), (0,pad)),
            mode="reflect"
        )

    return x


def informative_slices_weighted(y, sr, slice_duration=8, n_slices=10):
    hop_length = 512
    slice_len = int(sr * slice_duration)
 
    S = np.abs(librosa.stft(y, hop_length=hop_length))
 
    flux = np.sqrt(np.sum(np.diff(S, axis=1)**2, axis=0))
    flux = (flux - flux.min()) / (flux.max() + 1e-8)
 
    centroid = librosa.feature.spectral_centroid(S=S, sr=sr)[0]
    centroid = (centroid - centroid.min()) / (centroid.max() + 1e-8)
 
    centroid = centroid[:len(flux)]
 
    alpha = 0.7
    beta = 0.3
 
    score = alpha * flux + beta * centroid
 
    frame_to_sample = lambda f: int(f * hop_length)
 
    candidates = []
 
    for i in range(len(score)):
        start = frame_to_sample(i)
        end = start + slice_len
 
        if end > len(y):
            continue
 
        candidates.append((score[i], start, end))
 
    candidates = sorted(candidates, key=lambda x: x[0], reverse=True)
 
    slices = []
    slice_meta = []  # NEW: metadata list, parallel to `slices`
    used = []
 
    for s, start, end in candidates:
        if any(abs(start - u) < slice_len for u in used):
            continue
 
        y_slice = y[start:end]
 
        if np.mean(np.abs(y_slice)) < 0.01:
            continue
 
        slices.append(y_slice)
        slice_meta.append({
            "start": round(start / sr, 2),   # seconds
            "end": round(end / sr, 2),       # seconds
            "type": "informative",
            "score": round(float(s), 4),
        })
        used.append(start)
 
        if len(slices) >= n_slices:
            break
 
    return slices, slice_meta  
 
 
def random_slices(y, sr, slice_duration=8, n_slices=10):
    slice_len = sr * slice_duration
    total_len = len(y)
 
    slices = []
    slice_meta = []  
 
    for _ in range(n_slices):
        start = random.randint(0, max(0, total_len - slice_len))
        end = start + slice_len
        y_slice = y[start:end]
 
        if np.mean(np.abs(y_slice)) < 0.01:
            continue
 
        slices.append(y_slice)
        slice_meta.append({
            "start": round(start / sr, 2),
            "end": round(end / sr, 2),
            "type": "random",
        })
 
    return slices, slice_meta 

def safe_folder_name(file_path: str):
    base = os.path.basename(file_path)          
    name = os.path.splitext(base)[0]            

    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '_', name)     
    name = name.strip('_')

    if not name:
        name = "audio"

    return name

def plot_spectro(spectrograms, song_folder, base_dir="spectrograms"):
    output_dir = os.path.join(base_dir, song_folder, "slices")
    os.makedirs(output_dir, exist_ok=True)

    filenames = []

    for i, mel in enumerate(spectrograms[:10]):
        filename = f"slice_{i}.png"
        path = os.path.join(output_dir, filename)

        plt.figure(figsize=(4, 3))
        plt.imshow(mel, aspect='auto', origin='lower', cmap='magma')
        plt.axis('off')

        plt.tight_layout(pad=0)
        plt.savefig(path, dpi=150, bbox_inches='tight', pad_inches=0)
        plt.close()

        filenames.append(filename)

    return filenames

def plot_legend(output_dir="spectrograms"):
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}_legend.png"
    path = os.path.join(output_dir, filename)

    fig, ax = plt.subplots(figsize=(1, 4))

    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    cmap = plt.cm.magma

    fig.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
        cax=ax,
        orientation='vertical'
    )

    ax.set_title("Intensity", fontsize=8)
    plt.tight_layout()

    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()

    return filename

def compute_room_noise(y, sr):
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=512)) ** 2
    frame_energy = S.mean(axis=0)
    threshold = np.percentile(frame_energy, 5)
    quiet_frames = S[:, frame_energy <= threshold]

    if quiet_frames.shape[1] < 3:
        return 0.0

    noise_floor = quiet_frames.mean(axis=1)
    return float(librosa.power_to_db(noise_floor.mean()))


def compute_spectral_repetition(y, sr):
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
    norms = np.linalg.norm(S, axis=0, keepdims=True)
    S_norm = S / (norms + 1e-8)
    corrs = []
    for lag in range(8, 33):
        c = np.mean(np.sum(S_norm[:, lag:] * S_norm[:, :-lag], axis=0))
        corrs.append(c)
    return float(np.mean(corrs)) 

def loadmodel():
    global model, model_ready
    model = load_model("C:\\Users\\Asus\\web_skripsi\\backend\\model\\model_crnn_21April.keras")
    model_ready = True

threading.Thread(target=loadmodel).start()

def predict_lagu(
    file_path,
    model,
    global_mean,
    global_std
):
    y, sr = librosa.load(
        file_path,
        sr=SR,
        mono=True
    )

    duration = round(len(y) / sr, 2)

    eremes = librosa.feature.rms(y=y)[0]
    dynamic_range = librosa.power_to_db(eremes.max()**2) - librosa.power_to_db(eremes.min()**2 + 1e-8)

    room_noise = compute_room_noise(y, sr)

    rms = np.sqrt(np.mean(y**2))
    y = y * (TARGET_RMS / (rms + 1e-8))

    spectral_repetition = compute_spectral_repetition(y, sr)

   
    informative, informative_meta = informative_slices_weighted(y, SR, n_slices=7)
    random_part, random_meta = random_slices(y, SR, n_slices=3)
    final_slices = (informative + random_part)[:10]
    slices_meta = (informative_meta + random_meta)[:10]   

    if len(final_slices) < 10:
        raise ValueError("Slice kurang dari 10")

    features = [process_slice(s) for s in final_slices]
    x = np.stack(features)
    x = fix_length(x)
    x = (x - global_mean) / (global_std + 1e-6)
    x = x[..., None]
    x = np.expand_dims(x, 0)

    preds = model.predict(x, verbose=0)[0].flatten()
    final_score = np.median(preds)

    pred_class = 1 if final_score > 0.5 else 0
    confidence = final_score if pred_class == 1 else (1 - final_score)

    return final_score, pred_class, confidence, slices_meta, duration

def save_thumbnail(image_data: bytes, audio_id: str, mime: str = "image/jpeg") -> str | None:
    ext = "jpg" if "jpeg" in mime else mime.split("/")[-1]
    thumb_filename = f"{audio_id}_thumb.{ext}"
    thumb_path = os.path.join(AUDIO_DIR, thumb_filename)
    with open(thumb_path, "wb") as f:
        f.write(image_data)
    return thumb_filename

def extract_thumbnail_bytes(file_path: str) -> tuple[bytes, str] | tuple[None, None]:
    try:
        if file_path.endswith(".mp3"):
            tags = ID3(file_path)
            for tag in tags.values():
                if hasattr(tag, "data") and tag.FrameID.startswith("APIC"):
                    return tag.data, tag.mime or "image/jpeg"

        elif file_path.endswith(".flac"):
            audio = FLAC(file_path)
            if audio.pictures:
                pic = audio.pictures[0]
                return pic.data, pic.mime or "image/jpeg"

        elif file_path.endswith(".m4a"):
            audio = MP4(file_path)
            if "covr" in audio.tags:
                cover = audio.tags["covr"][0]
                return bytes(cover), "image/jpeg"

    except Exception:
        pass
    return None, None

def run_prediction(
    file_path: str,
    filename: str,
    userId: str = None,
    song_title: str = None,      
    thumbnail_bytes: bytes = None, 
    thumbnail_mime: str = None,
):
    invalid_uuid = [None, "", "undefined", "null"]
    history_id = None

    if thumbnail_bytes is None:
        thumbnail_bytes, thumbnail_mime = extract_thumbnail_bytes(file_path)

    final_score, pred_class, confidence, slices_meta, duration = predict_lagu(
        file_path, model, global_mean, global_std
    )

    prediction_result = "AI" if int(pred_class) == 1 else "Human"

    audio_id = str(uuid.uuid4())
    ext = os.path.splitext(filename)[1].lower()
    dest_path = os.path.join(AUDIO_DIR, f"{audio_id}{ext}")
    shutil.copy2(file_path, dest_path)

    thumb_filename = None
    if thumbnail_bytes:
        thumb_filename = save_thumbnail(thumbnail_bytes, audio_id, thumbnail_mime or "image/jpeg")

    display_title = song_title or filename  

    if userId not in invalid_uuid:
        result = supabase.table("prediction_history").insert({
            "user_id": userId,
            "song_title": display_title,
            "prediction": prediction_result,
            "confidence": float(confidence),
            "probability": float(final_score),
            "duration": float(duration),
            "audio_id": audio_id,
            "thumbnail": thumb_filename,
            "slices_meta": slices_meta,  
        }).execute()

        if result.data:
            history_id = result.data[0]["id"]

    return {
        "history_id": history_id,
        "prediction": prediction_result,
        "confidence": float(confidence),
        "probability": float(final_score),
        "duration": duration,
        "audio_id": audio_id,
        "song_title": display_title,
        "slices_meta": slices_meta,
        "thumbnail_url": f"/audio/thumb/{thumb_filename}" if thumb_filename else None
    }

@app.get("/")
def root():
    if not model_ready:
        return {"status": "belum"}
    
    return {
        "status": "udah"
    }

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    userId: str = Form(None)
):
    if not model_ready:
        return {"error": "Model belum siap"}

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=os.path.splitext(file.filename)[1]
    ) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        return run_prediction(tmp_path, file.filename, userId)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

@app.post("/api/login")
def login(data: LoginRequest):

    try:

        response = supabase_auth.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })

        if response.user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        return {
            "success": True,

            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,

            "user": {
                "id": response.user.id,
                "email": response.user.email
            }
        }

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


@app.post("/api/signup")
def signup(data: SignupRequest):

    if not data.email:
        raise HTTPException(
            status_code=400,
            detail="Email is required"
        )

    if not data.username:
        raise HTTPException(
            status_code=400,
            detail="Username is required"
        )

    if not data.firstName:
        raise HTTPException(
            status_code=400,
            detail="First name is required"
        )

    if not data.lastName:
        raise HTTPException(
            status_code=400,
            detail="Last name is required"
        )

    if not data.password:
        raise HTTPException(
            status_code=400,
            detail="Password is required"
        )

    if data.password != data.confirmPassword:
        raise HTTPException(
            status_code=400,
            detail="Password does not match"
        )

    existing_username = supabase.table("profiles") \
        .select("username") \
        .eq("username", data.username) \
        .execute()

    if existing_username.data:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    try:

        auth_response = supabase_auth.auth.sign_up({  
            "email": data.email,
            "password": data.password
        })

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    user = auth_response.user

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Signup failed"
        )

    try:

        supabase.table("profiles").insert({
            "id": user.id,
            "email": data.email,
            "username": data.username,
            "first_name": data.firstName,
            "last_name": data.lastName,
            "profile_picture_url": None
        }).execute()

    except APIError:

        raise HTTPException(
            status_code=400,
            detail="Failed to create profile"
        )

    return {
        "success": True,
        "message": "Signup success",
        "user_id": user.id
    }

@app.get("/api/profile/{user_id}")
def get_profile(user_id: str):

    response = supabase.table("profiles") \
        .select("username, first_name, last_name, profile_picture_url") \
        .eq("id", user_id) \
        .single() \
        .execute()

    return response.data

@app.post("/api/changes")
async def change_profile(

    userId: str = Form(...),

    profileEmail: str = Form(None),
    profilePassword: str = Form(None),
    profileUsername: str = Form(None),
    profileFirstName: str = Form(None),
    profileLastName: str = Form(None),
    confirmProfilePassword: str = Form(None),

    profileImage: UploadFile = File(None)

):

    try:

        update_data = {}

        if profileEmail:

            update_data["email"] = profileEmail

        if profileUsername:

            username_check = supabase \
                .table("profiles") \
                .select("username") \
                .eq("username", profileUsername) \
                .neq("id", userId) \
                .execute()

            if username_check.data:

                raise HTTPException(
                    status_code=400,
                    detail="Username already exists"
                )

            update_data["username"] = profileUsername

        if profileFirstName:

            update_data["first_name"] = profileFirstName

        if profileLastName:

            update_data["last_name"] = profileLastName

        if profilePassword:

            if (
                profilePassword !=
                confirmProfilePassword
            ):

                raise HTTPException(
                    status_code=400,
                    detail="Password does not match"
                )

            supabase.auth.admin.update_user_by_id(
                userId,
                {
                    "password": profilePassword
                }
            )

        if profileImage:

            file_bytes = await profileImage.read()

            extension = (
                profileImage.filename
                .split(".")[-1]
            )

            filename = (
                f"{uuid.uuid4()}.{extension}"
            )

            supabase.storage \
                .from_("profile_photo") \
                .upload(
                    filename,
                    file_bytes,
                    {
                        "content-type":
                        profileImage.content_type
                    }
                )

            image_url = supabase.storage \
                .from_("profile_photo") \
                .get_public_url(filename)

            update_data[
                "profile_picture_url"
            ] = image_url

        if update_data:

            supabase \
                .table("profiles") \
                .update(update_data) \
                .eq("id", userId) \
                .execute()

        return {
            "success": True,
            "message": "Profile updated"
        }

    except Exception as e:

        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/history/{user_id}")
def get_history(user_id: str):

    try:

        response = supabase \
            .table("prediction_history") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .execute()

        return response.data

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/dash/pred/{history_id}")
def get_predss(history_id: str):

    try:

        response = supabase \
            .table("prediction_history") \
            .select("*") \
            .eq("id", history_id)\
            .order("created_at", desc=True) \
            .execute()

        return response.data

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.delete("/history/{history_id}")
def delete_history(history_id: str):

    try:

        supabase \
            .table("prediction_history") \
            .delete() \
            .eq("id", history_id) \
            .execute()

        return {
            "success": True,
            "message": "History deleted"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.delete("/history/user/{user_id}/date/{date}")
def delete_history_thisday(date: str, user_id: str):

    parsed_date = datetime.strptime(date, "%Y-%m-%d").date()

    start = parsed_date.isoformat()
    end = (parsed_date + timedelta(days=1)).isoformat()

    try:

        supabase \
            .table("prediction_history") \
            .delete() \
            .eq("user_id", user_id) \
            .gte("created_at", start) \
            .lt("created_at", end) \
            .execute()

        return {
            "success": True,
            "message": f"history at {date} deleted"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@app.delete("/history/user/{user_id}/all")
def delete_all_history(user_id: str):

    try:

        supabase \
            .table("prediction_history") \
            .delete() \
            .eq("user_id", user_id) \
            .execute()

        return {
            "success": True,
            "message": "All history deleted"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        

@app.post("/songs")
async def predict_from_link(data: YoutubeRequest):
    if not model_ready:
        return {"error": "Model belum siap"}

    source = detect_source(data.link)
    if source == "unknown":
        return {"error": "Link tidak dikenali. Hanya mendukung YouTube dan Suno."}

    temp_dir = tempfile.mkdtemp()

    try:
        if source == "youtube":
            output_template = os.path.join(temp_dir, "%(id)s.%(ext)s")

            subprocess.run([
                "yt-dlp",
                "--no-playlist",
                "-f", "bestaudio/best",
                "-x",
                "--audio-format", "wav",
                "--write-thumbnail",
                "--convert-thumbnails", "jpg",
                "-o", output_template,
                data.link
            ], check=True)

            wav_file = None
            thumb_file = None

            for f in os.listdir(temp_dir):
                full = os.path.join(temp_dir, f)
                if f.endswith(".wav"):
                    wav_file = full
                elif f.endswith(".jpg") or f.endswith(".webp") or f.endswith(".png"):
                    thumb_file = full

            if wav_file is None:
                raise Exception("WAV file tidak ditemukan")

            info_result = subprocess.run([
                "yt-dlp", "--dump-json", "--no-playlist", data.link
            ], capture_output=True, text=True, check=True)

            info = json.loads(info_result.stdout)
            title = info.get("title") or os.path.basename(wav_file)
            artist = info.get("artist") or info.get("uploader") or None

            song_title = f"{title} - {artist}" if artist else title

            thumbnail_bytes = None
            thumbnail_mime = "image/jpeg"
            if thumb_file:
                with open(thumb_file, "rb") as f:
                    thumbnail_bytes = f.read()

        else:  
            wav_file, title, thumbnail_bytes, thumbnail_mime = download_suno_song(
                data.link, temp_dir
            )
            song_title = title

        return run_prediction(
            wav_file,
            os.path.basename(wav_file),
            data.userId,
            song_title=song_title,
            thumbnail_bytes=thumbnail_bytes,
            thumbnail_mime=thumbnail_mime,
        )

    except Exception as e:
        return {"error": str(e)}

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}

@app.get("/audio/thumb/{filename}")  
async def serve_thumbnail(filename: str):
    thumb_path = os.path.join(AUDIO_DIR, filename)

    if not os.path.exists(thumb_path):
        raise HTTPException(status_code=404, detail="Thumbnail tidak ditemukan")

    return FileResponse(path=thumb_path, media_type="image/jpeg")

@app.get("/audio/{audio_id}")
async def serve_audio(audio_id: str):
    matched = [
        f for f in os.listdir(AUDIO_DIR)
        if f.startswith(audio_id)
        and os.path.splitext(f)[1].lower() in AUDIO_EXTENSIONS
    ]

    if not matched:
        raise HTTPException(status_code=404, detail="Audio tidak ditemukan")

    file_path = os.path.join(AUDIO_DIR, matched[0])
    ext = os.path.splitext(matched[0])[1].lower()
    mime_map = {
        ".wav": "audio/wav",
        ".mp3": "audio/mpeg",
        ".flac": "audio/flac",
        ".ogg": "audio/ogg",
        ".m4a": "audio/mp4",
    }

    return FileResponse(
        path=file_path,
        media_type=mime_map.get(ext, "audio/wav")
    )


@app.delete("/audio/user/{audio_id}")
async def delete_audio(audio_id: str):
    matched = [
        f for f in os.listdir(AUDIO_DIR)
        if f.startswith(audio_id) and f.lower().endswith((".mp3", ".wav"))
    ]

    if not matched:
        raise HTTPException(status_code=404, detail="Audio tidak ditemukan")

    for f in matched:
        os.remove(os.path.join(AUDIO_DIR, f))

    supabase.table("prediction_history") \
        .update({"audio_id": None}) \
        .eq("audio_id", audio_id) \
        .execute()

    return {"success": True, "message": "Audio deleted"}


@app.delete("/audio/user/{user_id}/all")
async def delete_all_audio(user_id: str):
    response = supabase.table("prediction_history") \
        .select("audio_id") \
        .eq("user_id", user_id) \
        .execute()

    deleted = []
    not_found = []

    for row in response.data:
        audio_id = row.get("audio_id")
        if not audio_id:
            continue

        matched = [
            f for f in os.listdir(AUDIO_DIR)
            if f.startswith(audio_id) and f.lower().endswith((".mp3", ".wav"))
        ]

        for f in matched:
            os.remove(os.path.join(AUDIO_DIR, f))

        if matched:
            deleted.append(audio_id)
        else:
            not_found.append(audio_id)

    supabase.table("prediction_history") \
        .update({"audio_id": None}) \
        .eq("user_id", user_id) \
        .execute()

    return {
        "success": True,
        "deleted": len(deleted),
        "not_found": len(not_found)
    }

@app.get("/audio/info/{user_id}")
async def get_audio_info(user_id: str):
    result = supabase.table("prediction_history") \
        .select("audio_id, song_title, duration") \
        .eq("user_id", user_id) \
        .execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Tidak ada audio milik user ini")

    files = []
    for row in result.data:
        audio_id = row["audio_id"]
        if not audio_id:
            continue

        matched = [
            f for f in os.listdir(AUDIO_DIR)
            if f.startswith(audio_id)
        ]

        if matched:
            files.append({
                "audio_id": audio_id,
                "filename": row["song_title"],
                "duration": row["duration"],
                "file_path": os.path.join(AUDIO_DIR, matched[0])
            })

    return files