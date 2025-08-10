<script setup lang="ts">
import { useUserStore } from "../userInfo";
import ChatBot from "../components/ChatBot.vue";
import LiveDataCard from "../components/LiveDataCard.vue";
import MarketHeadlines from "../components/MarketHeadlines.vue";
import PortfolioCard from "../components/PortfolioCard.vue";
import HamburgerMenu from "../components/HamburgerMenu.vue";
import Toast from "../tools/Toast.vue";
const user = useUserStore();
</script>

<template>
  <div class="min-h-screen bg-gray-900">
    <div class="fixed top-0 left-0 right-0 z-20">
      <MarketHeadlines />
    </div>

    <div
      class="flex justify-between items-start sm:items-center p-4 sm:p-6 pb-0 pt-2 mt-8 gap-4"
    >
      <div class="flex-1 min-w-0">
        <h1
          class="font-bold text-white text-2xl sm:text-3xl md:text-4xl lg:text-5xl break-words"
        >
          Welcome, {{ user.user?.first_name || "Human" }}
        </h1>
      </div>

      <div class="flex-shrink-0">
        <HamburgerMenu />
      </div>
    </div>

    <div class="p-4 sm:p-6">
      <div class="mb-6">
        <div class="bg-white p-4 sm:p-6 rounded-lg shadow-md">
          <div class="text-center mb-4">
            <h3 class="text-lg sm:text-xl font-semibold text-gray-800 mb-2">
              Live Market Data
            </h3>
            <p class="text-gray-600 text-sm">NASDAQ Composite Index</p>
          </div>
          <div class="bg-gray-50 rounded-lg p-4">
            <LiveDataCard />
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <PortfolioCard />
        <div class="bg-white p-4 sm:p-6 rounded-lg shadow-md">
          <ChatBot />
        </div>
      </div>
    </div>
    <Toast ref="toastRef" />
  </div>
</template>
