<script setup lang="ts">
import { useUserStore } from '../userInfo.ts'
import StockLogo from '../tools/StockLogo.vue'
import Toast from '../tools/Toast.vue'
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { currencyLayerApi } from '../services/currencyLayerApi'

const user = useUserStore()
const toastRef = ref()

const activePortfolioTab = ref('all')
const searchQuery = ref('')
const showDropdown = ref(false)
const stocksWithValidData = ref<Set<string>>(new Set())
const failedTickers = ref<Set<string>>(new Set())

const stockData = ref<Map<string, any>>(new Map())
const loadingStates = ref<Map<string, boolean>>(new Map())
const errorStates = ref<Map<string, string | null>>(new Map())
const getTwelveDataApiKey = (): string | undefined => {
  if (typeof window !== 'undefined') {
    return (import.meta as any).env.VITE_TWELVE_DATA_API_KEY;
  }
  return undefined;
};

const hasApiKey = computed(() => {
  const API_KEY = getTwelveDataApiKey();
  return API_KEY && API_KEY !== 'your_twelve_data_api_key_here' && API_KEY !== 'unknown' && API_KEY !== 'undefined' && API_KEY !== '';
});

const filteredPortfolio = computed(() => {
  const allStocks = user.watchlist
  
  if (activePortfolioTab.value === 'all') {
    return allStocks
  }
  
  return allStocks.filter((ticker: string) => {
    const upperTicker = ticker.toUpperCase()
    
    if (activePortfolioTab.value === 'stocks') {
      return !upperTicker.includes('USDT') && 
             !upperTicker.includes('BTC') && 
             !upperTicker.includes('ETH') &&
             !upperTicker.includes('/') &&
             !upperTicker.includes('USD')
    } else if (activePortfolioTab.value === 'crypto') {
      return upperTicker.includes('USDT') || 
             upperTicker.includes('BTC') || 
             upperTicker.includes('ETH') ||
             upperTicker.includes('ADA') ||
             upperTicker.includes('DOT') ||
             upperTicker.includes('LINK') ||
             upperTicker.includes('LTC') ||
             upperTicker.includes('BCH') ||
             upperTicker.includes('UNI') ||
             upperTicker.includes('ATOM') ||
             upperTicker.includes('VET') ||
             upperTicker.includes('TRX') ||
             upperTicker.includes('ETC') ||
             upperTicker.includes('ALGO')
    } else if (activePortfolioTab.value === 'forex') {
      return upperTicker.includes('/') || 
             upperTicker.includes('USD') ||
             upperTicker.includes('EUR') ||
             upperTicker.includes('GBP') ||
             upperTicker.includes('JPY') ||
             upperTicker.includes('CHF') ||
             upperTicker.includes('AUD') ||
             upperTicker.includes('CAD') ||
             upperTicker.includes('NZD')
    }
    
    return false
  })
})


const stocksCount = computed(() => {
  const stockTickers = user.watchlist.filter((ticker: string) => {
    const upperTicker = ticker.toUpperCase()
    return !upperTicker.includes('USDT') && 
           !upperTicker.includes('BTC') && 
           !upperTicker.includes('ETH') &&
           !upperTicker.includes('/') &&
           !upperTicker.includes('USD')
  })
  return stockTickers.filter((ticker: string) => 
    stocksWithValidData.value.has(ticker.toUpperCase())
  ).length
})

const cryptoCount = computed(() => {
  const cryptoTickers = user.watchlist.filter((ticker: string) => {
    const upperTicker = ticker.toUpperCase()
    return upperTicker.includes('USDT') || 
           upperTicker.includes('BTC') || 
           upperTicker.includes('ETH') ||
           upperTicker.includes('ADA') ||
           upperTicker.includes('DOT') ||
           upperTicker.includes('LINK') ||
           upperTicker.includes('LTC') ||
           upperTicker.includes('BCH') ||
           upperTicker.includes('UNI') ||
           upperTicker.includes('ATOM') ||
           upperTicker.includes('VET') ||
           upperTicker.includes('TRX') ||
           upperTicker.includes('ETC') ||
           upperTicker.includes('ALGO')
  })
  return cryptoTickers.filter((ticker: string) => 
    stocksWithValidData.value.has(ticker.toUpperCase())
  ).length
})

