<script setup lang="ts">
import { API_URL } from '@/config'
import { ref, onMounted, onUnmounted, watch, computed } from 'vue';
import { gantiBahasaFunc } from '../composable/gantiBahasa.ts';
import ModalLogin from '../components/modalLogin.vue';
import { openWarningFunc } from '../composable/openWarning.ts';
import OpenWarning from '../components/modalWarning.vue';
import { darkFunc } from '../composable/darkMode.ts';
import Menu from '../components/menu.vue';
import WaveSurfer from 'wavesurfer.js';
import axios from 'axios';
import { nextTick } from 'vue';
import { loadmodelfunc } from '../composable/loadmodel.ts';
import { isuserloggedinFunc } from '../composable/isUserLoggedIn.ts';
import { activefunc } from '../composable/active.ts';
import Sidebar from '../components/sidebar.vue';
import Uploadbar from '../components/uploadBar.vue';
import { useAuthStore } from '../stores/authstore.ts';
import { useRoute, useRouter } from 'vue-router';
import { loadingFunc } from '../composable/globalVar.ts';
import WaveformSlices from '../components/haduh.vue';
import sliceExpla from '../components/expla.vue';

const route = useRoute();
const router = useRouter();

const authStore = useAuthStore();
const { isDarkMode } = darkFunc();
const { isUserLoggedin } = isuserloggedinFunc();
const { isDashActive, isHistoryActive, isHelpActive } = activefunc();
const { openWarning } = openWarningFunc();
const { modelLagiLoading } = loadmodelfunc();
const { predLoading, isCollapsed } = loadingFunc();
const errMsg = ref<string | null>(null);
const waveformRef = ref<HTMLElement | null>(null);
const wavesurfer = ref<any>(null);
const lagiLoading = ref(false);
const currentUrl = ref<string | null>(null);
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

const energyVar = ref<number | null>(null);
const flatnessMean = ref<number | null>(null);
const centroidMean = ref<number | null>(null);
const meanConf = ref<number | null>(null);
const stdConf = ref<number | null>(null);
const expanded = ref(false);
const sliceProbs = ref([]);

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

const handleLoading = (value: boolean) => {
  predLoading.value = value;
};

const handleFileSelect = (e: Event) => {
  const input = e.target as HTMLInputElement;
  const selectedFiles = Array.from(input.files || []);

  files.value = filterAudioFiles(selectedFiles);

  input.value = '';
};

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

