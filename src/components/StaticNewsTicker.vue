<script setup lang="ts">
import { ref } from 'vue'

interface NewsItem {
  id: number;
  text: string;
}

const news = ref<NewsItem[]>([
  { id: 1, text: "**SAMPLE DATA** Dow Jones Industrial Average rises 250 points on strong earnings reports" },
  { id: 2, text: "**SAMPLE DATA** Bitcoin reaches $45,000 as institutional adoption increases" },
  { id: 3, text: "**SAMPLE DATA** Federal Reserve signals potential interest rate cuts in 2024" },
  { id: 4, text: "**SAMPLE DATA** S&P 500 hits new record high amid tech sector rally" },
  { id: 5, text: "**SAMPLE DATA** Ethereum gains 5% as DeFi protocols see increased activity" },
  { id: 6, text: "**SAMPLE DATA** Apple reports record quarterly revenue, stock up 3%" },
  { id: 7, text: "**SAMPLE DATA** European markets rally on positive economic data" },
  { id: 8, text: "**SAMPLE DATA** Tesla stock surges 8% after strong delivery numbers" },
  { id: 9, text: "**SAMPLE DATA** Nasdaq Composite reaches all-time high led by tech stocks" },
  { id: 10, text: "**SAMPLE DATA** Dollar strengthens against major currencies in forex markets" },
  { id: 11, text: "**SAMPLE DATA** Treasury yields fall as investors seek safe haven assets" },
  { id: 12, text: "**SAMPLE DATA** NVIDIA reports strong AI chip demand, shares jump 12%" },
  { id: 13, text: "**SAMPLE DATA** Global markets react to central bank policy announcements" },
  { id: 14, text: "**SAMPLE DATA** Oil prices stabilize as OPEC+ maintains production cuts" },
  { id: 15, text: "**SAMPLE DATA** Goldman Sachs upgrades tech sector outlook for 2024" },
  { id: 16, text: "**SAMPLE DATA** SpaceX IPO rumors drive aerospace sector gains" },
  { id: 17, text: "**SAMPLE DATA** Retail investors flock to meme stocks amid market volatility" },
  { id: 18, text: "**SAMPLE DATA** JPMorgan Chase reports strong Q4 earnings, beats estimates" },
  { id: 19, text: "**SAMPLE DATA** Solana blockchain sees record transaction volume" },
  { id: 20, text: "**SAMPLE DATA** Market volatility index (VIX) drops to 6-month low" }
])
</script>

<template>
  <div class="w-full bg-black overflow-hidden whitespace-nowrap border-t border-b border-gray-700">
    <div class="text-white text-sm py-2">
      <div class="animate-marquee inline-block">
        <span
          v-for="(headline, index) in news"
          :key="index"
          class="mx-12 inline-block"
        >
          {{ headline.text }}
        </span>
  
        <span
          v-for="(headline, index) in news"
          :key="'duplicate-' + index"
          class="mx-12 inline-block"
        >
          {{ headline.text }}
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
</style> 