<script lang="ts" setup>
import { signupconffunc } from '../composable/signupconf';
import { openModalLogin } from '../composable/openmodalLogin';
const { openLoginModal } = openModalLogin();
const { closesignupconf, issignupconfopen } = signupconffunc();
import { gantiBahasaFunc } from '../composable/gantiBahasa';
const { isLangEnglish } = gantiBahasaFunc();


const okbtnFunc = () => {
  openLoginModal();
  closesignupconf();

};
</script>

<template>
    <div
      @click.self="closesignupconf"
      class="bgmodal fixed inset-0 flex items-center justify-center transition-opacity duration-500 z-22"
      :class="issignupconfopen ? 'bg-black/50' : 'pointer-events-none'"
    >
      <div
        class="modal bg-white px-6 py-4 rounded-lg w-130 h-40 relative transition-all duration-500 flex flex-col justify-between items-start gap-7"
        :class="issignupconfopen ? ' translate-y-0' : ' -translate-y-200'"
      >
        <div
          class="atas flex flex-col justify-start items-start w-full h-full overflow-hidden gap-4"
        >
          <div class="title flex flex-row justify-start items-center w-full gap-2">
            <h2 class="text-lg text-[#83009a] font-bold">
              {{ isLangEnglish? 'Signup Success' : 'Daftar Berhasil' }}
            </h2>
          </div>
          <div class="content w-full h-fit flex flex-row justify-start items-center gap-2">
            <p class="text-sm font-bold text-black">
              {{ isLangEnglish
                ? 'Sign up Success, you can now log in to your account' 
                : 'Pendaftaran Berhasil, anda sekarang bisa masuk ke akun Anda' }}
            </p>
          </div>
        </div>
        <div class="bawah flex flex-row justify-end items-center gap-2 w-full">
          <button
            @click="okbtnFunc"
            class="deletHistory flex flex-row justify-center items-center border border-[#83009a] rounded-[10px] w-24 px-2 py-2 cursor-pointer gap-2 hover:bg-[#480254] bg-[#83009a] transition transition-all duration-300"
          >
            <p class="text-xs text-white font-bold">
              {{ isLangEnglish? 'Ok' : 'Ok' }}
            </p>
          </button>
        </div>
      </div>
    </div>
</template>