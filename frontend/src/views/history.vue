<script lang="ts" setup>
import { API_URL } from '@/config'
import { openHistoryModal } from '../composable/openHistory';
import { deleteAllConfFunc } from '../composable/openDeleteAllConfModal';
import { deleteConfFunc } from '../composable/openDeleteConfModal';
import { ref, onMounted, onUnmounted, watch, computed } from 'vue';
import { gantiBahasaFunc } from '../composable/gantiBahasa';
import modalWarning from '../components/modalWarning.vue';
import { openWarningFunc } from '../composable/openWarning';
import { darkFunc } from '../composable/darkMode';
import Menu from '../components/menu.vue';
import axios from 'axios';
import { isuserloggedinFunc } from '../composable/isUserLoggedIn';
import { activefunc } from '../composable/active';
import Sidebar from '../components/sidebar.vue';
import { loadingFunc } from '@/composable/globalVar.ts';

import { useAuthStore } from '../stores/authstore';

const { isDarkMode } = darkFunc();
const { openWarning } = openWarningFunc();
const { isCollapsed } = loadingFunc();
const { isUserLoggedin } = isuserloggedinFunc();
const { isDashActive, isHistoryActive, isHelpActive } = activefunc();
const profile = ref<any>(null);
const authStore = useAuthStore();

const { isLangEnglish } = gantiBahasaFunc();
const { openConfdeletAll } = deleteAllConfFunc();
const { openConfdelet } = deleteConfFunc();
const isFilterOpen = ref(false);
const selectedFilter = ref('all');
const fetchHistoryLoading = ref(false);
const isDeletLoading = ref(false);
const idUser = ref('');

const histories = ref<any[]>([]);

const selectedFilterLabel = computed(() => {
  switch (selectedFilter.value) {
    case 'today':
      return isLangEnglish.value ? 'Today' : 'Hari ini';
    case 'week':
      return isLangEnglish.value ? 'This Week' : 'Minggu Ini';
    default:
      return isLangEnglish.value ? 'All Time' : 'Semua';
  }
});

const setFilter = (filter: string) => {
  selectedFilter.value = filter;
  isFilterOpen.value = false;
};
const fetchHistory = async () => {
  fetchHistoryLoading.value = true;
  const user = authStore.user;
  try {
    if (!user) {
      return;
    }

    const res = await axios.get(`${API_URL}/history/${user.id}`);

    histories.value = res.data;
  } catch (err) {
    console.log(err);
  } finally {
    fetchHistoryLoading.value = false;
  }
};

const filteredHistories = computed(() => {
  const now = new Date();

  return histories.value.filter((item) => {
    const itemDate = new Date(item.created_at);

    if (selectedFilter.value === 'today') {
      return itemDate.toDateString() === now.toDateString();
    }

    if (selectedFilter.value === 'week') {
      const diff = now.getTime() - itemDate.getTime();

      const days = diff / (1000 * 60 * 60 * 24);

      return days <= 7;
    }

    return true;
  });
});

const groupedHistories = computed(() => {
  const grouped: Record<
    string,
    {
      rawDate: string;
      items: any[];
    }
  > = {};

  filteredHistories.value.forEach((item) => {
    const itemDate = new Date(item.created_at);

    const displayDate = itemDate.toLocaleDateString('id-ID', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
    });

    const rawDate = itemDate.toISOString().split('T')[0]!;

    if (!grouped[displayDate]) {
      grouped[displayDate] = {
        rawDate,
        items: [],
      };
    }

    grouped[displayDate].items.push(item);
  });

  return grouped;
});

const deleteHistory = async (historyId: string) => {
  isDeletLoading.value = true;
  try {
    await axios.delete(`${API_URL}/history/${historyId}`);

    histories.value = histories.value.filter((item) => item.id !== historyId);
  } catch (err) {
    console.log(err);
  } finally {
    isDeletLoading.value = false;
  }
};

const deletethisday = async (date: string, user_id: string) => {
  console.log('DATE: ', date);
  isDeletLoading.value = true;
  try {
    await axios.delete(`${API_URL}/history/user/${user_id}/date/${date}`);
    fetchHistory();
  } catch (err) {
    console.log(err);
  } finally {
    isDeletLoading.value = false;
  }
};

