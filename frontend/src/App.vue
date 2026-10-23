<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import { onMounted } from 'vue';
import { useAuthStore } from './stores/authstore';
import { loadmodelfunc } from './composable/loadmodel';

const authStore = useAuthStore();
const { startPolling } = loadmodelfunc();

onMounted(async () => {
  startPolling();

  if (authStore.accessToken) {
    await authStore.fetchProfile();
  }

});
</script>

<template>
  <RouterView />
</template>
