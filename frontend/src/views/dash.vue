<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue';
import { gantiBahasaFunc } from '../composable/gantiBahasa';
import ModalLogin from '../components/modalLogin.vue';
import { openWarningFunc } from '../composable/openWarning';
import OpenWarning from '../components/modalWarning.vue';
import { darkFunc } from '../composable/darkMode';
import Menu from '../components/menu.vue';
import WaveSurfer from 'wavesurfer.js';
import axios from 'axios';
import { nextTick } from 'vue';
import { loadmodelfunc } from '../composable/loadmodel';
import { isuserloggedinFunc } from '../composable/isUserLoggedIn';
import { activefunc } from '../composable/active';
import Sidebar from '../components/sidebar.vue';
import { useAuthStore } from '../stores/authstore';
import { useRouter } from 'vue-router';
import uploadBar from '../components/uploadBar.vue';
import { loadingFunc } from '../composable/globalVar.ts';

const authStore = useAuthStore();
const { predLoading } = loadingFunc();
const router = useRouter();
const { isDarkMode } = darkFunc();
const { isUserLoggedin } = isuserloggedinFunc();
const { isDashActive, isHistoryActive, isHelpActive } = activefunc();
const { openWarning } = openWarningFunc();
const { modelLagiLoading } = loadmodelfunc();
const errMsg = ref<string | null>(null);
const waveformRef = ref<HTMLElement | null>(null);
const wavesurfer = ref<any>(null);
const lagiLoading = ref(false);
const currentUrl = ref<string | null>(null);
const isPlaying = ref(false);
const hasilAda = ref(false);
const { isLangEnglish } = gantiBahasaFunc();
const profile = ref<any>(null);
const spectroUrl = ref([]);
const legendSpectro = ref('');
const compareMode = ref(false);
const compareIndex = ref(1);

const isDragging = ref(false);
const files = ref<File[]>([]);
const hasilPredict = ref(null);
const probability = ref(null);
const confidenceLevel = ref(null);

const dynamicRange = ref<number | null>(null);
const energyVar = ref<number | null>(null);
const flatnessMean = ref<number | null>(null);
const centroidMean = ref<number | null>(null);
const meanConf = ref<number | null>(null);
const stdConf = ref<number | null>(null);
const expanded = ref(false);
const sliceProbs = ref([]);
const isUserCurrentlyLoggedIn = ref(false);

const namaLagu = ref<string | null>(null);
const dots = ref('.');
let interval: ReturnType<typeof setInterval> | null = null;

const filterAudioFiles = (fileList: File[]) => {
  const allowedTypes = ['audio/mpeg', 'audio/wav'];

  return fileList.filter((file) => allowedTypes.includes(file.type));
};

const handleDrop = (e: DragEvent) => {
  e.preventDefault();
  isDragging.value = false;

  const droppedFiles = Array.from(e.dataTransfer?.files || []);

  files.value = filterAudioFiles(droppedFiles);
};

const nextCompare = () => {
  let next = compareIndex.value >= spectroUrl.value.length - 1 ? 0 : compareIndex.value + 1;

  if (next === currentIndex.value) {
    next = next >= spectroUrl.value.length - 1 ? 0 : next + 1;
  }

  compareIndex.value = next;
};

const prevCompare = () => {
  let prev = compareIndex.value <= 0 ? spectroUrl.value.length - 1 : compareIndex.value - 1;

  if (prev === currentIndex.value) {
    prev = prev <= 0 ? spectroUrl.value.length - 1 : prev - 1;
  }

  compareIndex.value = prev;
};

const handleDragOver = (e: DragEvent) => {
  e.preventDefault();
  isDragging.value = true;
};

const handleDragLeave = () => {
  isDragging.value = false;
};

const tutupHasil = () => {
  hasilAda.value = false;
};

const handleFileSelect = (e: Event) => {
  const input = e.target as HTMLInputElement;
  const selectedFiles = Array.from(input.files || []);

  files.value = filterAudioFiles(selectedFiles);

  input.value = '';
};

