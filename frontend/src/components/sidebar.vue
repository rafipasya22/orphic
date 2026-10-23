<script setup lang="ts">
import { activefunc } from '../composable/active';
import { logoutconffunc } from '../composable/logoutconf';
import { darkFunc } from '../composable/darkMode';
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useAuthStore } from '../stores/authstore';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { watch } from 'vue';
import { loadingFunc } from '@/composable/globalVar';
import settingsModal from '../components/modalSettings.vue';
import { openSettingsFunc } from '@/composable/openSettings';
import { gantiBahasaFunc } from '@/composable/gantiBahasa.ts'
import logoutConfirmationModal from './logoutConfirmationModal.vue';

const { isCollapsed } = loadingFunc();
const { openSettings, isSettingsopen } = openSettingsFunc();
const { isLangEnglish } = gantiBahasaFunc();
const { openlogoutconf } = logoutconffunc();
const isHover = ref(false);

const showDropdown = ref(false);
const showDropdownRecent = ref(false);
const authStore = useAuthStore();

const histories = ref<any[]>([]);
const fetchHistoryLoading = ref(true);
const profile = ref<any>(null);

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
  isHover.value = !isHover.value;
};

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
};

const settingsToggle = () => {
  toggleDropdown();
  openSettings();
};

const logoutButton = () =>{
  toggleDropdown();
  openlogoutconf();
}

const toggleDropdownRecent = () => {
  showDropdownRecent.value = !showDropdownRecent.value;
};

const closeDropdown = (e: any) => {
  if (!e.target.closest('.dropdown-container')) {
    showDropdown.value = false;
  }
};

const closeDropdownRecent = (e: any) => {
  if (!e.target.closest('.recent-dropdown-container')) {
    showDropdownRecent.value = false;
  }
};

const fetchHistory = async () => {
  const user = authStore.user;
  try {
    if (!user) {
      return;
    }

    const res = await axios.get(`http://127.0.0.1:8000/history/${user.id}`);

    histories.value = res.data;
  } catch (err) {
    console.log(err);
  } finally {
    fetchHistoryLoading.value = false;
  }
};

const route = useRoute();

watch(
  () => route.fullPath,
  async () => {
    await fetchHistory();
  },
);

const { isDarkMode } = darkFunc();
const { isDashActive, isHistoryActive, isHelpActive } = activefunc();

onMounted(async () => {
  document.addEventListener('click', closeDropdown);
  document.addEventListener('click', closeDropdownRecent);

  const user = authStore.user;

  const res = await axios.get(`http://localhost:8000/api/profile/${user.id}`);

  profile.value = res.data;

  fetchHistory();
});

onBeforeUnmount(() => {
  document.removeEventListener('click', closeDropdown);
  document.removeEventListener('click', closeDropdownRecent);
});
</script>

