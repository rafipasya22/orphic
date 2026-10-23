import { ref} from 'vue';
import {openMenufunc} from './openmenu.ts';


const { isMenuOpen, closeMenu } = openMenufunc();

const isHistoryOpen = ref(false);

const openHistory = () => {
  if (isMenuOpen.value) {
    closeMenu();
  }

  isHistoryOpen.value = true;
};

const closeHistory = () => (isHistoryOpen.value = false);

export function openHistoryModal() {
  return {
    isHistoryOpen,
    openHistory,
    closeHistory,
  };
}
