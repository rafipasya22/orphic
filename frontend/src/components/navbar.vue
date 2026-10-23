<script setup lang="ts">
import { ref } from 'vue';
import { openModalLogin } from '../composable/openmodalLogin';
import { openSettingsFunc } from '../composable/openSettings';
import { useAuthStore } from '../stores/authstore';
import { openMenufunc } from '../composable/openmenu';
import { darkFunc } from '../composable/darkMode';

const navbarEl = ref<HTMLElement | null>(null);
const authStore = useAuthStore();
const { isDarkMode } = darkFunc();
const { openMenu } = openMenufunc();
const { openModal } = openModalLogin();
const { openSettings } = openSettingsFunc();
const { gantiWarnaNavbar } = defineProps<{
  gantiWarnaNavbar: boolean;
}>();

defineExpose({
  navbarEl,
});
</script>

<template>
  <div
    ref="navbarEl"
    class="navbar w-full h-[3rem] flex flex-row items-center justify-between px-20 fixed top-0 left-0 z-10 transition-all duration-500"
    :class="gantiWarnaNavbar ? (isDarkMode ? 'bg-[#2b2b2b]' : 'bg-[#ededed]') : 'bg-transparent'"
  >
    <div
      class="logo text-base font-bold"
      :class="
        gantiWarnaNavbar ? (isDarkMode ? 'text-[#ae04cc]' : 'text-[#83009a]') : 'text-gray-300'
      "
    >
      Artificial Beats Investigator
    </div>
    <div v-if="authStore.user" class="right flex flex-row justify-start items-center gap-2">
      <button
        @click="openMenu"
        class="text-lg hover:cursor-pointer flex flex-row items-center justify-center"
        :class="
          gantiWarnaNavbar
            ? isDarkMode
              ? 'text-[#ae04cc] hover:text-[#434343]'
              : 'text-[#83009a] hover:text-[#434343]'
            : 'text-gray-300 hover:text-[#83009a]'
        "
      >
        <span class="material-symbols-outlined"> menu_open </span>
      </button>
      <button
        v-if="authStore.user"
        class="text-base hover:cursor-pointer flex flex-row items-center justify-center"
        :class="
          gantiWarnaNavbar
            ? isDarkMode
              ? 'text-[#ae04cc] hover:text-[#434343]'
              : 'text-[#83009a] hover:text-[#434343]'
            : 'text-gray-300 hover:text-[#83009a]'
        "
        @click="openSettings"
      >
        <img
          v-if="authStore.profile?.profile_picture_url"
          :src="authStore.profile.profile_picture_url"
          alt="Account Image"
          class="w-6 h-6 rounded-full object-cover"
        />
        <img
          v-else
          src="../assets/imgs/user-default.png"
          alt="Account Image"
          class="w-6 h-6 rounded-full object-cover bg-gray-200 rounded-full"
        />
      </button>
      <button
        v-else
        class="text-lg hover:cursor-pointer flex flex-row items-center justify-center"
        :class="
          gantiWarnaNavbar
            ? isDarkMode
              ? 'text-[#ae04cc] hover:text-[#434343]'
              : 'text-[#83009a] hover:text-[#434343]'
            : 'text-gray-300 hover:text-[#83009a]'
        "
        @click="openModal"
      >
        <span class="material-symbols-outlined"> account_circle </span>
      </button>
    </div>
    <div v-else class="right flex flex-row justify-start items-center gap-2">
      <button
        @click="openMenu"
        class="text-lg hover:cursor-pointer flex flex-row items-center justify-center"
        :class="
          gantiWarnaNavbar
            ? isDarkMode
              ? 'text-[#ae04cc] hover:text-[#434343]'
              : 'text-[#83009a] hover:text-[#434343]'
            : 'text-gray-300 hover:text-[#83009a]'
        "
      >
        <span class="material-symbols-outlined"> menu_open </span>
      </button>
      <button
        class="text-lg hover:cursor-pointer flex flex-row items-center justify-center"
        :class="
          gantiWarnaNavbar
            ? 'text-[#83009a] hover:text-[#434343]'
            : 'text-gray-300 hover:text-[#83009a]'
        "
        @click="openModal"
      >
        <span class="material-symbols-outlined"> account_circle </span>
      </button>
    </div>
  </div>
</template>
