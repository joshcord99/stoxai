<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { finnhubApi } from '../services/finnhubApi'

const news = ref<string[]>([])
const loading = ref(true)

const fetchNews = async () => {
  try {
    const headlines = await finnhubApi.getMarketNews()
    news.value = headlines
    loading.value = false
  } catch (err: any) {
    console.error('Error fetching news:', err)
    loading.value = true
  }
}

onMounted(async () => {
  await fetchNews()
})
</script>

<template>
  <div class="w-full bg-black overflow-hidden whitespace-nowrap border-t border-b border-gray-700">
    
    <div v-if="loading || news.length === 0" class="text-white text-sm py-2">
      <div class="animate-marquee-fast inline-block">
        <span
          v-for="i in 20"
          :key="i"
          class="mx-12 inline-block"
        >
          Current news unavailable at this time
        </span>
      </div>
    </div>
    <div v-else class="text-white text-sm py-2">
      <div class="animate-marquee inline-block">
        <span
          v-for="(headline, index) in news"
          :key="index"
          class="mx-12 inline-block"
        >
          {{ headline }}
        </span>

        <span
          v-for="(headline, index) in news"
          :key="'duplicate-' + index"
          class="mx-12 inline-block"
        >
          {{ headline }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes marquee {
  0% {
    transform: translateX(0%);
  }
  100% {
    transform: translateX(-100%);
  }
}

.animate-marquee {
  display: inline-block;
  white-space: nowrap;
  animation: marquee 360s linear infinite;
}

.animate-marquee-fast {
  display: inline-block;
  white-space: nowrap;
  animation: marquee 120s linear infinite;
}
</style> 