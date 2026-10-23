<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';

const props = defineProps({
  src: { type: String, default: null },
  slices: { type: Array, default: () => [] },
  isLangEnglish: { type: Boolean, default: false },
  isDarkMode: { type: Boolean, default: false },
});

const canvasEl = ref(null);
const loading = ref(false);
let audioCtx = null;
let peaks = null;
let totalDuration = 0;
let resizeObserver = null;

const hoveredSlice = ref(null);
const tooltipX = ref(0);
const tooltipY = ref(0);

function formatTime(sec) {
  if (sec == null || isNaN(sec)) return '0:00';
  const m = Math.floor(sec / 60);
  const s = Math.round(sec % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
}

function sliceAt(timeSec) {
  return props.slices.find((s) => timeSec >= s.start && timeSec < s.end) ?? null;
}

function handleMouseMove(e) {
  if (!canvasEl.value || !totalDuration) return;
  const rect = canvasEl.value.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const ratio = Math.min(Math.max(x / rect.width, 0), 1);
  const timeSec = ratio * totalDuration;

  const slice = sliceAt(timeSec);
  hoveredSlice.value = slice;

  const tooltipWidth = 180;
  let left = x + 12;
  if (left + tooltipWidth > rect.width) left = x - tooltipWidth - 12;
  tooltipX.value = left;
  tooltipY.value = -8;
}

function handleMouseLeave() {
  hoveredSlice.value = null;
}

async function loadAndDraw() {
  if (!props.src || !canvasEl.value) return;
  loading.value = true;
  try {
    const res = await fetch(props.src);
    const arrayBuffer = await res.arrayBuffer();

    audioCtx = audioCtx || new (window.AudioContext || window.webkitAudioContext)();
    const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer.slice(0));

    totalDuration = audioBuffer.duration;
    const channelData = audioBuffer.getChannelData(0);

    const canvas = canvasEl.value;
    const width = canvas.clientWidth || 600;
    const dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr;
    canvas.height = canvas.clientHeight * dpr;

    const samplesPerPixel = Math.floor(channelData.length / width);
    peaks = new Float32Array(width);

    for (let i = 0; i < width; i++) {
      const start = i * samplesPerPixel;
      const end = Math.min(start + samplesPerPixel, channelData.length);
      let max = 0;
      for (let j = start; j < end; j++) {
        const abs = Math.abs(channelData[j]);
        if (abs > max) max = abs;
      }
      peaks[i] = max;
    }

    draw();
  } catch (err) {
    console.error('Failed to load waveform:', err);
  } finally {
    loading.value = false;
  }
}

function sliceColorAt(timeSec) {
  if (props.isDarkMode) {
    for (const s of props.slices) {
      if (timeSec >= s.start && timeSec < s.end) {
        return s.type === 'informative' ? '#83009a' : '#7d7d7d';
      }
    }
    return '#383838';
  } else {
    for (const s of props.slices) {
      if (timeSec >= s.start && timeSec < s.end) {
        return s.type === 'informative' ? '#83009a' : '#848a94';
      }
    }
    return '#d1d5db';
  }
}

function draw() {
  if (!peaks || !canvasEl.value) return;
  const canvas = canvasEl.value;
  const ctx = canvas.getContext('2d');
  ctx.imageSmoothingEnabled = false;
  const dpr = window.devicePixelRatio || 1;
  const width = canvas.width;
  const height = canvas.height;

  ctx.clearRect(0, 0, width, height);

  const barWidth = Math.max(4 * dpr, 1);
  const gap = Math.max(2.5 * dpr, 1);
  const step = barWidth + gap;
  const numBars = Math.floor(width / step);
  const centerY = height / 2;
  const minBarHeight = 6 * dpr;
  const radius = Math.min(2 * dpr, barWidth / 2);

  for (let b = 0; b < numBars; b++) {
    const startIdx = Math.floor((b / numBars) * peaks.length);
    const endIdx = Math.max(startIdx + 1, Math.floor(((b + 1) / numBars) * peaks.length));
    let amp = 0;
    for (let j = startIdx; j < endIdx && j < peaks.length; j++) {
      if (peaks[j] > amp) amp = peaks[j];
    }

    const timeSec = (startIdx / peaks.length) * totalDuration;
    const barHeight = Math.max(Math.round(amp * height * 0.85), minBarHeight);

    const x = Math.round(b * step);
    const y = Math.round(centerY - barHeight / 2);
    const w = Math.round(barWidth);

    ctx.fillStyle = sliceColorAt(timeSec);
    ctx.beginPath();
    if (ctx.roundRect) {
      ctx.roundRect(x, y, w, barHeight, radius);
    } else {
      ctx.rect(x, y, w, barHeight);
    }
    ctx.fill();
  }
}

