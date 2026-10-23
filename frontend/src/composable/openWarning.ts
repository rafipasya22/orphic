import { ref } from 'vue';

const isWarningOpen = ref(false);

const openWarning = () => {
  isWarningOpen.value = true;
};
const closeWarning = () => (isWarningOpen.value = false);

export function openWarningFunc() {
  return {
    isWarningOpen,
    openWarning,
    closeWarning,
  };
}