const interpretScore = computed(() => {
  let score = 0;

  const mean = meanConf.value ?? 0;
  const std = stdConf.value ?? 0;
  const dr = dynamicRange.value ?? 0;
  const flat = flatnessMean.value ?? 0;

  if (mean >= 0.85) score += 5;
  else if (mean >= 0.7) score += 4;
  else if (mean >= 0.5) score += 2;
  else if (mean >= 0.3) score += 1;
  else score -= 3;

  if (std <= 0.03) score += 2;
  else if (std <= 0.08) score += 1;

  if (dr <= 0.08) score += 2;
  else if (dr <= 0.18) score += 1;

  if (flat <= 0.08) score += 2;
  else if (flat <= 0.2) score += 1;

  return score;
});

const interpretationDetail = computed(() => {
  const score = interpretScore.value;

  if (isLangEnglish.value) {
    if (score >= 7) {
      return 'The audio exhibits multiple characteristics frequently associated with AI-generated music.';
    }

    if (score >= 4) {
      return 'The audio contains several characteristics that may resemble AI-generated music patterns.';
    }

    if (score >= 2) {
      return 'The audio shows mixed acoustic characteristics with limited indicators of AI-generated patterns.';
    }

    return 'The audio demonstrates more natural acoustic variation and fewer characteristics associated with AI-generated music.';
  }

  if (score >= 7) {
    return 'Audio menunjukkan berbagai karakteristik yang sering dikaitkan dengan musik hasil generasi AI.';
  }

  if (score >= 4) {
    return 'Audio mengandung beberapa karakteristik yang dapat menyerupai pola musik hasil generasi AI.';
  }

  if (score >= 2) {
    return 'Audio menunjukkan karakteristik akustik campuran dengan indikasi terbatas terhadap pola musik AI.';
  }

  return 'Audio menunjukkan variasi akustik yang lebih alami dengan lebih sedikit karakteristik yang umum dikaitkan dengan musik hasil generasi AI.';
});

watch(files, async (newFiles) => {
  if (newFiles.length === 0) {
    if (wavesurfer.value) {
      wavesurfer.value.stop();
      wavesurfer.value.empty();
    }

    if (currentUrl.value) {
      URL.revokeObjectURL(currentUrl.value);
      currentUrl.value = null;
    }

    return;
  }

  const file = newFiles[0];
  if (!file) return;

  await nextTick();

  if (!wavesurfer.value && waveformRef.value) {
    wavesurfer.value = WaveSurfer.create({
      container: waveformRef.value,
      waveColor: '#333333',
      progressColor: '#83009a',
      height: 160,
    });

    wavesurfer.value.on('play', () => (isPlaying.value = true));
    wavesurfer.value.on('pause', () => (isPlaying.value = false));
    wavesurfer.value.on('finish', () => (isPlaying.value = false));

    wavesurfer.value.on('load', () => (lagiLoading.value = true));
    wavesurfer.value.on('ready', () => (lagiLoading.value = false));
    wavesurfer.value.on('error', () => (lagiLoading.value = false));
  }

  if (!wavesurfer.value) return;

  if (currentUrl.value) {
    URL.revokeObjectURL(currentUrl.value);
  }

  const url = URL.createObjectURL(file);
  currentUrl.value = url;

  wavesurfer.value.load(url);
});

const currentIndex = ref(0);

const next = () => {
  if (currentIndex.value < spectroUrl.value.length - 1) {
    currentIndex.value++;
  }
};

const prev = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--;
  }
};

watch(
  () => spectroUrl,
  (newVal) => {
    currentIndex.value = 0;
  },
);

watch(currentIndex, (val) => {
  if (compareIndex.value === val) {
    compareIndex.value = val + 1 >= spectroUrl.value.length ? 0 : val + 1;
  }
});

