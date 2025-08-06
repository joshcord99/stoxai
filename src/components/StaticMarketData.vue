<script setup lang="ts">
import { ref } from 'vue'

const stockQuotes = ref([
  {
    symbol: 'AAPL',
    currentPrice: 202.38,
    change: -5.19,
    changePercent: -2.50,
    high: 213.58,
    low: 201.50,
    open: 210.87,
    previousClose: 207.57,
    type: 'stock'
  },
  {
    symbol: 'MSFT',
    currentPrice: 415.26,
    change: 8.45,
    changePercent: 2.08,
    high: 418.90,
    low: 408.20,
    open: 409.50,
    previousClose: 406.81,
    type: 'stock'
  },
  {
    symbol: 'GOOGL',
    currentPrice: 178.45,
    change: -2.15,
    changePercent: -1.19,
    high: 182.30,
    low: 177.80,
    open: 180.20,
    previousClose: 180.60,
    type: 'stock'
  },
  {
    symbol: 'AMZN',
    currentPrice: 185.90,
    change: 3.25,
    changePercent: 1.78,
    high: 187.50,
    low: 183.20,
    open: 184.30,
    previousClose: 182.65,
    type: 'stock'
  },
  {
    symbol: 'TSLA',
    currentPrice: 245.67,
    change: -12.33,
    changePercent: -4.78,
    high: 258.90,
    low: 242.10,
    open: 255.20,
    previousClose: 258.00,
    type: 'stock'
  },
  {
    symbol: 'META',
    currentPrice: 485.12,
    change: 15.88,
    changePercent: 3.38,
    high: 488.50,
    low: 472.30,
    open: 475.40,
    previousClose: 469.24,
    type: 'stock'
  },
  {
    symbol: 'NVDA',
    currentPrice: 875.45,
    change: 25.55,
    changePercent: 3.01,
    high: 880.20,
    low: 860.80,
    open: 865.30,
    previousClose: 849.90,
    type: 'stock'
  },
  {
    symbol: 'NFLX',
    currentPrice: 678.90,
    change: -8.10,
    changePercent: -1.18,
    high: 685.50,
    low: 675.20,
    open: 680.30,
    previousClose: 687.00,
    type: 'stock'
  },
  {
    symbol: 'ADBE',
    currentPrice: 567.23,
    change: 12.77,
    changePercent: 2.30,
    high: 570.80,
    low: 560.40,
    open: 562.50,
    previousClose: 554.46,
    type: 'stock'
  },
  {
    symbol: 'CRM',
    currentPrice: 298.45,
    change: -5.55,
    changePercent: -1.82,
    high: 305.20,
    low: 296.80,
    open: 300.30,
    previousClose: 304.00,
    type: 'stock'
  },
  {
    symbol: 'PYPL',
    currentPrice: 67.89,
    change: 1.23,
    changePercent: 1.85,
    high: 68.50,
    low: 66.80,
    open: 67.20,
    previousClose: 66.66,
    type: 'stock'
  },
  {
    symbol: 'INTC',
    currentPrice: 45.67,
    change: -0.33,
    changePercent: -0.72,
    high: 46.20,
    low: 45.40,
    open: 45.80,
    previousClose: 46.00,
    type: 'stock'
  },
  {
    symbol: 'AMD',
    currentPrice: 156.78,
    change: 4.22,
    changePercent: 2.77,
    high: 158.90,
    low: 154.20,
    open: 155.30,
    previousClose: 152.56,
    type: 'stock'
  },
  {
    symbol: 'ORCL',
    currentPrice: 134.56,
    change: 2.44,
    changePercent: 1.85,
    high: 135.80,
    low: 133.20,
    open: 133.80,
    previousClose: 132.12,
    type: 'stock'
  },
  {
    symbol: 'CSCO',
    currentPrice: 48.90,
    change: -0.10,
    changePercent: -0.20,
    high: 49.20,
    low: 48.60,
    open: 48.80,
    previousClose: 49.00,
    type: 'stock'
  }
])

