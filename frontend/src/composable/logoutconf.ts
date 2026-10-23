import { ref } from 'vue';

const islogoutconf = ref(false);

const openlogoutconf = () => (islogoutconf.value = true);
const closelogoutconf = () => (islogoutconf.value = false);

export function logoutconffunc() {
  return {
    openlogoutconf,
    closelogoutconf,
    islogoutconf,
  };
}