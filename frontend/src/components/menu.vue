<script lang="ts" setup>
import { openMenufunc } from '../composable/openmenu';
import { openModalLogin } from '../composable/openmodalLogin';
import { openSettingsFunc } from '../composable/openSettings.ts';
import { openHistoryModal } from '../composable/openHistory';
import { gantiBahasaFunc } from '../composable/gantiBahasa';
import { useAuthStore } from '../stores/authstore';
import { logoutconffunc } from '../composable/logoutconf';
import LogoutModal from './logoutConfirmationModal.vue';
import { darkFunc } from '../composable/darkMode';

const { isDarkMode } = darkFunc();
const authStore = useAuthStore();
const { isMenuOpen, closeMenu } = openMenufunc();
const { openModal } = openModalLogin();
const { openSettings } = openSettingsFunc();
const { openHistory } = openHistoryModal();
const { isLangEnglish, ganti } = gantiBahasaFunc();
const { openlogoutconf } = logoutconffunc();
</script>

<template>
  <div v-if="!isDarkMode" class="wrapper-menu relative h-fit w-full">
    <div
      @click.self="closeMenu"
      class="fixed inset-0 flex items-center justify-center transition-opacity duration-500 z-20"
      :class="isMenuOpen ? 'bg-black/50' : 'pointer-events-none'"
    >
      <div
        class="bg-white absolute top-0 right-0 py-4 rounded-l-[10px] w-89 h-128 transition-all duration-500 flex flex-col justify-between items-start"
        :class="isMenuOpen ? ' translate-x-0' : ' -translate-x-[-500px]'"
      >
        <div class="content-atas flex flex-col justify-start items-start w-full px-6">
          <div class="top flex flex-row justify-between items-center w-full">
            <h2 class="text-lg text-[#83009a] font-bold">Menu</h2>
          </div>
          <div
            v-if="authStore.user"
            class="TOC flex flex-col justify-start items-start w-full pt-5"
          >
            <h4 class="text-sm text-[#83009a] font-bold">
              {{ isLangEnglish ? 'Quick Access' : 'Akses Cepat' }}
            </h4>
            <ul class="text-gray-700 text-sm flex flex-col gap-1 ps-4">
              <li>
                <RouterLink
                  to="/"
                  class="hover:text-[#83009a] transition flex flex-row justify-start items-center gap-2"
                >
                  <div class="bulet h-1 w-1 rounded-full bg-[#83009a]"></div>
                  {{ isLangEnglish ? 'Landing Page' : 'Halaman Utama' }}
                </RouterLink>
              </li>
              <li>
                <RouterLink
                  to="/dash"
                  class="hover:text-[#83009a] transition flex flex-row justify-start items-center gap-2"
                >
                  <div class="bulet h-1 w-1 rounded-full bg-[#83009a]"></div>
                  {{ isLangEnglish ? 'Dashboard' : 'Dasbor' }}
                </RouterLink>
              </li>

              <li>
                <RouterLink
                  to="/dash/help"
                  class="hover:text-[#83009a] transition flex flex-row justify-start items-center gap-2"
                >
                  <div class="bulet h-1 w-1 rounded-full bg-[#83009a]"></div>
                  {{ isLangEnglish ? 'Help & Support' : 'Bantuan & Dukungan' }}
                </RouterLink>
              </li>
              <li>
                <RouterLink
                  to="/dash/manage-history"
                  class="hover:text-[#83009a] transition flex flex-row justify-start items-center gap-2"
                >
                  <div class="bulet h-1 w-1 rounded-full bg-[#83009a]"></div>
                  {{ isLangEnglish ? 'History' : 'Riwayat' }}
                </RouterLink>
              </li>
            </ul>
          </div>
          <div class="PO flex flex-col justify-start items-start w-full pt-5">
            <h4 class="text-sm text-[#83009a] font-bold">
              {{ isLangEnglish ? 'Page Options' : 'Opsi Halaman' }}
            </h4>
            <div class="options flex flex-col justify-start items-start w-full gap-2">
              <div class="option flex flex-row justify-between items-center w-full">
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
              <div class="option-darkmode flex flex-row justify-between items-center w-full">
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
          </div>
        </div>
        <div
          v-if="authStore.user"
          class="content-bawah-loggedin flex flex-row justify-between items-center w-full px-3"
        >
          <button
            @click="openSettings"
            class="account-loggedin flex flex-row justify-start items-center w-[60%] gap-3 cursor-pointer group"
          >
            <img
              v-if="authStore.profile?.profile_picture_url"
              :src="authStore.profile.profile_picture_url"
              alt="Account Image"
              class="w-10 h-10 rounded-full object-cover"
            />
            <img
              v-else
              src="../assets/imgs/user-default.png"
              alt="Account Image"
              class="w-8 h-8 rounded-full object-cover"
            />
            <div class="account-name flex flex-col justify-start items-start gap-0 w-[80%]">
              <p
                class="text-sm text-start text-[#83009a] font-bold group-hover:text-[#480254] truncate w-full"
              >
                {{ `${authStore.profile?.first_name} ${authStore.profile?.last_name}` }}
              </p>
              <p class="text-xs text-gray-700/80">@{{ authStore.profile?.username }}</p>
            </div>
          </button>
          <button
            @click="openlogoutconf()"
            class="logoutAccount flex flex-row justify-start items-center gap-1 group cursor-pointer"
          >
            <p
              class="text-xs text-gray-500 transition transition-all duration-300 group-hover:text-red-800"
            >
              Log Out
            </p>
            <span
              class="material-symbols-outlined text-gray-500 transition transition-all duration-300 group-hover:text-red-800"
            >
              logout
            </span>
          </button>
        </div>
        <div
          v-else
          class="content-bawah-notloggedin flex flex-row justify-between items-center w-full px-3"
        >
          <div class="account-notloggedin flex flex-row justify-start items-center w-[40%] gap-2">
            <img
              src="../assets/imgs/user-default.png"
              alt="Account Image"
              class="w-8 h-8 rounded-full object-cover border border-gray-500"
            />
            <div class="account-name flex flex-col justify-start items-center gap-0">
              <p class="text-sm text-gray-500 font-bold">
                {{ isLangEnglish ? 'Not Logged In' : 'Belum Masuk' }}
              </p>
            </div>
          </div>
          <button
            @click="openModal()"
            class="LoginRedirect flex flex-row justify-start items-center gap-1 group cursor-pointer"
          >
            <p
              class="text-xs text-gray-500 transition transition-all duration-300 group-hover:text-[#83009a]"
            >
              {{ isLangEnglish ? 'Log in' : 'Masuk' }}
            </p>
            <span
              class="material-symbols-outlined text-gray-500 transition transition-all duration-300 group-hover:text-[#83009a]"
            >
              login
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="wrapper-menu relative h-fit w-full">
    <div
      @click.self="closeMenu"
      class="fixed inset-0 flex items-center justify-center transition-opacity duration-500 z-20"
      :class="isMenuOpen ? 'bg-black/50' : 'pointer-events-none'"
    >
      <div
        class="bg-[#2b2b2b] absolute top-0 right-0 py-4 rounded-l-[10px] w-89 h-128 transition-all duration-500 flex flex-col justify-between items-start"
        :class="isMenuOpen ? ' translate-x-0' : ' -translate-x-[-500px]'"
      >
        <div class="content-atas flex flex-col justify-start items-start w-full px-6">
          <div class="top flex flex-row justify-between items-center w-full">
            <h2 class="text-lg text-[#ae04cc] font-bold">Menu</h2>
            <button @click="closeMenu" class="text-gray-400 hover:cursor-pointer">✕</button>
          </div>
          <div
            v-if="authStore.user"
            class="TOC flex flex-col justify-start items-start w-full pt-5"
          >
            <h4 class="text-sm text-[#ae04cc] font-bold">
              {{ isLangEnglish ? 'Quick Access' : 'Akses Cepat' }}
            </h4>
            <ul class="text-gray-400 text-sm flex flex-col gap-1 ps-4">
              <li>
                <RouterLink
                  to="/"
                  class="hover:text-[#ae04cc] transition flex flex-row justify-start items-center gap-2"
                >
                  <div class="bulet h-1 w-1 rounded-full bg-[#83009a]"></div>
                  {{ isLangEnglish ? 'Landing Page' : 'Halaman Utama' }}
                </RouterLink>
              </li>
              <li>
                <RouterLink
                  to="/dash"
                  class="hover:text-[#ae04cc] transition flex flex-row justify-start items-center gap-2"
                >
                  <div class="bulet h-1 w-1 rounded-full bg-[#83009a]"></div>
                  {{ isLangEnglish ? 'Dashboard' : 'Dasbor' }}
                </RouterLink>
              </li>

              <li>
                <RouterLink
                  to="/dash/help"
                  class="hover:text-[#ae04cc] transition flex flex-row justify-start items-center gap-2"
                >
                  <div class="bulet h-1 w-1 rounded-full bg-[#83009a]"></div>
                  {{ isLangEnglish ? 'Help & Support' : 'Bantuan & Dukungan' }}
                </RouterLink>
              </li>
              <li>
                <RouterLink
                  to="/dash/manage-history"
                  class="hover:text-[#ae04cc] transition flex flex-row justify-start items-center gap-2"
                >
                  <div class="bulet h-1 w-1 rounded-full bg-[#83009a]"></div>
                  {{ isLangEnglish ? 'History' : 'Riwayat' }}
                </RouterLink>
              </li>
            </ul>
          </div>
          <div class="PO flex flex-col justify-start items-start w-full pt-5">
            <h4 class="text-sm text-[#ae04cc] font-bold">
              {{ isLangEnglish ? 'Page Options' : 'Opsi Halaman' }}
            </h4>
            <div class="options flex flex-col justify-start items-start w-full gap-2">
              <div class="option flex flex-row justify-between items-center w-full">
                <div class="text-xs text-gray-400 font-bold">
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
              <div class="option-darkmode flex flex-row justify-between items-center w-full">
                <div class="text-xs text-gray-400 font-bold">
                  {{ isLangEnglish ? 'Dark Mode:' : 'Mode Gelap:' }}
                </div>
                <button
                  @click="isDarkMode = !isDarkMode"
                  class="relative inline-flex h-4 w-8 items-center rounded-full transition-colors duration-300 cursor-pointer"
                  :class="isDarkMode ? 'bg-[#ae04cc]' : 'bg-gray-300'"
                >
                  <span
                    class="inline-block h-2 w-2 transform rounded-full bg-white transition-transform duration-300"
                    :class="isDarkMode ? 'translate-x-5' : 'translate-x-1'"
                  />
                </button>
              </div>
            </div>
          </div>
        </div>
        <div
          v-if="authStore.user"
          class="content-bawah-loggedin flex flex-row justify-between items-center w-full px-3"
        >
          <button
            @click="openSettings"
            class="account-loggedin flex flex-row justify-start items-center w-[60%] gap-3 cursor-pointer group"
          >
            <img
              v-if="authStore.profile?.profile_picture_url"
              :src="authStore.profile.profile_picture_url"
              alt="Account Image"
              class="w-10 h-10 rounded-full object-cover"
            />
            <img
              v-else
              src="../assets/imgs/user-default.png"
              alt="Account Image"
              class="w-8 h-8 rounded-full object-cover"
            />
            <div class="account-name flex flex-col justify-start items-start gap-0 w-[80%]">
              <p
                class="text-sm text-start text-[#ae04cc] font-bold group-hover:text-[#480254] truncate w-full"
              >
                {{ `${authStore.profile?.first_name} ${authStore.profile?.last_name}` }}
              </p>
              <p class="text-xs text-gray-400/80">@{{ authStore.profile?.username }}</p>
            </div>
          </button>
          <button
            @click="openlogoutconf()"
            class="logoutAccount flex flex-row justify-start items-center gap-1 group cursor-pointer"
          >
            <p
              class="text-xs text-gray-400 transition transition-all duration-300 group-hover:text-red-800"
            >
              Log Out
            </p>
            <span
              class="material-symbols-outlined text-gray-400 transition transition-all duration-300 group-hover:text-red-800"
            >
              logout
            </span>
          </button>
        </div>
        <div
          v-else
          class="content-bawah-notloggedin flex flex-row justify-between items-center w-full px-3"
        >
          <div class="account-notloggedin flex flex-row justify-start items-center w-[40%] gap-2">
            <img
              src="../assets/imgs/user-default.png"
              alt="Account Image"
              class="w-8 h-8 rounded-full object-cover border border-gray-500"
            />
            <div class="account-name flex flex-col justify-start items-center gap-0">
              <p class="text-sm text-gray-400 font-bold">
                {{ isLangEnglish ? 'Not Logged In' : 'Belum Masuk' }}
              </p>
            </div>
          </div>
          <button
            @click="openModal()"
            class="LoginRedirect flex flex-row justify-start items-center gap-1 group cursor-pointer"
          >
            <p
              class="text-xs text-gray-400 transition transition-all duration-300 group-hover:text-[#ae04cc]"
            >
              {{ isLangEnglish ? 'Log in' : 'Masuk' }}
            </p>
            <span
              class="material-symbols-outlined text-gray-400 transition transition-all duration-300 group-hover:text-[#ae04cc]"
            >
              login
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
  <LogoutModal />
</template>
