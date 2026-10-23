<script setup lang="ts">
import { API_URL } from '@/config'
import { ref } from 'vue';
import { useAuthStore } from '../stores/authstore';
import { gantiBahasaFunc } from '../composable/gantiBahasa';
import { darkFunc } from '../composable/darkMode';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { loadingFunc } from '@/composable/globalVar';

const { isDarkMode } = darkFunc();
const { predLoading, isCollapsed } = loadingFunc();
const authStore = useAuthStore();
const { isLangEnglish } = gantiBahasaFunc();
const router = useRouter();
const Templink = ref<string>('');
const link = ref<string>('');
const isDragging = ref(false);
const files = ref<File[]>([]);
const sendError = ref<string>('');
const emit = defineEmits<{
  upload: [file: File];
}>();

const handleDragOver = (e: DragEvent) => {
  e.preventDefault();
  isDragging.value = true;
};

const handleDragLeave = () => {
  isDragging.value = false;
};

const filterAudioFiles = (fileList: File[]) => {
  const allowedTypes = ['audio/mpeg', 'audio/wav'];

  return fileList.filter((file) => allowedTypes.includes(file.type));
};

const handleDrop = (e: DragEvent) => {
  e.preventDefault();

  isDragging.value = false;

  const droppedFiles = Array.from(e.dataTransfer?.files || []);

  files.value = filterAudioFiles(droppedFiles);

  if (files.value.length > 0) {
    emit('upload', files.value[0]!);
  }
};

const handleFileSelect = (e: Event) => {
  const input = e.target as HTMLInputElement;

  const selectedFiles = Array.from(input.files || []);

  files.value = filterAudioFiles(selectedFiles);

  if (files.value.length > 0) {
    emit('upload', files.value[0]!);
  }

  input.value = '';
};

const submitLink = async () => {
  predLoading.value = true;
  sendError.value = '';
  Templink.value = link.value;
  link.value = '';

  try {
    const res = await axios.post(`${API_URL}/songs`, {
      link: Templink.value,
      userId: authStore.user.id,
    });

    console.log(res.data);

    const historyId = res.data.history_id;

    router.push(`/dash/predictions/${historyId}`);
  } catch (err: any) {
    sendError.value = err.response?.data?.detail || 'Something went wrong';

    setTimeout(() => {
      sendError.value = '';
    }, 3000);
  } finally {
    predLoading.value = false;
  }
};
const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && link.value.trim() && !predLoading.value) {
    submitLink();
  }
};
</script>

