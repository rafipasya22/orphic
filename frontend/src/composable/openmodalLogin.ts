import { ref} from 'vue';
import {openMenufunc} from './openmenu.ts';


const { isMenuOpen, closeMenu } = openMenufunc();

const isOpen = ref(false);
let isLogin = ref(true);

const openModal = () => {
  if (isMenuOpen.value) {
    closeMenu();
  }

  isOpen.value = true;
};
const closeModal = () => (isOpen.value = false, isLogin.value = true);
const openLoginModal = () => (isLogin.value = true);
const openSignupModal = () => (isLogin.value = false);

export function openModalLogin() {
  return {
    isOpen,
    isLogin,
    openModal,
    closeModal,
    openLoginModal,
    openSignupModal
  };
}