const forexCount = computed(() => {
  const forexTickers = user.watchlist.filter((ticker: string) => {
    const upperTicker = ticker.toUpperCase()
    return upperTicker.includes('/') || 
           upperTicker.includes('USD') ||
           upperTicker.includes('EUR') ||
           upperTicker.includes('GBP') ||
           upperTicker.includes('JPY') ||
           upperTicker.includes('CHF') ||
           upperTicker.includes('AUD') ||
           upperTicker.includes('CAD') ||
           upperTicker.includes('NZD')
  })
  return forexTickers.filter((ticker: string) => 
    stocksWithValidData.value.has(ticker.toUpperCase())
  ).length
})


const fetchStockData = async (ticker: string) => {
  try {
    loadingStates.value.set(ticker, true)
    errorStates.value.set(ticker, null)
    
    if (user.isStockDataCached(ticker)) {
      const cachedData = user.getCachedStockData(ticker)
      stockData.value.set(ticker, cachedData)
      updateStockDataStatus(ticker, true)
      loadingStates.value.set(ticker, false)
      return
    }
    
    if (!hasApiKey) {

      const upperTicker = ticker.toUpperCase()
      const isForex = upperTicker.includes('/') || upperTicker.includes('USD') || upperTicker.includes('EUR') ||
                     upperTicker.includes('GBP') || upperTicker.includes('JPY') || upperTicker.includes('CHF') ||
                     upperTicker.includes('AUD') || upperTicker.includes('CAD') || upperTicker.includes('NZD')
      
      const demoData = {
        currentPrice: isForex ? 1.25 + Math.random() * 0.1 : 150.25 + Math.random() * 50,
        open: isForex ? 1.24 : 150.00,
        high: isForex ? 1.26 : 155.00,
        low: isForex ? 1.23 : 148.00,
        volume: isForex ? 0 : 1000000,
        previousClose: isForex ? 1.24 : 149.50,
        change: isForex ? (Math.random() - 0.5) * 0.01 : Math.random() * 10 - 5,
        changePercent: isForex ? (Math.random() - 0.5) * 2 : Math.random() * 6 - 3,
        marketType: ticker.includes('USDT') || ticker.includes('BTC') || ticker.includes('ETH') ? 'CRYPTO' : 
                   isForex ? 'FX' : 'CS',
        tickerName: ticker
      }
      
      user.setCachedStockData(ticker, demoData)
      stockData.value.set(ticker, demoData)
      updateStockDataStatus(ticker, true)
      loadingStates.value.set(ticker, false)
      return
    }
    

    const upperTicker = ticker.toUpperCase()
    if (upperTicker.includes('/') || upperTicker.includes('USD') || upperTicker.includes('EUR') ||
        upperTicker.includes('GBP') || upperTicker.includes('JPY') || upperTicker.includes('CHF') ||
        upperTicker.includes('AUD') || upperTicker.includes('CAD') || upperTicker.includes('NZD')) {
      

      const forexData = await currencyLayerApi.getLiveForexRates()
      const forexSymbol = upperTicker.includes('/') ? upperTicker : `USD/${upperTicker.replace('USD', '')}`
      const forexItem = forexData.find(forex => forex.symbol === forexSymbol)
      
      if (forexItem) {
        const processedData = {
          currentPrice: forexItem.currentPrice,
          open: forexItem.open,
          high: forexItem.high,
          low: forexItem.low,
          volume: 0,
          previousClose: forexItem.previousClose,
          change: forexItem.change,
          changePercent: forexItem.changePercent,
          marketType: 'FX',
          tickerName: forexItem.symbol
        }
        
        user.setCachedStockData(ticker, processedData)
        stockData.value.set(ticker, processedData)
        updateStockDataStatus(ticker, true)
      } else {
        throw new Error('Forex data not found')
      }
    } else {

      const API_KEY = getTwelveDataApiKey()
      const res = await axios.get(`https://api.twelvedata.com/quote`, {
        params: {
          symbol: ticker,
          apikey: API_KEY
        }
      })
      
      if (res.data && res.data.symbol && res.data.close && res.data.previous_close) {
        const data = res.data
        
        const currentPrice = parseFloat(data.close)
        const previousClose = parseFloat(data.previous_close)
        const change = parseFloat(data.change)
        const changePercent = parseFloat(data.percent_change)
        
        let marketType = 'CS'
        if (ticker.includes('USDT') || ticker.includes('BTC') || ticker.includes('ETH')) {
          marketType = 'CRYPTO'
        } else if (ticker.includes('/') || ticker.includes('USD')) {
          marketType = 'FX'
        }
        
        const processedData = {
          currentPrice: currentPrice,
          open: parseFloat(data.open),
          high: parseFloat(data.high),
          low: parseFloat(data.low),
          volume: parseInt(data.volume),
          previousClose: previousClose,
          change: change,
          changePercent: changePercent,
          marketType: marketType,
          tickerName: data.name || ticker
        }
        
        user.setCachedStockData(ticker, processedData)
        stockData.value.set(ticker, processedData)
        updateStockDataStatus(ticker, true)
      } else {
        throw new Error('No data available')
      }
    }
  } catch (err: any) {
    let errorMsg = 'Failed to load data'
    if (err.response?.status === 404) {
      errorMsg = `Symbol "${ticker}" not found`
    } else if (err.response?.status === 429) {
      errorMsg = 'Rate limit exceeded'
    } else if (err.response?.status === 401) {
      errorMsg = 'API key invalid'
    } else {
      errorMsg = `Failed to load data for ${ticker}`
    }
    
    errorStates.value.set(ticker, errorMsg)
    updateStockDataStatus(ticker, false)
  } finally {
    loadingStates.value.set(ticker, false)
  }
}

