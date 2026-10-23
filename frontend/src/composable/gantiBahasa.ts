import { ref, watch } from 'vue';

const savedLang = localStorage.getItem('isLangEnglish');

const isLangEnglish = ref(
  savedLang !== null ? JSON.parse(savedLang) : true
);

const ganti = () => {
  isLangEnglish.value = !isLangEnglish.value;
};

watch(isLangEnglish, (newValue) => {
  localStorage.setItem('isLangEnglish', JSON.stringify(newValue));
});

export function gantiBahasaFunc() {
  return {
    ganti,
    isLangEnglish,
  };
}