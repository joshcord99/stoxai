<script setup lang="ts">
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js'

import { ref, onMounted } from 'vue'
import StockLogo from '../tools/StockLogo.vue'
import { currencyLayerApi } from '../services/currencyLayerApi'
import { finnhubApi } from '../services/finnhubApi'
import { twelveDataApi } from '../services/twelveDataApi'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
)

const stockQuotes = ref<any[]>([])
const cryptoQuotes = ref<any[]>([])
const forexQuotes = ref<any[]>([])
const activeTab = ref('stocks')
const isRefreshing = ref(false)



const fetchData = async () => {
  try {
    isRefreshing.value = true

    if (!finnhubApi.hasApiKey()) {
      stockQuotes.value = finnhubApi.getDemoStockQuotes()
      cryptoQuotes.value = twelveDataApi.getDemoCryptoQuotes()
      forexQuotes.value = await currencyLayerApi.getLiveForexRates()
      isRefreshing.value = false
      return
    }

    const allStockSymbols = [
      'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'ADBE', 'CRM',
      'PYPL', 'INTC', 'AMD', 'ORCL', 'CSCO', 'IBM', 'QCOM', 'TXN', 'AVGO', 'MU',
      'AMAT', 'KLAC', 'LRCX', 'ADI', 'MCHP', 'ASML', 'TSM', 'JPM', 'BAC', 'WFC',
      'GS', 'MS', 'C', 'USB', 'PNC', 'TFC', 'COF', 'JNJ', 'PFE', 'UNH',
      'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'BMY', 'AMGN', 'XOM', 'CVX', 'COP',
      'EOG', 'SLB', 'PSX', 'VLO', 'MPC', 'HAL', 'BKR', 'DIS', 'NKE', 'HD',
      'LOW', 'COST', 'TGT', 'WMT', 'SBUX', 'MCD', 'KO', 'PEP', 'PG', 'JNJ'
    ]
    
    const stockSymbols = allStockSymbols
      .sort(() => Math.random() - 0.5)
      .slice(0, 15)

    const allCryptoSymbols = [
      'BTC', 'ETH', 'BNB', 'ADA', 'XRP', 'DOT', 'LINK', 'LTC', 'BCH', 'UNI',
      'ATOM', 'VET', 'TRX', 'ETC', 'ALGO', 'SOL', 'MATIC', 'AVAX', 'FTM', 'NEAR',
      'ICP', 'FIL', 'XTZ', 'THETA', 'CAKE', 'CHZ', 'HOT', 'DOGE', 'SHIB', 'MANA',
      'SAND', 'ENJ', 'AXS', 'GALA', 'XLM', 'EOS', 'XMR', 'DASH', 'ZEC', 'BAT',
      'NEO', 'QTUM', 'IOTA', 'OMG', 'ZRX', 'KNC', 'COMP', 'AAVE', 'SNX', 'CRV',
      'YFI', 'SUSHI', '1INCH', 'REN', 'BAND', 'OCEAN', 'ALPHA', 'ZEN', 'RSR', 'STORJ',
      'ANKR', 'COTI', 'CHR', 'DUSK', 'FET', 'GRT', 'HBAR', 'ICX', 'JASMY', 'KAVA',
      'LRC', 'MASK', 'NMR', 'OGN', 'PERP', 'QNT', 'RLC', 'SKL', 'TLM', 'UMA',
      'VGX', 'WOO', 'XEC', 'YGG', 'ZEN', 'ZIL', 'ZRX', 'AAVE', 'COMP', 'SNX'
    ]
    
    const cryptoSymbols = allCryptoSymbols
      .sort(() => Math.random() - 0.5)
      .slice(0, 15)


    const stockData = await finnhubApi.getMultipleStockQuotes(stockSymbols)
    
 
    const cryptoData = await twelveDataApi.getMultipleCryptoQuotes(cryptoSymbols)


    const forexData = await currencyLayerApi.getLiveForexRates()

    stockQuotes.value = stockData
    cryptoQuotes.value = cryptoData
    forexQuotes.value = forexData
    

    console.log('Stock data:', stockData.length, 'items')
    console.log('Crypto data:', cryptoData.length, 'items')
    console.log('Forex data:', forexData.length, 'items')
    
  } catch (err: any) {
    console.error('Error fetching data:', err)
  } finally {
    isRefreshing.value = false
  }
}

