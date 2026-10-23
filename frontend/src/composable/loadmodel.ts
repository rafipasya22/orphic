import { API_URL } from '@/config'
import { ref } from 'vue';

const modelLagiLoading = ref(true);
let intervalId: ReturnType<typeof setInterval> | null = null;

const isModelLoading = async () => {
  try {
    const res = await fetch(`${API_URL}/`);
    const data = await res.json();

    if (data.status === 'udah') {
      modelLagiLoading.value = false;

      if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
      }
    } else {
      modelLagiLoading.value = true;
    }
  } catch (err) {
    console.error(err);
  }
};

const startPolling = () => {
  if (intervalId) return;

  isModelLoading();

  intervalId = setInterval(() => {
    isModelLoading();
  }, 3000);
};

export function loadmodelfunc() {
  return {
    modelLagiLoading,
    startPolling
  };
}