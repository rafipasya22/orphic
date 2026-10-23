<script setup lang="ts">
import { API_URL } from '@/config'
import { ref, watch, onMounted, onUnmounted } from 'vue';
import axios from 'axios';
import { munculinTooltip } from '../composable/tooltip';
import { generateUsernameFunc } from '../composable/generateUsername';
import { openSettingsFunc } from '../composable/openSettings';
import { gantiBahasaFunc } from '../composable/gantiBahasa';
import { useAuthStore } from '../stores/authstore';
import { darkFunc } from '../composable/darkMode';

const { isDarkMode } = darkFunc();
const { tooltipVisible, hoverbtn, Gahoverbtn } = munculinTooltip();
const { username, generateUsername } = generateUsernameFunc();
const { closeSettings, isSettingsopen } = openSettingsFunc();
const { isLangEnglish, ganti } = gantiBahasaFunc();
const authStore = useAuthStore();
const isProfileSetting = ref(true);
const isWebSetting = ref(false);

const profileEmail = ref<string>('');
const profilePassword = ref<string>('');
const confirmProfilePassword = ref<string>('');
const profileFirstName = ref<string>('');
const profileLastName = ref<string>('');
const profileImage = ref<File | null>(null);
const previewImage = ref('');
const fileInput = ref<HTMLInputElement | null>(null);
const changeLoading = ref(false);
const isDeletLoading = ref(false);

const openFilePicker = () => {
  fileInput.value?.click();
};

const setProfileSettingActive = () => {
  isProfileSetting.value = true;
  if (isWebSetting.value) {
    isWebSetting.value = false;
  }
};

const setWebSettingActive = () => {
  isWebSetting.value = true;
  if (isProfileSetting.value) {
    isProfileSetting.value = false;
  }
};

const handleImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;

  if (!target.files || !target.files[0]) {
    return;
  }

  profileImage.value = target.files[0];

  previewImage.value = URL.createObjectURL(profileImage.value);
};

const user = authStore.user;

const submitChanges = async () => {
  changeLoading.value = true;

  try {
    const formData = new FormData();

    formData.append('userId', user.id);

    formData.append('profileEmail', profileEmail.value);

    formData.append('profilePassword', profilePassword.value);

    formData.append('profileUsername', username.value);

    formData.append('profileFirstName', profileFirstName.value);

    formData.append('profileLastName', profileLastName.value);

    formData.append('confirmProfilePassword', confirmProfilePassword.value);

    if (profileImage.value) {
      formData.append('profileImage', profileImage.value);
    }

    const res = await axios.post(`${API_URL}/api/changes`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    console.log(res.data);
    await authStore.fetchProfile();

    window.location.reload();
  } catch (err) {
    console.log(err);
  } finally {
    changeLoading.value = false;
  }
};

interface savedSong {
  audio_id: string;
  filename: string;
  duration: number;
  file_path: string;
}

const savedSongs = ref<savedSong[]>([]);

const fetchSaved = async () => {
  const user = authStore.user;
  try {
    if (!user) {
      return;
    }

    const res = await axios.get(`${API_URL}/audio/info/${user.id}`);

    savedSongs.value = res.data as savedSong[];
  } catch (err) {
    console.log(err);
  }
};

const formatTime = (seconds: number) => {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);

  return `${mins}:${secs.toString().padStart(2, '0')}`;
};

const deleteSaved = async (audioId: string) => {
  isDeletLoading.value = true;
  try {
    await axios.delete(`${API_URL}/audio/user/${audioId}`);

    savedSongs.value = savedSongs.value.filter((item) => item.audio_id !== audioId);
  } catch (err) {
    console.log(err);
  } finally {
    isDeletLoading.value = false;
  }
};

const deleteAllSaved = async (user_id: string) => {
  isDeletLoading.value = true;
  try {
    await axios.delete(`${API_URL}/audio/user/${user_id}/all`);
    fetchSaved();
  } catch (err) {
    console.log(err);
  } finally {
    isDeletLoading.value = false;
  }
};

watch(
  () => isSettingsopen.value,
  (opened) => {
    if (opened && authStore.profile) {
      fetchSaved();
      username.value = authStore.profile.username || '';

      profileFirstName.value = authStore.profile.first_name || '';

      profileLastName.value = authStore.profile.last_name || '';
    }
  },
);

onMounted(() => {
  console.log('tolong');
  fetchSaved();
});