const cryptoQuotes = ref([
  {
    symbol: 'BTCUSDT',
    currentPrice: 67890.45,
    change: 1234.55,
    changePercent: 1.86,
    high: 68200.00,
    low: 66500.00,
    open: 66655.90,
    previousClose: 66655.90,
    type: 'crypto'
  },
  {
    symbol: 'ETHUSDT',
    currentPrice: 3456.78,
    change: -45.22,
    changePercent: -1.29,
    high: 3520.00,
    low: 3440.00,
    open: 3502.00,
    previousClose: 3502.00,
    type: 'crypto'
  },
  {
    symbol: 'BNBUSDT',
    currentPrice: 567.89,
    change: 12.11,
    changePercent: 2.18,
    high: 570.00,
    low: 555.00,
    open: 555.78,
    previousClose: 555.78,
    type: 'crypto'
  },
  {
    symbol: 'ADAUSDT',
    currentPrice: 0.4567,
    change: 0.0123,
    changePercent: 2.77,
    high: 0.4600,
    low: 0.4450,
    open: 0.4444,
    previousClose: 0.4444,
    type: 'crypto'
  },
  {
    symbol: 'XRPUSDT',
    currentPrice: 0.5678,
    change: -0.0089,
    changePercent: -1.54,
    high: 0.5750,
    low: 0.5650,
    open: 0.5767,
    previousClose: 0.5767,
    type: 'crypto'
  },
  {
    symbol: 'DOTUSDT',
    currentPrice: 7.234,
    change: 0.156,
    changePercent: 2.21,
    high: 7.280,
    low: 7.100,
    open: 7.078,
    previousClose: 7.078,
    type: 'crypto'
  },
  {
    symbol: 'LINKUSDT',
    currentPrice: 15.678,
    change: 0.322,
    changePercent: 2.10,
    high: 15.800,
    low: 15.400,
    open: 15.356,
    previousClose: 15.356,
    type: 'crypto'
  },
  {
    symbol: 'LTCUSDT',
    currentPrice: 89.45,
    change: -1.55,
    changePercent: -1.70,
    high: 91.20,
    low: 89.00,
    open: 91.00,
    previousClose: 91.00,
    type: 'crypto'
  },
  {
    symbol: 'BCHUSDT',
    currentPrice: 234.56,
    change: 8.44,
    changePercent: 3.73,
    high: 236.00,
    low: 228.00,
    open: 226.12,
    previousClose: 226.12,
    type: 'crypto'
  },
  {
    symbol: 'UNIUSDT',
    currentPrice: 8.901,
    change: 0.199,
    changePercent: 2.29,
    high: 8.950,
    low: 8.750,
    open: 8.702,
    previousClose: 8.702,
    type: 'crypto'
  },
  {
    symbol: 'ATOMUSDT',
    currentPrice: 12.345,
    change: -0.155,
    changePercent: -1.24,
    high: 12.500,
    low: 12.300,
    open: 12.500,
    previousClose: 12.500,
    type: 'crypto'
  },
  {
    symbol: 'VETUSDT',
    currentPrice: 0.0234,
    change: 0.0006,
    changePercent: 2.63,
    high: 0.0236,
    low: 0.0228,
    open: 0.0228,
    previousClose: 0.0228,
    type: 'crypto'
  },
  {
    symbol: 'TRXUSDT',
    currentPrice: 0.0789,
    change: 0.0011,
    changePercent: 1.41,
    high: 0.0795,
    low: 0.0780,
    open: 0.0778,
    previousClose: 0.0778,
    type: 'crypto'
  },
  {
    symbol: 'ETCUSDT',
    currentPrice: 34.567,
    change: -0.433,
    changePercent: -1.24,
    high: 35.000,
    low: 34.500,
    open: 35.000,
    previousClose: 35.000,
    type: 'crypto'
  },
  {
    symbol: 'ALGOUSDT',
    currentPrice: 0.1234,
    change: 0.0026,
    changePercent: 2.15,
    high: 0.1240,
    low: 0.1210,
    open: 0.1208,
    previousClose: 0.1208,
    type: 'crypto'
  }
])