const updateStockDataStatus = (ticker: string, hasValidData: boolean) => {
  if (hasValidData) {
    stocksWithValidData.value.add(ticker.toUpperCase())
  } else {
    stocksWithValidData.value.delete(ticker.toUpperCase())
  }
}

const searchStocks = async (query: string) => {
  if (!query.trim()) return []
  
  try {
    const API_KEY = getTwelveDataApiKey()
    const res = await axios.get(`https://api.twelvedata.com/symbol_search`, {
      params: {
        symbol: query,
        apikey: API_KEY
      }
    })
    
    if (res.data && res.data.data) {
      const results = res.data.data.slice(0, 10).map((item: any) => ({
        symbol: item.symbol,
        name: item.instrument_name,
        type: item.type
      }))
      
     
      return results.filter((item: any) => !failedTickers.value.has(item.symbol.toUpperCase()))
    }
    return []
  } catch (error) {
    return []
  }
}

const selectStock = async (stock: any) => {
  try {
   
    if (user.watchlist.includes(stock.symbol)) {
      if (toastRef.value) {
        toastRef.value.addToast(`${stock.symbol} is already in your portfolio`, 'warning')
      }
      searchQuery.value = ''
      showDropdown.value = false
      return
    }

  
    const hasData = await checkStockData(stock.symbol)
    
    if (!hasData) {
      if (toastRef.value) {
        toastRef.value.addToast(`Sorry, no data available for ${stock.symbol}`, 'error')
      }
     
      console.warn(`No data available for ticker: ${stock.symbol}`)
      searchQuery.value = ''
      showDropdown.value = false
      return
    }

    await user.addStock(stock.symbol)
    await user.loadWatchlist()
    
    
    await fetchStockData(stock.symbol)
    
 
    if (toastRef.value) {
      toastRef.value.addToast(`${stock.symbol} added successfully!`, 'success')
    }
    
    searchQuery.value = ''
    showDropdown.value = false
  } catch (error) {
    if (toastRef.value) {
      toastRef.value.addToast('Failed to add stock', 'error')
    }
  }
}

const checkStockData = async (ticker: string) => {
  try {
    const upperTicker = ticker.toUpperCase()
    
  
    if (upperTicker.includes('/') || upperTicker.includes('USD') || upperTicker.includes('EUR') ||
        upperTicker.includes('GBP') || upperTicker.includes('JPY') || upperTicker.includes('CHF') ||
        upperTicker.includes('AUD') || upperTicker.includes('CAD') || upperTicker.includes('NZD')) {
      
     
      const forexData = await currencyLayerApi.getLiveForexRates()
      const forexSymbol = upperTicker.includes('/') ? upperTicker : `USD/${upperTicker.replace('USD', '')}`
      
      const hasData = forexData.some(forex => forex.symbol === forexSymbol)
      
      if (!hasData) {
       
        console.warn(`Forex data not available for: ${ticker}`)
      }
      
      return hasData
    } else {
     
      const API_KEY = getTwelveDataApiKey()
      const res = await axios.get(`https://api.twelvedata.com/quote`, {
        params: {
          symbol: ticker,
          apikey: API_KEY
        }
      })
      
      const hasData = res.data && res.data.symbol && res.data.close && res.data.previous_close
      
      if (!hasData) {
       
        console.warn(`Stock/Crypto data not available for: ${ticker}`)
      }
      
      return hasData
    }
  } catch (err: any) {
   
    console.warn(`Error checking data for ${ticker}:`, err.message || err)
    return false
  }
}

