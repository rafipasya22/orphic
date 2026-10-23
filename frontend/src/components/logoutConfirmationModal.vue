<script lang="ts" setup>
import { logoutconffunc } from '../composable/logoutconf';
import { useAuthStore } from '../stores/authstore';
import { openMenufunc } from '../composable/openmenu';
import { darkFunc } from '../composable/darkMode';

const { isDarkMode } = darkFunc();
const authStore = useAuthStore();

const { closeMenu } = openMenufunc();
const { closelogoutconf, islogoutconf } = logoutconffunc();
import { gantiBahasaFunc } from '../composable/gantiBahasa';
const { isLangEnglish } = gantiBahasaFunc();

const logoutFunc = () => {
  authStore.logout();
  closelogoutconf();
  closeMenu();
};
</script>

<template>
  <div
    v-if="!isDarkMode"
    @click.self="closelogoutconf"
    class="bgmodal fixed inset-0 flex items-center justify-center transition-opacity duration-500 z-22"
    :class="islogoutconf ? 'bg-black/50' : 'pointer-events-none'"
  >
    <div
      class="modal bg-white px-6 py-4 rounded-lg w-100 h-40 relative transition-all duration-500 flex flex-col justify-between items-start gap-7"
      :class="islogoutconf ? ' translate-y-0' : ' -translate-y-200'"
    >
      <div class="atas flex flex-col justify-start items-start w-full h-full overflow-hidden gap-4">
        <div class="title flex flex-row justify-start items-center w-full gap-2">
          <h2 class="text-lg text-[#83009a] font-bold">
            {{ isLangEnglish ? 'Log Out' : 'Keluar' }}
          </h2>
        </div>
        <div class="content w-full h-fit flex flex-row justify-start items-center gap-2">
          <p class="text-sm font-bold text-black">
            {{
              isLangEnglish
                ? 'Are you sure you want to log out from your account?'
                : 'Apakah Anda yakin ingin keluar dari akun Anda?'
            }}
          </p>
        </div>
      </div>
      <div class="bawah flex flex-row justify-end items-center gap-2 w-full">
        <button
          @click="closelogoutconf"
          class="cancel flex flex-row justify-center items-center border border-gray-300 bg-gray-300 rounded-[10px] w-24 px-2 py-2 cursor-pointer gap-2 hover:bg-gray-500 transition transition-all duration-300"
        >
          <p class="text-xs text-[#83009a] font-bold">
            {{ isLangEnglish ? 'Cancel' : 'Batal' }}
          </p>
        </button>
        <button
          @click="logoutFunc"
          class="deletHistory flex flex-row justify-center items-center border border-[#83009a] rounded-[10px] w-24 px-2 py-2 cursor-pointer gap-2 hover:bg-[#480254] bg-[#83009a] transition transition-all duration-300"
        >
          <p class="text-xs text-white font-bold">
            {{ isLangEnglish ? 'Log out' : 'Keluar' }}
          </p>
        </button>
      </div>
    </div>
  </div>
  <div
    v-else
    @click.self="closelogoutconf"
    class="bgmodal fixed inset-0 flex items-center justify-center transition-opacity duration-500 z-22"
    :class="islogoutconf ? 'bg-black/50' : 'pointer-events-none'"
  >
    <div
      class="modal bg-[#1b1b1b] px-6 py-4 rounded-lg w-100 h-40 relative transition-all duration-500 flex flex-col justify-between items-start gap-7"
      :class="islogoutconf ? ' translate-y-0' : ' -translate-y-200'"
    >
      <div class="atas flex flex-col justify-start items-start w-full h-full overflow-hidden gap-4">
        <div class="title flex flex-row justify-start items-center w-full gap-2">
          <h2 class="text-lg text-[#ae04cc] font-bold">
            {{ isLangEnglish ? 'Log Out' : 'Keluar' }}
          </h2>
        </div>
        <div class="content w-full h-fit flex flex-row justify-start items-center gap-2">
          <p class="text-sm font-bold text-gray-200">
            {{
              isLangEnglish
                ? 'Are you sure you want to log out from your account?'
                : 'Apakah Anda yakin ingin keluar dari akun Anda?'
            }}
          </p>
        </div>
      </div>
      <div class="bawah flex flex-row justify-end items-center gap-2 w-full">
        <button
          @click="closelogoutconf"
          class="cancel flex flex-row justify-center items-center border border-[#1b1b1b] bg-[#2b2b2b] rounded-[10px] w-24 px-2 py-2 cursor-pointer gap-2 hover:bg-[#101010] transition transition-all duration-300"
        >
          <p class="text-xs text-[#ae04cc] font-bold">
            {{ isLangEnglish ? 'Cancel' : 'Batal' }}
          </p>
        </button>
        <button
          @click="logoutFunc"
          class="deletHistory flex flex-row justify-center items-center border border-[#480254] rounded-[10px] w-24 px-2 py-2 cursor-pointer gap-2 hover:bg-[#480254] bg-[#83009a] transition transition-all duration-300"
        >
          <p class="text-xs text-white font-bold">
            {{ isLangEnglish ? 'Log out' : 'Keluar' }}
          </p>
        </button>
      </div>
    </div>
  </div>
</template>