const uploadLagu = async () => {
  const user = authStore.user;
  predLoading.value = true;
  expanded.value = false;
  const file = files.value[0];
  if (file) {
    namaLagu.value = file?.name;
  }

  if (!file) {
    console.log('No file');
    return;
  }

  const formData = new FormData();
  formData.append('file', file);
  formData.append('userId', user.id);

  try {
    const res = await fetch('http://127.0.0.1:8000/predict', {
      method: 'POST',
      body: formData,
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || 'Server error');
    }

    if (data.error) {
      throw new Error(data.error);
    }

    hasilPredict.value = data.prediction;
    confidenceLevel.value = data.confidence;
    probability.value = data.probability;
    sliceProbs.value = data.slice_probs;
    dynamicRange.value = data.analysis.audio_features.dynamic_range;
    energyVar.value = data.analysis.audio_features.energy_variance;
    flatnessMean.value = data.analysis.audio_features.spectral_flatness;
    centroidMean.value = data.analysis.audio_features.spectral_centroid;
    meanConf.value = data.analysis.slice.mean_confidence;
    stdConf.value = data.analysis.slice.std_confidence;
    spectroUrl.value = data.analysis.spectrogram.slices;
    legendSpectro.value = data.analysis.spectrogram.legend;

    console.log('Received data:', {
      hasilPredict: hasilPredict.value,
      confidenceLevel: confidenceLevel.value,
      probability: probability.value,
      dynamicRange: dynamicRange.value,
      energyVar: energyVar.value,
      flatnessMean: flatnessMean.value,
      centroidMean: centroidMean.value,
      meanConf: meanConf.value,
      stdConf: stdConf.value,
      spectroUrl: spectroUrl.value,
      sliceProbs: sliceProbs.value,
    });

    hasilAda.value = true;
  } catch (error) {
    console.error(error);

    errMsg.value = error instanceof Error ? error.message : 'Unknown error';

    hasilAda.value = false;
  } finally {
    predLoading.value = false;
  }
};

const hasilPreds = computed(() => {
  if (probability.value == null) {
    return '';
  }

  if (probability.value >= 0.8) {
    return isLangEnglish.value ? 'Almost certainly AI-generated' : 'Hampir pasti buatan AI';
  }

  if (probability.value >= 0.5) {
    return isLangEnglish.value ? 'Likely AI-generated' : 'Kemungkinan besar buatan AI';
  }

  if (probability.value >= 0.2) {
    return isLangEnglish.value ? 'Likely Human-made' : 'Kemungkinan besar buatan manusia';
  }

  return isLangEnglish.value ? 'Almost certainly Human-made' : 'Hampir pasti buatan manusia';
});

const handleAudioUpload = async (file: File) => {
  const user = authStore.user;
  predLoading.value = true;
  const formData = new FormData();

  formData.append('file', file);

  formData.append('userId', user.id);

  try {
    const res = await fetch('http://127.0.0.1:8000/predict', {
      method: 'POST',
      body: formData,
    });

    const data = await res.json();

    const historyId = data.history_id;

    router.push(`/dash/predictions/${historyId}`);
  } catch (err) {
    console.error(err);
  } finally {
    predLoading.value = false;
  }
};

onMounted(async () => {
  isDashActive.value = true;
  isHistoryActive.value = false;
  isHelpActive.value = false;
  const user = authStore.user;

  const res = await axios.get(`http://localhost:8000/api/profile/${user.id}`);

  profile.value = res.data;

  interval = setInterval(() => {
    dots.value = dots.value.length >= 5 ? '.' : dots.value + '.';
  }, 400);
});

onUnmounted(() => {
  if (wavesurfer.value) {
    wavesurfer.value.destroy();
  }

  if (interval) clearInterval(interval);
});
</script>

