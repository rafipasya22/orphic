import { ref } from 'vue';

let isDashActive = ref(false);
let isHistoryActive = ref(false);
let isHelpActive = ref(false);

export function activefunc() {
  return {
    isDashActive,
    isHistoryActive,
    isHelpActive,
  };
}