const removeStock = async (ticker: string) => {
  try {
    await user.removeStock(ticker)
    stocksWithValidData.value.delete(ticker.toUpperCase())
    stockData.value.delete(ticker)
    await user.loadWatchlist()
  } catch (error) {
    if (toastRef.value) {
      toastRef.value.addToast('Failed to remove stock', 'error')
    }
  }
}

const isRefreshing = ref(false)

const handleRefresh = async () => {
  try {
    isRefreshing.value = true
    user.clearAllCache()
    stocksWithValidData.value.clear()
    stockData.value.clear()
    await user.loadWatchlist()
    

    for (const ticker of user.watchlist) {
      await fetchStockData(ticker)
    }
  } catch (error) {
    if (toastRef.value) {
      toastRef.value.addToast('Failed to refresh watchlist', 'error')
    }
  } finally {
    isRefreshing.value = false
  }
}

const searchResults = ref<any[]>([])
const isSearching = ref(false)

const handleSearch = async () => {
  if (!searchQuery.value.trim()) {
    searchResults.value = []
    showDropdown.value = false
    return
  }
  
  isSearching.value = true
  try {
    const results = await searchStocks(searchQuery.value)
    searchResults.value = results
    showDropdown.value = results.length > 0
  } catch (error) {
    searchResults.value = []
    showDropdown.value = false
  } finally {
    isSearching.value = false
  }
}

const closeDropdown = () => {
  setTimeout(() => {
    showDropdown.value = false
  }, 200)
}



onMounted(async () => {
  try {
    if (user.isAuthenticated) {
      await user.loadWatchlist()
      
   
      for (const ticker of user.watchlist) {
  
        if (failedTickers.value.has(ticker.toUpperCase())) {
          console.log(`Skipping known failed ticker: ${ticker}`)
          continue
        }
        
        await fetchStockData(ticker)
      }
      
     
      if (failedTickers.value.size > 0) {
        console.log('Failed tickers that were automatically removed:', Array.from(failedTickers.value))
      }
    }
  } catch (error) {
    console.error('Failed to load watchlist:', error)
  }
})
</script>