<template>
  <div
    v-if="!isDarkMode"
    class="background w-full h-screen bg-white flex flex-row items-start justify-start"
  >
    <Sidebar />

    <div v-if="authStore.user" class="right relative w-full h-full">
      <div
        class="h-full overflow-y-scroll w-full container-content flex flex-col items-start justify-start overflow-y-scroll"
      >
        <div class="top w-full h-max-20 flex flex-row justify-between items-center px-4 py-3">
          <p class="text-base !font-semibold text-black">
            {{ isLangEnglish ? 'Dashboard' : 'Dashboard' }}
          </p>
          <div
            v-if="!modelLagiLoading"
            class="model-ready px-2 py-1 flex flex-row justify-center items-center bg-[#EBEBEB] gap-2 rounded-[5px]"
          >
            <div class="bulet rounded-full h-2 w-2 bg-[#83009a]"></div>
            <p class="text-sm text-black">{{ isLangEnglish ? 'Model Ready' : 'Model Siap' }}</p>
          </div>
          <div
            v-else
            class="model-ready px-2 py-1 flex flex-row justify-center items-center bg-[#EBEBEB] gap-2 rounded-[5px]"
          >
            <div
              class="w-4 h-4 border-4 border-gray-300 border-t-purple-700 rounded-full animate-spin"
            ></div>
            <p class="text-sm text-black">{{ isLangEnglish ? 'Loading Model' : 'Memuat Model' }}</p>
          </div>
        </div>
        <div
          v-if="predLoading"
          class="content w-full h-full flex flex-col justify-center items-center"
        >
          <div class="flex items-center gap-2">
            <span class="jump-dot"></span>
            <span class="jump-dot"></span>
            <span class="jump-dot"></span>
          </div>
        </div>
        <div v-else class="content w-full h-full flex flex-col justify-center items-center">
          <p class="text-[#83009a] text-center !font-bold !text-lg break-words">{{isLangEnglish ? 'Welcome!' :'Selamat Datang!'}}</p>
          <p class="text-black text-center !text-lg break-words !font-bold">
            {{ isLangEnglish? 'What are we listening to today? Upload a file or paste a link below.':'Apa yang akan kita dengarkan hari ini? Unggah file atau tempelkan tautan di bawah ini.'}}
          </p>
        </div>
      </div>

      <uploadBar @upload="handleAudioUpload" />
    </div>
  </div>
  <div
    v-else
    class="background w-full h-screen bg-[#090909] flex flex-row items-start justify-start"
  >
    <Sidebar />

    <div v-if="authStore.user" class="right relative w-full h-full">
      <div
        class="h-full overflow-y-scroll w-full container-content flex flex-col items-start justify-start overflow-y-scroll"
      >
        <div class="top w-full h-max-20 flex flex-row justify-between items-center px-4 py-3">
          <p class="text-base !font-semibold text-white">
            {{ isLangEnglish ? 'Prediction Result' : 'Hasil Prediksi' }}
          </p>
          <div
            v-if="!modelLagiLoading"
            class="model-ready px-2 py-1 flex flex-row justify-center items-center bg-[#1b1b1b] gap-2 rounded-[5px]"
          >
            <div class="bulet rounded-full h-2 w-2 bg-[#83009a]"></div>
            <p class="text-sm text-white">{{ isLangEnglish ? 'Model Ready' : 'Model Siap' }}</p>
          </div>
          <div
            v-else
            class="model-ready px-2 py-1 flex flex-row justify-center items-center bg-[#1b1b1b] gap-2 rounded-[5px]"
          >
            <div
              class="w-4 h-4 border-4 border-gray-300 border-t-purple-700 rounded-full animate-spin"
            ></div>
            <p class="text-sm text-white">{{ isLangEnglish ? 'Loading Model' : 'Memuat Model' }}</p>
          </div>
        </div>
        <div
          v-if="predLoading"
          class="content w-full h-full flex flex-col justify-center items-center"
        >
          <div class="flex items-center gap-2">
            <span class="jump-dot"></span>
            <span class="jump-dot"></span>
            <span class="jump-dot"></span>
          </div>
        </div>
        <div v-else class="content w-full h-full flex flex-col justify-center items-center">
          <p class="text-[#83009a] text-center !font-bold !text-lg break-words">{{isLangEnglish ? 'Welcome!' :'Selamat Datang!'}}</p>
          <p class="text-white text-center !text-lg break-words !font-bold">
            {{ isLangEnglish? 'What are we listening to today? Upload a file or paste a link below.':'Apa yang akan kita dengarkan hari ini? Unggah file atau tempelkan tautan di bawah ini.'}}
          </p>
        </div>
      </div>

      <uploadBar @upload="handleAudioUpload" />
    </div>
  </div>
  <Menu :isUserLoggedin="isUserLoggedin" />
  <OpenWarning />
  <ModalLogin />
</template>
