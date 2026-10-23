import { ref} from 'vue';
import {openMenufunc} from './openmenu.ts';


const { isMenuOpen, closeMenu } = openMenufunc();

const isSettingsopen = ref(false);

const openSettings = () => {
  if (isMenuOpen.value) {
    closeMenu();
  }

  isSettingsopen.value = true;
};

const closeSettings = () => (isSettingsopen.value = false);

export function openSettingsFunc() {
  return {
    isSettingsopen,
    openSettings,
    closeSettings,
  };
}

