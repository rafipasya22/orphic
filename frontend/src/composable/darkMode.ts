import { ref, watch } from 'vue';

const storedDarkMode = localStorage.getItem('isDarkMode');

const isDarkMode = ref(
  storedDarkMode ? JSON.parse(storedDarkMode) : false
);

watch(isDarkMode, (newValue) => {
  localStorage.setItem('isDarkMode', JSON.stringify(newValue));
});

export function darkFunc() {
  return {
    isDarkMode,
  };
}