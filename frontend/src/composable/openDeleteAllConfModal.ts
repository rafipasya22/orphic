import { ref } from 'vue';

const isConfdeletAllOpen = ref(false);

const openConfdeletAll = () => (isConfdeletAllOpen.value = true);
const closeConfdeletAll = () => (isConfdeletAllOpen.value = false);

export function deleteAllConfFunc() {
  return {
    openConfdeletAll,
    closeConfdeletAll,
    isConfdeletAllOpen,
  };
}