onMounted(() => {
  loadAndDraw();
  resizeObserver = new ResizeObserver(() => {
    if (peaks) draw();
  });
  if (canvasEl.value) {
    resizeObserver.observe(canvasEl.value);
    canvasEl.value.addEventListener('mousemove', handleMouseMove);
    canvasEl.value.addEventListener('mouseleave', handleMouseLeave);
  }
});

onBeforeUnmount(() => {
  if (resizeObserver) resizeObserver.disconnect();
  if (canvasEl.value) {
    canvasEl.value.removeEventListener('mousemove', handleMouseMove);
    canvasEl.value.removeEventListener('mouseleave', handleMouseLeave);
  }
});

watch(
  () => props.src,
  () => {
    loadAndDraw();
  },
);

watch(
  () => props.slices,
  () => {
    if (peaks) draw();
  },
);
</script>

<template>
  <div class="waveform-slices w-full flex flex-col gap-3">
    <div
      class="relative w-full h-36 rounded-xl border py-2"
      :class="isDarkMode ? 'bg-[#090909] border-[#1b1b1b]' : 'bg-white border-gray-300'"
    >
      <div class="w-full h-full overflow-hidden rounded-xl">
        <canvas ref="canvasEl" class="w-full h-full block cursor-pointer"></canvas>

        <div
          v-if="loading"
          class="absolute inset-0 flex items-center justify-center text-xs text-gray-400"
        >
          {{ isLangEnglish ? 'Loading waveform...' : 'Memuat waveform...' }}
        </div>
      </div>

      <div
        v-if="hoveredSlice"
        class="absolute z-10 pointer-events-none rounded-lg px-3 py-2 text-xs shadow-lg"
        :class="
          isDarkMode
            ? 'bg-[#1b1b1b] text-white border border-[#2b2b2b]'
            : 'bg-white text-gray-800 border border-gray-200'
        "
        :style="{ left: tooltipX + 'px', top: tooltipY + 'px', width: '180px' }"
      >
        <p
          class="font-medium mb-1"
          :class="
            hoveredSlice.type === 'informative'
              ? 'text-[#83009a]'
              : isDarkMode
                ? 'text-[#a0a0a0]'
                : 'text-gray-500'
          "
        >
          {{
            hoveredSlice.type === 'informative'
              ? isLangEnglish
                ? 'Informative Segment'
                : 'Segmen Informatif'
              : isLangEnglish
                ? 'Random Segment'
                : 'Segmen Acak'
          }}
        </p>
        <p :class="isDarkMode ? 'text-[#8a8a8a]' : 'text-gray-500'">
          {{ formatTime(hoveredSlice.start) }} – {{ formatTime(hoveredSlice.end) }}
        </p>
        <p
          v-if="hoveredSlice.score != null"
          :class="isDarkMode ? 'text-[#8a8a8a]' : 'text-gray-500'"
        >
          {{ isLangEnglish ? 'Score' : 'Skor' }}: {{ hoveredSlice.score.toFixed(2) }}
        </p>
      </div>
    </div>

    <div class="flex items-center gap-4 px-1">
      <div class="flex items-center gap-1.5">
        <span class="w-3 h-3 rounded-sm bg-[#83009a]"></span>
        <span class="text-xs" :class="isDarkMode ? 'text-[#6d6d6d]' : 'text-gray-500'">{{
          isLangEnglish ? 'Informative segment' : 'Segmen informatif'
        }}</span>
      </div>
      <div class="flex items-center gap-1.5">
        <span class="w-3 h-3 rounded-sm bg-[#848a94]"></span>
        <span class="text-xs" :class="isDarkMode ? 'text-[#6d6d6d]' : 'text-gray-500'">{{
          isLangEnglish ? 'Random segment' : 'Segmen acak'
        }}</span>
      </div>
    </div>
  </div>
</template>