const handleRefresh = () => {
  fetchData()
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="w-full">

    
    <div class="flex justify-between items-center mb-4 gap-3">
      <div class="flex gap-1 overflow-x-auto">
        <button 
          @click="activeTab = 'stocks'"
          :class="activeTab === 'stocks' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'"
          class="px-2 sm:px-4 py-2 rounded-lg font-medium transition-colors text-xs sm:text-sm"
        >
          Stocks ({{ stockQuotes.length }})
        </button>
        <button 
          @click="activeTab = 'crypto'"
          :class="activeTab === 'crypto' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'"
          class="px-2 sm:px-4 py-2 rounded-lg font-medium transition-colors text-xs sm:text-sm"
        >
          Crypto ({{ cryptoQuotes.length }})
        </button>
        <button 
          @click="activeTab = 'forex'"
          :class="activeTab === 'forex' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'"
          class="px-2 sm:px-4 py-2 rounded-lg font-medium transition-colors text-xs sm:text-sm"
        >
          Forex ({{ forexQuotes.length }})
        </button>
      </div>
      
      <button 
        @click="handleRefresh"
        :disabled="isRefreshing"
        class="flex items-center space-x-2 px-2 sm:px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-xs sm:text-sm"
      >
        <svg 
          :class="{ 'animate-spin': isRefreshing }"
          class="hidden sm:block w-3 h-3 sm:w-4 sm:h-4" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <span class="hidden sm:inline">{{ isRefreshing ? 'Refreshing...' : 'Refresh' }}</span>
        <svg 
          v-if="isRefreshing"
          class="sm:hidden w-3 h-3 animate-spin" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <span v-else class="sm:hidden">↻</span>
      </button>
    </div>
    
    <div v-if="activeTab === 'stocks'" class="space-y-2 max-h-96 overflow-y-auto">
      <div 
        v-for="stock in stockQuotes" 
        :key="stock.symbol"
        class="bg-gray-800 rounded-lg p-3 border border-gray-700 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2"
      >
        <div class="flex items-center space-x-3">
          <StockLogo :ticker="stock.symbol" />
          <div class="text-white font-bold text-lg">{{ stock.symbol }}</div>
        </div>
        
        <div class="flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-4">
          <div class="flex items-center">
            <span 
              :class="stock.changePercent >= 0 ? 'text-green-400' : 'text-red-400'"
              class="text-sm font-medium"
            >
              {{ stock.changePercent >= 0 ? '↗' : '↘' }} {{ stock.changePercent.toFixed(2) }}%
            </span>
            <span 
              :class="stock.changePercent >= 0 ? 'text-green-400' : 'text-red-400'"
              class="text-sm ml-2"
            >
              ({{ stock.change >= 0 ? '+' : '' }}{{ stock.change.toFixed(2) }})
            </span>
          </div>
        
          <div class="flex items-center space-x-4">
            <div class="text-white font-bold text-lg">${{ stock.currentPrice.toFixed(2) }}</div>
            <div class="text-xs text-gray-400">
              H: ${{ stock.high.toFixed(2) }} | L: ${{ stock.low.toFixed(2) }}
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeTab === 'crypto'" class="space-y-2 max-h-96 overflow-y-auto">
      <div 
        v-for="crypto in cryptoQuotes" 
        :key="crypto.symbol"
        class="bg-gray-800 rounded-lg p-3 border border-gray-700 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2"
      >
        <div class="flex items-center space-x-3">
          <StockLogo :ticker="crypto.symbol" />
          <div class="text-white font-bold text-lg">{{ crypto.symbol }}</div>
        </div>
        
        <div class="flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-4">
          <div class="flex items-center">
            <span 
              :class="crypto.changePercent >= 0 ? 'text-green-400' : 'text-red-400'"
              class="text-sm font-medium"
            >
              {{ crypto.changePercent >= 0 ? '↗' : '↘' }} {{ crypto.changePercent.toFixed(2) }}%
            </span>
            <span 
              :class="crypto.changePercent >= 0 ? 'text-green-400' : 'text-red-400'"
              class="text-sm ml-2"
            >
              ({{ crypto.change >= 0 ? '+' : '' }}{{ crypto.change.toFixed(2) }})
            </span>
          </div>
        
          <div class="flex items-center space-x-4">
            <div class="text-white font-bold text-lg">${{ crypto.currentPrice.toFixed(2) }}</div>
            <div class="text-xs text-gray-400">
              H: ${{ crypto.high.toFixed(2) }} | L: ${{ crypto.low.toFixed(2) }}
            </div>
          </div>
        </div>
      </div>
    </div>


    <div v-if="activeTab === 'forex'" class="space-y-2 max-h-96 overflow-y-auto">
      <div 
        v-for="forex in forexQuotes" 
        :key="forex.symbol"
        class="bg-gray-800 rounded-lg p-3 border border-gray-700 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2"
      >
        <div class="flex items-center space-x-3">
          <StockLogo :ticker="forex.symbol" />
          <div class="text-white font-bold text-lg">{{ forex.symbol }}</div>
        </div>
        
        <div class="flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-4">
          <div class="flex items-center">
            <span 
              :class="forex.changePercent >= 0 ? 'text-green-400' : 'text-red-400'"
              class="text-sm font-medium"
            >
              {{ forex.changePercent >= 0 ? '↗' : '↘' }} {{ forex.changePercent.toFixed(2) }}%
            </span>
            <span 
              :class="forex.changePercent >= 0 ? 'text-green-400' : 'text-red-400'"
              class="text-sm ml-2"
            >
              ({{ forex.change >= 0 ? '+' : '' }}{{ forex.change.toFixed(2) }})
            </span>
          </div>
        
          <div class="flex items-center space-x-4">
            <div class="text-white font-bold text-lg">{{ forex.currentPrice.toFixed(4) }}</div>
            <div class="text-xs text-gray-400">
              H: {{ forex.high.toFixed(4) }} | L: {{ forex.low.toFixed(4) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template> 