<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue';
import { gantiBahasaFunc } from '../composable/gantiBahasa';
import ModalLogin from '../components/modalLogin.vue';
import { isuserloggedinFunc } from '../composable/isUserLoggedIn';
import Navbar from '../components/navbar.vue';
import DeleteConfModal from '../components/deleteConfirmationModal.vue';
import DeleteAllConfModal from '../components/deleteAllConfirmationModal.vue';
import { darkFunc } from '../composable/darkMode';
import Menu from '../components/menu.vue';
import axios from 'axios';

import { useAuthStore } from '../stores/authstore';

const { isLangEnglish } = gantiBahasaFunc();
const { isUserLoggedin } = isuserloggedinFunc();
const { isDarkMode } = darkFunc();
const profile = ref<any>(null);

const tekskeatas = ref(false);
const bukaScroll = ref(false);
const contentRef = ref<HTMLElement | null>(null);
const navbarRefOutside = ref<InstanceType<typeof Navbar> | null>(null);
const openingDivHeader = ref<HTMLElement | null>(null);
const headerRef = ref<HTMLElement | null>(null);
const secondDivHeader = ref<HTMLElement | null>(null);
const hideDivHeader = ref(false);
const showSecondDivHeader = ref(false);
let gantiWarnaNavbar = ref(false);
const posisiCursorDiatas = ref(false);
const lewatHeader = ref(false);
let hideTimeout: ReturnType<typeof setTimeout> | null = null;
const activeIndex = ref<number | null>(null);
let intervalId: ReturnType<typeof setInterval> | null = null;
const activeIsland = ref<number | null>(null);
const authStore = useAuthStore();

const toggleIsland = (index: number) => {
  activeIsland.value = activeIsland.value === index ? null : index;
};

const toggleFAQ = (index: number) => {
  activeIndex.value = activeIndex.value === index ? null : index;
};

const startHideTimer = () => {
  if (hideTimeout) clearTimeout(hideTimeout);

  hideTimeout = setTimeout(() => {
    if (navbarRefOutside.value?.navbarEl) {
      navbarRefOutside.value.navbarEl.style.transform = 'translateY(-3rem)';
    }
  }, 5000);
};

const handleWheel = (e: WheelEvent) => {
  if (!tekskeatas.value && e.deltaY > 0) {
    e.preventDefault();
    tekskeatas.value = true;

    if (openingDivHeader.value && secondDivHeader.value) {
      hideDivHeader.value = true;
      showSecondDivHeader.value = true;
    }

    setTimeout(() => {
      bukaScroll.value = true;
    }, 800);
  } else if ((contentRef.value?.scrollTop ?? 0) <= 1 && e.deltaY < 0) {
    tekskeatas.value = false;
    if (openingDivHeader.value && secondDivHeader.value) {
      hideDivHeader.value = false;
      showSecondDivHeader.value = false;
    }
    bukaScroll.value = false;
  }

  if (!bukaScroll.value) {
    e.preventDefault();
  }

  return;
};

const handleScroll = () => {
  const scrollTop = contentRef.value?.scrollTop ?? 0;
  const headerHeight = headerRef.value?.offsetHeight ?? window.innerHeight;

  const prevLewat = lewatHeader.value;
  lewatHeader.value = scrollTop >= headerHeight;

  const navbar = navbarRefOutside.value?.navbarEl;
  if (!navbar) return;

  if (lewatHeader.value) {
    gantiWarnaNavbar.value = true;
    if (!prevLewat) {
      startHideTimer();
    }
  } else {
    gantiWarnaNavbar.value = false;
    navbar.style.transform = 'translateY(0)';

    if (hideTimeout) {
      clearTimeout(hideTimeout);
      hideTimeout = null;
    }
  }
};

const handleCursor = (e: MouseEvent) => {
  posisiCursorDiatas.value = e.clientY <= 100;

  const navbar = navbarRefOutside.value?.navbarEl;
  if (!navbar || !lewatHeader.value) return;

  if (posisiCursorDiatas.value) {
    navbar.style.transform = 'translateY(0)';

    if (hideTimeout) {
      clearTimeout(hideTimeout);
      hideTimeout = null;
    }
  } else {
    startHideTimer();
  }
};

const faqs = [
  {
    q: 'What is this website for?',
    a: 'This website is used to detect whether a music file is AI-generated or human-made.',
  },
  {
    q: 'What audio formats are supported?',
    a: 'Currently, MP3 and WAV formats are supported.',
  },
  {
    q: 'How does the AI music detection work?',
    a: 'The system analyzes Mel-Spectrogram patterns using a deep learning model trained on AI and human music datasets.',
  },
  {
    q: 'Can this website detect edited AI music?',
    a: 'Detection accuracy may decrease if the AI-generated music has been heavily edited or post-processed.',
  },
  {
    q: 'Do I need to create an account?',
    a: 'Yes, you need to create an account to use the detection feature.',
  },
  {
    q: 'Is my uploaded audio stored permanently?',
    a: 'No, uploaded files are processed temporarily and automatically deleted after analysis.',
  },
  {
    q: 'How accurate is the detection result?',
    a: 'The detection model provides a probability score, but results are not guaranteed to be 100% accurate.',
  },
];

const faqsId = [
  {
    q: 'Untuk apa website ini?',
    a: 'Website ini digunakan untuk mendeteksi apakah sebuah file musik dibuat oleh AI atau manusia.',
  },
  {
    q: 'Format audio apa saja yang didukung?',
    a: 'Saat ini format MP3 dan WAV didukung.',
  },
  {
    q: 'Bagaimana cara kerja deteksi musik AI?',
    a: 'Sistem menganalisis pola Mel-Spectrogram menggunakan model deep learning yang dilatih dengan dataset musik AI dan manusia.',
  },
  {
    q: 'Apakah website ini bisa mendeteksi musik AI yang sudah diedit?',
    a: 'Akurasi deteksi dapat menurun jika musik AI telah melalui proses editing atau post-processing yang signifikan.',
  },
  {
    q: 'Apakah harus membuat akun?',
    a: 'Ya, pengguna harus membuat akun terlebih dahulu untuk dapat menggunakan fitur deteksi lagu AI',
  },
  {
    q: 'Apakah file audio yang diupload disimpan permanen?',
    a: 'Tidak, file yang diupload hanya diproses sementara dan otomatis dihapus setelah analisis selesai.',
  },
  {
    q: 'Seberapa akurat hasil deteksinya?',
    a: 'Model deteksi memberikan skor probabilitas, namun hasil tidak dijamin 100% akurat.',
  },
];

