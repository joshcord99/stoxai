<script setup lang="ts">
import { useUserStore } from '../userInfo.ts'
import ChatBot from '../components/ChatBot.vue'
import LiveDataCard from '../components/LiveDataCard.vue'
import MarketHeadlines from '../components/MarketHeadlines.vue'
import PortfolioCard from '../components/PortfolioCard.vue'
import HamburgerMenu from '../components/HamburgerMenu.vue'
import Toast from '../tools/Toast.vue'
import { onMounted } from 'vue'

const user = useUserStore()


</script>

<template>
  <div class="min-h-screen bg-gray-900">
    <div class="fixed top-0 left-0 right-0 z-20">
      <MarketHeadlines />
    </div>

    <div class="flex justify-between items-center p-6 pb-0 pt-2 mt-8">
      <div>
        <h1 class="font-bold text-white" style="font-size: 50px;">
          Welcome, {{ user.user?.first_name || 'Human' }}
        </h1>
      </div>
      
      <HamburgerMenu />
    </div>

    <div class="p-6">
      <div class="mb-6">
        <div class="bg-white p-6 rounded-lg shadow-md">
          <div class="text-center mb-4">
            <h3 class="text-xl font-semibold text-gray-800 mb-2">Live Market Data</h3>
            <p class="text-gray-600 text-sm">NASDAQ Composite Index</p>
          </div>
          <div class="bg-gray-50 rounded-lg p-4">
            <LiveDataCard />
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10rem;">
        <PortfolioCard />
        <div class="bg-white p-6 rounded-lg shadow-md">
          <ChatBot />
        </div>
      </div>
    </div>
    <Toast ref="toastRef" />
  </div>
</template>
