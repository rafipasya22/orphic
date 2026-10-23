# Orphic

Orphic is a web app that tells whether a song is AI-generated or human-made. Upload an audio file or paste a YouTube or Suno link. Orphic analyzes it with a CRNN model on mel-spectrograms and returns a verdict with a confidence score. Past results are saved to a personal history.

## Features

- Detect AI vs. human music from an uploaded file (`.wav` and `.mp3`) or a YouTube / Suno link
- Confidence score, plus per-slice breakdown and spectrogram visualization
- User accounts: signup, login, editable profile and avatar
- Prediction history with audio playback, per-day and bulk deletion
- JWT-protected API: every user can only read or delete their own data

## How it works

1. The audio is loaded at 22,050 Hz mono and RMS-normalized.
2. Ten 8-second slices are selected: 7 "informative" slices (ranked by spectral flux and centroid) and 3 random ones.
3. Each slice becomes a 128-bin mel-spectrogram (30–8000 Hz), converted to dB and normalized.
4. The CRNN scores the 10-slice stack, and the **median** score gives the final prediction (> 0.5 means AI).
5. Extra signals are computed for analysis: duration, dynamic range, room noise, and spectral repetition.

## Tech stack

| Layer    | Tech                                                            |
| -------- | --------------------------------------------------------------- |
| Frontend | Vue 3, TypeScript, Vite, Axios                                  |
| Backend  | FastAPI, TensorFlow/Keras, librosa, torchaudio, yt-dlp, ffmpeg  |
| Data     | Supabase (Postgres, Auth, Storage)                              |
| Deploy   | Docker Compose, Vercel (frontend), Tailscale Funnel (backend)   |

## Getting started

### Prerequisites

- Docker and Docker Compose, or Python 3.13 and Node 22 for local dev
- A Supabase project
- The trained model file placed at `backend/model/model_crnn_21April.keras`

### 1. Supabase

Create two tables.

- `profiles`: `id` (uuid, references `auth.users.id`), `email`, `username` (unique), `first_name`, `last_name`, `profile_picture_url`, `created_at`
- `prediction_history`: `id`, `user_id`, `song_title`, `prediction`, `confidence`, `probability`, `duration`, `audio_id`, `thumbnail`, `slices_meta` (jsonb), `created_at`, plus optional `dynamic_range`, `room_noise`, `spectral_repetition`

Also create a public Storage bucket named `profile_photo`. Enable RLS on both tables as a safety net. The backend uses the service-role key, which bypasses RLS, so access control is enforced in the API itself.

### 2. Environment variables

`backend/.env`

```env
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=<service_role key>      
SUPABASE_ANON_KEY=<anon key>
ALLOWED_ORIGINS=http://localhost:8080,http://localhost:5173
```

Root `.env` (used by Docker Compose, optional)

```env
VITE_API_URL=http://localhost:8000
```

### 3. Run with Docker

```bash
docker compose up --build -d
```

- Frontend: http://localhost:8080
- API: http://localhost:8000 (`GET /` returns `{"status":"udah"}` once the model has loaded)

Changing `VITE_API_URL` requires a frontend rebuild, because Vite bakes it in at build time:

```bash
docker compose build frontend
```

### Run without Docker

```bash
# backend
cd backend
python -m venv venv && venv\Scripts\activate      # source venv/bin/activate on macOS/Linux
pip install -r requirements.txt
uvicorn main:app --reload

# frontend
cd frontend
npm install
npm run dev
```

`ffmpeg` and `yt-dlp` must be installed and on your `PATH` for YouTube and Suno links.

## API overview

| Method | Endpoint                                 | Auth     | Description                      |
| ------ | ---------------------------------------- | -------- | -------------------------------- |
| GET    | `/`                                      | public   | Model status                     |
| POST   | `/api/signup`, `/api/login`, `/api/refresh` | public | Account and session              |
| POST   | `/predict`                               | optional | Predict from an uploaded file    |
| POST   | `/songs`                                 | optional | Predict from a YouTube/Suno link |
| GET    | `/api/profile/{user_id}`                 | JWT      | Get profile                      |
| POST   | `/api/changes`                           | JWT      | Update profile / avatar          |
| GET    | `/history/{user_id}`                     | JWT      | List prediction history          |
| GET    | `/dash/pred/{history_id}`                | JWT      | Single prediction                |
| DELETE | `/history/{id}`, `/history/user/{id}/all`, `/history/user/{id}/date/{date}` | JWT | Delete history |
| GET    | `/audio/info/{user_id}`                  | JWT      | List stored audio                |
| DELETE | `/audio/user/{audio_id}`, `/audio/user/{id}/all` | JWT | Delete stored audio              |
| GET    | `/audio/{audio_id}`, `/audio/thumb/{file}` | public | Stream audio / cover (unguessable UUIDs) |

Protected routes expect `Authorization: Bearer <access_token>`. A user can only access their own `user_id`, and any other id returns `403`. Guests can call `/predict` and `/songs` without a token, but results are not saved.


## Notes

- The model file, `audio/`, and `.env` files are gitignored. Never commit the `service_role` key.
- Audio and thumbnails are stored on the backend's disk (`backend/audio`). Mount it as a Docker volume to keep them across restarts.
- Detection is probabilistic. Treat results as an estimate, not proof.

## Acknowledgements

Built as an undergraduate thesis project on AI-generated music detection.
