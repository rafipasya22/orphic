<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue';
import { gantiBahasaFunc } from '../composable/gantiBahasa';
import modalWarning from '../components/modalWarning.vue';
import { openWarningFunc } from '../composable/openWarning';
import Menu from '../components/menu.vue';
import axios from 'axios';
import { isuserloggedinFunc } from '../composable/isUserLoggedIn';
import { activefunc } from '../composable/active';
import Sidebar from '../components/sidebar.vue';
import { darkFunc } from '../composable/darkMode';
import { useAuthStore } from '../stores/authstore.ts';
import { loadingFunc } from '../composable/globalVar.ts';

const { isUserLoggedin } = isuserloggedinFunc();
const { isCollapsed } = loadingFunc();
const { isDarkMode } = darkFunc();
const { isDashActive, isHistoryActive, isHelpActive } = activefunc();
const { openWarning } = openWarningFunc();
const { isLangEnglish } = gantiBahasaFunc();
const authStore = useAuthStore();

const activeIsland = ref<number | null>(null);

const toggleIsland = (index: number) => {
  activeIsland.value = activeIsland.value === index ? null : index;
};

const faqData = [
  {
    judul: 'How does AI music detection work?',
    desc: 'Our system analyzes audio patterns using Mel-Spectrogram representations and deep learning models to determine whether a track is AI-generated or human-created.',

    detail: {
      title: 'How does AI music detection work?',
      subtitle:
        'Our system combines audio signal processing and deep learning techniques to identify patterns commonly found in AI-generated music.',

      points: [
        {
          title: 'Mel Spectrogram Analysis',
          desc: 'Every uploaded song is converted into a Mel Spectrogram, a visual representation of sound frequencies over time. This allows the model to examine audio in a format similar to an image.',
        },
        {
          title: 'Pattern Recognition',
          desc: 'The neural network analyzes frequency distributions, harmonics, and temporal structures that may differ between human-created and AI-generated music.',
        },
        {
          title: 'Prediction Generation',
          desc: 'After processing multiple audio segments, the model combines the results and produces an AI probability score along with a confidence level.',
        },
      ],
    },
  },

  {
    judul: 'What is a Mel Spectrogram?',
    desc: 'A Mel Spectrogram is a visual representation of sound frequencies over time. It helps our AI model identify patterns that may indicate synthetic or human-made music.',

    detail: {
      title: 'What is a Mel Spectrogram?',
      subtitle:
        'Mel Spectrograms are one of the most important inputs used by the detection model.',

      points: [
        {
          title: 'Frequency Representation',
          desc: 'They display how sound frequencies change over time, making complex audio patterns easier to analyze.',
        },
        {
          title: 'Human Hearing Inspired',
          desc: 'The Mel scale is designed to better match how humans perceive pitch differences.',
        },
        {
          title: 'Deep Learning Friendly',
          desc: 'Since spectrograms resemble images, convolutional neural networks can effectively learn meaningful audio features from them.',
        },
      ],
    },
  },

  {
    judul: 'Which audio formats are supported?',
    desc: 'The system supports common audio formats such as MP3 and WAV For best results, upload high-quality audio files.',

    detail: {
      title: 'Which audio formats are supported?',
      subtitle: 'The model accepts several popular audio formats for analysis.',

      points: [
        {
          title: 'Supported Formats',
          desc: 'MP3 and WAV files are supported by the system.',
        },
        {
          title: 'Audio Quality',
          desc: 'Higher quality audio generally provides more reliable predictions.',
        },
        {
          title: 'Recommendation',
          desc: 'Whenever possible, upload the original audio file instead of heavily compressed versions.',
        },
      ],
    },
  },

  {
    judul: 'Which music genres can be analyzed?',
    desc: 'Our model is designed to analyze a wide range of genres, including pop, rock, classical, electronic, jazz, hip-hop, and instrumental music.',

    detail: {
      title: 'Which music genres can be analyzed?',
      subtitle: 'The system is designed to work across a wide variety of musical styles.',

      points: [
        {
          title: 'Popular Genres',
          desc: 'Pop, rock, electronic, hip-hop, jazz, classical, and instrumental tracks are generally supported.',
        },
        {
          title: 'Cross-Genre Capability',
          desc: 'The model focuses on audio characteristics rather than genre labels.',
        },
        {
          title: 'Limitations',
          desc: 'Very unusual genres or heavily altered recordings may affect prediction reliability.',
        },
      ],
    },
  },

  {
    judul: 'How accurate is the detection?',
    desc: 'Detection accuracy depends on audio quality and the type of AI-generated music. The system provides a confidence score alongside each prediction.',

    detail: {
      title: 'How accurate is the detection?',
      subtitle:
        'Prediction accuracy depends on the quality and characteristics of the uploaded audio.',

      points: [
        {
          title: 'Confidence Score',
          desc: 'A higher confidence score generally indicates stronger evidence supporting the prediction.',
        },
        {
          title: 'Audio Quality Matters',
          desc: 'Low bitrate files, excessive noise, or severe compression can reduce performance.',
        },
        {
          title: 'Best Practice',
          desc: 'For the most reliable results, upload original audio files whenever possible.',
        },
      ],
    },
  },

  {
    judul: 'Can edited AI music still be detected?',
    desc: 'Significantly post-processed AI music may be more difficult to identify, as editing can alter the patterns learned by the detection model.',

    detail: {
      title: 'Can edited AI music still be detected?',
      subtitle:
        'Detection becomes more difficult when AI-generated music has been heavily modified.',

      points: [
        {
          title: 'Post-Processing Effects',
          desc: 'Mixing, mastering, filtering, and other editing techniques can alter the patterns used by the detection model.',
        },
        {
          title: 'Partial Detection',
          desc: 'Some AI traces may remain detectable depending on the extent of the modifications.',
        },
        {
          title: 'Research Limitation',
          desc: 'The highest accuracy is typically achieved on AI music that has not undergone significant post-processing.',
        },
      ],
    },
  },

  {
    judul: 'Why does the system show confidence scores?',
    desc: 'Confidence scores indicate how certain the model is about its prediction, helping users better interpret the results.',

    detail: {
      title: 'Why does the system show confidence scores?',
      subtitle: 'Confidence scores help users better understand prediction reliability.',

      points: [
        {
          title: 'Prediction Certainty',
          desc: 'Confidence scores represent how strongly the model supports its prediction.',
        },
        {
          title: 'Better Interpretation',
          desc: 'Users can use confidence scores to evaluate how trustworthy a result may be.',
        },
        {
          title: 'Additional Context',
          desc: 'Confidence scores should be considered alongside the prediction itself.',
        },
      ],
    },
  },

  {
    judul: 'What audio features are analyzed?',
    desc: 'The model evaluates Mel-Spectrogram patterns, spectral characteristics, frequency distributions, and temporal audio structures.',

    detail: {
      title: 'What audio features are analyzed?',
      subtitle: 'Several complementary audio features are examined during prediction.',

      points: [
        {
          title: 'Mel Spectrogram',
          desc: 'Captures frequency content over time and serves as the primary model input.',
        },
        {
          title: 'Spectral Features',
          desc: 'Includes measurements such as spectral centroid, flatness, energy variation, and dynamic range.',
        },
        {
          title: 'Temporal Features',
          desc: 'The model evaluates how audio patterns evolve over time to identify potential AI-generated structures.',
        },
      ],
    },
  },
];

