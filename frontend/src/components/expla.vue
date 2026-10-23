<script setup>
import { computed } from 'vue';

const props = defineProps({
  slices: { type: Array, default: () => [] },
  songDuration: { type: Number, default: 0 },
  isLangEnglish: { type: Boolean, default: false },
  isDarkMode: { type: Boolean, default: false },
});

function formatTime(sec) {
  if (sec == null || isNaN(sec)) return '0:00';
  const m = Math.floor(sec / 60);
  const s = Math.round(sec % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
}

const informativeCount = computed(
  () => props.slices.filter((s) => s.type === 'informative').length,
);
const randomCount = computed(() => props.slices.filter((s) => s.type === 'random').length);

const topSlice = computed(() => {
  const informative = props.slices.filter((s) => s.type === 'informative' && s.score != null);
  if (informative.length === 0) return null;
  return informative.reduce((max, s) => (s.score > max.score ? s : max), informative[0]);
});

const totalAnalyzedSeconds = computed(() =>
  props.slices.reduce((sum, s) => sum + (s.end - s.start), 0),
);

const coveragePercent = computed(() => {
  if (!props.songDuration) return 0;
  return Math.min(100, (totalAnalyzedSeconds.value / props.songDuration) * 100);
});

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

const explanationItems = computed(() => [
  {
    icon: 'ti-adjustments',
    title: props.isLangEnglish ? 'Sampling Strategy' : 'Strategi Pengambilan Sampel',
    description: props.isLangEnglish
      ? `The system analyzes ${props.slices.length} segments of this track using a hybrid slicing strategy: ${informativeCount.value} segments were selected based on the highest spectral variation score (a weighted combination of spectral flux and spectral centroid), while ${randomCount.value} segments were sampled randomly to preserve diversity across the track.`
      : `Sistem menganalisis ${props.slices.length} segmen dari lagu ini menggunakan strategi hybrid slicing: ${informativeCount.value} segmen dipilih berdasarkan skor variasi spektral tertinggi (kombinasi berbobot dari spectral flux dan spectral centroid), sementara ${randomCount.value} segmen lainnya diambil secara acak untuk menjaga keragaman sampel di sepanjang lagu.`,
  },
  {
    icon: 'ti-target-arrow',
    title: props.isLangEnglish ? 'Most Informative Segment' : 'Segmen Paling Informatif',
    description: topSlice.value
      ? props.isLangEnglish
        ? `The segment at ${formatTime(topSlice.value.start)}–${formatTime(topSlice.value.end)} has the highest spectral variation score (${topSlice.value.score.toFixed(2)}) among all analyzed segments, indicating this part likely contains the most prominent shift in texture or instrumentation in the track.`
        : `Segmen pada ${formatTime(topSlice.value.start)}–${formatTime(topSlice.value.end)} memiliki skor variasi spektral tertinggi (${topSlice.value.score.toFixed(2)}) di antara seluruh segmen yang dianalisis, menandakan bagian ini kemungkinan memuat perubahan tekstur atau instrumentasi paling menonjol dalam lagu ini.`
      : '',
  },
  {
    icon: 'ti-waveform',
    title: props.isLangEnglish ? 'Analysis Coverage' : 'Cakupan Analisis',
    description: props.isLangEnglish
      ? `The model analyzed a total of ${Math.round(totalAnalyzedSeconds.value)} seconds across ${props.slices.length} selected segments, covering approximately ${coveragePercent.value.toFixed(0)}% of the track's full duration (${formatTime(props.songDuration)}).`
      : `Model menganalisis total ${Math.round(totalAnalyzedSeconds.value)} detik dari ${props.slices.length} segmen terpilih, mencakup sekitar ${coveragePercent.value.toFixed(0)}% dari keseluruhan durasi lagu (${formatTime(props.songDuration)}).`,
  },
]);
</script>

<template>
  <div class="insights w-full flex flex-col justify-start items-start !mt-5 gap-3">
    <p class="text-sm font-semibold" :class="isDarkMode ? 'text-[#6d6d6d]' : 'text-gray-500'">
      {{ isLangEnglish ? 'How This Track Was Analyzed' : 'Cara Lagu Ini Dianalisis' }}
    </p>
    <div
      class="w-full px-6 py-5 flex flex-col justify-start items-center gap-8 rounded-[10px] border"
      :class="isDarkMode ? 'bg-[#1b1b1b] border-[#202020]' : 'bg-[#EBEBEB] border-gray-300'"
    >
      <div
        v-for="(item, index) in explanationItems"
        :key="index"
        class="items w-full flex flex-row justify-start items-start gap-3"
      >
        <div
          class="music-logo rounded-[5px] bg-[#83009a]/50 w-15 h-15 flex justify-center items-center"
        >
          <span class="material-symbols-outlined text-[#83009a] !text-3xl">
            {{ logos[index]?.tag }}
          </span>
        </div>
        <div class="details flex flex-col justify-start items-start w-[90%]">
          <p class="title !text-base" :class="isDarkMode ? 'text-white' : 'text-black'">{{ item.title }}</p>
          <p class="details w-full !text-xs break-words"
          :class="isDarkMode ? 'text-[#6d6d6d]' : 'text-gray-500'">
            {{ item.description }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