const forexQuotes = ref([
  {
    symbol: 'USD/EUR',
    currentPrice: 0.9234,
    change: 0.0023,
    changePercent: 0.25,
    high: 0.9250,
    low: 0.9220,
    open: 0.9211,
    previousClose: 0.9211,
    type: 'forex'
  },
  {
    symbol: 'USD/GBP',
    currentPrice: 0.7890,
    change: -0.0045,
    changePercent: -0.57,
    high: 0.7920,
    low: 0.7880,
    open: 0.7935,
    previousClose: 0.7935,
    type: 'forex'
  },
  {
    symbol: 'USD/JPY',
    currentPrice: 148.56,
    change: 0.78,
    changePercent: 0.53,
    high: 148.80,
    low: 147.90,
    open: 147.78,
    previousClose: 147.78,
    type: 'forex'
  },
  {
    symbol: 'USD/CHF',
    currentPrice: 0.8765,
    change: -0.0034,
    changePercent: -0.39,
    high: 0.8780,
    low: 0.8750,
    open: 0.8799,
    previousClose: 0.8799,
    type: 'forex'
  },
  {
    symbol: 'USD/AUD',
    currentPrice: 1.5234,
    change: 0.0089,
    changePercent: 0.59,
    high: 1.5250,
    low: 1.5200,
    open: 1.5145,
    previousClose: 1.5145,
    type: 'forex'
  },
  {
    symbol: 'USD/CAD',
    currentPrice: 1.3456,
    change: -0.0123,
    changePercent: -0.91,
    high: 1.3480,
    low: 1.3440,
    open: 1.3579,
    previousClose: 1.3579,
    type: 'forex'
  },
  {
    symbol: 'USD/NZD',
    currentPrice: 1.6789,
    change: 0.0156,
    changePercent: 0.94,
    high: 1.6800,
    low: 1.6750,
    open: 1.6633,
    previousClose: 1.6633,
    type: 'forex'
  },
  {
    symbol: 'USD/CNY',
    currentPrice: 7.2345,
    change: 0.0234,
    changePercent: 0.32,
    high: 7.2400,
    low: 7.2300,
    open: 7.2111,
    previousClose: 7.2111,
    type: 'forex'
  },
  {
    symbol: 'USD/HKD',
    currentPrice: 7.8234,
    change: -0.0123,
    changePercent: -0.16,
    high: 7.8250,
    low: 7.8200,
    open: 7.8357,
    previousClose: 7.8357,
    type: 'forex'
  },
  {
    symbol: 'USD/SGD',
    currentPrice: 1.3456,
    change: 0.0056,
    changePercent: 0.42,
    high: 1.3470,
    low: 1.3440,
    open: 1.3400,
    previousClose: 1.3400,
    type: 'forex'
  },
  {
    symbol: 'USD/SEK',
    currentPrice: 10.5678,
    change: -0.1234,
    changePercent: -1.15,
    high: 10.5800,
    low: 10.5600,
    open: 10.6912,
    previousClose: 10.6912,
    type: 'forex'
  },
  {
    symbol: 'USD/NOK',
    currentPrice: 10.2345,
    change: -0.1456,
    changePercent: -1.40,
    high: 10.2500,
    low: 10.2200,
    open: 10.3801,
    previousClose: 10.3801,
    type: 'forex'
  },
  {
    symbol: 'USD/DKK',
    currentPrice: 6.8901,
    change: -0.0456,
    changePercent: -0.66,
    high: 6.8950,
    low: 6.8850,
    open: 6.9357,
    previousClose: 6.9357,
    type: 'forex'
  },
  {
    symbol: 'USD/PLN',
    currentPrice: 3.9876,
    change: 0.0234,
    changePercent: 0.59,
    high: 3.9900,
    low: 3.9850,
    open: 3.9642,
    previousClose: 3.9642,
    type: 'forex'
  },
  {
    symbol: 'USD/CZK',
    currentPrice: 23.4567,
    change: -0.2345,
    changePercent: -0.99,
    high: 23.4800,
    low: 23.4400,
    open: 23.6912,
    previousClose: 23.6912,
    type: 'forex'
  }
])

const activeTab = ref('stocks') 
</script>

<template>
  <div class="w-full">

    <div class="flex justify-between items-center mb-4">

      <div class="flex space-x-1">
        <button 
          @click="activeTab = 'stocks'"
          :class="activeTab === 'stocks' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'"
          class="px-4 py-2 rounded-lg font-medium transition-colors"
        >
          Stocks ({{ stockQuotes.length }})
        </button>
        <button 
          @click="activeTab = 'crypto'"
          :class="activeTab === 'crypto' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'"
          class="px-4 py-2 rounded-lg font-medium transition-colors"
        >
          Crypto ({{ cryptoQuotes.length }})
        </button>
        <button 
          @click="activeTab = 'forex'"
          :class="activeTab === 'forex' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'"
          class="px-4 py-2 rounded-lg font-medium transition-colors"
        >
          Forex ({{ forexQuotes.length }})
        </button>
      </div>
    </div>
    
 
    <div v-if="activeTab === 'stocks'" class="space-y-2 max-h-96 overflow-y-auto">
      <div 
        v-for="stock in stockQuotes" 
        :key="stock.symbol"
        class="bg-gray-800 rounded-lg p-3 border border-gray-700 flex justify-between items-center"
      >

        <div class="flex items-center space-x-4">
          <div class="text-white font-bold text-lg">{{ stock.symbol }}</div>
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
        </div>
        

        <div class="flex items-center space-x-4">
          <div class="text-white font-bold text-lg">${{ stock.currentPrice.toFixed(2) }}</div>
          <div class="text-xs text-gray-400">
            H: ${{ stock.high.toFixed(2) }} | L: ${{ stock.low.toFixed(2) }}
          </div>
        </div>
      </div>
    </div>


    <div v-if="activeTab === 'crypto'" class="space-y-2 max-h-96 overflow-y-auto">
      <div 
        v-for="crypto in cryptoQuotes" 
        :key="crypto.symbol"
        class="bg-gray-800 rounded-lg p-3 border border-gray-700 flex justify-between items-center"
      >

        <div class="flex items-center space-x-4">
          <div class="text-white font-bold text-lg">{{ crypto.symbol }}</div>
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
        </div>

        <div class="flex items-center space-x-4">
          <div class="text-white font-bold text-lg">${{ crypto.currentPrice.toFixed(2) }}</div>
          <div class="text-xs text-gray-400">
            H: ${{ crypto.high.toFixed(2) }} | L: ${{ crypto.low.toFixed(2) }}
          </div>
        </div>
      </div>
    </div>


    <div v-if="activeTab === 'forex'" class="space-y-2 max-h-96 overflow-y-auto">
      <div 
        v-for="forex in forexQuotes" 
        :key="forex.symbol"
        class="bg-gray-800 rounded-lg p-3 border border-gray-700 flex justify-between items-center"
      >
    
        <div class="flex items-center space-x-4">
          <div class="text-white font-bold text-lg">{{ forex.symbol }}</div>
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
</template> 