<template>
  <div
    v-if="!isDarkMode"
    :class="[
      'h-screen flex flex-col bg-white border-r border-gray-300 transition-all duration-300',
      isCollapsed ? 'w-[80px]' : 'w-[30%]',
    ]"
  >
    <div v-if="!isCollapsed" class="flex items-center justify-between px-3 py-3 text-[#83009a]">
      <button class="p-2 flex items-center justify-center cursor-pointer">
        <span class="material-symbols-outlined !text-3xl">graphic_eq</span>
      </button>

      <button
        v-if="!isCollapsed"
        @click="toggleSidebar"
        class="px-2 py-1 hover:bg-[#EBEBEB] cursor-pointer rounded-[5px] transition transition-all duration-100"
      >
        <span class="material-symbols-outlined !text-xl">
          {{ isCollapsed ? 'dock_to_right' : 'dock_to_left' }}
        </span>
      </button>
    </div>
    <div v-else class="flex items-center justify-center px-3 py-3 text-[#83009a]">
      <button
        @click="isCollapsed = !isCollapsed"
        @mouseenter="isHover = true"
        @mouseleave="isHover = false"
        class="p-2 flex items-center justify-center cursor-pointer hover:bg-[#EBEBEB] rounded-[5px] h-10 h-max-10 w-10"
      >
        <span class="material-symbols-outlined" :class="isHover ? '!text-xl' : '!text-3xl'">
          {{ isHover ? 'dock_to_left' : 'graphic_eq' }}
        </span>
      </button>
    </div>

    <div
      class="flex-1 overflow-y-auto flex flex-col justify-start items-center px-4 !mt-10"
      :class="isCollapsed ? 'gap-4' : 'gap-2'"
    >
      <RouterLink
        v-if="!isCollapsed"
        to="/dash"
        class="w-full flex flex-row justify-start items-center bg-[#83009a] rounded-[10px] p-2 gap-5 group cursor-pointer hover:bg-[#6d0080] transition transition-all duration-100"
      >
        <div class="bulet rounded-full bg-white flex items-center justify-center">
          <span
            class="material-symbols-outlined !text-black text-base group-hover:rotate-180 transition transition-all duration-900"
          >
            add
          </span>
        </div>
        <div class="text-white text-sm !font-semibold">{{isLangEnglish? 'New Scan' : 'Pemindaian Baru'}}</div>
      </RouterLink>
      <RouterLink
        v-else
        to="/dash"
        class="w-full flex flex-row justify-center items-center bg-[#83009a] rounded-[10px] p-2 gap-5 group cursor-pointer hover:bg-[#6d0080] transition transition-all duration-100"
      >
        <div class="bulet rounded-full bg-white flex items-center justify-center">
          <span
            class="material-symbols-outlined !text-black text-base group-hover:rotate-180 transition transition-all duration-900"
          >
            add
          </span>
        </div>
      </RouterLink>

      <div
        v-if="!isCollapsed"
        class="recent-detections h-full w-full flex flex-col justify-start items-center ps-2"
      >
        <div class="top flex flex-row justify-between items-start w-full">
          <div class="left h-full flex flex-row justify-start gap-5 items-center">
            <span class="material-symbols-outlined text-[#83009a]"> history </span>
            <div class="text-black text-sm">{{ isLangEnglish? 'Recent Detections' : 'Deteksi Terbaru'}}</div>
          </div>
          <div class="recent-dropdown-container relative">
            <button
              @click.stop="toggleDropdownRecent"
              class="right relative group flex justify-center items-center hover:bg-[#EBEBEB] rounded-[5px] py-1 px-2 transition transition-all duration-100 cursor-pointer"
            >
              <span
                class="material-symbols-outlined !text-lg text-[#83009a] cursor-pointer group-hover:text-[#6d0080] transition transition-all duration-100"
              >
                discover_tune
              </span>
            </button>
            <Transition
              enter-active-class="transition duration-150"
              enter-from-class="opacity-0 -translate-y-2"
              enter-to-class="opacity-100 translate-y-0"
              leave-active-class="transition duration-100"
              leave-from-class="opacity-100 translate-y-0"
              leave-to-class="opacity-0 -translate-y-2"
            >
              <div
                v-if="showDropdownRecent"
                class="absolute top-full right-0 mb-2 w-40 bg-white rounded-lg border-2 border-gray-300 z-50"
              >
                <RouterLink
                  to="/dash/manage-history"
                  class="w-full text-left px-4 py-2 hover:bg-[#EBEBEB] text-gray-500 !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
                >
                  <span class="material-symbols-outlined !text-base text-[#83009a]">
                    manage_history
                  </span>
                  {{isLangEnglish?'Manage History' : 'Kelola Riwayat'}}
                </RouterLink>
              </div>
            </Transition>
          </div>
        </div>
        <div
          v-if="fetchHistoryLoading"
          class="content h-80 w-full flex flex-col justify-center items-center gap-2 pt-5"
        >
          <div
            class="w-8 h-8 border-4 border-gray-300 border-t-purple-700 rounded-full animate-spin"
          ></div>
          <p class="text-gray-400 text-center">Loading</p>
        </div>
        <div
          v-else-if="histories.length === 0"
          class="content h-100 w-full flex flex-col justify-center items-center gap-2 pt-5"
        >
          <span class="material-symbols-outlined text-gray-500"> history_off </span>
          <p class="text-gray-400 text-center">{{ isLangEnglish?'No recent detections' : 'Tidak Ada Deteksi Terbaru'}}</p>
        </div>
        <div
          v-else
          class="content h-fit max-h-90 w-full flex flex-col gap-2 py-2 ps-5 overflow-y-scroll"
        >
          <RouterLink
            :to="`/dash/predictions/${lagu.id}`"
            class="recent-preds w-65 py-1 px-3 flex flex-row justify-start items-start text-gray-500 hover:text-black text-sm hover:bg-[#EBEBEB] rounded-[5px] hover:border-r-3 hover:border-[#83009a] cursor-pointer transition transition-all duration-100"
            v-for="lagu in histories"
            :key="lagu.id"
          >
            <span class="truncate block w-full text-left">
              {{ lagu.song_title }}
            </span>
          </RouterLink>
        </div>
      </div>
      <div v-else class="recent-detections h-fit w-full flex flex-col justify-center items-center">
        <div class="top flex flex-row justify-center items-center w-full">
          <div class="left h-full flex flex-row justify-center gap-5 items-center">
            <span class="material-symbols-outlined text-[#83009a]"> history </span>
          </div>
        </div>
      </div>
    </div>

    <div class="border-t border-gray-200 p-3 flex items-center justify-between">
      <div
        v-if="!isCollapsed"
        class="account w-full h-full flex flex-row justify-start items-center gap-3"
      >
        <div
          class="profile-pic rounded-full bg-[#83009a] w-8 h-8 flex items-center justify-center text-white text-lg"
          v-if="authStore.profile?.profile_picture_url"
        >
          <img
            v-if="authStore.profile?.profile_picture_url"
            :src="authStore.profile.profile_picture_url"
            alt="Account Image"
            class="w-8 h-8 rounded-full object-cover"
          />
        </div>
        <div
          class="profile-pic rounded-full bg-[#83009a] w-8 h-8 flex items-center justify-center text-white text-lg"
          v-else
        >
          {{ authStore.profile?.first_name.charAt(0) || 'U' }}
        </div>
        <div class="creds flex flex-col justify-start items-start">
          <div class="name text-black text-sm">
            {{ `${authStore.profile?.first_name} ${authStore.profile?.last_name}` || 'Loading' }}
          </div>
          <div class="username text-[#83009a] text-xs">@{{ profile?.username || 'Loading' }}</div>
        </div>
      </div>
      <button
        v-else
        class="account w-full h-full flex flex-row justify-center items-center gap-3 relative cursor-pointer"
        @click.stop="toggleDropdown"
      >
        <div
          class="profile-pic rounded-full bg-[#83009a] w-8 h-8 flex items-center justify-center text-white text-lg"
          v-if="authStore.profile?.profile_picture_url"
        >
          <img
            v-if="authStore.profile?.profile_picture_url"
            :src="authStore.profile.profile_picture_url"
            alt="Account Image"
            class="w-8 h-8 rounded-full object-cover"
          />
        </div>
        <div
          class="profile-pic rounded-full bg-[#83009a] w-8 h-8 flex items-center justify-center text-white text-lg"
          v-else
        >
          {{ authStore.profile?.first_name.charAt(0) || 'U' }}
        </div>
        <Transition
          enter-active-class="transition duration-150"
          enter-from-class="opacity-0 translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-100"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 translate-y-2"
        >
          <div
            v-if="showDropdown"
            class="absolute bottom-10 left-0 mb-2 w-40 bg-white rounded-lg border-2 border-gray-300 z-50"
          >
            <button
              @click="openSettings"
              class="w-full text-left px-4 py-2 hover:bg-[#EBEBEB] text-gray-500 !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
            >
              <span class="material-symbols-outlined !text-base"> settings </span>
              {{isLangEnglish? 'Settings' : 'Pengaturan'}}
            </button>

            <RouterLink
              to="/dash/help"
              class="w-full text-left px-4 py-2 hover:bg-[#EBEBEB] text-gray-500 !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
            >
              <span class="material-symbols-outlined !text-base"> help </span>
              {{isLangEnglish? 'Help' : 'Bantuan'}}
            </RouterLink>

            <button
              @click="logoutButton"            
              class="w-full text-left hover:bg-[#EBEBEB] px-4 py-2 text-red-500 !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
            >
              <span class="material-symbols-outlined !text-base"> power_settings_new </span>
              {{isLangEnglish? 'Log Out' : 'Keluar'}}
            </button>
          </div>
        </Transition>
      </button>

      <div v-if="!isCollapsed" class="dropdown-container relative">
        <button
          @click.stop="toggleDropdown"
          class="px-1 py-1 hover:bg-[#EBEBEB] cursor-pointer rounded-[5px] transition transition-all duration-100"
        >
          <span
            class="material-symbols-outlined !text-lg text-[#83009a] cursor-pointer group-hover:text-[#6d0080] transition transition-all duration-100"
          >
            more_vert
          </span>
        </button>
        <Transition
          enter-active-class="transition duration-150"
          enter-from-class="opacity-0 translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-100"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 translate-y-2"
        >
          <div
            v-if="showDropdown"
            class="absolute bottom-10 left-0 mb-2 w-40 bg-white rounded-lg border-2 border-gray-300 z-50"
          >
            <button
              @click="settingsToggle"
              class="w-full text-left px-4 py-2 hover:bg-[#EBEBEB] text-gray-500 !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
            >
              <span class="material-symbols-outlined !text-base"> settings </span>
              {{isLangEnglish? 'Settings' : 'Pengaturan'}}
            </button>

            <RouterLink
              to="/dash/help"
              class="w-full text-left px-4 py-2 hover:bg-[#EBEBEB] text-gray-500 !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
            >
              <span class="material-symbols-outlined !text-base"> help </span>
              {{isLangEnglish? 'Help' : 'Bantuan'}}
            </RouterLink>

            <button
              @click="logoutButton"            
              class="w-full text-left hover:bg-[#EBEBEB] px-4 py-2 text-red-500 !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
            >
              <span class="material-symbols-outlined !text-base"> power_settings_new </span>
              {{isLangEnglish? 'Log Out' : 'Keluar'}}
            </button>
          </div>
        </Transition>
      </div>
    </div>
    <settingsModal />
  </div>
  <div
    v-else
    :class="[
      'h-screen flex flex-col bg-[#090909] border-r border-[#202020] transition-all duration-300',
      isCollapsed ? 'w-[80px]' : 'w-[30%]',
    ]"
  >
    <div v-if="!isCollapsed" class="flex items-center justify-between px-3 py-3 text-[#83009a]">
      <button class="p-2 flex items-center justify-center cursor-pointer">
        <span class="material-symbols-outlined !text-3xl">graphic_eq</span>
      </button>

      <button
        v-if="!isCollapsed"
        @click="toggleSidebar"
        class="px-2 py-1 hover:bg-[#1b1b1b] cursor-pointer rounded-[5px] transition transition-all duration-100"
      >
        <span class="material-symbols-outlined !text-xl">
          {{ isCollapsed ? 'dock_to_right' : 'dock_to_left' }}
        </span>
      </button>
    </div>
    <div v-else class="flex items-center justify-center px-3 py-3 text-[#83009a]">
      <button
        @click="isCollapsed = !isCollapsed"
        @mouseenter="isHover = true"
        @mouseleave="isHover = false"
        class="p-2 flex items-center justify-center cursor-pointer hover:bg-[#1b1b1b] rounded-[5px] h-10 h-max-10 w-10"
      >
        <span class="material-symbols-outlined" :class="isHover ? '!text-xl' : '!text-3xl'">
          {{ isHover ? 'dock_to_left' : 'graphic_eq' }}
        </span>
      </button>
    </div>

    <div
      class="flex-1 overflow-y-auto flex flex-col justify-start items-center px-4 !mt-10"
      :class="isCollapsed ? 'gap-4' : 'gap-2'"
    >
      <RouterLink
        v-if="!isCollapsed"
        to="/dash"
        class="w-full flex flex-row justify-start items-center bg-[#83009a] rounded-[10px] p-2 gap-5 group cursor-pointer hover:bg-[#6d0080] transition transition-all duration-100"
      >
        <div class="bulet rounded-full bg-white flex items-center justify-center">
          <span
            class="material-symbols-outlined !text-black text-base group-hover:rotate-180 transition transition-all duration-900"
          >
            add
          </span>
        </div>
        <div class="text-white text-sm !font-semibold">
          {{ isLangEnglish ? 'New Scan' : 'Pemindaian Baru' }}
        </div>
      </RouterLink>
      <RouterLink
        v-else
        to="/dash"
        class="w-full flex flex-row justify-center items-center bg-[#83009a] rounded-[10px] p-2 gap-5 group cursor-pointer hover:bg-[#6d0080] transition transition-all duration-100"
      >
        <div class="bulet rounded-full bg-white flex items-center justify-center">
          <span
            class="material-symbols-outlined !text-black text-base group-hover:rotate-180 transition transition-all duration-900"
          >
            add
          </span>
        </div>
      </RouterLink>

      <div
        v-if="!isCollapsed"
        class="recent-detections h-full w-full flex flex-col justify-start items-center ps-2"
      >
        <div class="top flex flex-row justify-between items-start w-full">
          <div class="left h-full flex flex-row justify-start gap-5 items-center">
            <span class="material-symbols-outlined text-[#83009a]"> history </span>
            <div class="text-white text-sm">
              {{ isLangEnglish ? 'Recent Detections' : 'Deteksi Terbaru' }}
            </div>
          </div>
          <div class="recent-dropdown-container relative">
            <button
              @click.stop="toggleDropdownRecent"
              class="right relative group flex justify-center items-center hover:bg-[#1b1b1b] rounded-[5px] py-1 px-2 transition transition-all duration-100 cursor-pointer"
            >
              <span
                class="material-symbols-outlined !text-lg text-[#83009a] cursor-pointer group-hover:text-[#6d0080] transition transition-all duration-100"
              >
                discover_tune
              </span>
            </button>
            <Transition
              enter-active-class="transition duration-150"
              enter-from-class="opacity-0 -translate-y-2"
              enter-to-class="opacity-100 translate-y-0"
              leave-active-class="transition duration-100"
              leave-from-class="opacity-100 translate-y-0"
              leave-to-class="opacity-0 -translate-y-2"
            >
              <div
                v-if="showDropdownRecent"
                class="absolute top-full right-0 mb-2 w-40 bg-black rounded-lg border-2 border-[#1b1b1b] z-50"
              >
                <RouterLink
                  to="/dash/manage-history"
                  class="w-full text-left px-4 py-2 hover:bg-[#1b1b1b] text-gray-500 !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
                >
                  <span class="material-symbols-outlined !text-base text-[#83009a]">
                    manage_history
                  </span>
                  {{ isLangEnglish ? 'Manage History' : 'Kelola Riwayat' }}
                </RouterLink>
              </div>
            </Transition>
          </div>
        </div>
        <div
          v-if="fetchHistoryLoading"
          class="content h-80 w-full flex flex-col justify-center items-center gap-2 pt-5"
        >
          <div
            class="w-8 h-8 border-4 border-gray-300 border-t-purple-700 rounded-full animate-spin"
          ></div>
          <p class="text-gray-400 text-center">Loading</p>
        </div>
        <div
          v-else-if="histories.length === 0"
          class="content h-100 w-full flex flex-col justify-center items-center gap-2 pt-5"
        >
          <span class="material-symbols-outlined text-gray-500"> history_off </span>
          <p class="text-gray-400 text-center">
            {{ isLangEnglish ? 'No recent detections' : 'Tidak Ada Deteksi Terbaru' }}
          </p>
        </div>
        <div
          v-else
          class="content h-fit max-h-90 w-full flex flex-col gap-2 py-2 ps-5 overflow-y-scroll"
        >
          <RouterLink
            :to="`/dash/predictions/${lagu.id}`"
            class="recent-preds w-65 py-1 px-3 flex flex-row justify-start items-start text-[#6d6d6d] hover:text-white text-sm hover:bg-[#1b1b1b] rounded-[5px] hover:border-r-3 hover:border-[#83009a] cursor-pointer transition transition-all duration-100"
            v-for="lagu in histories"
            :key="lagu.id"
          >
            <span class="truncate block w-full text-left">
              {{ lagu.song_title }}
            </span>
          </RouterLink>
        </div>
      </div>
      <div v-else class="recent-detections h-fit w-full flex flex-col justify-center items-center">
        <div class="top flex flex-row justify-center items-center w-full">
          <div class="left h-full flex flex-row justify-center gap-5 items-center">
            <span class="material-symbols-outlined text-[#83009a]"> history </span>
          </div>
        </div>
      </div>
    </div>

    <div class="border-t border-[#202020] p-3 flex items-center justify-between">
      <div
        v-if="!isCollapsed"
        class="account w-full h-full flex flex-row justify-start items-center gap-3"
      >
        <div
          class="profile-pic rounded-full bg-[#83009a] w-8 h-8 flex items-center justify-center text-white text-lg"
          v-if="authStore.profile?.profile_picture_url"
        >
          <img
            v-if="authStore.profile?.profile_picture_url"
            :src="authStore.profile.profile_picture_url"
            alt="Account Image"
            class="w-8 h-8 rounded-full object-cover"
          />
        </div>
        <div
          class="profile-pic rounded-full bg-[#83009a] w-8 h-8 flex items-center justify-center text-white text-lg"
          v-else
        >
          {{ authStore.profile?.first_name.charAt(0) || 'U' }}
        </div>
        <div class="creds flex flex-col justify-start items-start">
          <div class="name text-white text-sm">
            {{ `${authStore.profile?.first_name} ${authStore.profile?.last_name}` || 'Loading' }}
          </div>
          <div class="username text-[#83009a] text-xs">@{{ profile?.username || 'Loading' }}</div>
        </div>
      </div>
      <button
        v-else
        class="account w-full h-full flex flex-row justify-center items-center gap-3 relative cursor-pointer"
        @click.stop="toggleDropdown"
      >
        <div
          class="profile-pic rounded-full bg-[#83009a] w-8 h-8 flex items-center justify-center text-white text-lg"
          v-if="authStore.profile?.profile_picture_url"
        >
          <img
            v-if="authStore.profile?.profile_picture_url"
            :src="authStore.profile.profile_picture_url"
            alt="Account Image"
            class="w-8 h-8 rounded-full object-cover"
          />
        </div>
        <div
          class="profile-pic rounded-full bg-[#83009a] w-8 h-8 flex items-center justify-center text-white text-lg"
          v-else
        >
          {{ authStore.profile?.first_name.charAt(0) || 'U' }}
        </div>
        <Transition
          enter-active-class="transition duration-150"
          enter-from-class="opacity-0 translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-100"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 translate-y-2"
        >
          <div
            v-if="showDropdown"
            class="absolute bottom-10 left-0 mb-2 w-40 bg-black rounded-lg border-2 border-[#1b1b1b] z-50"
          >
            <button
              @click="openSettings"
              class="w-full text-left px-4 py-2 hover:bg-[#1b1b1b] text-[#6d6d6d] !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
            >
              <span class="material-symbols-outlined !text-base"> settings </span>
              {{ isLangEnglish ? 'Settings' : 'Pengaturan' }}
            </button>

            <RouterLink
              to="/dash/help"
              class="w-full text-left px-4 py-2 hover:bg-[#1b1b1b] text-[#6d6d6d] !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
            >
              <span class="material-symbols-outlined !text-base"> help </span>
              {{ isLangEnglish ? 'Help' : 'Bantuan' }}
            </RouterLink>

            <button
            
              @click="logoutButton"   
              class="w-full text-left hover:bg-[#1b1b1b] px-4 py-2 text-red-500 !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
            >
              <span class="material-symbols-outlined !text-base"> power_settings_new </span>
              {{ isLangEnglish ? 'Log Out' : 'Keluar' }}
            </button>
          </div>
        </Transition>
      </button>

      <div v-if="!isCollapsed" class="dropdown-container relative">
        <button
          @click.stop="toggleDropdown"
          class="px-1 py-1 hover:bg-[#1b1b1b] cursor-pointer rounded-[5px] transition transition-all duration-100"
        >
          <span
            class="material-symbols-outlined !text-lg text-[#83009a] cursor-pointer group-hover:text-[#6d0080] transition transition-all duration-100"
          >
            more_vert
          </span>
        </button>
        <Transition
          enter-active-class="transition duration-150"
          enter-from-class="opacity-0 translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-100"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 translate-y-2"
        >
          <div
            v-if="showDropdown"
            class="absolute bottom-10 left-0 mb-2 w-40 bg-black rounded-lg border-2 border-[#1b1b1b] z-50"
          >
            <button
              @click="settingsToggle"
              class="w-full text-left px-4 py-2 hover:bg-[#1b1b1b] text-[#6d6d6d] !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
            >
              <span class="material-symbols-outlined !text-base"> settings </span>
              {{ isLangEnglish ? 'Settings' : 'Pengaturan' }}
            </button>

            <RouterLink
              to="/dash/help"
              class="w-full text-left px-4 py-2 hover:bg-[#1b1b1b] text-[#6d6d6d] !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
            >
              <span class="material-symbols-outlined !text-base"> help </span>
              {{ isLangEnglish ? 'Help' : 'Bantuan' }}
            </RouterLink>

            <button
            
              @click="logoutButton"   
              class="w-full text-left hover:bg-[#1b1b1b] px-4 py-2 text-red-500 !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
            >
              <span class="material-symbols-outlined !text-base"> power_settings_new </span>
              {{ isLangEnglish ? 'Log Out' : 'Keluar' }}
            </button>
          </div>
        </Transition>
      </div>
    </div>
    <settingsModal />
  </div>
  <logoutConfirmationModal/>
</template>