const deleteall = async (user_id: string) => {
  isDeletLoading.value = true;
  try {
    await axios.delete(`${API_URL}/history/user/${user_id}/all`);

    fetchHistory();
  } catch (err) {
    console.log(err);
  } finally {
    isDeletLoading.value = false;
  }
};

onMounted(async () => {
  isDashActive.value = false;
  isHistoryActive.value = true;
  isHelpActive.value = false;
  const user = authStore.user;
  if (!user) {
    openWarning();
    return;
  }
  idUser.value = user.id;

  const res = await axios.get(`${API_URL}/api/profile/${user.id}`);

  profile.value = res.data;

  fetchHistory();
});
</script>

<template>
  <div
    v-if="!isDarkMode"
    class="background w-full h-screen bg-white flex flex-row items-start justify-start"
  >
    <Sidebar />

    <div class="right relative w-[95%] h-full">
      <div
        class="h-full overflow-y-scroll w-full container-content flex flex-col items-start justify-start overflow-hidden gap-2"
      >
        <div class="top w-full h-max-20 flex flex-row justify-between items-center px-4 py-3">
          <p class="text-base !font-semibold text-black">
            {{ isLangEnglish ? 'Manage History' : 'Kelola Riwayat' }}
          </p>
        </div>
        <div
          class="content w-full h-[90%] flex flex-col justify-center items-center gap-6"
          :class="isCollapsed ? 'px-25' : 'px-15'"
        >
          <div class="top w-full flex flex-row justify-between items-center py-2 h-[3rem]">
            <div class="sort relative">
              <button
                @click="isFilterOpen = !isFilterOpen"
                class="flex items-center hover:bg-gray-100 gap-2 px-3 py-2 rounded-[10px] text-xs text-[#83009a] shadow-lg bg-white transition-all duration-100 cursor-pointer hover:border-r-4 hover:border-[#83009a]/80"
                :class="isFilterOpen ? 'border-r-4 border-[#83009a]' : ''"
              >
                {{ selectedFilterLabel }}
                <span
                  class="material-symbols-outlined text-base transition-transform duration-300"
                  :class="isFilterOpen ? 'rotate-180' : ''"
                >
                  expand_more
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
                  v-if="isFilterOpen"
                  class="absolute top-15 left-0 mb-2 w-40 bg-white rounded-lg border-2 border-gray-300 z-50"
                >
                  <button
                    @click="setFilter('today')"
                    class="w-full text-left hover:bg-[#EBEBEB] px-4 py-2 text-gray-500 !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
                  >
                    {{ isLangEnglish ? 'Today' : 'Hari ini' }}
                  </button>

                  <button
                    @click="setFilter('week')"
                    class="w-full text-left hover:bg-[#EBEBEB] px-4 py-2 text-gray-500 !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
                  >
                    {{ isLangEnglish ? 'Past Week' : 'Minggu Lalu' }}
                  </button>

                  <button
                    @click="setFilter('all')"
                    class="w-full text-left hover:bg-[#EBEBEB] px-4 py-2 text-gray-500 !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
                  >
                    {{ isLangEnglish ? 'All Time' : 'Semua' }}
                  </button>
                </div>
              </Transition>
            </div>

            <div class="util flex flex-row justify-start items-center gap-2">
              <button
                @click="fetchHistory"
                class="flex items-center gap-1 px-3 py-2 rounded-[10px] shadow-lg text-xs text-[#83009a] bg-white transition-all duration-100 cursor-pointer group hover:bg-gray-100 hover:border-r-4 hover:border-[#83009a]/80"
              >
                Refresh
                <span
                  class="material-symbols-outlined text-base group-hover:rotate-90 transition-transform duration-300 !text-lg"
                >
                  refresh
                </span>
              </button>
              <button
                v-if="!isDeletLoading"
                @click="deleteall(idUser)"
                class="deletall flex items-center gap-1 px-3 py-2 rounded-[10px] shadow-lg text-xs text-[#83009a] bg-white transition-all duration-100 cursor-pointer group hover:bg-gray-100 hover:border-r-4 hover:border-[#83009a]/80"
              >
                <div class="text">{{ isLangEnglish ? 'Delete all' : 'Hapus semua' }}</div>
                <span class="material-symbols-outlined"> delete_history </span>
              </button>
              <button
                v-else
                @click="deleteall(idUser)"
                class="deletall flex items-center gap-1 px-3 py-2 rounded-[10px] shadow-lg text-xs text-[#83009a] bg-white transition-all duration-100 cursor-pointer group hover:bg-gray-100 hover:border-r-4 hover:border-[#83009a]/80"
              >
                <p class="text-center">
                  {{ isLangEnglish ? 'Deleting' : 'Menghapus' }}
                </p>
                <div
                  class="w-5 h-5 border-4 border-gray-400 border-t-purple-700 rounded-full animate-spin"
                ></div>
              </button>
            </div>
          </div>
          <div
            class="content w-full h-[calc(100%-4rem)] flex bg-[#EBEBEB] rounded-[20px] p-4 border border-gray-300"
          >
            <div
              v-if="fetchHistoryLoading"
              class="absolute inset-0 flex-col flex items-center justify-center w-full h-full"
            >
              <div
                class="w-8 h-8 border-4 border-gray-300 border-t-purple-700 rounded-full animate-spin"
              ></div>
              <p class="text-gray-400 text-center">
                {{ isLangEnglish ? 'Loading History' : 'Memuat Riwayat' }}
              </p>
            </div>
            <div
              v-else
              class="content w-full h-full flex flex-col justify-start items-start gap-6 overflow-y-scroll"
            >
              <div
                v-if="filteredHistories.length === 0"
                class="w-full h-full flex flex-col justify-center items-center gap-2"
              >
                <span class="material-symbols-outlined text-gray-500 !text-[3rem]">
                  history_off
                </span>
                <p class="text-gray-500">
                  {{ isLangEnglish ? 'No history found' : 'Riwayat tidak ditemukan' }}
                </p>
              </div>
              <div
                v-else
                v-for="(group, date) in groupedHistories"
                :key="date"
                class="history-wrapper w-full h-fit h-max-70 flex flex-col justify-start items-end gap-3"
              >
                <div class="history-date w-full flex flex-row justify-between items-center p-2">
                  <p class="text-xs text-[#83009a] !font-bold">
                    {{ date }}
                  </p>
                  <button
                    v-if="group.items.length > 1 && !isDeletLoading"
                    @click="deletethisday(group.rawDate, idUser)"
                    class="deletdate flex flex-row justify-start rounded-[5px] items-center bg-red-300 hover:bg-red-400 text-red-700 hover:text-red-900 gap-1 text-xs cursor-pointer transition transition-all duration-100 px-2 py-1 hover:border-r-3 hover:border-red-700/80"
                  >
                    <span class="material-symbols-outlined"> delete </span>
                    <span>{{ isLangEnglish ? 'Delete all' : 'Hapus semua' }}</span>
                  </button>
                  <button
                    v-else-if="isDeletLoading"
                    class="flex items-center gap-1 px-3 py-1 rounded-[5px] shadow-lg text-xs text-red-700 bg-red-300 transition-all duration-100 pointer-events-none"
                  >
                    <p class="text-center">
                      {{ isLangEnglish ? 'Deleting' : 'Menghapus' }}
                    </p>
                    <div
                      class="w-3 h-3 border-2 border-red-700 border-t-red-400 rounded-full animate-spin"
                    ></div>
                  </button>
                </div>
                <div
                  class="detection-histories h-fit h-max-70 w-[95%] flex flex-col justify-start items-start gap-4 overflow-y-scroll"
                >
                  <div
                    v-for="item in group.items"
                    :key="item.id"
                    class="history-item flex flex-row justify-between items-center w-full h-fit py-3 border-b border-gray-300"
                  >
                    <div class="kiri flex flex-row justify-start items-center gap-4 w-[80%]">
                      <div class="bulet h-1 w-1 rounded-full bg-[#83009a]"></div>
                      <div class="details flex flex-col items-start gap-1">
                        <p class="text-sm text-[#83009a] font-bold">
                          {{ item.song_title }}
                        </p>
                        <p class="text-xs text-gray-500">
                          {{
                            isLangEnglish
                              ? `Result: ${item.prediction} (${Math.round(item.confidence * 100)}% confidence)`
                              : `Hasil: ${item.prediction} (${Math.round(item.confidence * 100)}% kepercayaan)`
                          }}
                        </p>
                      </div>
                    </div>
                    <div class="kanan flex flex-row justify-end items-center gap-2 w-[20%]">
                      <button
                        @click="deleteHistory(item.id)"
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
      </div>
    </div>
  </div>
  <div
    v-else
    class="background w-full h-screen bg-[#090909] flex flex-row items-start justify-start"
  >
    <Sidebar />

    <div class="right relative w-[95%] h-full">
      <div
        class="h-full overflow-y-scroll w-full container-content flex flex-col items-start justify-start overflow-hidden gap-2"
      >
        <div class="top w-full h-max-20 flex flex-row justify-between items-center px-4 py-3">
          <p class="text-base !font-semibold text-white">
            {{ isLangEnglish ? 'Manage History' : 'Kelola Riwayat' }}
          </p>
        </div>
        <div
          class="content w-full h-[90%] flex flex-col justify-center items-center gap-6"
          :class="isCollapsed ? 'px-25' : 'px-15'"
        >
          <div class="top w-full flex flex-row justify-between items-center py-2 h-[3rem]">
            <div class="sort relative">
              <button
                @click="isFilterOpen = !isFilterOpen"
                class="flex items-center hover:bg-[#1f1f1f] gap-2 px-3 py-2 rounded-[10px] text-xs text-[#83009a] shadow-lg bg-[#1b1b1b] transition-all duration-100 cursor-pointer hover:border-r-4 hover:border-[#83009a]/80"
                :class="isFilterOpen ? 'border-r-4 border-[#83009a]' : ''"
              >
                {{ selectedFilterLabel }}
                <span
                  class="material-symbols-outlined text-base transition-transform duration-300"
                  :class="isFilterOpen ? 'rotate-180' : ''"
                >
                  expand_more
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
                  v-if="isFilterOpen"
                  class="absolute top-15 left-0 mb-2 w-40 bg-[#090909] rounded-lg border-2 border-[#202020] z-50"
                >
                  <button
                    @click="setFilter('today')"
                    class="w-full text-left hover:bg-[#1b1b1b] px-4 py-2 text-[#6d6d6d] !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
                  >
                    {{ isLangEnglish ? 'Today' : 'Hari ini' }}
                  </button>

                  <button
                    @click="setFilter('week')"
                    class="w-full text-left hover:bg-[#1b1b1b] px-4 py-2 text-[#6d6d6d] !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
                  >
                    {{ isLangEnglish ? 'Past Week' : 'Minggu Lalu' }}
                  </button>

                  <button
                    @click="setFilter('all')"
                    class="w-full text-left hover:bg-[#1b1b1b] px-4 py-2 text-[#6d6d6d] !text-xs flex flex-row justify-start items-center gap-2 cursor-pointer transition transition-all duration-100"
                  >
                    {{ isLangEnglish ? 'All Time' : 'Semua' }}
                  </button>
                </div>
              </Transition>
            </div>

            <div class="util flex flex-row justify-start items-center gap-2">
              <button
                @click="fetchHistory"
                class="flex items-center gap-1 px-3 py-2 rounded-[10px] shadow-lg text-xs text-[#83009a] bg-[#1b1b1b] transition-all duration-100 cursor-pointer group hover:bg-[#1f1f1f] hover:border-r-4 hover:border-[#83009a]/80"
              >
                Refresh
                <span
                  class="material-symbols-outlined text-base group-hover:rotate-90 transition-transform duration-300 !text-lg"
                >
                  refresh
                </span>
              </button>
              <button
                v-if="!isDeletLoading"
                @click="deleteall(idUser)"
                class="deletall flex items-center gap-1 px-3 py-2 rounded-[10px] shadow-lg text-xs text-[#83009a] bg-[#1b1b1b] transition-all duration-100 cursor-pointer group hover:bg-[#1f1f1f] hover:border-r-4 hover:border-[#83009a]/80"
              >
                <div class="text">{{ isLangEnglish ? 'Delete all' : 'Hapus semua' }}</div>
                <span class="material-symbols-outlined"> delete_history </span>
              </button>
              <button
                v-else
                @click="deleteall(idUser)"
                class="deletall flex items-center gap-1 px-3 py-2 rounded-[10px] shadow-lg text-xs text-[#83009a] bg-[#1b1b1b] transition-all duration-100 cursor-pointer group hover:bg-[#1f1f1f] hover:border-r-4 hover:border-[#83009a]/80"
              >
                <p class="text-center">
                  {{ isLangEnglish ? 'Deleting' : 'Menghapus' }}
                </p>
                <div
                  class="w-5 h-5 border-4 border-gray-400 border-t-purple-700 rounded-full animate-spin"
                ></div>
              </button>
            </div>
          </div>
          <div
            class="content w-full h-[calc(100%-4rem)] flex bg-[#1b1b1b] rounded-[20px] p-4 border border-[#202020]"
          >
            <div
              v-if="fetchHistoryLoading"
              class="absolute inset-0 flex-col flex items-center justify-center w-full h-full"
            >
              <div
                class="w-8 h-8 border-4 border-[#202020] border-t-purple-700 rounded-full animate-spin"
              ></div>
              <p class="text-gray-400 text-center">
                {{ isLangEnglish ? 'Loading History' : 'Memuat Riwayat' }}
              </p>
            </div>
            <div
              v-else
              class="content w-full h-full flex flex-col justify-start items-start gap-6 overflow-y-scroll"
            >
              <div
                v-if="filteredHistories.length === 0"
                class="w-full h-full flex flex-col justify-center items-center gap-2"
              >
                <span class="material-symbols-outlined text-[#6d6d6d] !text-[3rem]">
                  history_off
                </span>
                <p class="text-[#6d6d6d]">
                  {{ isLangEnglish ? 'No history found' : 'Riwayat tidak ditemukan' }}
                </p>
              </div>
              <div
                v-else
                v-for="(group, date) in groupedHistories"
                :key="date"
                class="history-wrapper w-full h-fit h-max-70 flex flex-col justify-start items-end gap-3"
              >
                <div class="history-date w-full flex flex-row justify-between items-center p-2">
                  <p class="text-xs text-[#83009a] !font-bold">
                    {{ date }}
                  </p>
                  <button
                    v-if="group.items.length > 1 && !isDeletLoading"
                    @click="deletethisday(group.rawDate, idUser)"
                    class="deletdate flex flex-row justify-start rounded-[5px] items-center bg-red-300 hover:bg-red-400 text-red-700 hover:text-red-900 gap-1 text-xs cursor-pointer transition transition-all duration-100 px-2 py-1 hover:border-r-3 hover:border-red-700/80"
                  >
                    <span class="material-symbols-outlined"> delete </span>
                    <span>{{ isLangEnglish ? 'Delete all' : 'Hapus semua' }}</span>
                  </button>
                  <button
                    v-else-if="isDeletLoading"
                    class="flex items-center gap-1 px-3 py-1 rounded-[5px] shadow-lg text-xs text-red-700 bg-red-300 transition-all duration-100 pointer-events-none"
                  >
                    <p class="text-center">
                      {{ isLangEnglish ? 'Deleting' : 'Menghapus' }}
                    </p>
                    <div
                      class="w-3 h-3 border-2 border-red-700 border-t-red-400 rounded-full animate-spin"
                    ></div>
                  </button>
                </div>
                <div
                  class="detection-histories h-fit h-max-70 w-[95%] flex flex-col justify-start items-start gap-4 overflow-y-scroll"
                >
                  <div
                    v-for="item in group.items"
                    :key="item.id"
                    class="history-item flex flex-row justify-between items-center w-full h-fit py-3 border-b border-[#303030]"
                  >
                    <div class="kiri flex flex-row justify-start items-center gap-4 w-[80%]">
                      <div class="bulet h-1 w-1 rounded-full bg-[#83009a]"></div>
                      <div class="details flex flex-col items-start gap-1">
                        <p class="text-sm text-[#83009a] font-bold">
                          {{ item.song_title }}
                        </p>
                        <p class="text-xs text-[#6d6d6d]">
                          {{
                            isLangEnglish
                              ? `Result: ${item.prediction} (${Math.round(item.confidence * 100)}% confidence)`
                              : `Hasil: ${item.prediction} (${Math.round(item.confidence * 100)}% kepercayaan)`
                          }}
                        </p>
                      </div>
                    </div>
                    <div class="kanan flex flex-row justify-end items-center gap-2 w-[20%]">
                      <button
                        @click="deleteHistory(item.id)"
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
      </div>
    </div>
  </div>
  <Menu :isUserLoggedin="isUserLoggedin" />
  <modalWarning />
</template>
