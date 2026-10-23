import {ref} from 'vue';
let hoverTimeout: number | null = null;
const tooltipVisible = ref(false);

function hoverbtn() {
  hoverTimeout = setTimeout(() => {
    tooltipVisible.value = true;
  }, 2000);
}

function Gahoverbtn() {
  if (hoverTimeout) clearTimeout(hoverTimeout);
  tooltipVisible.value = false;
}

export function munculinTooltip() {
  return {
    tooltipVisible,
    hoverbtn,
    Gahoverbtn,
  };
}