const handleAudioUpload = async (file: File) => {
  const user = authStore.user;
  predLoading.value = true;
  const formData = new FormData();

  formData.append('file', file);

  formData.append('userId', user.id);

  try {
    const res = await fetch(`${API_URL}/predict`, {
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

const preds = ref<any[]>([]);

watch(
  () => preds.value[0]?.song_title,
  (title) => {
    document.title = title ? `Orphic | ${title} prediction` : 'Orphic | Prediction';
  },
  { immediate: true },
);

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

const isPlaying = ref(false);
const src = computed(() => {
  const audioId = preds.value[0]?.audio_id;
  if (!audioId) return '';
  return `${API_URL}/audio/${audioId}`;
});

watch(src, async (newSrc) => {
  if (!newSrc || !audio.value) return;
  await nextTick();
  audio.value.load();
  currentTime.value = 0;
  isPlaying.value = false;
});

const audio = ref<HTMLAudioElement>();
const currentTime = ref(0);
const duration = ref(0);
const progressBar = ref<HTMLElement>();

const formatTime = (seconds: number) => {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);

  return `${mins}:${secs.toString().padStart(2, '0')}`;
};

const progress = computed(() => {
  if (!duration.value) return 0;
  return (currentTime.value / duration.value) * 100;
});

const togglePlay = () => {
  if (!audio.value) return;

  if (isPlaying.value) {
    audio.value.pause();
  } else {
    audio.value.play();
  }
};

const seek = (event: MouseEvent) => {
  if (!audio.value || !progressBar.value) return;

  const rect = progressBar.value.getBoundingClientRect();
  const percentage = (event.clientX - rect.left) / rect.width;

  audio.value.currentTime = percentage * duration.value;
};

const getRelativeTime = (dateString: string) => {
  const rtf = new Intl.RelativeTimeFormat(isLangEnglish.value ? 'en' : 'id', { numeric: 'always' });

  const normalized = dateString.endsWith('Z') ? dateString : dateString + 'Z';
  const diffSeconds = Math.floor((Date.now() - new Date(normalized).getTime()) / 1000);

  const prefix = isLangEnglish.value ? 'Scanned' : 'Dipindai';

  if (diffSeconds < 60) return isLangEnglish.value ? 'Scanned just now' : 'Baru saja dipindai';

  const diffMinutes = Math.floor(diffSeconds / 60);
  if (diffMinutes < 60) return `${prefix} ${rtf.format(-diffMinutes, 'minute')}`;

  const diffHours = Math.floor(diffMinutes / 60);
  if (diffHours < 24) return `${prefix} ${rtf.format(-diffHours, 'hour')}`;

  const diffDays = Math.floor(diffHours / 24);
  return `${prefix} ${rtf.format(-diffDays, 'day')}`;
};

const logos = [
  {
    tag: 'edit_audio',
  },
  {
    tag: 'waves',
  },
  {
    tag: 'cadence',
  },
];

function fromattwaktu(sec: any) {
  if (sec == null || isNaN(sec)) return '0:00';
  const m = Math.floor(sec / 60);
  const s = Math.round(sec % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
}

const predsDetails = computed(() => {
  const slices = preds.value[0]?.slices_meta ?? [];
  const informative = slices.filter((s: any) => s.type === 'informative');

  const scores = informative.map((s: any) => s.score).filter((s: any) => s != null);
  const minScore = scores.length ? Math.min(...scores) : null;
  const maxScore = scores.length ? Math.max(...scores) : null;
  const avgScore = scores.length
    ? scores.reduce((a: any, b: any) => a + b, 0) / scores.length
    : null;

  const starts = slices.map((s: any) => s.start);
  const ends = slices.map((s: any) => s.end);
  const earliestStart = starts.length ? Math.min(...starts) : null;
  const latestEnd = ends.length ? Math.max(...ends) : null;

  return isLangEnglish.value ? [
    {
      category: 'Informative Score Range',
      value:
        minScore != null && maxScore != null
          ? `${minScore.toFixed(2)} – ${maxScore.toFixed(2)}`
          : '-',
      class: (() => {
        if (minScore == null || maxScore == null) return '';
        const spread = maxScore - minScore;
        if (spread >= 0.15) return 'Wide Spread';
        if (spread >= 0.05) return 'Moderate Spread';
        return 'Narrow Spread';
      })(),
      classColor: 'text-[#83009a]',
    },
    {
      category: 'Informative Score Avg',
      value: avgScore != null ? avgScore.toFixed(2) : '-',
      class: '',
      classColor: 'text-[#83009a]',
    },
    {
      category: 'Analysis Time Range',
      value:
        earliestStart != null && latestEnd != null
          ? `${fromattwaktu(earliestStart)} – ${fromattwaktu(latestEnd)}`
          : '-',
      class: '',
      classColor: 'text-[#83009a]',
    },
  ]

  :

  [
    {
      category: 'Rentang Skor Informatif',
      value:
        minScore != null && maxScore != null
          ? `${minScore.toFixed(2)} – ${maxScore.toFixed(2)}`
          : '-',
      class: (() => {
        if (minScore == null || maxScore == null) return '';
        const spread = maxScore - minScore;
        if (spread >= 0.15) return 'Sebaran Lebar';
        if (spread >= 0.05) return 'Sebaran Sedang';
        return 'Sebaran Sempit';
      })(),
      classColor: 'text-[#83009a]',
    },
    {
      category: 'Rata-rata Skor Informatif',
      value: avgScore != null ? avgScore.toFixed(2) : '-',
      class: '',
      classColor: 'text-[#83009a]',
    },
    {
      category: 'Rentang Waktu Analisis',
      value:
        earliestStart != null && latestEnd != null
          ? `${fromattwaktu(earliestStart)} – ${fromattwaktu(latestEnd)}`
          : '-',
      class: '',
      classColor: 'text-[#83009a]',
    },
  ];


});

watch(
  () => route.params.historyId,
  async (historyId) => {
    if (!historyId) return;

    const res = await axios.get(`${API_URL}/dash/pred/${historyId}`);

    preds.value = res.data;
    console.log('valpreds', preds.value);
    console.log('src: ', src);
  },
  {
    immediate: true,
  },
);

onMounted(async () => {
  isDashActive.value = true;
  isHistoryActive.value = false;
  isHelpActive.value = false;
  const user = authStore.user;

  const res = await axios.get(`${API_URL}/api/profile/${user.id}`);

  profile.value = res.data;

  interval = setInterval(() => {
    dots.value = dots.value.length >= 5 ? '.' : dots.value + '.';
  }, 400);
});

onUnmounted(() => {
  document.title = 'Orphic | Trace the Sound to Its Source';
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
            {{ isLangEnglish ? 'Prediction Result' : 'Hasil Prediksi' }}
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
          v-if="predLoading || preds.length == 0"
          class="content w-full h-full flex flex-col justify-center items-center"
        >
          <div class="flex items-center gap-2">
            <span class="jump-dot"></span>
            <span class="jump-dot"></span>
            <span class="jump-dot"></span>
          </div>
        </div>
        <div
          v-else
          class="content w-full h-full flex flex-col justify-start items-center overflow-y-scroll pt-3 pb-[100px]"
          :class="isCollapsed ? 'px-35' : 'px-15'"
        >
          <div
            class="pred-result w-full bg-[#EBEBEB] px-6 py-3 flex flex-col justify-start items-center gap-5 rounded-[10px] border border-gray-300"
          >
            <div class="main-results w-full flex flex-col justify-start items-center gap-5">
              <div class="top w-full flex flex-row justify-between items-center">
                <div class="left flex flex-row justify-start items-center gap-3">
                  <div
                    class="music-logo rounded-[5px] bg-gray-300 w-15 h-15 flex justify-center items-center overflow-hidden"
                  >
                    <img
                      v-if="preds[0]?.thumbnail"
                      :src="`${API_URL}/audio/thumb/${preds[0].thumbnail}`"
                      class="w-full h-full object-cover rounded-[5px]"
                      alt="thumbnail"
                    />
                    <span v-else class="material-symbols-outlined text-[#101010] !text-3xl">
                      music_note_2
                    </span>
                  </div>
                  <div class="songs flex flex-col justify-start items-start">
                    <p class="title text-gray-600 text-lg w-60 max-w-60 truncate">
                      {{ preds[0]?.song_title }}
                    </p>
                    <div class="details flex flex-row gap-3 justify-start items-center">
                      <p class="text-[#83009a] !text-xs">
                        {{
                          preds[0].duration
                            ? formatTime(preds[0]?.duration ?? 0)
                            : isLangEnglish
                              ? 'No data'
                              : 'Data tidak ada'
                        }}
                      </p>
                      <div class="bulet rounded-full h-1 w-1 bg-gray-500"></div>
                      <p class="text-[#83009a] !text-xs">
                        {{ getRelativeTime(preds[0]?.created_at) }}
                      </p>
                    </div>
                  </div>
                </div>
                <div
                  class="pred-verdict flex !text-sm items-center bg-[#83009a]/50 border border-2 border-[#83009a] rounded-[20px] text-[#83009a] px-3 py-2"
                >
                  {{ preds[0]?.prediction }}
                </div>
              </div>
              <div class="pred-probs w-full flex flex-col justify-start items-center gap-2">
                <div class="human-probs w-full flex flex-col justify-start items-start">
                  <p class="title text-black text-sm">
                    {{ isLangEnglish ? 'Human-Made Probability' : 'Kemungkinan Buatan Manusia' }}:
                  </p>
                  <div class="probs-bar flex flex-row justify-start items-center w-full gap-2">
                    <div class="w-[95%] bg-gray-400 rounded-full h-2 overflow-hidden">
                      <div
                        class="h-full bg-[#83009a] transition-all duration-300"
                        :style="{ width: `${(1 - preds[0]?.probability) * 100}%` }"
                      />
                    </div>
                    <p class="details w-[5%] text-black">
                      {{
                        (preds[0].probability ? (1 - preds[0]?.probability) * 100 : 0).toFixed(1)
                      }}%
                    </p>
                  </div>
                </div>
                <div class="AIgen-probs w-full flex flex-col justify-start items-start">
                  <p class="title text-black text-sm">
                    {{ isLangEnglish ? 'AI-Generated Probability' : 'Kemungkinan Buatan AI' }}:
                  </p>
                  <div class="probs-bar flex flex-row justify-start items-center w-full gap-2">
                    <div class="w-[95%] bg-gray-400 rounded-full h-2 overflow-hidden">
                      <div
                        class="h-full bg-[#83009a] transition-all duration-300"
                        :style="{ width: `${preds[0]?.probability * 100}%` }"
                      />
                    </div>
                    <p class="details w-[5%] text-black">
                      {{ (preds[0].probability ? preds[0]?.probability * 100 : 0).toFixed(1) }}%
                    </p>
                  </div>
                </div>
              </div>
              <WaveformSlices
                v-if="src !== ''"
                :src="src"
                :slices="preds[0]?.slices_meta"
                :isLangEnglish="isLangEnglish"
              />
              <div
                class="pred-details w-full flex flex-row justify-evenly items-center px-10 gap-4"
              >
                <div
                  v-for="(items, index) in predsDetails"
                  :key="index"
                  class="container h-25 max-w-60 flex flex-col justify-start items-start px-2 py-2 border border-gray-300 bg-white rounded-[10px] gap-2"
                >
                  <p class="text-[#6d6d6d] text-xs">{{ items.category }}</p>
                  <p v-if="index == 0" class="text-2xl" :class="items.classColor">
                    {{ items.value }}
                  </p>
                  <p v-else-if="index == 1" class="text-2xl" :class="items.classColor">
                    {{ items.value }}
                  </p>
                  <p v-else class="text-2xl" :class="items.classColor">
                    {{ items.value }}
                  </p>
                  <p class="text-[#6d6d6d] text-xs">{{ items.class }}</p>
                </div>
              </div>
              <div v-if="src !== ''" class="w-[80%] h-px bg-gray-300 !mt-2 !mb-2"></div>
              <div
                v-if="src !== ''"
                class="media-player w-full flex items-center gap-4 px-4 py-3 rounded-xl border border-gray-300 !mb-2"
              >
                <button
                  @click="togglePlay"
                  class="w-10 h-10 flex items-center justify-center rounded-full hover:bg-gray-100 cursor-pointer"
                >
                  <span class="material-symbols-outlined text-[#83009a]">
                    {{ isPlaying ? 'pause' : 'play_arrow' }}
                  </span>
                </button>

                <div ref="progressBar" class="flex-1 relative cursor-pointer" @click="seek">
                  <div class="w-full h-1 bg-gray-300 rounded-full" />
                  <div
                    class="absolute left-0 top-0 h-1 bg-purple-600 rounded-full"
                    :style="{ width: `${progress}%` }"
                  />
                  <div
                    class="absolute top-1/2 -translate-y-1/2 w-3 h-3 bg-purple-600 rounded-full shadow"
                    :style="{ left: `calc(${progress}% - 6px)` }"
                  />
                </div>

                <div class="text-sm text-gray-500 min-w-[90px] text-right">
                  {{ formatTime(currentTime) }}/{{ formatTime(duration) }}
                </div>

                <audio
                  ref="audio"
                  :src="src"
                  preload="metadata"
                  @loadedmetadata="duration = audio?.duration ?? 0"
                  @timeupdate="currentTime = audio?.currentTime ?? 0"
                  @play="isPlaying = true"
                  @pause="isPlaying = false"
                  @ended="isPlaying = false"
                />
              </div>
            </div>
          </div>
          <sliceExpla
            :slices="preds[0]?.slices_meta"
            :songDuration="duration"
            :isLangEnglish="isLangEnglish"
          />
        </div>
      </div>

      <Uploadbar @upload="handleAudioUpload" />
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
          v-if="predLoading || preds.length == 0"
          class="content w-full h-full flex flex-col justify-center items-center"
        >
          <div class="flex items-center gap-2">
            <span class="jump-dot"></span>
            <span class="jump-dot"></span>
            <span class="jump-dot"></span>
          </div>
        </div>
        <div
          v-else
          class="content w-full h-full flex flex-col justify-start items-center overflow-y-scroll pt-3 pb-[100px]"
          :class="isCollapsed ? 'px-35' : 'px-15'"
        >
          <div
            class="pred-result w-full bg-[#1b1b1b] px-6 py-3 flex flex-col justify-start items-center gap-5 rounded-[10px] border border-[#202020]"
          >
            <div class="main-results w-full flex flex-col justify-start items-center gap-5">
              <div class="top w-full flex flex-row justify-between items-center">
                <div class="left flex flex-row justify-start items-center gap-3">
                  <div
                    class="music-logo rounded-[5px] bg-[#303030] w-15 h-15 flex justify-center items-center overflow-hidden"
                  >
                    <img
                      v-if="preds[0]?.thumbnail"
                      :src="`${API_URL}/audio/thumb/${preds[0].thumbnail}`"
                      class="w-full h-full object-cover rounded-[5px]"
                      alt="thumbnail"
                    />
                    <span v-else class="material-symbols-outlined text-[#101010] !text-3xl">
                      music_note_2
                    </span>
                  </div>
                  <div class="songs flex flex-col justify-start items-start">
                    <p class="title text-white text-lg w-60 max-w-60 truncate">
                      {{ preds[0]?.song_title }}
                    </p>
                    <div class="details flex flex-row gap-3 justify-start items-center">
                      <p class="text-[#83009a] !text-xs">
                        {{
                          preds[0].duration
                            ? formatTime(preds[0]?.duration ?? 0)
                            : isLangEnglish
                              ? 'No data'
                              : 'Data tidak ada'
                        }}
                      </p>
                      <div class="bulet rounded-full h-1 w-1 bg-[#6d6d6d]"></div>
                      <p class="text-[#83009a] !text-xs">
                        {{ getRelativeTime(preds[0]?.created_at) }}
                      </p>
                    </div>
                  </div>
                </div>
                <div
                  class="pred-verdict flex !text-sm items-center bg-[#101010] rounded-[20px] text-[#83009a] px-3 py-2"
                >
                  {{ preds[0]?.prediction }}
                </div>
              </div>
              <div class="pred-probs w-full flex flex-col justify-start items-center gap-2">
                <div class="human-probs w-full flex flex-col justify-start items-start">
                  <p class="title text-[#6d6d6d] text-sm">
                    {{ isLangEnglish ? 'Human-Made Probability' : 'Kemungkinan Buatan Manusia' }}:
                  </p>
                  <div class="probs-bar flex flex-row justify-start items-center w-full gap-2">
                    <div class="w-[95%] bg-[#6d6d6d] rounded-full h-2 overflow-hidden">
                      <div
                        class="h-full bg-[#83009a] transition-all duration-300"
                        :style="{ width: `${(1 - preds[0]?.probability) * 100}%` }"
                      />
                    </div>
                    <p class="details w-[5%] text-[#6d6d6d]">
                      {{
                        (preds[0].probability ? (1 - preds[0]?.probability) * 100 : 0).toFixed(1)
                      }}%
                    </p>
                  </div>
                </div>
                <div class="AIgen-probs w-full flex flex-col justify-start items-start">
                  <p class="title text-[#6d6d6d] text-sm">
                    {{ isLangEnglish ? 'AI-Generated Probability' : 'Kemungkinan Buatan AI' }}:
                  </p>
                  <div class="probs-bar flex flex-row justify-start items-center w-full gap-2">
                    <div class="w-[95%] bg-[#6d6d6d] rounded-full h-2 overflow-hidden">
                      <div
                        class="h-full bg-[#83009a] transition-all duration-300"
                        :style="{ width: `${preds[0]?.probability * 100}%` }"
                      />
                    </div>
                    <p class="details w-[5%] text-[#6d6d6d]">
                      {{ (preds[0].probability ? preds[0]?.probability * 100 : 0).toFixed(1) }}%
                    </p>
                  </div>
                </div>
              </div>
              <WaveformSlices
                v-if="src !== ''"
                :isDarkMode="isDarkMode"
                :src="src"
                :slices="preds[0]?.slices_meta"
                :isLangEnglish="isLangEnglish"
              />
              <div
                class="pred-details w-full flex flex-row justify-evenly items-center px-10 gap-4"
              >
                <div
                  v-for="(items, index) in predsDetails"
                  :key="index"
                  class="container h-25 max-w-60 flex flex-col justify-start items-start px-2 py-2 border border-[#1b1b1b] bg-[#090909] rounded-[10px] gap-2"
                >
                  <p class="text-[#6d6d6d] text-xs">{{ items.category }}</p>
                  <p v-if="index == 0" class="text-2xl" :class="items.classColor">
                    {{ items.value }}
                  </p>
                  <p v-else-if="index == 1" class="text-2xl" :class="items.classColor">
                    {{ items.value }}
                  </p>
                  <p v-else class="text-2xl" :class="items.classColor">
                    {{ items.value }}
                  </p>
                  <p class="text-[#6d6d6d] text-xs">{{ items.class }}</p>
                </div>
              </div>
              <div v-if="src !== ''" class="w-[80%] h-px bg-[#404040] !mt-4 !mb-2"></div>
              <div
                v-if="src !== ''"
                class="media-player w-full flex items-center gap-4 px-4 py-3 rounded-xl border border-[#404040] !mb-2"
              >
                <button
                  @click="togglePlay"
                  class="w-10 h-10 flex items-center justify-center rounded-full hover:bg-[#1b1b1b] cursor-pointer"
                >
                  <span class="material-symbols-outlined text-[#83009a]">
                    {{ isPlaying ? 'pause' : 'play_arrow' }}
                  </span>
                </button>

                <div ref="progressBar" class="flex-1 relative cursor-pointer" @click="seek">
                  <div class="w-full h-1 bg-[#6d6d6d] rounded-full" />
                  <div
                    class="absolute left-0 top-0 h-1 bg-[#83009a] rounded-full"
                    :style="{ width: `${progress}%` }"
                  />
                  <div
                    class="absolute top-1/2 -translate-y-1/2 w-3 h-3 bg-[#83009a] rounded-full shadow"
                    :style="{ left: `calc(${progress}% - 6px)` }"
                  />
                </div>

                <div class="text-sm text-[#6d6d6d] min-w-[90px] text-right">
                  {{ formatTime(currentTime) }}/{{ formatTime(duration) }}
                </div>

                <audio
                  ref="audio"
                  :src="src"
                  preload="metadata"
                  @loadedmetadata="duration = audio?.duration ?? 0"
                  @timeupdate="currentTime = audio?.currentTime ?? 0"
                  @play="isPlaying = true"
                  @pause="isPlaying = false"
                  @ended="isPlaying = false"
                />
              </div>
            </div>
          </div>
          <sliceExpla
            :isDarkMode="isDarkMode"
            :slices="preds[0]?.slices_meta"
            :songDuration="duration"
            :isLangEnglish="isLangEnglish"
          />
        </div>
      </div>

      <Uploadbar @upload="handleAudioUpload" />
    </div>
  </div>
  <Menu :isUserLoggedin="isUserLoggedin" />
  <OpenWarning />
  <ModalLogin />
</template>