const faqDataId = [
  {
    judul: 'Bagaimana deteksi musik AI bekerja?',
    desc: 'Sistem kami menganalisis pola audio menggunakan representasi Mel-Spectrogram dan model deep learning untuk menentukan apakah sebuah lagu dibuat oleh AI atau manusia.',

    detail: {
      title: 'Bagaimana deteksi musik AI bekerja?',
      subtitle:
        'Sistem kami menggabungkan pemrosesan sinyal audio dan teknik deep learning untuk mengidentifikasi pola yang umum ditemukan pada musik hasil generasi AI.',

      points: [
        {
          title: 'Analisis Mel Spectrogram',
          desc: 'Setiap lagu yang diunggah akan dikonversi menjadi Mel Spectrogram, yaitu representasi visual frekuensi suara terhadap waktu. Hal ini memungkinkan model menganalisis audio dalam format yang menyerupai gambar.',
        },
        {
          title: 'Pengenalan Pola',
          desc: 'Jaringan saraf menganalisis distribusi frekuensi, harmonik, serta struktur temporal yang dapat berbeda antara musik buatan manusia dan musik hasil generasi AI.',
        },
        {
          title: 'Pembuatan Prediksi',
          desc: 'Setelah memproses beberapa segmen audio, model menggabungkan hasil analisis dan menghasilkan skor probabilitas AI beserta tingkat keyakinannya.',
        },
      ],
    },
  },

  {
    judul: 'Apa itu Mel Spectrogram?',
    desc: 'Mel Spectrogram adalah representasi visual frekuensi suara terhadap waktu. Representasi ini membantu model AI mengenali pola yang menunjukkan musik sintetis maupun musik buatan manusia.',

    detail: {
      title: 'Apa itu Mel Spectrogram?',
      subtitle:
        'Mel Spectrogram merupakan salah satu masukan paling penting yang digunakan oleh model deteksi.',

      points: [
        {
          title: 'Representasi Frekuensi',
          desc: 'Mel Spectrogram menampilkan bagaimana frekuensi suara berubah dari waktu ke waktu sehingga pola audio yang kompleks menjadi lebih mudah dianalisis.',
        },
        {
          title: 'Terinspirasi dari Pendengaran Manusia',
          desc: 'Skala Mel dirancang agar lebih sesuai dengan cara manusia merasakan perbedaan tinggi rendahnya nada.',
        },
        {
          title: 'Cocok untuk Deep Learning',
          desc: 'Karena bentuknya menyerupai gambar, jaringan saraf konvolusional (CNN) dapat mempelajari fitur audio yang bermakna secara efektif.',
        },
      ],
    },
  },

  {
    judul: 'Format audio apa saja yang didukung?',
    desc: 'Sistem mendukung format audio umum seperti MP3 dan WAV. Untuk hasil terbaik, gunakan file audio dengan kualitas yang baik.',

    detail: {
      title: 'Format audio apa saja yang didukung?',
      subtitle: 'Model menerima beberapa format audio populer untuk dianalisis.',

      points: [
        {
          title: 'Format yang Didukung',
          desc: 'File MP3 dan WAV dapat diproses oleh sistem.',
        },
        {
          title: 'Kualitas Audio',
          desc: 'Audio dengan kualitas yang lebih tinggi umumnya menghasilkan prediksi yang lebih andal.',
        },
        {
          title: 'Rekomendasi',
          desc: 'Jika memungkinkan, unggah file audio asli dibandingkan versi yang telah mengalami kompresi berat.',
        },
      ],
    },
  },

  {
    judul: 'Genre musik apa saja yang dapat dianalisis?',
    desc: 'Model dirancang untuk menganalisis berbagai genre, termasuk pop, rock, klasik, elektronik, jazz, hip-hop, dan musik instrumental.',

    detail: {
      title: 'Genre musik apa saja yang dapat dianalisis?',
      subtitle: 'Sistem dirancang untuk bekerja pada berbagai jenis dan gaya musik.',

      points: [
        {
          title: 'Genre Populer',
          desc: 'Genre seperti pop, rock, elektronik, hip-hop, jazz, klasik, dan instrumental umumnya dapat dianalisis dengan baik.',
        },
        {
          title: 'Kemampuan Lintas Genre',
          desc: 'Model berfokus pada karakteristik audio, bukan label genre, sehingga dapat digunakan pada berbagai jenis musik.',
        },
        {
          title: 'Keterbatasan',
          desc: 'Genre yang sangat tidak umum atau rekaman yang telah banyak dimodifikasi dapat memengaruhi keandalan prediksi.',
        },
      ],
    },
  },

  {
    judul: 'Seberapa akurat hasil deteksinya?',
    desc: 'Tingkat akurasi bergantung pada kualitas audio dan jenis musik AI yang dianalisis. Sistem juga menampilkan skor kepercayaan untuk membantu interpretasi hasil.',

    detail: {
      title: 'Seberapa akurat hasil deteksinya?',
      subtitle: 'Akurasi prediksi bergantung pada kualitas dan karakteristik audio yang diunggah.',

      points: [
        {
          title: 'Skor Kepercayaan',
          desc: 'Skor kepercayaan yang lebih tinggi umumnya menunjukkan bahwa model menemukan bukti yang lebih kuat untuk mendukung prediksinya.',
        },
        {
          title: 'Kualitas Audio Penting',
          desc: 'File dengan bitrate rendah, noise berlebih, atau kompresi yang terlalu tinggi dapat menurunkan performa deteksi.',
        },
        {
          title: 'Praktik Terbaik',
          desc: 'Untuk hasil yang paling andal, unggahlah file audio asli jika memungkinkan.',
        },
      ],
    },
  },

  {
    judul: 'Apakah musik AI yang sudah diedit masih bisa dideteksi?',
    desc: 'Musik AI yang telah mengalami proses editing atau post-processing secara signifikan mungkin lebih sulit dideteksi karena pola aslinya telah berubah.',

    detail: {
      title: 'Apakah musik AI yang sudah diedit masih bisa dideteksi?',
      subtitle:
        'Deteksi menjadi lebih sulit ketika musik hasil generasi AI telah mengalami banyak modifikasi.',

      points: [
        {
          title: 'Efek Post-Processing',
          desc: 'Mixing, mastering, filtering, dan teknik pengolahan audio lainnya dapat mengubah pola yang digunakan model untuk melakukan deteksi.',
        },
        {
          title: 'Deteksi Sebagian',
          desc: 'Beberapa jejak AI mungkin masih dapat terdeteksi tergantung pada tingkat modifikasi yang dilakukan.',
        },
        {
          title: 'Keterbatasan Penelitian',
          desc: 'Tingkat akurasi tertinggi biasanya diperoleh pada musik AI yang belum mengalami post-processing secara signifikan.',
        },
      ],
    },
  },

  {
    judul: 'Mengapa sistem menampilkan confidence score?',
    desc: 'Confidence score menunjukkan tingkat keyakinan model terhadap prediksi yang diberikan sehingga pengguna dapat memahami hasil dengan lebih baik.',

    detail: {
      title: 'Mengapa sistem menampilkan confidence score?',
      subtitle: 'Skor kepercayaan membantu pengguna memahami tingkat keandalan prediksi.',

      points: [
        {
          title: 'Tingkat Keyakinan Prediksi',
          desc: 'Confidence score menunjukkan seberapa kuat model mendukung hasil prediksi yang diberikan.',
        },
        {
          title: 'Interpretasi yang Lebih Baik',
          desc: 'Pengguna dapat memanfaatkan skor ini untuk menilai seberapa dapat dipercaya suatu hasil prediksi.',
        },
        {
          title: 'Konteks Tambahan',
          desc: 'Confidence score sebaiknya dipertimbangkan bersama hasil prediksi utama, bukan sebagai satu-satunya indikator.',
        },
      ],
    },
  },

  {
    judul: 'Fitur audio apa yang dianalisis?',
    desc: 'Model mengevaluasi pola Mel-Spectrogram, karakteristik spektral, distribusi frekuensi, serta struktur temporal dalam audio.',

    detail: {
      title: 'Fitur audio apa yang dianalisis?',
      subtitle: 'Beberapa fitur audio yang saling melengkapi diperiksa selama proses prediksi.',

      points: [
        {
          title: 'Mel Spectrogram',
          desc: 'Merepresentasikan konten frekuensi terhadap waktu dan menjadi masukan utama bagi model.',
        },
        {
          title: 'Fitur Spektral',
          desc: 'Meliputi pengukuran seperti spectral centroid, spectral flatness, variasi energi, dan dynamic range.',
        },
        {
          title: 'Fitur Temporal',
          desc: 'Model mengevaluasi bagaimana pola audio berkembang dari waktu ke waktu untuk mengidentifikasi struktur yang berpotensi berasal dari AI.',
        },
      ],
    },
  },
];