const islandContents = [
  {
    judul: 'How It Works',
    desc: 'Easily detect whether a piece of music is AI-generated or human-made in just a few simple steps. Our system is designed to deliver fast and accurate results without requiring any technical expertise.',
  },
  {
    judul: 'Simple, Fast, and Reliable Detection',
    desc: 'Save time and skip the complexity. Instantly analyze music with a fast, reliable system designed for effortless use. No expertise required',
  },
  {
    judul: 'Built for Accurate Detection',
    desc: 'Our detection system leverages modern AI and audio analysis to identify subtle patterns that differentiate AI-generated music from human compositions, ensuring accurate and dependable results',
  },
];

const islandContentsId = [
  {
    judul: 'Cara Kerja',
    desc: 'Dengan mudah ketahui apakah sebuah lagu dihasilkan oleh AI atau dibuat oleh manusia hanya dalam beberapa langkah sederhana. Sistem kami dirancang untuk memberikan hasil yang cepat dan akurat tanpa memerlukan keahlian teknis apa pun.',
  },
  {
    judul: 'Sederhana, Cepat, dan Andal',
    desc: 'Hemat waktu dan hindari kerumitan. Analisis musik secara instan dengan sistem yang cepat dan andal, dirancang agar mudah digunakan. Tidak perlu keahlian khusus',
  },
  {
    judul: 'Dirancang untuk Deteksi Akurat',
    desc: 'Sistem pendeteksian kami memanfaatkan kecerdasan buatan (AI) modern dan analisis audio untuk mengidentifikasi pola-pola halus yang membedakan musik yang dihasilkan AI dari komposisi manusia, sehingga memastikan hasil yang akurat dan dapat diandalkan',
  },
];

const islandContentsExpandedId = [
  {
    title: 'Cara Kerja',
    subtitle:
      'Dengan mudah ketahui apakah sebuah lagu dihasilkan oleh AI atau dibuat oleh manusia hanya dalam beberapa langkah sederhana. Sistem kami dirancang untuk memberikan hasil yang cepat dan akurat tanpa memerlukan keahlian teknis apa pun.',
    points: [
      {
        title: 'Unggah Audio',
        description:
          'Pengguna mengunggah file musik yang ingin dianalisis melalui antarmuka website.',
      },
      {
        title: 'Ekstraksi Fitur',
        description:
          'Audio diubah menjadi representasi Mel-Spectrogram untuk menangkap pola dan karakteristik penting dari musik.',
      },
      {
        title: 'Proses Klasifikasi',
        description:
          'Model deep learning menganalisis fitur yang telah diekstraksi untuk menentukan sumber musik.',
      },
      {
        title: 'Hasil Deteksi',
        description:
          'Sistem menampilkan hasil prediksi apakah musik tersebut dibuat oleh AI atau manusia dalam waktu singkat.',
      },
    ],
  },
  {
    title: 'Sederhana, Cepat, dan Andal',
    subtitle:
      'Hemat waktu dan hindari kerumitan. Analisis musik secara instan dengan sistem yang cepat dan andal, dirancang agar mudah digunakan. Tidak perlu keahlian khusus',
    points: [
      {
        title: 'Mudah Digunakan',
        description:
          'Pengguna hanya perlu mengunggah file musik tanpa memerlukan pengetahuan teknis.',
      },
      {
        title: 'Proses Cepat',
        description:
          'Sistem dioptimalkan untuk memberikan hasil analisis dalam waktu yang singkat.',
      },
      {
        title: 'Dapat Diakses Kapan Saja',
        description:
          'Dapat digunakan langsung melalui browser tanpa perlu instalasi perangkat lunak tambahan.',
      },
      {
        title: 'Hasil Konsisten',
        description:
          'Model telah dilatih dan dievaluasi menggunakan berbagai dataset musik untuk menghasilkan prediksi yang andal.',
      },
    ],
  },
  {
    title: 'Dirancang untuk Deteksi Akurat',
    subtitle:
      'Sistem pendeteksian kami memanfaatkan kecerdasan buatan (AI) modern dan analisis audio untuk mengidentifikasi pola-pola halus yang membedakan musik yang dihasilkan AI dari komposisi manusia, sehingga memastikan hasil yang akurat dan dapat diandalkan',
    points: [
      {
        title: 'Analisis Mel-Spectrogram',
        description:
          'Menganalisis representasi waktu-frekuensi yang mampu menangkap pola penting dalam sebuah lagu.',
      },
      {
        title: 'Karakteristik Spektral',
        description:
          'Mempelajari distribusi frekuensi dan struktur spektrum yang sering menunjukkan ciri khas tertentu.',
      },
      {
        title: 'Pola Temporal',
        description: 'Mengamati perubahan karakteristik musik dari waktu ke waktu sepanjang lagu.',
      },
      {
        title: 'Model Deep Learning',
        description:
          'Memanfaatkan jaringan saraf terlatih untuk mengenali perbedaan antara musik AI dan musik buatan manusia.',
      },
    ],
  },
];

const islandContentsExpanded = [
  {
    title: 'How It Works',
    subtitle:
      'Easily detect whether a piece of music is AI-generated or human-made in just a few simple steps. Our system is designed to deliver fast and accurate results without requiring any technical expertise.',
    points: [
      {
        title: 'Upload Audio',
        description: 'Upload a supported music file through the web interface for analysis.',
      },
      {
        title: 'Feature Extraction',
        description:
          'The system converts the audio into Mel-Spectrogram representations and extracts relevant audio patterns.',
      },
      {
        title: 'AI Classification',
        description:
          'A trained deep learning model analyzes the extracted features and predicts the source of the music.',
      },
      {
        title: 'Instant Results',
        description:
          'Detection results are presented within seconds along with prediction confidence.',
      },
    ],
  },
  {
    title: 'Simple, Fast, and Reliable Detection',
    subtitle:
      'Save time and skip the complexity. Instantly analyze music with a fast, reliable system designed for effortless use. No expertise required',
    points: [
      {
        title: 'Easy to Use',
        description: 'No technical expertise is required to upload and analyze music.',
      },
      {
        title: 'Fast Processing',
        description: 'Optimized inference pipelines allow quick analysis and response times.',
      },
      {
        title: 'Accessible Anywhere',
        description: 'Use the system directly from your browser without additional software.',
      },
      {
        title: 'Reliable Predictions',
        description:
          'Built on trained machine learning models evaluated using real-world datasets.',
      },
    ],
  },
  {
    title: 'Built for Accurate Detection',
    subtitle:
      'Our detection system leverages modern AI and audio analysis to identify subtle patterns that differentiate AI-generated music from human compositions, ensuring accurate and dependable results',
    points: [
      {
        title: 'Mel Spectrogram Analysis',
        description:
          'Captures detailed time-frequency representations that reveal hidden musical patterns.',
      },
      {
        title: 'Spectral Characteristics',
        description:
          'Examines frequency distributions and spectral structures often associated with AI-generated content.',
      },
      {
        title: 'Temporal Patterns',
        description:
          'Analyzes how musical information evolves over time across different sections of a track.',
      },
      {
        title: 'Deep Learning Detection',
        description:
          'Uses trained neural networks to distinguish between human compositions and AI-generated music.',
      },
    ],
  },
];