onUnmounted(() => {
  console.log('gatau');
});
</script>

<template>
  <div
    v-if="!isDarkMode"
    @click.self="closeSettings"
    class="bgmodal fixed inset-0 flex items-center justify-center transition-opacity duration-500 z-20"
    :class="isSettingsopen ? 'bg-black/50' : 'pointer-events-none'"
  >
    <div
      class="modal x rounded-lg w-200 h-130 relative transition-all duration-500 flex flex-row justify-start items-center overflow-hidden"
      :class="
        isSettingsopen
          ? isDarkMode
            ? 'bg-[#090909] translate-y-0'
            : ' translate-y-0 bg-white'
          : ' -translate-y-200'
      "
    >
      <div
        class="left h-full w-[20%] flex flex-col justify-start items-start border-r-1 border-gray-200"
      >
        <button
          @click="setProfileSettingActive"
          class="w-full h-fit text-left px-3 py-3 hover:bg-gray-300 hover:border-r-3 hover:border-[#83009a] text-gray-500 !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
          :class="isProfileSetting ? 'bg-[#EBEBEB] border-r-3 border-[#83009a]' : ''"
        >
          <span class="material-symbols-outlined !text-base text-[#83009a]"> person </span>
          {{ isLangEnglish ? 'Profile' : 'Profil' }}
        </button>
        <button
          @click="setWebSettingActive"
          class="w-full h-fit text-left px-3 py-3 hover:bg-gray-300 hover:border-r-3 hover:border-[#83009a] text-gray-500 !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
          :class="isWebSetting ? 'bg-[#EBEBEB] border-r-3 border-[#83009a]' : ''"
        >
          <span class="material-symbols-outlined !text-base text-[#83009a]"> language </span>
          {{ isLangEnglish ? 'Web Settings' : 'Pengaturan Web' }}
        </button>
      </div>
      <div
        v-if="isProfileSetting"
        class="right h-full w-[80%] px-3 py-6 flex flex-col justify-start items-center"
      >
        <div
          class="atas flex flex-col justify-start items-start w-full h-full overflow-hidden gap-4"
        >
          <div class="content w-full h-fit flex flex-row justify-start items-start gap-2">
            <div
              class="kiri w-[25%] border border-gray-300 rounded-[10px] flex flex-col justify-center items-center py-4 gap-2"
            >
              <img
                v-if="previewImage"
                :src="previewImage"
                class="w-16 h-16 rounded-full object-cover"
              />

              <img
                v-else-if="authStore.profile?.profile_picture_url"
                :src="authStore.profile.profile_picture_url"
                class="w-16 h-16 rounded-full object-cover"
              />

              <img
                v-else
                src="../assets/imgs/user-default.png"
                class="w-16 h-16 rounded-full object-cover bg-gray-200"
              />
              <div class="textandname flex flex-col justify-center items-center gap-0">
                <div class="name text-base font-bold text-[#83009a]">
                  {{ `${authStore.profile?.first_name} ${authStore.profile?.last_name}` }}
                </div>
                <div class="username text-xs text-gray-700">@{{ authStore.profile?.username }}</div>
              </div>
              <button
                @click="openFilePicker"
                class="text-xs text-[#83009a] hover:underline cursor-pointer"
              >
                {{ isLangEnglish ? 'Edit Photo' : 'Edit Foto' }}
              </button>
            </div>
            <div
              class="kanan w-[75%] border border-gray-300 rounded-[10px] flex flex-col justify-center items-center py-4 gap-2"
            >
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleImageUpload"
              />
              <div class="name-form flex flex-row justify-start items-start w-[95%] gap-3">
                <div class="firstname-input flex flex-col justify-start items-start w-[70%]">
                  <div class="title">
                    <p class="text-xs text-[#83009a]">
                      {{ isLangEnglish ? 'First Name' : 'Nama Depan' }}
                    </p>
                  </div>
                  <input
                    v-if="isLangEnglish"
                    v-model="profileFirstName"
                    type="first name"
                    placeholder="Change first name"
                    class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-full text-black"
                  />
                  <input
                    v-else
                    v-model="profileFirstName"
                    type="first name"
                    placeholder="Ganti nama depan"
                    class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-full text-black"
                  />
                </div>
                <div class="lastName-input flex flex-col justify-start items-start w-full">
                  <div class="title">
                    <p class="text-xs text-[#83009a]">
                      {{ isLangEnglish ? 'Last Name' : 'Nama Belakang' }}
                    </p>
                  </div>
                  <input
                    v-if="isLangEnglish"
                    v-model="profileLastName"
                    type="last name"
                    placeholder="Change last name"
                    class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-full text-black"
                  />
                  <input
                    v-else
                    v-model="profileLastName"
                    type="last name"
                    placeholder="Ganti nama belakang"
                    class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-full text-black"
                  />
                </div>
              </div>

              <div
                class="emailandusername-form flex flex-col justify-start items-center gap-3 w-[95%]"
              >
                <div class="Username-input flex flex-col justify-start items-start w-full">
                  <div class="title">
                    <p class="text-xs text-[#83009a]">Username</p>
                  </div>
                  <div
                    class="input flex flex-row justify-start items-center gap-2 border border-gray-300 rounded-md w-full"
                  >
                    <input
                      v-if="isLangEnglish"
                      v-model="username"
                      type="text"
                      placeholder="Change your Username"
                      class="mt-1 px-3 py-2 w-full text-black w-[80%]"
                    />
                    <input
                      v-else
                      v-model="username"
                      type="text"
                      placeholder="Ganti username Anda"
                      class="mt-1 px-3 py-2 w-full text-black w-[80%]"
                    />
                    <button
                      type="button"
                      class="generate-username relative text-gray-500 flex items-center h-full w-[15%] cursor-pointer group"
                      @click="generateUsername"
                      @mouseenter="hoverbtn"
                      @mouseleave="Gahoverbtn"
                    >
                      <span
                        class="material-symbols-outlined rotate-45 group-hover:text-[#83009a] group-hover:rotate-135 transition transition-all duration-500"
                      >
                        cached
                      </span>
                      <div
                        v-if="tooltipVisible"
                        class="absolute -right-10 -top-7 bg-black text-white text-xs px-2 py-1 rounded whitespace-nowrap"
                      >
                        Generate username
                      </div>
                    </button>
                  </div>
                </div>
              </div>
              <div class="pass-form flex flex-row justify-start items-center gap-3 w-[95%]">
                <div class="password-input flex flex-col justify-start items-start w-full">
                  <div class="title">
                    <p class="text-xs text-[#83009a]">Password</p>
                  </div>
                  <input
                    v-if="isLangEnglish"
                    v-model="profilePassword"
                    type="password"
                    placeholder="Change your password"
                    class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-full text-black"
                  />
                  <input
                    v-else
                    v-model="profilePassword"
                    type="password"
                    placeholder="Ganti password Anda"
                    class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-full text-black"
                  />
                </div>
                <div class="confirm-password-input flex flex-col justify-start items-start w-full">
                  <div class="title">
                    <p class="text-xs text-[#83009a]">Confirm Password</p>
                  </div>
                  <input
                    v-if="isLangEnglish"
                    v-model="confirmProfilePassword"
                    type="password"
                    placeholder="Confirm your new password"
                    class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-full text-black"
                  />
                  <input
                    v-else
                    v-model="confirmProfilePassword"
                    type="password"
                    placeholder="Konfirmasi password baru Anda"
                    class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-full text-black"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="bawah flex flex-row justify-end items-center gap-2 w-full">
          <button
            @click="closeSettings"
            class="cancel flex flex-row justify-center items-center border border-gray-300 bg-gray-300 rounded-[10px] w-24 px-2 py-2 cursor-pointer gap-2 hover:bg-gray-500 transition transition-all duration-300"
          >
            <p class="text-xs text-[#83009a] font-bold">{{ isLangEnglish ? 'Cancel' : 'Batal' }}</p>
          </button>
          <button
            @click="submitChanges"
            class="submitedit flex flex-row justify-center items-center border border-[#83009a] rounded-[10px] w-24 px-2 py-2 cursor-pointer gap-2 hover:bg-[#480254] bg-[#83009a] transition transition-all duration-300"
          >
            <p class="text-xs text-white font-bold">
              {{ isLangEnglish ? 'Save Changes' : 'Simpan' }}
            </p>
          </button>
        </div>
      </div>
      <div
        v-else
        class="right h-full w-[80%] px-3 py-6 flex flex-col justify-start items-start gap-3"
      >
        <div class="appearance-settings flex flex-col justify-start items-start gap-2 w-full">
          <p class="text-[#83009a] !text-sm">
            {{ isLangEnglish ? 'Web Appearances' : 'Penampilan Web' }}
          </p>
          <div class="lang flex flex-row justify-between items-center w-full px-4">
            <div class="text-xs text-gray-700 font-bold">
              {{ isLangEnglish ? 'Page Language:' : 'Bahasa Halaman:' }}
            </div>
            <div class="language-options flex flex-row justify-start items-center gap-1">
              <button
                @click="ganti()"
                class="text-[#ae04cc] hover:text-[#480254] disabled:no-underline underline text-xs transition flex flex-row justify-start items-center gap-2 disabled:text-gray-400 disabled:pointer-events-none cursor-pointer"
                :disabled="isLangEnglish"
              >
                {{ isLangEnglish ? 'English' : 'Bahasa Inggris' }}
              </button>
              <div class="divider text-[#ae04cc] text-xs">/</div>
              <button
                @click="ganti()"
                class="text-[#ae04cc] hover:text-[#480254] disabled:no-underline underline text-xs transition flex flex-row justify-start items-center gap-2 disabled:text-gray-400 disabled:pointer-events-none cursor-pointer"
                :disabled="!isLangEnglish"
              >
                {{ isLangEnglish ? 'Indonesian' : 'Bahasa Indonesia' }}
              </button>
            </div>
          </div>
          <div class="theme flex flex-row justify-between items-center w-full px-4">
            <div class="text-xs text-gray-700 font-bold">
              {{ isLangEnglish ? 'Dark Mode:' : 'Mode Gelap:' }}
            </div>
            <button
              @click="isDarkMode = !isDarkMode"
              class="relative inline-flex h-4 w-8 items-center rounded-full transition-colors duration-300 cursor-pointer"
              :class="isDarkMode ? 'bg-[#83009a]' : 'bg-gray-300'"
            >
              <span
                class="inline-block h-2 w-2 transform rounded-full bg-white transition-transform duration-300"
                :class="isDarkMode ? 'translate-x-5' : 'translate-x-1'"
              />
            </button>
          </div>
        </div>

        <div class="cache flex flex-col justify-start items-start gap-2 w-full">
          <p class="text-[#83009a] !text-sm">
            {{ isLangEnglish ? 'Storage' : 'Penyimpanan' }}
          </p>
          <div class="saved-songs flex flex-col justify-start items-start w-full h-fit gap-3">
            <div class="option flex flex-row justify-between items-center w-full px-4">
              <div class="text-xs text-gray-700 font-bold">
                {{
                  isLangEnglish ? 'Saved Songs in History:' : 'Lagu yang Tersimpan dalam Riwayat:'
                }}
              </div>
            </div>
            <div
              class="flex flex-col justify-start items-center w-full h-80 h-max-80 overflow-y-scroll px-4"
            >
              <div
                v-for="(items, index) in savedSongs"
                :key="index"
                class="items flex flex-row justify-between px-3 py-2 w-full border-b border-gray-300"
              >
                <div class="flex flex-col justify-start items-start w-fit gap-1">
                  <p class="text-black !text-sm w-60 truncate">{{ items?.filename }}</p>
                  <p class="text-[#83009a] !text-xs">{{ formatTime(items?.duration!) }}</p>
                </div>

                <button
                  @click="deleteSaved(items?.audio_id)"
                  class="delet w-8 h-8 text-base cursor-pointer rounded-full hover:bg-red-300 text-red-700 hover:text-red-900 flex justify-center items-center transition transition-all duration-300 cursor-pointer"
                >
                  <span class="material-symbols-outlined"> delete </span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div
    v-else
    @click.self="closeSettings"
    class="bgmodal fixed inset-0 flex items-center justify-center transition-opacity duration-500 z-20"
    :class="isSettingsopen ? 'bg-black/50' : 'pointer-events-none'"
  >
    <div
      class="modal bg-[#090909] rounded-lg w-200 h-130 relative transition-all duration-500 flex flex-row justify-start items-center overflow-hidden"
      :class="isSettingsopen ? ' translate-y-0' : ' -translate-y-200'"
    >
      <div
        class="left h-full w-[20%] flex flex-col justify-start items-start border-r-1 border-[#202020]"
      >
        <button
          @click="setProfileSettingActive"
          class="w-full h-fit text-left px-3 py-3 hover:bg-[#2b2b2b] hover:border-r-3 hover:border-[#83009a] text-[#6d6d6d] !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
          :class="isProfileSetting ? 'bg-[#1b1b1b] border-r-3 border-[#83009a]' : ''"
        >
          <span class="material-symbols-outlined !text-base text-[#83009a]"> person </span>
          {{ isLangEnglish ? 'Profile' : 'Profil' }}
        </button>
        <button
          @click="setWebSettingActive"
          class="w-full h-fit text-left px-3 py-3 hover:bg-[#2b2b2b] hover:border-r-3 hover:border-[#83009a] text-[#6d6d6d] !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
          :class="isWebSetting ? 'bg-[#1b1b1b] border-r-3 border-[#83009a]' : ''"
        >
          <span class="material-symbols-outlined !text-base text-[#83009a]"> language </span>
          {{ isLangEnglish ? 'Web Settings' : 'Pengaturan Web' }}
        </button>
      </div>
      <div
        v-if="isProfileSetting"
        class="right h-full w-[80%] px-3 py-6 flex flex-col justify-start items-center"
      >
        <div
          class="atas flex flex-col justify-start items-start w-full h-full overflow-hidden gap-4"
        >
          <div class="content w-full h-fit flex flex-row justify-start items-start gap-2">
            <div
              class="kiri w-[25%] border border-[#202020] rounded-[10px] flex flex-col justify-center items-center py-4 gap-2"
            >
              <img
                v-if="previewImage"
                :src="previewImage"
                class="w-16 h-16 rounded-full object-cover"
              />

              <img
                v-else-if="authStore.profile?.profile_picture_url"
                :src="authStore.profile.profile_picture_url"
                class="w-16 h-16 rounded-full object-cover"
              />

              <img
                v-else
                src="../assets/imgs/user-default.png"
                class="w-16 h-16 rounded-full object-cover bg-gray-200"
              />
              <div class="textandname flex flex-col justify-center items-center gap-0">
                <div class="name text-base font-bold text-[#83009a]">
                  {{ `${authStore.profile?.first_name} ${authStore.profile?.last_name}` }}
                </div>
                <div class="username text-xs text-gray-700">@{{ authStore.profile?.username }}</div>
              </div>
              <button
                @click="openFilePicker"
                class="text-xs text-[#83009a] hover:underline cursor-pointer"
              >
                {{ isLangEnglish ? 'Edit Photo' : 'Edit Foto' }}
              </button>
            </div>
            <div
              class="kanan w-[75%] border border-[#202020] rounded-[10px] flex flex-col justify-center items-center py-4 gap-2"
            >
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleImageUpload"
              />
              <div class="name-form flex flex-row justify-start items-start w-[95%] gap-3">
                <div class="firstname-input flex flex-col justify-start items-start w-[70%]">
                  <div class="title">
                    <p class="text-xs text-[#83009a]">
                      {{ isLangEnglish ? 'First Name' : 'Nama Depan' }}
                    </p>
                  </div>
                  <input
                    v-if="isLangEnglish"
                    v-model="profileFirstName"
                    type="first name"
                    placeholder="Change first name"
                    class="mt-1 px-3 py-2 border border-[#1b1b1b] rounded-md w-full text-[#6d6d6d]"
                  />
                  <input
                    v-else
                    v-model="profileFirstName"
                    type="first name"
                    placeholder="Ganti nama depan"
                    class="mt-1 px-3 py-2 border border-[#1b1b1b] rounded-md w-full text-[#6d6d6d]"
                  />
                </div>
                <div class="lastName-input flex flex-col justify-start items-start w-full">
                  <div class="title">
                    <p class="text-xs text-[#83009a]">
                      {{ isLangEnglish ? 'Last Name' : 'Nama Belakang' }}
                    </p>
                  </div>
                  <input
                    v-if="isLangEnglish"
                    v-model="profileLastName"
                    type="last name"
                    placeholder="Change last name"
                    class="mt-1 px-3 py-2 border border-[#1b1b1b] rounded-md w-full text-[#6d6d6d]"
                  />
                  <input
                    v-else
                    v-model="profileLastName"
                    type="last name"
                    placeholder="Ganti nama belakang"
                    class="mt-1 px-3 py-2 border border-[#1b1b1b] rounded-md w-full text-[#6d6d6d]"
                  />
                </div>
              </div>

              <div
                class="emailandusername-form flex flex-col justify-start items-center gap-3 w-[95%]"
              >
                <div class="Username-input flex flex-col justify-start items-start w-full">
                  <div class="title">
                    <p class="text-xs text-[#83009a]">Username</p>
                  </div>
                  <div
                    class="input flex flex-row justify-start items-center gap-2 border border-[#1b1b1b] rounded-md w-full"
                  >
                    <input
                      v-if="isLangEnglish"
                      v-model="username"
                      type="text"
                      placeholder="Change your Username"
                      class="mt-1 px-3 py-2 w-full text-[#6d6d6d] w-[80%]"
                    />
                    <input
                      v-else
                      v-model="username"
                      type="text"
                      placeholder="Ganti username Anda"
                      class="mt-1 px-3 py-2 w-full text-[#6d6d6d] w-[80%]"
                    />
                    <button
                      type="button"
                      class="generate-username relative text-gray-500 flex items-center h-full w-[15%] cursor-pointer group"
                      @click="generateUsername"
                      @mouseenter="hoverbtn"
                      @mouseleave="Gahoverbtn"
                    >
                      <span
                        class="material-symbols-outlined rotate-45 group-hover:text-[#83009a] group-hover:rotate-135 transition transition-all duration-500"
                      >
                        cached
                      </span>
                      <div
                        v-if="tooltipVisible"
                        class="absolute -right-10 -top-7 bg-black text-white text-xs px-2 py-1 rounded whitespace-nowrap"
                      >
                        Generate username
                      </div>
                    </button>
                  </div>
                </div>
              </div>
              <div class="pass-form flex flex-row justify-start items-center gap-3 w-[95%]">
                <div class="password-input flex flex-col justify-start items-start w-full">
                  <div class="title">
                    <p class="text-xs text-[#83009a]">Password</p>
                  </div>
                  <input
                    v-if="isLangEnglish"
                    v-model="profilePassword"
                    type="password"
                    placeholder="Change your password"
                    class="mt-1 px-3 py-2 border border-[#1b1b1b] rounded-md w-full text-[#6d6d6d]"
                  />
                  <input
                    v-else
                    v-model="profilePassword"
                    type="password"
                    placeholder="Ganti password Anda"
                    class="mt-1 px-3 py-2 border border-[#1b1b1b] rounded-md w-full text-[#6d6d6d]"
                  />
                </div>
                <div class="confirm-password-input flex flex-col justify-start items-start w-full">
                  <div class="title">
                    <p class="text-xs text-[#83009a]">Confirm Password</p>
                  </div>
                  <input
                    v-if="isLangEnglish"
                    v-model="confirmProfilePassword"
                    type="password"
                    placeholder="Confirm your new password"
                    class="mt-1 px-3 py-2 border border-[#1b1b1b] rounded-md w-full text-[#6d6d6d]"
                  />
                  <input
                    v-else
                    v-model="confirmProfilePassword"
                    type="password"
                    placeholder="Konfirmasi password baru Anda"
                    class="mt-1 px-3 py-2 border border-[#1b1b1b] rounded-md w-full text-[#6d6d6d]"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="bawah flex flex-row justify-end items-center gap-2 w-full">
          <button
            @click="closeSettings"
            class="cancel flex flex-row justify-center items-center border border-[#1b1b1b] bg-[#1b1b1b] rounded-[10px] w-24 px-2 py-2 cursor-pointer gap-2 hover:bg-[#2b2b2b] transition transition-all duration-300"
          >
            <p class="text-xs text-[#83009a] font-bold">{{ isLangEnglish ? 'Cancel' : 'Batal' }}</p>
          </button>
          <button
            @click="submitChanges"
            class="submitedit flex flex-row justify-center items-center border border-[#83009a] rounded-[10px] w-24 px-2 py-2 cursor-pointer gap-2 hover:bg-[#480254] bg-[#83009a] transition transition-all duration-300"
          >
            <p class="text-xs text-white font-bold">
              {{ isLangEnglish ? 'Save Changes' : 'Simpan' }}
            </p>
          </button>
        </div>
      </div>
      <div
        v-else
        class="right h-full w-[80%] px-3 py-6 flex flex-col justify-start items-start gap-3"
      >
        <div class="appearance-settings flex flex-col justify-start items-start gap-2 w-full">
          <p class="text-[#83009a] !text-sm">
            {{ isLangEnglish ? 'Web Appearances' : 'Penampilan Web' }}
          </p>
          <div class="lang flex flex-row justify-between items-center w-full px-4">
            <div class="text-xs text-[#6d6d6d] font-bold">
              {{ isLangEnglish ? 'Page Language:' : 'Bahasa Halaman:' }}
            </div>
            <div class="language-options flex flex-row justify-start items-center gap-1">
              <button
                @click="ganti()"
                class="text-[#ae04cc] hover:text-[#480254] disabled:no-underline underline text-xs transition flex flex-row justify-start items-center gap-2 disabled:text-[#6d6d6d] disabled:pointer-events-none cursor-pointer"
                :disabled="isLangEnglish"
              >
                {{ isLangEnglish ? 'English' : 'Bahasa Inggris' }}
              </button>
              <div class="divider text-[#ae04cc] text-xs">/</div>
              <button
                @click="ganti()"
                class="text-[#ae04cc] hover:text-[#480254] disabled:no-underline underline text-xs transition flex flex-row justify-start items-center gap-2 disabled:text-[#6d6d6d] disabled:pointer-events-none cursor-pointer"
                :disabled="!isLangEnglish"
              >
                {{ isLangEnglish ? 'Indonesian' : 'Bahasa Indonesia' }}
              </button>
            </div>
          </div>
          <div class="theme flex flex-row justify-between items-center w-full px-4">
            <div class="text-xs text-[#6d6d6d] font-bold">
              {{ isLangEnglish ? 'Dark Mode:' : 'Mode Gelap:' }}
            </div>
            <button
              @click="isDarkMode = !isDarkMode"
              class="relative inline-flex h-4 w-8 items-center rounded-full transition-colors duration-300 cursor-pointer"
              :class="isDarkMode ? 'bg-[#83009a]' : 'bg-[#1b1b1b]'"
            >
              <span
                class="inline-block h-2 w-2 transform rounded-full bg-white transition-transform duration-300"
                :class="isDarkMode ? 'translate-x-5' : 'translate-x-1'"
              />
            </button>
          </div>
        </div>

        <div class="cache flex flex-col justify-start items-start gap-2 w-full">
          <p class="text-[#83009a] !text-sm">
            {{ isLangEnglish ? 'Storage' : 'Penyimpanan' }}
          </p>
          <div class="saved-songs flex flex-col justify-start items-start w-full h-fit gap-3">
            <div class="option flex flex-row justify-between items-center w-full px-4">
              <div class="text-xs text-[#6d6d6d] font-bold">
                {{
                  isLangEnglish ? 'Saved Songs in History:' : 'Lagu yang Tersimpan dalam Riwayat:'
                }}
              </div>
            </div>
            <div
              class="flex flex-col justify-start items-center w-full h-80 h-max-80 overflow-y-scroll px-4"
            >
              <div
                v-for="(items, index) in savedSongs"
                :key="index"
                class="items flex flex-row justify-between px-3 py-2 w-full border-b border-[#202020]"
              >
                <div class="flex flex-col justify-start items-start w-fit gap-1">
                  <p class="text-[#6d6d6d] !text-sm w-60 truncate">{{ items?.filename }}</p>
                  <p class="text-[#83009a] !text-xs">{{ formatTime(items?.duration!) }}</p>
                </div>

                <button
                  @click="deleteSaved(items?.audio_id)"
                  class="delet w-8 h-8 text-base cursor-pointer rounded-full hover:bg-red-300 text-red-700 hover:text-red-900 flex justify-center items-center transition transition-all duration-300 cursor-pointer"
                >
                  <span class="material-symbols-outlined"> delete </span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!--
      
      -->
    </div>
  </div>
  <div
    v-if="changeLoading && isDarkMode"
    class="absolute inset-0 flex-col flex items-center justify-center w-full h-full z-40 bg-black/70"
  >
    <div
      class="w-8 h-8 border-4 border-gray-500 border-t-purple-700 rounded-full animate-spin"
    ></div>
    <p>{{ isLangEnglish ? 'Saving Changes' : 'Menyimpan Perubahan' }}</p>
  </div>
  <div
    v-else-if="changeLoading && !isDarkMode"
    class="absolute inset-0 flex-col flex items-center justify-center w-full h-full z-40 bg-black/70"
  >
    <div
      class="w-8 h-8 border-4 border-gray-300 border-t-purple-700 rounded-full animate-spin"
    ></div>
    <p>{{ isLangEnglish ? 'Saving Changes' : 'Menyimpan Perubahan' }}</p>
  </div>
</template>
