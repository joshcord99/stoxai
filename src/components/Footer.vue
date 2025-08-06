<template>
  <footer class="bg-gray-900 text-white py-4">
    <div class="container mx-auto px-4">
      <div class="flex flex-col md:flex-row items-center">
        <div class="flex-1"></div>
        <div class="text-sm mb-2 md:mb-0">
          Made by 
          <a 
            href="https://github.com/joshcord99" 
            target="_blank" 
            rel="noopener noreferrer"
            class="text-blue-400 hover:text-blue-300 underline"
          >
            @github/joshcord99
          </a>
        </div>
        <div class="flex-1 flex justify-end items-center space-x-4 text-sm">
          <router-link 
            to="/market-lingo" 
            class="text-gray-300 hover:text-white transition-colors"
          >
            Market Lingo
          </router-link>
          <span class="text-gray-400">|</span>
          <router-link 
            to="/tickers" 
            class="text-gray-300 hover:text-white transition-colors"
          >
            Tickers
          </router-link>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
</script> 