const faq = computed(() => (isLangEnglish.value ? faqData : faqDataId));

const profile = ref<any>(null);

onMounted(async () => {
  isDashActive.value = false;
  isHistoryActive.value = false;
  isHelpActive.value = true;
  const user = authStore.user;

  if (!user) {
    openWarning();
    return;
  }

  const res = await axios.get(`http://localhost:8000/api/profile/${user.id}`);

  profile.value = res.data;
});

onUnmounted(() => {});
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
            {{ isLangEnglish ? 'Help' : 'Bantuan' }}
          </p>
        </div>
        <div
          class="content w-full h-[90%] flex flex-col justify-center items-center gap-6"
          :class="isCollapsed ? 'px-20' : 'px-15'"
        >
          <div class="islands grid grid-cols-[repeat(auto-fit,minmax(320px,1fr))] gap-5 w-full">
            <div v-for="(island, index) in faq" :key="index" class="relative">
              <div
                @click="toggleIsland(index + 1)"
                class="container w-86 h-30 gap-1 bg-[#EBEBEB] border border-gray-300 rounded-[10px] flex flex-col items-start justify-between px-5 pt-5 pb-8 shadow-lg cursor-pointer transition-all duration-100 hover:border-r-4 hover:border-[#83009a]"
                :class="
                  activeIsland === index + 1 ? 'opacity-0 pointer-events-none' : 'opacity-100'
                "
              >
                <div class="top flex flex-row justify-center items-start gap-1 w-full">
                  <div
                    class="title w-[90%] flex items-start justify-between rounded-full text-[#83009a] font-bold"
                  >
                    <p class="text-black text-sm text-start font-bold">{{ island.judul }}</p>
                  </div>
                  <span class="material-symbols-outlined text-[#83009a]"> bubble </span>
                </div>
                <div class="mid-text w-[80%]">
                  <p class="text-gray-700 text-xs text-start line-clamp-2">
                    {{ island.desc }}
                  </p>
                </div>
              </div>
              <transition name="cardfade">
                <div
                  v-if="activeIsland === index + 1"
                  @click="toggleIsland(index + 1)"
                  class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-[600px] h-fit bg-white rounded-[10px] flex flex-col items-center justify-start gap-5 px-5 pt-5 pb-8 shadow-lg border border-gray-300 cursor-pointer"
                >
                  <div class="top w-full flex flex-row justify-start items-start gap-3">
                    <span class="material-symbols-outlined text-[#83009a] !mt-1"> help </span>
                    <div class="text-top flex flex-col gap-1 justify-start items-start">
                      <p class="text-black text-base font-bold">{{ island.detail.title }}</p>
                      <p class="text-gray-700 text-xs">
                        {{ island.detail.subtitle }}
                      </p>
                    </div>
                  </div>
                  <div
                    v-for="(point, i) in island.detail.points"
                    :key="i"
                    class="flex flex-row gap-3 h-fit w-full justify-start items-center ps-8"
                  >
                    <div class="h-1 w-1 rounded-full bg-[#83009a] mt-2"></div>

                    <div class="flex flex-col gap-1">
                      <p class="text-[#83009a] text-sm font-bold">
                        {{ point.title }}
                      </p>

                      <p class="text-gray-700 text-xs">
                        {{ point.desc }}
                      </p>
                    </div>
                  </div>
                </div>
              </transition>
            </div>
          </div>

          <div
            v-if="activeIsland !== null"
            class="fixed inset-0 bg-black/70 z-40"
            @click="activeIsland = null"
          ></div>
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
            {{ isLangEnglish ? 'Help' : 'Bantuan' }}
          </p>
        </div>
        <div
          class="content w-full h-[90%] flex flex-col justify-center items-center gap-6"
          :class="isCollapsed ? 'px-20' : 'px-15'"
        >
          <div class="islands grid grid-cols-[repeat(auto-fit,minmax(320px,1fr))] gap-5 w-full">
          <div v-for="(island, index) in faq" :key="index" class="relative">
            <div
              @click="toggleIsland(index + 1)"
              class="container w-86 h-30 gap-1 bg-[#1b1b1b] rounded-[10px] flex flex-col items-start justify-between px-5 pt-5 pb-8 shadow-lg cursor-pointer transition-all duration-100 hover:border-r-4 hover:border-[#83009a]"
              :class="activeIsland === index + 1 ? 'opacity-0 pointer-events-none' : 'opacity-100'"
            >
              <div class="top flex flex-row justify-center items-start gap-1 w-full">
                <div
                  class="title w-[90%] flex items-start justify-between rounded-full text-[#83009a] font-bold"
                >
                  <p class="text-white text-sm text-start font-bold">{{ island.judul }}</p>
                </div>
                <span class="material-symbols-outlined text-[#83009a]"> bubble </span>
              </div>
              <div class="mid-text w-[80%]">
                <p class="text-[#6d6d6d] text-xs text-start line-clamp-2">
                  {{ island.desc }}
                </p>
              </div>
            </div>
            <transition name="cardfade">
              <div
                v-if="activeIsland === index + 1"
                @click="toggleIsland(index + 1)"
                class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-[600px] h-fit bg-[#1b1b1b] rounded-[10px] flex flex-col items-center justify-start gap-5 px-5 pt-5 pb-8 shadow-lg cursor-pointer"
              >
                <div class="top w-full flex flex-row justify-start items-start gap-3">
                  <span class="material-symbols-outlined text-[#83009a] !mt-1"> help </span>
                  <div class="text-top flex flex-col gap-1 justify-start items-start">
                    <p class="text-white text-base font-bold">{{ island.detail.title }}</p>
                    <p class="text-[#6d6d6d] text-xs">
                      {{ island.detail.subtitle }}
                    </p>
                  </div>
                </div>
                <div
                  v-for="(point, i) in island.detail.points"
                  :key="i"
                  class="flex flex-row gap-3 h-fit w-full justify-start items-center ps-8"
                >
                  <div class="h-1 w-1 rounded-full bg-[#83009a] mt-2"></div>

                  <div class="flex flex-col gap-1">
                    <p class="text-[#83009a] text-sm font-bold">
                      {{ point.title }}
                    </p>

                    <p class="text-[#6d6d6d] text-xs">
                      {{ point.desc }}
                    </p>
                  </div>
                </div>
              </div>
            </transition>
          </div>
        </div>

          <div
            v-if="activeIsland !== null"
            class="fixed inset-0 bg-black/70 z-40"
            @click="activeIsland = null"
          ></div>
        </div>
      </div>
    </div>
  </div>
  <Menu :isUserLoggedin="isUserLoggedin" />
  <modalWarning />
</template>
