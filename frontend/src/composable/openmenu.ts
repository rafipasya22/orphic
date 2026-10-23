import { ref} from 'vue';

const isMenuOpen = ref(false);

const openMenu = () => {
  isMenuOpen.value = true;
};

const closeMenu = () => {
  isMenuOpen.value = false;
};

export function openMenufunc() {
  return {
    isMenuOpen,
    openMenu,
    closeMenu,
  };
}
