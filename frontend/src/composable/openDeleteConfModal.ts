import { ref } from 'vue';

const isConfdeletOpen = ref(false);

const openConfdelet = () => (isConfdeletOpen.value = true);
const closeConfdelet = () => (isConfdeletOpen.value = false);

export function deleteConfFunc() {
  return {
    openConfdelet,
    closeConfdelet,
    isConfdeletOpen,
  };
}