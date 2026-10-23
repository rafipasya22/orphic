import { ref } from 'vue';

const issignupconfopen = ref(false);

const opensignupconf = () => (issignupconfopen.value = true);
const closesignupconf = () => (issignupconfopen.value = false);

export function signupconffunc() {
  return {
    opensignupconf,
    closesignupconf,
    issignupconfopen,
  };
}