<script lang="ts" setup>
import { openWarningFunc } from '../composable/openWarning';
import { openModalLogin } from '../composable/openmodalLogin';
const { openModal } = openModalLogin();
import router from '../router/index.ts';
const { isWarningOpen, closeWarning } = openWarningFunc();
import { darkFunc } from '../composable/darkMode';
import { gantiBahasaFunc } from '../composable/gantiBahasa';
const { isLangEnglish } = gantiBahasaFunc();
const { isDarkMode } = darkFunc();

function func() {
  closeWarning();
  router.push('/');
  openModal();
}


</script>

<template>
  <div
    v-if="!isDarkMode"
    class="bgmodal fixed inset-0 flex items-center justify-center transition-opacity duration-500 z-22"
    :class="isWarningOpen ? 'bg-black/50' : 'pointer-events-none'"
  >
    <div
      class="modal bg-white px-6 py-4 rounded-lg w-162 h-40 relative transition-all duration-500 flex flex-col justify-between items-start gap-7"
      :class="isWarningOpen ? ' translate-y-0' : ' -translate-y-200'"
    >
      <div class="atas flex flex-col justify-start items-start w-full h-full overflow-hidden gap-4">
        <div class="title flex flex-row justify-start items-center w-full gap-2">
          <h2 class="text-lg text-[#83009a] font-bold">
            {{ isLangEnglish ? 'Warning' : 'Peringatan' }}
          </h2>
        </div>
        <div class="content w-full h-fit flex flex-row justify-start items-center gap-2">
          <p class="text-sm font-bold text-black">
            {{
              isLangEnglish
                ? "You haven't logged in yet. You cannot access this page. Please log in first."
                : 'Kamu belum login. Silakan login terlebih dahulu.'
            }}
          </p>
        </div>
      </div>
      <div class="bawah flex flex-row justify-end items-center gap-2 w-full">
        
        <button
          @click="func"
          class="deletHistory flex flex-row justify-center items-center border border-[#83009a] rounded-[10px] w-24 px-2 py-2 cursor-pointer gap-2 hover:bg-[#480254] bg-[#83009a] transition transition-all duration-300"
        >
          <p class="text-xs text-white font-bold">
            {{ isLangEnglish ? 'Login' : 'Login' }}
          </p>
        </button>
      </div>
    </div>
  </div>
  <div
    v-else
    class="bgmodal fixed inset-0 flex items-center justify-center transition-opacity duration-500 z-22"
    :class="isWarningOpen ? 'bg-black/50' : 'pointer-events-none'"
  >
    <div
      class="modal bg-[#2b2b2b] px-6 py-4 rounded-lg w-162 h-40 relative transition-all duration-500 flex flex-col justify-between items-start gap-7"
      :class="isWarningOpen ? ' translate-y-0' : ' -translate-y-200'"
    >
      <div class="atas flex flex-col justify-start items-start w-full h-full overflow-hidden gap-4">
        <div class="title flex flex-row justify-start items-center w-full gap-2">
          <h2 class="text-lg text-[#ae04cc] font-bold">
            {{ isLangEnglish ? 'Warning' : 'Peringatan' }}
          </h2>
        </div>
        <div class="content w-full h-fit flex flex-row justify-start items-center gap-2">
          <p class="text-sm font-bold text-white">
            {{
              isLangEnglish
                ? "You haven't logged in yet. You cannot access this page. Please log in first."
                : 'Kamu belum login. Silakan login terlebih dahulu.'
            }}
          </p>
        </div>
      </div>
      <div class="bawah flex flex-row justify-end items-center gap-2 w-full">
        
        <button
          @click="func"
          class="deletHistory flex flex-row justify-center items-center border border-[#ae04cc] rounded-[10px] w-24 px-2 py-2 cursor-pointer gap-2 hover:bg-[#ae04cc] bg-[#83009a] transition transition-all duration-300"
        >
          <p class="text-xs text-white font-bold">
            {{ isLangEnglish ? 'Login' : 'Login' }}
          </p>
        </button>
      </div>
    </div>
  </div>
</template>
