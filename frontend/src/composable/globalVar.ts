import { ref } from 'vue';

let predLoading = ref(false);
let isCollapsed = ref(false)

export function loadingFunc() {

  return {
    predLoading,
    isCollapsed
  };
}