<template>
  <div
    v-if="!isDarkMode"
    class="absolute bottom-0 left-0 w-full px-4 py-6 flex justify-center bg-gradient-to-t from-white via-white/50 to-transparent"
  >
    <div
      class="relative max-w-4xl"
      :class="isCollapsed ? 'w-[70%]' : 'w-[80%]'"
      @drop="handleDrop"
      @dragover="handleDragOver"
      @dragleave="handleDragLeave"
    >
      <div
        class="w-full rounded-3xl border bg-white px-4 py-1 flex items-center gap-3 transition-all duration-200"
        :class="
          isDragging
            ? 'border-[#83009a] shadow-lg shadow-purple-500/20'
            : 'border-gray-300 hover:border-gray-400'
        "
      >
        <input
          v-model="link"
          type="text"
          :placeholder="isLangEnglish ? 'Paste YouTube or Suno link...' : 'Masukkan link YouTube atau Suno...'"
          class="flex-1 bg-transparent !text-sm outline-none text-black placeholder:text-gray-500"
          @keydown="handleKeydown"
        />

        <label
          class="cursor-pointer flex items-center justify-center p-2 rounded-full hover:bg-gray-100 transition group"
        >
          <input type="file" class="hidden" accept=".mp3,.wav" @change="handleFileSelect" />

          <span
            class="material-symbols-outlined text-gray-500 !text-2xl group-hover:text-[#83009a]"
          >
            attach_file
          </span>
        </label>

        <button
          v-if="!predLoading"
          @click="submitLink"
          class="w-8 h-8 rounded-full bg-white border border-[#83009a] text-[#83009a] flex items-center justify-center hover:text-white hover:bg-[#83009a] transition cursor-pointer"
        >
          <span class="material-symbols-outlined !text-lg"> arrow_upward </span>
        </button>
        <button
          v-else
          class="w-8 h-8 rounded-full bg-white border border-[#83009a] text-[#83009a] flex items-center justify-center hover:text-white hover:bg-[#83009a] transition pointer-events-none"
        >
          <div
            class="w-4 h-4 border-4 border-gray-300 border-t-purple-700 rounded-full animate-spin"
          ></div>
        </button>
      </div>

      <div
        v-if="isDragging"
        class="absolute inset-0 rounded-3xl bg-white/80 backdrop-blur-sm flex items-center justify-center pointer-events-none border-2 border-dashed border-[#83009a]"
      >
        <div class="flex flex-col items-center gap-2">
          <span class="material-symbols-outlined text-[#83009a] text-4xl"> audio_file </span>

          <p class="text-[#83009a] font-medium">
            {{ isLangEnglish ? 'Drop audio file here' : 'Lepaskan file audio di sini' }}
          </p>
        </div>
      </div>
    </div>
  </div>
  <div
    v-else
    class="absolute bottom-0 left-0 w-full px-4 py-6 flex justify-center bg-gradient-to-t from-[#090909] via-[#090909]/50 to-transparent"
  >
    <div
      class="relative max-w-4xl"
      :class="isCollapsed ? 'w-[70%]' : 'w-[80%]'"
      @drop="handleDrop"
      @dragover="handleDragOver"
      @dragleave="handleDragLeave"
    >
      <div
        class="w-full rounded-3xl border bg-[#090909] px-4 py-1 flex items-center gap-3 transition-all duration-200"
        :class="
          isDragging
            ? 'border-[#83009a] shadow-lg shadow-purple-500/20'
            : 'border-[#202020] hover:border-[#292929]'
        "
      >
        <input
          v-model="link"
          type="text"
          :placeholder="isLangEnglish ? 'Paste YouTube or Suno link...' : 'Masukkan link YouTube atay Suno...'"
          class="flex-1 bg-transparent !text-sm outline-none text-white placeholder:text-[#6d6d6d]"
          @keydown="handleKeydown"
        />

        <label
          class="cursor-pointer flex items-center justify-center p-2 rounded-full transition group"
        >
          <input type="file" class="hidden" accept=".mp3,.wav" @change="handleFileSelect" />

          <span
            class="material-symbols-outlined text-[#6d6d6d] !text-2xl group-hover:text-[#83009a]"
          >
            attach_file
          </span>
        </label>

        <button
          v-if="!predLoading"
          @click="submitLink"
          class="w-8 h-8 rounded-full bg-[#090909] border border-[#83009a] text-[#83009a] flex items-center justify-center hover:text-white hover:bg-[#83009a] transition cursor-pointer"
        >
          <span class="material-symbols-outlined !text-lg"> arrow_upward </span>
        </button>
        <button
          v-else
          class="w-8 h-8 rounded-full bg-white border border-[#83009a] text-[#83009a] flex items-center justify-center hover:text-white hover:bg-[#83009a] transition pointer-events-none"
        >
          <div
            class="w-4 h-4 border-4 border-gray-300 border-t-purple-700 rounded-full animate-spin"
          ></div>
        </button>
      </div>

      <div
        v-if="isDragging"
        class="absolute inset-0 rounded-3xl bg-white/80 backdrop-blur-sm flex items-center justify-center pointer-events-none border-2 border-dashed border-[#83009a]"
      >
        <div class="flex flex-col items-center gap-2">
          <span class="material-symbols-outlined text-[#83009a] text-4xl"> audio_file </span>

          <p class="text-[#83009a] font-medium">
            {{ isLangEnglish ? 'Drop audio file here' : 'Lepaskan file audio di sini' }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
