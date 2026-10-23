<script setup lang="ts">
import { darkFunc } from '../composable/darkMode';
import { openModalLogin } from '../composable/openmodalLogin';
import { munculinTooltip } from '../composable/tooltip';
import { generateUsernameFunc } from '../composable/generateUsername';
import { gantiBahasaFunc } from '../composable/gantiBahasa';
import signupConfirmationModal from './signupConfirmationModal.vue';
import { signupconffunc } from '../composable/signupconf';
import { authFunc } from '../composable/authFunc';

const { opensignupconf, issignupconfopen } = signupconffunc();
const { closeModal, isOpen, isLogin, openSignupModal, openLoginModal } = openModalLogin();
const { isLangEnglish } = gantiBahasaFunc();
const { isDarkMode } = darkFunc();
const { tooltipVisible, hoverbtn, Gahoverbtn } = munculinTooltip();
const { username, generateUsername } = generateUsernameFunc();
const {
  email,
  password,
  confirmPassword,
  firstName,
  lastName,
  loggingInLoading,
  signupLoading,
  signupError,
  loginError,
  submitLoginForm,
  submitSignupForm,
} = authFunc();
</script>

<template>
  <div
    @click.self="closeModal"
    class="bgmodal fixed inset-0 flex items-center justify-center transition-opacity duration-500 z-20"
    :class="isOpen ? 'bg-black/50' : 'pointer-events-none'"
  >
    <div
      class="modal px-6 py-4 rounded-lg w-162 h-96 relative transition-all duration-500 flex flex-col justify-start items-start gap-7"
      :class="[
        isOpen ? ' translate-y-0' : ' -translate-y-200',
        isDarkMode ? 'bg-[#2b2b2b]' : 'bg-white',
      ]"
    >
      <div
        class="container flex flex-row relative justify-center items-center w-full h-full overflow-hidden"
      >
        <div
          class="login h-full w-full absolute flex flex-col justify-between items-start gap-7 transition-all duration-500"
          :class="isLogin ? 'translate-x-0' : '-translate-x-180'"
        >
          <div class="top flex flex-col justify-start items-start w-full gap-6">
            <div class="title flex flex-row justify-start items-center">
              <div class="text flex flex-col justify-start items-start">
                <h2
                  class="text-xl font-bold mb-4"
                  :class="!isDarkMode ? 'text-[#83009a]' : 'text-[#ae04cc]'"
                >
                  {{ isLangEnglish ? 'Log in' : 'Masuk' }}
                </h2>
                <p class="text-xs" :class="!isDarkMode ? 'text-gray-700' : 'text-gray-300'">
                  {{
                    isLangEnglish
                      ? 'Welcome back, log in to access additional features'
                      : 'Selamat datang kembali, masuk untuk mengakses fitur tambahan'
                  }}
                </p>
              </div>
            </div>
            <div class="content flex flex-col justify-start items-start gap-3 w-full">
              <form
                @submit.prevent="submitLoginForm"
                class="flex flex-col justify-start items-start gap-3 w-full"
              >
                <div class="email-input flex flex-col justify-start items-start w-full">
                  <div class="title">
                    <p class="text-xs" :class="!isDarkMode ? 'text-[#83009a]' : 'text-[#ae04cc]'">
                      {{ isLangEnglish ? 'Email Address' : 'Alamat Email' }}
                    </p>
                  </div>
                  <input
                    v-if="isLangEnglish"
                    v-model="email"
                    type="email"
                    placeholder="Enter your email"
                    class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-[80%] placeholder:text-gray-500"
                    :class="!isDarkMode ? 'text-black' : 'text-white'"
                  />
                  <input
                    v-else
                    v-model="email"
                    type="email"
                    placeholder="Masukkan alamat email Anda"
                    class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-[80%] placeholder:text-gray-500"
                    :class="!isDarkMode ? 'text-black' : 'text-white'"
                  />
                </div>
                <div class="password-input flex flex-col justify-start items-start w-full">
                  <div class="title">
                    <p class="text-xs" :class="!isDarkMode ? 'text-[#83009a]' : 'text-[#ae04cc]'">
                      Password
                    </p>
                  </div>
                  <input
                    v-if="isLangEnglish"
                    v-model="password"
                    type="password"
                    placeholder="Enter your password"
                    class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-[50%] placeholder:text-gray-500"
                    :class="!isDarkMode ? 'text-black' : 'text-white'"
                  />
                  <input
                    v-else
                    v-model="password"
                    type="password"
                    placeholder="Masukkan password Anda"
                    class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-[50%] placeholder:text-gray-500"
                    :class="!isDarkMode ? 'text-black' : 'text-white'"
                  />
                </div>
              </form>
              <div v-if="loginError" class="text-red-500 text-sm font-medium">
                {{ loginError }}
              </div>
            </div>
          </div>

          <div class="bottom flex flex-row justify-between items-center w-full">
            <button class="gotosignup cursor-pointer group" @click="openSignupModal">
              <div
                class="group-hover:underline text-xs"
                :class="!isDarkMode ? 'text-[#83009a]' : 'text-[#ae04cc]'"
              >
                {{ isLangEnglish ? "Don't have an account? Sign Up" : 'Belum punya akun? Daftar' }}
              </div>
            </button>
            <button
              @click="submitLoginForm"
              class="loginbtn flex flex-row justify-center items-center border rounded-[10px] w-24 px-2 py-2 cursor-pointer gap-2 hover:bg-[#83009a] transition transition-all duration-300 group"
              :class="
                !isDarkMode
                  ? 'bg-transparent border-[#83009a] '
                  : 'bg-[#ae04cc] border-[#ae04cc] hover:border-[#83009a]'
              "
            >
              <p
                class="text-xs"
                :class="!isDarkMode ? 'text-[#83009a] group-hover:text-white' : 'text-white'"
              >
                {{ isLangEnglish ? 'Login' : 'Masuk' }}
              </p>
            </button>
          </div>
        </div>
        <div
          class="signup absolute top-0 left-0 w-full flex flex-col justify-between h-full items-start gap-5 transition-all duration-500"
          :class="!isLogin ? 'translate-x-0' : 'translate-x-180'"
        >
          <div class="top flex flex-col w-full justify-start items-start gap-4">
            <div class="title flex flex-row justify-start items-center">
              <div class="text flex flex-col justify-start items-start">
                <h2 class="text-xl font-bold mb-4"
                :class="!isDarkMode ? 'text-[#83009a]' : 'text-[#ae04cc]'"
                >
                  {{ isLangEnglish ? 'Sign Up' : 'Daftar' }}
                </h2>
                <p class="text-xs"
                :class="!isDarkMode ? 'text-gray-700' : 'text-gray-300'"
                >
                  {{
                    isLangEnglish
                      ? 'Create an account to access additional features'
                      : 'Buat akun untuk mengakses fitur tambahan'
                  }}
                </p>
              </div>
            </div>
            <div class="content flex flex-col justify-start items-start gap-2 w-full">
              <form
                @submit.prevent="submitSignupForm"
                class="flex flex-col justify-start items-start gap-3 w-full"
              >
                <div class="name-form flex flex-row justify-start items-start w-[95%] gap-3">
                  <div class="firstname-input flex flex-col justify-start items-start w-[70%]">
                    <div class="title">
                      <p class="text-xs"
                      :class="!isDarkMode ? 'text-[#83009a]' : 'text-[#ae04cc]'"
                      >
                        {{ isLangEnglish ? 'First Name' : 'Nama Depan' }}
                      </p>
                    </div>
                    <input
                      v-if="isLangEnglish"
                      v-model="firstName"
                      type="first name"
                      placeholder="Enter your first name"
                      class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-full placeholder:text-gray-500"
                      :class="!isDarkMode ? 'text-black' : 'text-white'"
                    />
                    <input
                      v-else
                      v-model="firstName"
                      type="first name"
                      placeholder="Masukkan nama depan Anda"
                      class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-full placeholder:text-gray-500"
                      :class="!isDarkMode ? 'text-black' : 'text-white'"
                    />
                  </div>
                  <div class="lastName-input flex flex-col justify-start items-start w-full">
                    <div class="title">
                      <p class="text-xs"
                      :class="!isDarkMode ? 'text-[#83009a]' : 'text-[#ae04cc]'"
                      >
                        {{ isLangEnglish ? 'Last Name' : 'Nama Belakang' }}
                      </p>
                    </div>
                    <input
                      v-if="isLangEnglish"
                      v-model="lastName"
                      type="last name"
                      placeholder="Enter your last name"
                      class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-full placeholder:text-gray-500"
                      :class="!isDarkMode ? 'text-black' : 'text-white'"
                    />
                    <input
                      v-else
                      v-model="lastName"
                      type="last name"
                      placeholder="Masukkan nama belakang Anda"
                      class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-full placeholder:text-gray-500"
                      :class="!isDarkMode ? 'text-black' : 'text-white'"
                    />
                  </div>
                </div>
                <div
                  class="emailandusername-form flex flex-row justify-start items-center gap-3 w-[90%]"
                >
                  <div class="email-input flex flex-col justify-start items-start w-full">
                    <div class="title">
                      <p class="text-xs"
                      :class="!isDarkMode ? 'text-[#83009a]' : 'text-[#ae04cc]'"
                      >
                        {{ isLangEnglish ? 'Email Address' : 'Alamat Email' }}
                      </p>
                    </div>
                    <input
                      v-if="isLangEnglish"
                      v-model="email"
                      type="email"
                      placeholder="Enter your email"
                      class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-full placeholder:text-gray-500"
                      :class="!isDarkMode ? 'text-black' : 'text-white'"
                    />
                    <input
                      v-else
                      v-model="email"
                      type="email"
                      placeholder="Masukkan alamat email Anda"
                      class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-full placeholder:text-gray-500"
                      :class="!isDarkMode ? 'text-black' : 'text-white'"
                    />
                  </div>
                  <div class="Username-input flex flex-col justify-start items-start w-full">
                    <div class="title">
                      <p class="text-xs"
                      :class="!isDarkMode ? 'text-[#83009a]' : 'text-[#ae04cc]'"
                      >
                        {{ isLangEnglish ? 'Username' : 'Nama Pengguna' }}
                      </p>
                    </div>
                    <div
                      class="input flex flex-row justify-start items-center gap-2 border border-gray-300 rounded-md w-full"
                    >
                      <input
                        v-if="isLangEnglish"
                        v-model="username"
                        type="text"
                        placeholder="Enter your Username"
                        class="mt-1 px-3 py-2 w-full placeholder:text-gray-500 w-[80%]"
                        :class="!isDarkMode ? 'text-black' : 'text-white'"
                      />
                      <input
                        v-else
                        v-model="username"
                        type="text"
                        placeholder="Masukkan Username Anda"
                        class="mt-1 px-3 py-2 w-full placeholder:text-gray-500 w-[80%]"
                        :class="!isDarkMode ? 'text-black' : 'text-white'"
                      />
                      <button
                        type="button"
                        class="generate-username relative flex items-center h-full w-[15%] cursor-pointer group"
                        :class="!isDarkMode ? 'text-black' : 'text-white'" 
                        @click="generateUsername"
                        @mouseenter="hoverbtn"
                        @mouseleave="Gahoverbtn"
                      >
                        <span
                          class="material-symbols-outlined text-gray-500 rotate-45 group-hover:text-[#83009a] group-hover:rotate-135 transition transition-all duration-500"
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

                <div class="pass-form flex flex-row justify-start items-center gap-3 w-full">
                  <div class="password-input flex flex-col justify-start items-start w-full">
                    <div class="title">
                      <p class="text-xs"
                      :class="!isDarkMode ? 'text-[#83009a]' : 'text-[#ae04cc]'"
                      >
                        {{ isLangEnglish ? 'Password' : 'Password' }}
                      </p>
                    </div>
                    <input
                      v-if="isLangEnglish"
                      v-model="password"
                      type="password"
                      placeholder="Enter your password"
                      class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-full placeholder:text-gray-500"
                      :class="!isDarkMode ? 'text-black' : 'text-white'"
                    />
                    <input
                      v-else
                      v-model="password"
                      type="password"
                      placeholder="Masukkan password Anda"
                      class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-full placeholder:text-gray-500"
                      :class="!isDarkMode ? 'text-black' : 'text-white'"
                    />
                  </div>
                  <div
                    class="confirm-password-input flex flex-col justify-start items-start w-full"
                  >
                    <div class="title">
                      <p class="text-xs"
                      :class="!isDarkMode ? 'text-[#83009a]' : 'text-[#ae04cc]'"
                      >
                        {{ isLangEnglish ? 'Confirm Password' : 'Konfirmasi Password' }}
                      </p>
                    </div>
                    <input
                      v-if="isLangEnglish"
                      v-model="confirmPassword"
                      type="password"
                      placeholder="Confirm your password"
                      class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-full placeholder:text-gray-500"
                      :class="!isDarkMode ? 'text-black' : 'text-white'"
                    />
                    <input
                      v-else
                      v-model="confirmPassword"
                      type="password"
                      placeholder="Konfirmasi password Anda"
                      class="mt-1 px-3 py-2 border border-gray-300 rounded-md w-full placeholder:text-gray-500"
                      :class="!isDarkMode ? 'text-black' : 'text-white'"
                    />
                  </div>
                </div>
              </form>
              <div v-if="signupError" class="text-red-500 text-sm font-medium">
                {{ signupError }}
              </div>
            </div>
          </div>

          <div class="bottom flex flex-row justify-between items-center w-full">
            <button class="gotosignup cursor-pointer group" @click="openLoginModal">
              <div
                class="group-hover:underline text-xs"
                :class="!isDarkMode ? 'text-[#83009a]' : 'text-[#ae04cc]'"
              >
                {{ isLangEnglish ? 'Already have an account? Log in' : 'Sudah punya akun? Masuk' }}
              </div>
            </button>
            <button
              @click="submitSignupForm"
              class="signupbtn flex flex-row justify-center items-center border rounded-[10px] w-24 px-2 py-2 cursor-pointer gap-2 hover:bg-[#83009a] transition transition-all duration-300 group"
              :class="
                !isDarkMode
                  ? 'bg-transparent border-[#83009a] '
                  : 'bg-[#ae04cc] border-[#ae04cc] hover:border-[#83009a]'
              "
            >
              <p
                class="text-xs"
                :class="!isDarkMode ? 'text-black group-hover:text-white' : 'text-white'"
              >
                {{ isLangEnglish ? 'Sign up' : 'Daftar' }}
              </p>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div
    v-if="loggingInLoading"
    class="absolute inset-0 flex-col flex items-center justify-center w-full h-full z-40 bg-black/70"
  >
    <div
      class="w-8 h-8 border-4 border-gray-300 border-t-purple-700 rounded-full animate-spin"
    ></div>
    <p>{{ isLangEnglish ? 'Logging in...' : 'Mencoba Masuk...' }}</p>
  </div>
  <div
    v-if="signupLoading"
    class="absolute inset-0 flex-col flex items-center justify-center w-full h-full z-40 bg-black/70"
  >
    <div
      class="w-8 h-8 border-4 border-gray-300 border-t-purple-700 rounded-full animate-spin"
    ></div>
    <p>{{ isLangEnglish ? 'Signing up...' : 'Mencoba Mendaftar...' }}</p>
  </div>
  <signupConfirmationModal />
</template>