const genres = ['Pop', 'Hip Hop', 'Electronic', 'Blues', 'Rock', 'Classical', 'Metal'];

onMounted(async () => {
  contentRef.value?.addEventListener('wheel', handleWheel, { passive: false });
  contentRef.value?.addEventListener('scroll', handleScroll);
  window.addEventListener('mousemove', handleCursor);

  const user = authStore.user;

  const res = await axios.get(`http://localhost:8000/api/profile/${user.id}`);

  profile.value = res.data;
});

onUnmounted(() => {
  contentRef.value?.removeEventListener('wheel', handleWheel);
  contentRef.value?.removeEventListener('scroll', handleScroll);
  window.removeEventListener('mousemove', handleCursor);
  if (intervalId) clearInterval(intervalId);
});
</script>

<template>
  <header>
    <link href="/src/assets/main.css" rel="stylesheet" />
  </header>

  <main>
    <div class="wrapper w-full h-screen">
      <Navbar ref="navbarRefOutside" :gantiWarnaNavbar="gantiWarnaNavbar" />

      <div
        ref="contentRef"
        class="content h-full overflow-y-scroll scroll-smooth"
        :class="!isDarkMode ? 'bg-white' : 'bg-black'"
      >
        <div
          ref="headerRef"
          class="header relative w-full h-screen snap-start"
          :class="
            !isDarkMode
              ? 'bg-[linear-gradient(134deg,_#640475_11%,_#37006b_32%,_#640475_51%,_#37006b_75%,_#640475_90%)]'
              : 'bg-[linear-gradient(134deg,_#403f3f_11%,_#292929_32%,_#403f3f_51%,_#292929_75%,_#403f3f_90%)]'
          "
        >
          <div
            ref="openingDivHeader"
            class="opening absolute inset-0 flex flex-col items-center justify-center transition-transform duration-1200 gap-4"
            :class="!showSecondDivHeader ? 'translate-y-0' : 'translate-y-[-1000px]'"
          >
            <div class="openingtext flex flex-col items-center justify-center">
              <h1 class="text-2xl text-white font-bold mb-4">
                {{
                  isLangEnglish
                    ? 'Detect AI-Generated Music Instantly'
                    : 'Deteksi Musik yang Dihasilkan oleh AI Secara Instan'
                }}
              </h1>
              <p class="text-white/80 text-sm">
                {{
                  isLangEnglish
                    ? 'Upload your audio and get accurate results in seconds—no technical skills required.'
                    : 'Unggah audio Anda dan dapatkan hasil yang akurat dalam hitungan detik—tidak perlu keterampilan teknis.'
                }}
              </p>
            </div>
          </div>
          <div
            ref="secondDivHeader"
            class="opening absolute inset-0 px-30 flex flex-row items-center justify-center gap-[250px] w-full"
          >
            <div
              class="openingtext flex flex-col gap-1 items-start justify-start transition-all duration-1200 w-[500px]"
              :class="
                !hideDivHeader
                  ? 'translate-y-[1000px] opacity-0 delay-[200ms]'
                  : 'translate-y-0 opacity-100 delay-0'
              "
            >
              <h1 class="text-2xl text-white font-bold mb-4 w-full">
                {{
                  isLangEnglish
                    ? 'Simple, Fast, and Reliable Detection'
                    : 'Deteksi yang Sederhana, Cepat, dan Andal'
                }}
              </h1>
              <p class="text-white/80 text-left text-sm w-full">
                {{
                  isLangEnglish
                    ? 'Upload any audio file and let the model do the work. In just seconds, you’ll get a clear prediction on whether the music is AI-generated or human-made. No setup, no complexity.'
                    : 'Unggah file audio apa pun dan biarkan model yang mengerjakannya. Hanya dalam hitungan detik, Anda akan mendapatkan prediksi yang jelas apakah musik tersebut dihasilkan oleh AI atau dibuat oleh manusia. Tanpa pengaturan, tanpa kerumitan.'
                }}
              </p>
            </div>
            <div
              class="w-px h-100 bg-gray-400 transition-all duration-800"
              :class="!hideDivHeader ? 'translate-y-[-1000px]' : 'translate-y-0'"
            ></div>
            <div
              class="openingtext flex flex-col items-end gap-1 justify-end transition-all duration-1200 w-[500px]"
              :class="
                !hideDivHeader
                  ? 'translate-y-[-1000px] opacity-0 delay-[200ms]'
                  : 'translate-y-0 opacity-100 delay-0'
              "
            >
              <h1 class="text-2xl text-right text-white font-bold mb-4 w-full">
                {{ isLangEnglish ? 'Built for Everyone' : 'Dibuat untuk Semua Orang' }}
              </h1>
              <p class="text-white/80 text-right text-sm w-full">
                {{
                  isLangEnglish
                    ? "Whether you're a researcher, creator, or casual listener, our tool makes AI music detection accessible with a clean interface and minimal steps."
                    : 'Baik Anda seorang peneliti, kreator, atau pendengar biasa, alat kami memudahkan pendeteksian musik berbasis AI dengan antarmuka yang sederhana dan langkah-langkah yang minim.'
                }}
              </p>
            </div>
          </div>
        </div>
        <div
          class="content-pertama flex flex-col items-center justify-center w-full h-fit px-20 gap-4"
        >
          <div v-if="!isDarkMode" class="islands flex flex-row items-center justify-center gap-8">
            <div
              v-if="isLangEnglish"
              v-for="(island, index) in islandContents"
              :key="index"
              class="relative"
            >
              <div
                @click="toggleIsland(index + 1)"
                class="container w-64 h-48 bg-white rounded-[10px] flex flex-col items-center justify-between p-5 shadow-lg border border-gray-300 cursor-pointer transition-all duration-500 hover:translate-y-[-45px]"
                :class="[
                  hideDivHeader ? 'translate-y-[-35px]' : '',
                  activeIsland === index + 1 ? 'opacity-0 pointer-events-none' : 'opacity-100',
                ]"
              >
                <div class="top flex flex-col justify-center items-center gap-1">
                  <div
                    class="icon w-16 h-16 border-2 border-[#83009a] flex items-center justify-center rounded-full text-[#83009a] font-bold"
                  >
                    <span class="material-symbols-outlined"> music_note </span>
                  </div>
                  <p class="text-black text-center font-bold">{{ island.judul }}</p>
                </div>
                <div class="mid-text">
                  <p class="text-gray-700 text-sm text-center line-clamp-2">
                    {{ island.desc }}
                  </p>
                </div>
              </div>
              <transition name="cardfade">
                <div
                  v-if="activeIsland === index + 1"
                  @click="toggleIsland(index + 1)"
                  class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-[600px] h-[400px] bg-white rounded-[10px] flex flex-col items-center justify-start gap-5 p-5 shadow-lg border border-gray-300 cursor-pointer"
                >
                  <div class="top w-full flex flex-col justify-center items-center gap-1">
                    <div
                      class="icon w-16 h-16 border-2 border-[#83009a] flex items-center justify-center rounded-full text-[#83009a] font-bold"
                    >
                      <span class="material-symbols-outlined"> music_note </span>
                    </div>
                    <div class="text-top flex flex-col gap-1 justify-center items-center">
                      <p class="text-black text-base font-bold">
                        {{ islandContentsExpanded[index]?.title }}
                      </p>
                      <p class="text-gray-700 text-xs">
                        {{ islandContentsExpanded[index]?.subtitle }}
                      </p>
                    </div>
                  </div>
                  <div
                    class="mid-text-row1 flex flex-row items-center justify-between w-full gap-3"
                  >
                    <div class="point flex flex-row items-center justify-start w-full gap-3">
                      <div class="bulet h-1 w-1 rounded-full bg-[#83009a]"></div>
                      <div class="features w-full flex flex-col justify-start items-start gap-1">
                        <p class="text-[#83009a] text-sm font-bold">
                          {{ islandContentsExpanded[index]?.points[0]?.title }}
                        </p>
                        <p class="text-gray-700 text-xs">
                          {{ islandContentsExpanded[index]?.points[0]?.description }}
                        </p>
                      </div>
                    </div>
                    <div class="point flex flex-row items-center justify-start w-full gap-3">
                      <div class="bulet h-1 w-1 rounded-full bg-[#83009a]"></div>
                      <div class="features w-full flex flex-col justify-start items-start gap-1">
                        <p class="text-[#83009a] text-sm font-bold">
                          {{ islandContentsExpanded[index]?.points[1]?.title }}
                        </p>
                        <p class="text-gray-700 text-xs">
                          {{ islandContentsExpanded[index]?.points[1]?.description }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div
                    class="mid-text-row2 flex flex-row items-center justify-between w-full gap-3"
                  >
                    <div class="point flex flex-row items-center justify-start w-full gap-3">
                      <div class="bulet h-1 w-1 rounded-full bg-[#83009a]"></div>
                      <div class="features w-full flex flex-col justify-start items-start gap-1">
                        <p class="text-[#83009a] text-sm font-bold">
                          {{ islandContentsExpanded[index]?.points[2]?.title }}
                        </p>
                        <p class="text-gray-700 text-xs">
                          {{ islandContentsExpanded[index]?.points[2]?.description }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </transition>
            </div>
            <div v-else v-for="(island, idx) in islandContentsId" :key="idx" class="relative">
              <div
                @click="toggleIsland(idx + 1)"
                class="container w-64 h-48 bg-white rounded-[10px] flex flex-col items-center justify-between p-5 shadow-lg border border-gray-300 cursor-pointer transition-all duration-500 hover:translate-y-[-45px]"
                :class="[
                  hideDivHeader ? 'translate-y-[-35px]' : '',
                  activeIsland === idx + 1 ? 'opacity-0 pointer-events-none' : 'opacity-100',
                ]"
              >
                <div class="top flex flex-col justify-center items-center gap-1">
                  <div
                    class="icon w-16 h-16 border-2 border-[#83009a] flex items-center justify-center rounded-full text-[#83009a] font-bold"
                  >
                    <span class="material-symbols-outlined"> music_note </span>
                  </div>
                  <p class="text-black text-center font-bold">{{ island.judul }}</p>
                </div>
                <div class="mid-text">
                  <p class="text-gray-700 text-sm text-center line-clamp-2">
                    {{ island.desc }}
                  </p>
                </div>
              </div>
              <transition name="cardfade">
                <div
                  v-if="activeIsland === idx + 1"
                  @click="toggleIsland(idx + 1)"
                  class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-[600px] h-[400px] bg-white rounded-[10px] flex flex-col items-center justify-start gap-5 p-5 shadow-lg border border-gray-300 cursor-pointer"
                >
                  <div class="top w-full flex flex-col justify-center items-center gap-1">
                    <div
                      class="icon w-16 h-16 border-2 border-[#83009a] flex items-center justify-center rounded-full text-[#83009a] font-bold"
                    >
                      <span class="material-symbols-outlined"> music_note </span>
                    </div>
                    <div class="text-top flex flex-col gap-1 justify-center items-center">
                      <p class="text-black text-base font-bold">
                        {{ islandContentsExpandedId[idx]?.title }}
                      </p>
                      <p class="text-gray-700 text-xs">
                        {{ islandContentsExpandedId[idx]?.subtitle }}
                      </p>
                    </div>
                  </div>
                  <div
                    class="mid-text-row1 flex flex-row items-center justify-between w-full gap-3"
                  >
                    <div class="point flex flex-row items-center justify-start w-full gap-3">
                      <div class="bulet h-1 w-1 rounded-full bg-[#83009a]"></div>
                      <div class="features w-full flex flex-col justify-start items-start gap-1">
                        <p class="text-[#83009a] text-sm font-bold">
                          {{ islandContentsExpandedId[idx]?.points[0]?.title }}
                        </p>
                        <p class="text-gray-700 text-xs">
                          {{ islandContentsExpandedId[idx]?.points[0]?.description }}
                        </p>
                      </div>
                    </div>
                    <div class="point flex flex-row items-center justify-start w-full gap-3">
                      <div class="bulet h-1 w-1 rounded-full bg-[#83009a]"></div>
                      <div class="features w-full flex flex-col justify-start items-start gap-1">
                        <p class="text-[#83009a] text-sm font-bold">
                          {{ islandContentsExpandedId[idx]?.points[1]?.title }}
                        </p>
                        <p class="text-gray-700 text-xs">
                          {{ islandContentsExpandedId[idx]?.points[1]?.description }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div
                    class="mid-text-row2 flex flex-row items-center justify-between w-full gap-3"
                  >
                    <div class="point flex flex-row items-center justify-start w-full gap-3">
                      <div class="bulet h-1 w-1 rounded-full bg-[#83009a]"></div>
                      <div class="features w-full flex flex-col justify-start items-start gap-1">
                        <p class="text-[#83009a] text-sm font-bold">
                          {{ islandContentsExpandedId[idx]?.points[2]?.title }}
                        </p>
                        <p class="text-gray-700 text-xs">
                          {{ islandContentsExpandedId[idx]?.points[2]?.description }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </transition>
            </div>
          </div>
          <div v-else class="islands flex flex-row items-center justify-center gap-8">
            <div
              v-if="isLangEnglish"
              v-for="(island, index) in islandContents"
              :key="index"
              class="relative"
            >
              <div
                @click="toggleIsland(index + 1)"
                class="container w-64 h-48 bg-[#2b2b2b] rounded-[10px] flex flex-col items-center justify-between p-5 shadow-lg border border-[#2b2b2b] cursor-pointer transition-all duration-500 hover:translate-y-[-45px]"
                :class="[
                  hideDivHeader ? 'translate-y-[-35px]' : '',
                  activeIsland === index + 1 ? 'opacity-0 pointer-events-none' : 'opacity-100',
                ]"
              >
                <div class="top flex flex-col justify-center items-center gap-1">
                  <div
                    class="icon w-16 h-16 border-2 border-[#ae04cc] flex items-center justify-center rounded-full text-[#ae04cc] font-bold"
                  >
                    <span class="material-symbols-outlined"> music_note </span>
                  </div>
                  <p class="text-white text-center font-bold">{{ island.judul }}</p>
                </div>
                <div class="mid-text">
                  <p class="text-white text-sm text-center line-clamp-2">
                    {{ island.desc }}
                  </p>
                </div>
              </div>
              <transition name="cardfade">
                <div
                  v-if="activeIsland === index + 1"
                  @click="toggleIsland(index + 1)"
                  class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-[600px] h-[400px] bg-[#2b2b2b] rounded-[10px] flex flex-col items-center justify-start gap-5 p-5 shadow-lg border border-black cursor-pointer"
                >
                  <div class="top w-full flex flex-col justify-center items-center gap-1">
                    <div
                      class="icon w-16 h-16 border-2 border-[#ae04cc] flex items-center justify-center rounded-full text-[#ae04cc] font-bold"
                    >
                      <span class="material-symbols-outlined"> music_note </span>
                    </div>
                    <div class="text-top flex flex-col gap-1 justify-center items-center">
                      <p class="text-white text-base font-bold">
                        {{ islandContentsExpanded[index]?.title }}
                      </p>
                      <p class="text-gray-300 text-xs">
                        {{ islandContentsExpanded[index]?.subtitle }}
                      </p>
                    </div>
                  </div>
                  <div
                    class="mid-text-row1 flex flex-row items-center justify-between w-full gap-3"
                  >
                    <div class="point flex flex-row items-center justify-start w-full gap-3">
                      <div class="bulet h-1 w-1 rounded-full bg-[#83009a]"></div>
                      <div class="features w-full flex flex-col justify-start items-start gap-1">
                        <p class="text-[#ae04cc] text-sm font-bold">
                          {{ islandContentsExpanded[index]?.points[0]?.title }}
                        </p>
                        <p class="text-gray-300 text-xs">
                          {{ islandContentsExpanded[index]?.points[0]?.description }}
                        </p>
                      </div>
                    </div>
                    <div class="point flex flex-row items-center justify-start w-full gap-3">
                      <div class="bulet h-1 w-1 rounded-full bg-[#ae04cc]"></div>
                      <div class="features w-full flex flex-col justify-start items-start gap-1">
                        <p class="text-[#ae04cc] text-sm font-bold">
                          {{ islandContentsExpanded[index]?.points[1]?.title }}
                        </p>
                        <p class="text-gray-300 text-xs">
                          {{ islandContentsExpanded[index]?.points[1]?.description }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div
                    class="mid-text-row2 flex flex-row items-center justify-between w-full gap-3"
                  >
                    <div class="point flex flex-row items-center justify-start w-full gap-3">
                      <div class="bulet h-1 w-1 rounded-full bg-[#ae04cc]"></div>
                      <div class="features w-full flex flex-col justify-start items-start gap-1">
                        <p class="text-[#ae04cc] text-sm font-bold">
                          {{ islandContentsExpanded[index]?.points[2]?.title }}
                        </p>
                        <p class="text-gray-300 text-xs">
                          {{ islandContentsExpanded[index]?.points[2]?.description }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </transition>
            </div>
            <div v-else v-for="(island, idx) in islandContentsId" :key="idx" class="relative">
              <div
                @click="toggleIsland(idx + 1)"
                class="container w-64 h-48 bg-[#2b2b2b] rounded-[10px] flex flex-col items-center justify-between p-5 shadow-lg border border-[#2b2b2b] cursor-pointer transition-all duration-500 hover:translate-y-[-45px]"
                :class="[
                  hideDivHeader ? 'translate-y-[-35px]' : '',
                  activeIsland === idx + 1 ? 'opacity-0 pointer-events-none' : 'opacity-100',
                ]"
              >
                <div class="top flex flex-col justify-center items-center gap-1">
                  <div
                    class="icon w-16 h-16 border-2 border-[#ae04cc] flex items-center justify-center rounded-full text-[#ae04cc] font-bold"
                  >
                    <span class="material-symbols-outlined"> music_note </span>
                  </div>
                  <p class="text-white text-center font-bold">{{ island.judul }}</p>
                </div>
                <div class="mid-text">
                  <p class="text-white text-sm text-center line-clamp-2">
                    {{ island.desc }}
                  </p>
                </div>
              </div>
              <transition name="cardfade">
                <div
                  v-if="activeIsland === idx + 1"
                  @click="toggleIsland(idx + 1)"
                  class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-[600px] h-[400px] bg-[#2b2b2b] rounded-[10px] flex flex-col items-center justify-start gap-5 p-5 shadow-lg border border-black cursor-pointer"
                >
                  <div class="top w-full flex flex-col justify-center items-center gap-1">
                    <div
                      class="icon w-16 h-16 border-2 border-[#ae04cc] flex items-center justify-center rounded-full text-[#ae04cc] font-bold"
                    >
                      <span class="material-symbols-outlined"> music_note </span>
                    </div>
                    <div class="text-top flex flex-col gap-1 justify-center items-center">
                      <p class="text-white text-base font-bold">
                        {{ islandContentsExpandedId[idx]?.title }}
                      </p>
                      <p class="text-gray-300 text-xs">
                        {{ islandContentsExpandedId[idx]?.subtitle }}
                      </p>
                    </div>
                  </div>
                  <div
                    class="mid-text-row1 flex flex-row items-center justify-between w-full gap-3"
                  >
                    <div class="point flex flex-row items-center justify-start w-full gap-3">
                      <div class="bulet h-1 w-1 rounded-full bg-[#ae04cc]"></div>
                      <div class="features w-full flex flex-col justify-start items-start gap-1">
                        <p class="text-[#ae04cc] text-sm font-bold">
                          {{ islandContentsExpandedId[idx]?.points[0]?.title }}
                        </p>
                        <p class="text-gray-300 text-xs">
                          {{ islandContentsExpandedId[idx]?.points[0]?.description }}
                        </p>
                      </div>
                    </div>
                    <div class="point flex flex-row items-center justify-start w-full gap-3">
                      <div class="bulet h-1 w-1 rounded-full bg-[#ae04cc]"></div>
                      <div class="features w-full flex flex-col justify-start items-start gap-1">
                        <p class="text-[#ae04cc] text-sm font-bold">
                          {{ islandContentsExpandedId[idx]?.points[1]?.title }}
                        </p>
                        <p class="text-gray-300 text-xs">
                          {{ islandContentsExpandedId[idx]?.points[1]?.description }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div
                    class="mid-text-row2 flex flex-row items-center justify-between w-full gap-3"
                  >
                    <div class="point flex flex-row items-center justify-start w-full gap-3">
                      <div class="bulet h-1 w-1 rounded-full bg-[#ae04cc]"></div>
                      <div class="features w-full flex flex-col justify-start items-start gap-1">
                        <p class="text-[#ae04cc] text-sm font-bold">
                          {{ islandContentsExpandedId[idx]?.points[2]?.title }}
                        </p>
                        <p class="text-gray-300 text-xs">
                          {{ islandContentsExpandedId[idx]?.points[2]?.description }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </transition>
            </div>
          </div>
        </div>
        <div
          v-if="!isDarkMode"
          class="content-kedua w-full h-fit flex flex-col items-center justify-between snap-start pt-10 pb-5 gap-10 px-20"
        >
          <div class="k flex flex-col items-center justify-center gap-2">
            <h2 class="text-2xl font-bold mb-4 text-black">
              {{ isLangEnglish ? 'Easy to use' : 'Mudah untuk Digunakan' }}
            </h2>
            <p class="text-gray-700 text-center text-sm mb-2">
              {{
                isLangEnglish
                  ? 'Our AI music detection model is designed for effortless use, allowing anyone to analyze audio without technical expertise. Simply upload a file, and the system will process it and deliver accurate results within seconds. With a clean interface and minimal steps, it provides a fast and reliable way to distinguish between AI-generated and human-made music.'
                  : 'Model pendeteksi musik berbasis AI kami dirancang agar mudah digunakan, sehingga siapa pun dapat menganalisis audio tanpa perlu memiliki keahlian teknis. Cukup unggah file, dan sistem akan memprosesnya serta memberikan hasil yang akurat dalam hitungan detik. Dengan antarmuka yang sederhana dan langkah-langkah yang minim, model ini menawarkan cara yang cepat dan andal untuk membedakan antara musik yang dihasilkan oleh AI dan musik yang dibuat oleh manusia.'
              }}
            </p>
          </div>

          <div class="howitworks w-full h-fit flex flex-row items-center justify-center gap-2">
            <div class="step flex flex-col items-center justify-center gap-4">
              <div
                class="icon w-16 h-16 bg-transparent rounded-full flex items-center justify-center text-white font-bold border-[2px] border-[#83009a] text-black"
              >
                <p class="text-[#83009a] text-center">
                  <span class="material-symbols-outlined"> cloud_upload </span>
                </p>
              </div>
              <p class="text-gray-700 text-center">
                {{ isLangEnglish ? 'Step 1: Upload your audio' : 'Langkah 1: Unggah audio Anda' }}
              </p>
            </div>
            <div class="w-50 h-px bg-gray-400 transition-all duration-800"></div>
            <div class="step flex flex-col items-center justify-center gap-4">
              <div
                class="icon w-16 h-16 bg-transparent rounded-full flex items-center justify-center text-white font-bold border-[2px] border-[#83009a] text-[#83009a]"
              >
                <p class="text-[#83009a] text-center">
                  <span class="material-symbols-outlined"> robot_2 </span>
                </p>
              </div>
              <p class="text-gray-700 text-center">
                {{
                  isLangEnglish
                    ? 'Step 2: Let the model analyze your audio'
                    : 'Langkah 2: Biarkan model menganalisis audio Anda'
                }}
              </p>
            </div>
            <div class="w-50 h-px bg-gray-400 transition-all duration-800"></div>
            <div class="step flex flex-col items-center justify-center gap-4">
              <div
                class="icon w-16 h-16 bg-transparent rounded-full flex items-center justify-center text-white font-bold border-[2px] border-[#83009a] text-[#83009a]"
              >
                <p class="text-[#83009a] text-center">
                  <span class="material-symbols-outlined"> music_note </span>
                </p>
              </div>
              <p class="text-gray-700 text-center">
                {{ isLangEnglish ? 'Step 3: Get your results' : 'Langkah 3: Dapatkan hasil Anda' }}
              </p>
            </div>
          </div>
          <div
            class="desc w-full h-fit flex flex-col items-center justify-between snap-start pt-5 pb-5 gap-10 px-20"
          >
            <div class="text flex flex-col items-center justify-center gap-0">
              <h2 class="text-2xl font-bold mb-4 text-black">
                {{ isLangEnglish ? 'Supported Genres' : 'Genre yang Didukung' }}
              </h2>
              <h5 class="text-[#83009a] text-sm">
                {{
                  isLangEnglish
                    ? 'Our model currently works best with these genres:'
                    : 'Model kami saat ini bekerja paling baik dengan genre-genre berikut:'
                }}
              </h5>
            </div>

            <div class="w-full px-10">
              <div
                class="flex flex-row justify-start items-start gap-6 overflow-x-auto snap-x snap-mandatory scroll-smooth pb-1"
              >
                <div
                  v-for="i in 7"
                  :key="i"
                  class="flex-shrink-0 snap-start w-52 h-40 bg-[#83009a] rounded-xl flex flex-col items-center justify-between p-5 shadow-lg border border-gray-300 transition"
                >
                  <div
                    class="w-12 h-12 rounded-full flex items-center justify-center border-2 border-white"
                  >
                    <p class="text-white font-bold">{{ i }}</p>
                  </div>

                  <p class="text-white font-medium">{{ genres[i - 1] }}</p>
                </div>
              </div>
            </div>

            <div class="text-xs text-gray-500 pb-4">
              <p>
                {{
                  isLangEnglish
                    ? '*These are the genres we have the most training data for. Results for other genres may be less accurate.'
                    : '*Ini adalah genre-genre yang memiliki data pelatihan paling banyak. Hasil untuk genre lain mungkin kurang akurat.'
                }}
              </p>
            </div>
          </div>
        </div>
        <div
          v-else
          class="content-kedua w-full h-fit flex flex-col items-center justify-between snap-start pt-10 pb-5 gap-10 px-20"
        >
          <div class="k flex flex-col items-center justify-center gap-2">
            <h2 class="text-2xl font-bold mb-4 text-[#ae04cc]">
              {{ isLangEnglish ? 'Easy to use' : 'Mudah untuk Digunakan' }}
            </h2>
            <p class="text-white text-center text-sm mb-2">
              {{
                isLangEnglish
                  ? 'Our AI music detection model is designed for effortless use, allowing anyone to analyze audio without technical expertise. Simply upload a file, and the system will process it and deliver accurate results within seconds. With a clean interface and minimal steps, it provides a fast and reliable way to distinguish between AI-generated and human-made music.'
                  : 'Model pendeteksi musik berbasis AI kami dirancang agar mudah digunakan, sehingga siapa pun dapat menganalisis audio tanpa perlu memiliki keahlian teknis. Cukup unggah file, dan sistem akan memprosesnya serta memberikan hasil yang akurat dalam hitungan detik. Dengan antarmuka yang sederhana dan langkah-langkah yang minim, model ini menawarkan cara yang cepat dan andal untuk membedakan antara musik yang dihasilkan oleh AI dan musik yang dibuat oleh manusia.'
              }}
            </p>
          </div>

          <div class="howitworks w-full h-fit flex flex-row items-center justify-center gap-2">
            <div class="step flex flex-col items-center justify-center gap-4">
              <div
                class="icon w-16 h-16 bg-transparent rounded-full flex items-center justify-center text-white font-bold border-[2px] border-[#ae04cc] text-[#ae04cc]"
              >
                <p class="text-[#ae04cc] text-center">
                  <span class="material-symbols-outlined"> cloud_upload </span>
                </p>
              </div>
              <p class="text-white text-center">
                {{ isLangEnglish ? 'Step 1: Upload your audio' : 'Langkah 1: Unggah audio Anda' }}
              </p>
            </div>
            <div class="w-50 h-px bg-gray-400 transition-all duration-800"></div>
            <div class="step flex flex-col items-center justify-center gap-4">
              <div
                class="icon w-16 h-16 bg-transparent rounded-full flex items-center justify-center text-white font-bold border-[2px] border-[#ae04cc] text-[#ae04cc]"
              >
                <p class="text-[#ae04cc] text-center">
                  <span class="material-symbols-outlined"> robot_2 </span>
                </p>
              </div>
              <p class="text-white text-center">
                {{
                  isLangEnglish
                    ? 'Step 2: Let the model analyze your audio'
                    : 'Langkah 2: Biarkan model menganalisis audio Anda'
                }}
              </p>
            </div>
            <div class="w-50 h-px bg-gray-400 transition-all duration-800"></div>
            <div class="step flex flex-col items-center justify-center gap-4">
              <div
                class="icon w-16 h-16 bg-transparent rounded-full flex items-center justify-center text-white font-bold border-[2px] border-[#ae04cc] text-[#ae04cc]"
              >
                <p class="text-[#ae04cc] text-center">
                  <span class="material-symbols-outlined"> music_note </span>
                </p>
              </div>
              <p class="text-white text-center">
                {{ isLangEnglish ? 'Step 3: Get your results' : 'Langkah 3: Dapatkan hasil Anda' }}
              </p>
            </div>
          </div>
          <div
            class="desc w-full h-fit flex flex-col items-center justify-between snap-start pt-5 pb-5 gap-10 px-20"
          >
            <div class="text flex flex-col items-center justify-center gap-0">
              <h2 class="text-2xl font-bold mb-4 text-[#ae04cc]">
                {{ isLangEnglish ? 'Supported Genres' : 'Genre yang Didukung' }}
              </h2>
              <h5 class="text-white text-sm">
                {{
                  isLangEnglish
                    ? 'Our model currently works best with these genres:'
                    : 'Model kami saat ini bekerja paling baik dengan genre-genre berikut:'
                }}
              </h5>
            </div>

            <div class="w-full px-10">
              <div
                class="flex flex-row justify-start items-start gap-6 overflow-x-auto snap-x snap-mandatory scroll-smooth pb-1"
              >
                <div
                  v-for="i in 7"
                  :key="i"
                  class="flex-shrink-0 snap-start w-52 h-40 bg-[#83009a] rounded-xl flex flex-col items-center justify-between p-5 shadow-lg border border-black transition"
                >
                  <div
                    class="w-12 h-12 rounded-full flex items-center justify-center border-2 border-white"
                  >
                    <p class="text-white font-bold">{{ i }}</p>
                  </div>

                  <p class="text-white font-medium">{{ genres[i - 1] }}</p>
                </div>
              </div>
            </div>

            <div class="text-xs text-gray-200 pb-4">
              <p>
                {{
                  isLangEnglish
                    ? '*These are the genres we have the most training data for. Results for other genres may be less accurate.'
                    : '*Ini adalah genre-genre yang memiliki data pelatihan paling banyak. Hasil untuk genre lain mungkin kurang akurat.'
                }}
              </p>
            </div>
          </div>
        </div>

        <div
          v-if="!isDarkMode"
          class="content-keempat w-full h-fit flex flex-col items-center justify-between snap-start pt-10 pb-25 gap-10 px-50"
        >
          <div class="tex flex flex-col items-center justify-center gap-0">
            <h2 class="text-2xl font-bold text-black">FAQ</h2>
            <h5 class="text-[#83009a] text-sm">
              {{
                isLangEnglish ? 'Frequently Asked Questions' : 'Pertanyaan yang Sering Ditanyakan'
              }}
            </h5>
          </div>

          <div class="questions w-[80%] flex flex-col gap-4">
            <div
              v-if="isLangEnglish"
              v-for="(faq, index) in faqs"
              :key="index"
              class="border border-gray-300 rounded-[10px] overflow-hidden shadow-lg"
            >
              <div
                @click="toggleFAQ(index)"
                class="bg-white flex justify-between items-center p-3 cursor-pointer"
              >
                <span class="font-bold text-black text-sm"
                  ><span class="text-[#83009a] font-bold text-base">Q:</span> {{ faq.q }}</span
                >

                <span
                  class="material-symbols-outlined transition-transform duration-300 text-[#83009a]"
                  :class="activeIndex === index ? 'rotate-180' : ''"
                >
                  keyboard_arrow_down
                </span>
              </div>

              <div
                class="bg-[#83009a] text-white text-sm transition-all duration-500 overflow-hidden"
                :class="activeIndex === index ? 'max-h-40 p-3' : 'max-h-0 p-0'"
              >
                <span class="font-bold text-base">A:</span> {{ faq.a }}
              </div>
            </div>
            <div
              v-else
              v-for="(faq, idx) in faqsId"
              :key="idx"
              class="border border-gray-300 rounded-[10px] overflow-hidden shadow-lg"
            >
              <div
                @click="toggleFAQ(idx)"
                class="bg-white flex justify-between items-center p-3 cursor-pointer"
              >
                <span class="font-bold text-black text-sm"
                  ><span class="text-[#83009a] font-bold text-base">Q:</span> {{ faq.q }}</span
                >

                <span
                  class="material-symbols-outlined transition-transform duration-300 text-[#83009a]"
                  :class="activeIndex === idx ? 'rotate-180' : ''"
                >
                  keyboard_arrow_down
                </span>
              </div>

              <div
                class="bg-[#83009a] text-white text-sm transition-all duration-500 overflow-hidden"
                :class="activeIndex === idx ? 'max-h-40 p-3' : 'max-h-0 p-0'"
              >
                <span class="font-bold text-base">A:</span> {{ faq.a }}
              </div>
            </div>
          </div>
        </div>
        <div
          v-else
          class="content-keempat w-full h-fit flex flex-col items-center justify-between snap-start pt-10 pb-25 gap-10 px-50"
        >
          <div class="tex flex flex-col items-center justify-center gap-0">
            <h2 class="text-2xl font-bold text-[#ae04cc]">FAQ</h2>
            <h5 class="text-white text-sm">
              {{
                isLangEnglish ? 'Frequently Asked Questions' : 'Pertanyaan yang Sering Ditanyakan'
              }}
            </h5>
          </div>

          <div class="questions w-[80%] flex flex-col gap-4">
            <div
              v-if="isLangEnglish"
              v-for="(faq, index) in faqs"
              :key="index"
              class="border border-black rounded-[10px] overflow-hidden shadow-lg"
            >
              <div
                @click="toggleFAQ(index)"
                class="bg-[#2b2b2b] flex justify-between items-center p-3 cursor-pointer"
              >
                <span class="font-bold text-white text-sm"
                  ><span class="text-[#ae04cc] font-bold text-base">Q:</span> {{ faq.q }}</span
                >

                <span
                  class="material-symbols-outlined transition-transform duration-300 text-[#ae04cc]"
                  :class="activeIndex === index ? 'rotate-180' : ''"
                >
                  keyboard_arrow_down
                </span>
              </div>

              <div
                class="bg-[#ae04cc] text-white text-sm transition-all duration-500 overflow-hidden"
                :class="activeIndex === index ? 'max-h-40 p-3' : 'max-h-0 p-0'"
              >
                <span class="font-bold text-base">A:</span> {{ faq.a }}
              </div>
            </div>
            <div
              v-else
              v-for="(faq, idx) in faqsId"
              :key="idx"
              class="border border-black rounded-[10px] overflow-hidden shadow-lg"
            >
              <div
                @click="toggleFAQ(idx)"
                class="bg-[#2b2b2b] flex justify-between items-center p-3 cursor-pointer"
              >
                <span class="font-bold text-white text-sm"
                  ><span class="text-[#ae04cc] font-bold text-base">Q:</span> {{ faq.q }}</span
                >

                <span
                  class="material-symbols-outlined transition-transform duration-300 text-[#ae04cc]"
                  :class="activeIndex === idx ? 'rotate-180' : ''"
                >
                  keyboard_arrow_down
                </span>
              </div>

              <div
                class="bg-[#ae04cc] text-white text-sm transition-all duration-500 overflow-hidden"
                :class="activeIndex === idx ? 'max-h-40 p-3' : 'max-h-0 p-0'"
              >
                <span class="font-bold text-base">A:</span> {{ faq.a }}
              </div>
            </div>
          </div>
        </div>
        <div
          v-if="!isDarkMode"
          class="Footer w-full h-fit flex flex-col items-center bg-[#83009a] justify-between snap-start pt-5 pb-5 gap-10"
        >
          <p class="text-white text-sm">© 2026 Buat Skripsi.</p>
        </div>
        <div
          v-else
          class="Footer w-full h-fit flex flex-col items-center bg-[#2b2b2b] justify-between snap-start pt-5 pb-5 gap-10"
        >
          <p class="text-[#ae04cc] text-sm">© 2026 Buat Skripsi.</p>
        </div>
      </div>
    </div>

    <Menu :isUserLoggedin="isUserLoggedin" />
    <ModalLogin />
    <ModalHistory />
    <DeleteConfModal />
    <DeleteAllConfModal />

    <div
      v-if="activeIsland !== null"
      class="fixed inset-0 bg-black/70 z-40"
      @click="activeIsland = null"
    ></div>
  </main>
</template>