<template>
  <div class="bg-white p-4 sm:p-6 rounded-lg shadow-md">
    <div class="flex justify-between items-center mb-4 gap-4">
      <h2 class="text-lg sm:text-xl font-semibold text-center sm:text-left flex-1 break-words">{{ user.displayName || user.fullName || 'Human' }}'s Portfolio</h2>
      <button 
        @click="handleRefresh"
        :disabled="isRefreshing"
        class="flex items-center space-x-2 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm sm:text-base"
      >
        <svg 
          :class="{ 'animate-spin': isRefreshing }"
          class="hidden sm:block w-4 h-4" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <span class="hidden sm:inline">{{ isRefreshing ? 'Refreshing...' : 'Refresh' }}</span>
        <span class="sm:hidden">{{ isRefreshing ? '...' : '↻' }}</span>
      </button>
    </div>
    

    <div class="mb-6 relative">
      <div class="flex space-x-2">
        <div class="flex-1 relative">
          <input
            v-model="searchQuery"
            @input="handleSearch"
            @focus="showDropdown = true"
            @blur="closeDropdown"
            type="text"
            placeholder="Search and click to add stocks, crypto, or forex to your portfolio..."
            class="w-full px-3 sm:px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base"
          />
          
       
          <div
            v-if="showDropdown && searchResults.length > 0"
            class="absolute top-full left-0 right-0 bg-white border border-gray-300 rounded-lg shadow-lg z-50 max-h-60 overflow-y-auto"
          >
            <div
              v-for="result in searchResults"
              :key="result.symbol"
              @click="selectStock(result)"
              class="px-3 sm:px-4 py-2 hover:bg-gray-100 cursor-pointer border-b border-gray-200 last:border-b-0"
            >
              <div class="font-medium text-sm sm:text-base">{{ result.symbol }}</div>
              <div class="text-xs sm:text-sm text-gray-600 truncate">{{ result.name }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    

    <div class="flex flex-wrap gap-1 mb-4">
      <button 
        @click="activePortfolioTab = 'all'"
        :class="activePortfolioTab === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'"
        class="px-2 sm:px-4 py-2 rounded-lg font-medium transition-colors text-xs sm:text-sm"
      >
        All ({{ user.watchlist.length }})
      </button>
      <button 
        @click="activePortfolioTab = 'stocks'"
        :class="activePortfolioTab === 'stocks' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'"
        class="px-2 sm:px-4 py-2 rounded-lg font-medium transition-colors text-xs sm:text-sm"
      >
        Stocks ({{ stocksCount }})
      </button>
      <button 
        @click="activePortfolioTab = 'crypto'"
        :class="activePortfolioTab === 'crypto' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'"
        class="px-2 sm:px-4 py-2 rounded-lg font-medium transition-colors text-xs sm:text-sm"
      >
        Crypto ({{ cryptoCount }})
      </button>
      <button 
        @click="activePortfolioTab = 'forex'"
        :class="activePortfolioTab === 'forex' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'"
        class="px-2 sm:px-4 py-2 rounded-lg font-medium transition-colors text-xs sm:text-sm"
      >
        Forex ({{ forexCount }})
      </button>
    </div>
    
 
    <div class="space-y-4">
      <div v-if="filteredPortfolio.length === 0" class="text-center py-8 text-gray-500">
        <p class="text-sm sm:text-base">No assets in your portfolio yet.</p>
        <p class="text-xs sm:text-sm mt-2">Use the search bar above to add stocks, crypto, or forex.</p>
      </div>
      
      <div v-else class="space-y-4">
        <div
          v-for="ticker in filteredPortfolio"
          :key="ticker"
          class="relative"
        >
        
          <div v-if="loadingStates.get(ticker)" class="bg-gray-100 rounded-lg p-4">
            <div class="text-gray-500 text-sm">Loading {{ ticker }}...</div>
          </div>
          

          
   
          <div v-else-if="stockData.get(ticker)" class="bg-[#282c34] rounded-lg p-3 sm:p-4">
            <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3">
              <div class="flex items-center space-x-2 sm:space-x-4 min-w-0">
                <div class="flex items-center space-x-2 sm:space-x-3 min-w-0">
                  <StockLogo :ticker="ticker" />
                  <div class="text-white font-bold text-base sm:text-lg truncate">{{ ticker }}</div>
                </div>
                <div class="flex items-center space-x-1 sm:space-x-2">
                  <span 
                    :class="stockData.get(ticker).changePercent >= 0 ? 'text-green-400' : 'text-[#f08080]'"
                    class="text-xs sm:text-sm font-medium"
                  >
                    {{ stockData.get(ticker).changePercent >= 0 ? '↗' : '↘' }} {{ stockData.get(ticker).changePercent.toFixed(2) }}%
                  </span>
                  <span 
                    :class="stockData.get(ticker).changePercent >= 0 ? 'text-green-400' : 'text-[#f08080]'"
                    class="text-xs sm:text-sm"
                  >
                    ({{ stockData.get(ticker).change >= 0 ? '+' : '' }}{{ stockData.get(ticker).change.toFixed(2) }})
                  </span>
                </div>
              </div>
              
              <div class="flex flex-col sm:flex-row sm:items-center space-y-2 sm:space-y-0 sm:space-x-4">
                <div class="text-white font-bold text-base sm:text-lg">${{ stockData.get(ticker).currentPrice.toFixed(2) }}</div>
                <div class="text-xs text-gray-400 hidden sm:block">
                  H: ${{ stockData.get(ticker).high.toFixed(2) }} | L: ${{ stockData.get(ticker).low.toFixed(2) }}
                </div>
                <button
                  @click="removeStock(ticker)"
                  class="text-red-600 hover:underline text-xs sm:text-sm self-start sm:self-auto"
                >
                  Remove
                </button>
              </div>
            </div>
          </div>
          
          <div v-else class="bg-gray-100 rounded-lg p-3 sm:p-4">
            <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3">
              <div class="flex items-center space-x-2 sm:space-x-4 min-w-0">
                <div class="flex items-center space-x-2 sm:space-x-3 min-w-0">
                  <StockLogo :ticker="ticker" />
                  <div class="text-gray-700 font-bold text-base sm:text-lg truncate">{{ ticker }}</div>
                </div>
                <div class="text-gray-500 text-xs sm:text-sm">
                  No data available
                </div>
              </div>
              
              <div class="flex flex-col sm:flex-row sm:items-center space-y-2 sm:space-y-0 sm:space-x-4">
                <div class="text-gray-500 text-xs sm:text-sm">No price data</div>
                <button
                  @click="removeStock(ticker)"
                  class="text-red-600 hover:underline text-xs sm:text-sm self-start sm:self-auto"
                >
                  Remove
                </button>
              </div>
            </div>
          </div>
          

        </div>
      </div>
    </div>
    
 
    <Toast ref="toastRef" />
  </div>
</template> 