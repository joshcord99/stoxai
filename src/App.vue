<script setup lang="ts">
import { onMounted } from 'vue';
import { useUserStore } from './userInfo';
import Footer from './components/Footer.vue';

const userStore = useUserStore();

onMounted(() => {
  userStore.initializeAuth();
});
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <main class="flex-1">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
