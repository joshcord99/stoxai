<script setup lang="ts">
import { ref, computed } from 'vue'

interface TickerInfo {
  ticker: string
  name: string
  type: 'stock' | 'crypto' | 'forex'
  logo?: string
  description?: string
}

const searchQuery = ref('')
const activeTab = ref<'all' | 'stocks' | 'crypto' | 'forex'>('all')

const tickers: TickerInfo[] = [
 
  { ticker: 'AAPL', name: 'Apple Inc.', type: 'stock', logo: 'https://logo.clearbit.com/apple.com' },
  { ticker: 'MSFT', name: 'Microsoft Corporation', type: 'stock', logo: 'https://logo.clearbit.com/microsoft.com' },
  { ticker: 'GOOGL', name: 'Alphabet Inc.', type: 'stock', logo: 'https://logo.clearbit.com/google.com' },
  { ticker: 'AMZN', name: 'Amazon.com Inc.', type: 'stock', logo: 'https://logo.clearbit.com/amazon.com' },
  { ticker: 'META', name: 'Meta Platforms Inc.', type: 'stock', logo: 'https://logo.clearbit.com/meta.com' },
  { ticker: 'TSLA', name: 'Tesla Inc.', type: 'stock', logo: 'https://logo.clearbit.com/tesla.com' },
  { ticker: 'NVDA', name: 'NVIDIA Corporation', type: 'stock', logo: 'https://logo.clearbit.com/nvidia.com' },
  { ticker: 'JPM', name: 'JPMorgan Chase & Co.', type: 'stock', logo: 'https://logo.clearbit.com/jpmorganchase.com' },
  { ticker: 'JNJ', name: 'Johnson & Johnson', type: 'stock', logo: 'https://logo.clearbit.com/jnj.com' },
  { ticker: 'PG', name: 'Procter & Gamble Co.', type: 'stock', logo: 'https://logo.clearbit.com/pg.com' },
  { ticker: 'UNH', name: 'UnitedHealth Group Inc.', type: 'stock', logo: 'https://logo.clearbit.com/unitedhealthgroup.com' },
  { ticker: 'HD', name: 'The Home Depot Inc.', type: 'stock', logo: 'https://logo.clearbit.com/homedepot.com' },
  { ticker: 'DIS', name: 'The Walt Disney Company', type: 'stock', logo: 'https://logo.clearbit.com/disney.com' },
  { ticker: 'PYPL', name: 'PayPal Holdings Inc.', type: 'stock', logo: 'https://logo.clearbit.com/paypal.com' },
  { ticker: 'ADBE', name: 'Adobe Inc.', type: 'stock', logo: 'https://logo.clearbit.com/adobe.com' },
  { ticker: 'NFLX', name: 'Netflix Inc.', type: 'stock', logo: 'https://logo.clearbit.com/netflix.com' },
  { ticker: 'CRM', name: 'Salesforce Inc.', type: 'stock', logo: 'https://logo.clearbit.com/salesforce.com' },
  { ticker: 'INTC', name: 'Intel Corporation', type: 'stock', logo: 'https://logo.clearbit.com/intel.com' },
  { ticker: 'AMD', name: 'Advanced Micro Devices Inc.', type: 'stock', logo: 'https://logo.clearbit.com/amd.com' },
  { ticker: 'CSCO', name: 'Cisco Systems Inc.', type: 'stock', logo: 'https://logo.clearbit.com/cisco.com' },
  { ticker: 'ORCL', name: 'Oracle Corporation', type: 'stock', logo: 'https://logo.clearbit.com/oracle.com' },
  { ticker: 'KO', name: 'The Coca-Cola Company', type: 'stock', logo: 'https://logo.clearbit.com/coca-cola.com' },
  { ticker: 'PEP', name: 'PepsiCo Inc.', type: 'stock', logo: 'https://logo.clearbit.com/pepsico.com' },
  { ticker: 'WMT', name: 'Walmart Inc.', type: 'stock', logo: 'https://logo.clearbit.com/walmart.com' },
  { ticker: 'COST', name: 'Costco Wholesale Corporation', type: 'stock', logo: 'https://logo.clearbit.com/costco.com' },
  { ticker: 'MCD', name: 'McDonald\'s Corporation', type: 'stock', logo: 'https://logo.clearbit.com/mcdonalds.com' },
  { ticker: 'NKE', name: 'NIKE Inc.', type: 'stock', logo: 'https://logo.clearbit.com/nike.com' },
  { ticker: 'SBUX', name: 'Starbucks Corporation', type: 'stock', logo: 'https://logo.clearbit.com/starbucks.com' },
  { ticker: 'TGT', name: 'Target Corporation', type: 'stock', logo: 'https://logo.clearbit.com/target.com' },
  { ticker: 'BAC', name: 'Bank of America Corporation', type: 'stock', logo: 'https://logo.clearbit.com/bankofamerica.com' },
  { ticker: 'WFC', name: 'Wells Fargo & Company', type: 'stock', logo: 'https://logo.clearbit.com/wellsfargo.com' },
  { ticker: 'GS', name: 'Goldman Sachs Group Inc.', type: 'stock', logo: 'https://logo.clearbit.com/goldmansachs.com' },
  { ticker: 'MS', name: 'Morgan Stanley', type: 'stock', logo: 'https://logo.clearbit.com/morganstanley.com' },
  { ticker: 'CVX', name: 'Chevron Corporation', type: 'stock', logo: 'https://logo.clearbit.com/chevron.com' },
  { ticker: 'XOM', name: 'Exxon Mobil Corporation', type: 'stock', logo: 'https://logo.clearbit.com/exxonmobil.com' },
  { ticker: 'ABBV', name: 'AbbVie Inc.', type: 'stock', logo: 'https://logo.clearbit.com/abbvie.com' },
  { ticker: 'ABT', name: 'Abbott Laboratories', type: 'stock', logo: 'https://logo.clearbit.com/abbott.com' },
  { ticker: 'BMY', name: 'Bristol-Myers Squibb Company', type: 'stock', logo: 'https://logo.clearbit.com/bms.com' },
  { ticker: 'PFE', name: 'Pfizer Inc.', type: 'stock', logo: 'https://logo.clearbit.com/pfizer.com' },
  { ticker: 'MRK', name: 'Merck & Co. Inc.', type: 'stock', logo: 'https://logo.clearbit.com/merck.com' },
  { ticker: 'TMO', name: 'Thermo Fisher Scientific Inc.', type: 'stock', logo: 'https://logo.clearbit.com/thermofisher.com' },
  { ticker: 'DHR', name: 'Danaher Corporation', type: 'stock', logo: 'https://logo.clearbit.com/danaher.com' },
  { ticker: 'AMGN', name: 'Amgen Inc.', type: 'stock', logo: 'https://logo.clearbit.com/amgen.com' },

  
  { ticker: 'BTC', name: 'Bitcoin', type: 'crypto', logo: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png' },
  { ticker: 'ETH', name: 'Ethereum', type: 'crypto', logo: 'https://cryptologos.cc/logos/ethereum-eth-logo.png' },
  { ticker: 'BNB', name: 'BNB', type: 'crypto', logo: 'https://cryptologos.cc/logos/bnb-bnb-logo.png' },
  { ticker: 'ADA', name: 'Cardano', type: 'crypto', logo: 'https://cryptologos.cc/logos/cardano-ada-logo.png' },
  { ticker: 'SOL', name: 'Solana', type: 'crypto', logo: 'https://cryptologos.cc/logos/solana-sol-logo.png' },
  { ticker: 'DOT', name: 'Polkadot', type: 'crypto', logo: 'https://cryptologos.cc/logos/polkadot-new-dot-logo.png' },
  { ticker: 'LINK', name: 'Chainlink', type: 'crypto', logo: 'https://cryptologos.cc/logos/chainlink-link-logo.png' },
  { ticker: 'LTC', name: 'Litecoin', type: 'crypto', logo: 'https://cryptologos.cc/logos/litecoin-ltc-logo.png' },
  { ticker: 'BCH', name: 'Bitcoin Cash', type: 'crypto', logo: 'https://cryptologos.cc/logos/bitcoin-cash-bch-logo.png' },
  { ticker: 'UNI', name: 'Uniswap', type: 'crypto', logo: 'https://cryptologos.cc/logos/uniswap-uni-logo.png' },
  { ticker: 'ATOM', name: 'Cosmos', type: 'crypto', logo: 'https://cryptologos.cc/logos/cosmos-atom-logo.png' },
  { ticker: 'VET', name: 'VeChain', type: 'crypto', logo: 'https://cryptologos.cc/logos/vechain-vet-logo.png' },
  { ticker: 'TRX', name: 'TRON', type: 'crypto', logo: 'https://cryptologos.cc/logos/tron-trx-logo.png' },
  { ticker: 'ETC', name: 'Ethereum Classic', type: 'crypto', logo: 'https://cryptologos.cc/logos/ethereum-classic-etc-logo.png' },
  { ticker: 'ALGO', name: 'Algorand', type: 'crypto', logo: 'https://cryptologos.cc/logos/algorand-algo-logo.png' },
  { ticker: 'XRP', name: 'XRP', type: 'crypto', logo: 'https://cryptologos.cc/logos/xrp-xrp-logo.png' },
  { ticker: 'DOGE', name: 'Dogecoin', type: 'crypto', logo: 'https://cryptologos.cc/logos/dogecoin-doge-logo.png' },
  { ticker: 'SHIB', name: 'Shiba Inu', type: 'crypto', logo: 'https://cryptologos.cc/logos/shiba-inu-shib-logo.png' },
  { ticker: 'MATIC', name: 'Polygon', type: 'crypto', logo: 'https://cryptologos.cc/logos/polygon-matic-logo.png' },
  { ticker: 'NEAR', name: 'NEAR Protocol', type: 'crypto', logo: 'https://cryptologos.cc/logos/near-protocol-near-logo.png' },
  { ticker: 'AVAX', name: 'Avalanche', type: 'crypto', logo: 'https://cryptologos.cc/logos/avalanche-avax-logo.png' },
  { ticker: 'FTM', name: 'Fantom', type: 'crypto', logo: 'https://cryptologos.cc/logos/fantom-ftm-logo.png' },
  { ticker: 'FIL', name: 'Filecoin', type: 'crypto', logo: 'https://cryptologos.cc/logos/filecoin-fil-logo.png' },
  { ticker: 'ICP', name: 'Internet Computer', type: 'crypto', logo: 'https://cryptologos.cc/logos/internet-computer-icp-logo.png' },
  { ticker: 'THETA', name: 'Theta Network', type: 'crypto', logo: 'https://cryptologos.cc/logos/theta-theta-logo.png' },
  { ticker: 'XTZ', name: 'Tezos', type: 'crypto', logo: 'https://cryptologos.cc/logos/tezos-xtz-logo.png' },
  { ticker: 'CAKE', name: 'PancakeSwap', type: 'crypto', logo: 'https://cryptologos.cc/logos/pancakeswap-cake-logo.png' },
  { ticker: 'CHZ', name: 'Chiliz', type: 'crypto', logo: 'https://cryptologos.cc/logos/chiliz-chz-logo.png' },
  { ticker: 'HOT', name: 'Holo', type: 'crypto', logo: 'https://cryptologos.cc/logos/holo-hot-logo.png' },
  { ticker: 'GALA', name: 'Gala', type: 'crypto', logo: 'https://cryptologos.cc/logos/gala-gala-logo.png' },
  { ticker: 'AXS', name: 'Axie Infinity', type: 'crypto', logo: 'https://cryptologos.cc/logos/axie-infinity-axs-logo.png' },
  { ticker: 'SAND', name: 'The Sandbox', type: 'crypto', logo: 'https://cryptologos.cc/logos/the-sandbox-sand-logo.png' },
  { ticker: 'MANA', name: 'Decentraland', type: 'crypto', logo: 'https://cryptologos.cc/logos/decentraland-mana-logo.png' },
  { ticker: 'ENJ', name: 'Enjin Coin', type: 'crypto', logo: 'https://cryptologos.cc/logos/enjin-coin-enj-logo.png' },


  { ticker: 'EUR/USD', name: 'Euro / US Dollar', type: 'forex' },
  { ticker: 'GBP/USD', name: 'British Pound / US Dollar', type: 'forex' },
  { ticker: 'USD/JPY', name: 'US Dollar / Japanese Yen', type: 'forex' },
  { ticker: 'USD/CHF', name: 'US Dollar / Swiss Franc', type: 'forex' },
  { ticker: 'AUD/USD', name: 'Australian Dollar / US Dollar', type: 'forex' },
  { ticker: 'USD/CAD', name: 'US Dollar / Canadian Dollar', type: 'forex' },
  { ticker: 'NZD/USD', name: 'New Zealand Dollar / US Dollar', type: 'forex' },
  { ticker: 'EUR/GBP', name: 'Euro / British Pound', type: 'forex' },
  { ticker: 'EUR/JPY', name: 'Euro / Japanese Yen', type: 'forex' },
  { ticker: 'GBP/JPY', name: 'British Pound / Japanese Yen', type: 'forex' },
  { ticker: 'EUR/CHF', name: 'Euro / Swiss Franc', type: 'forex' },
  { ticker: 'AUD/JPY', name: 'Australian Dollar / Japanese Yen', type: 'forex' },
  { ticker: 'CAD/JPY', name: 'Canadian Dollar / Japanese Yen', type: 'forex' },
  { ticker: 'NZD/JPY', name: 'New Zealand Dollar / Japanese Yen', type: 'forex' },
  { ticker: 'GBP/CHF', name: 'British Pound / Swiss Franc', type: 'forex' },
  { ticker: 'AUD/CHF', name: 'Australian Dollar / Swiss Franc', type: 'forex' },
  { ticker: 'CAD/CHF', name: 'Canadian Dollar / Swiss Franc', type: 'forex' },
  { ticker: 'NZD/CHF', name: 'New Zealand Dollar / Swiss Franc', type: 'forex' },
  { ticker: 'EUR/AUD', name: 'Euro / Australian Dollar', type: 'forex' },
  { ticker: 'EUR/CAD', name: 'Euro / Canadian Dollar', type: 'forex' },
  { ticker: 'EUR/NZD', name: 'Euro / New Zealand Dollar', type: 'forex' },
  { ticker: 'GBP/AUD', name: 'British Pound / Australian Dollar', type: 'forex' },
  { ticker: 'GBP/CAD', name: 'British Pound / Canadian Dollar', type: 'forex' },
  { ticker: 'GBP/NZD', name: 'British Pound / New Zealand Dollar', type: 'forex' },
  { ticker: 'AUD/CAD', name: 'Australian Dollar / Canadian Dollar', type: 'forex' },
  { ticker: 'AUD/NZD', name: 'Australian Dollar / New Zealand Dollar', type: 'forex' },
  { ticker: 'CAD/NZD', name: 'Canadian Dollar / New Zealand Dollar', type: 'forex' }
]

const filteredTickers = computed(() => {
  let filtered = tickers.filter(ticker => {
    const matchesSearch = ticker.ticker.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         ticker.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    if (activeTab.value === 'all') {
      return matchesSearch
    } else {
      return ticker.type === activeTab.value && matchesSearch
    }
  })
  
  return filtered.sort((a, b) => a.ticker.localeCompare(b.ticker))
})

const groupedTickers = computed(() => {
  const groups: { [key: string]: TickerInfo[] } = {}
  
  filteredTickers.value.forEach(ticker => {
    const firstLetter = ticker.ticker.charAt(0).toUpperCase()
    if (!groups[firstLetter]) {
      groups[firstLetter] = []
    }
    groups[firstLetter].push(ticker)
  })
  
  return groups
})

const getTabCount = (type: 'stock' | 'crypto' | 'forex') => {
  return tickers.filter(ticker => ticker.type === type).length
}
</script>

<template>
  <div class="min-h-screen bg-gray-900">
    <div class="container mx-auto px-4 py-4 sm:py-8">
      <div class="bg-white rounded-lg shadow-lg p-4 sm:p-6">
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-4 sm:mb-6 text-center">Tickers Directory</h1>
        
        <div class="mb-4 sm:mb-6">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search tickers or company names..."
            class="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm sm:text-base"
          />
        </div>
        
        <div class="flex flex-wrap gap-2 mb-4 sm:mb-6">
          <button
            @click="activeTab = 'all'"
            :class="activeTab === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
            class="px-2 sm:px-4 py-2 rounded-lg font-medium transition-colors text-xs sm:text-sm"
          >
            All ({{ tickers.length }})
          </button>
          <button
            @click="activeTab = 'stocks'"
            :class="activeTab === 'stocks' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
            class="px-2 sm:px-4 py-2 rounded-lg font-medium transition-colors text-xs sm:text-sm"
          >
            Stocks ({{ getTabCount('stock') }})
          </button>
          <button
            @click="activeTab = 'crypto'"
            :class="activeTab === 'crypto' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
            class="px-2 sm:px-4 py-2 rounded-lg font-medium transition-colors text-xs sm:text-sm"
          >
            Crypto ({{ getTabCount('crypto') }})
          </button>
          <button
            @click="activeTab = 'forex'"
            :class="activeTab === 'forex' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
            class="px-2 sm:px-4 py-2 rounded-lg font-medium transition-colors text-xs sm:text-sm"
          >
            Forex ({{ getTabCount('forex') }})
          </button>
        </div>
        
        <div class="space-y-4 sm:space-y-6">
          <div
            v-for="(tickers, letter) in groupedTickers"
            :key="letter"
            class="space-y-3 sm:space-y-4"
          >
            <div class="flex items-center space-x-2 sm:space-x-4">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 sm:w-10 sm:h-10 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold text-sm sm:text-lg">
                  {{ letter }}
                </div>
              </div>
              <div class="flex-1 border-t border-gray-300"></div>
            </div>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 sm:gap-4">
              <div
                v-for="ticker in tickers"
                :key="ticker.ticker"
                class="bg-gray-50 rounded-lg p-3 sm:p-4 border border-gray-200 hover:shadow-md transition-shadow"
              >
                <div class="flex items-center space-x-2 sm:space-x-3">
                  <div v-if="ticker.logo" class="flex-shrink-0">
                    <img
                      :src="ticker.logo"
                      :alt="ticker.name"
                      class="w-6 h-6 sm:w-8 sm:h-8 rounded-full object-cover"
                      @error="(event: Event) => { const target = event.target as HTMLImageElement; if (target) target.style.display = 'none' }"
                    />
                  </div>
                  <div v-else class="flex-shrink-0">
                    <div class="w-6 h-6 sm:w-8 sm:h-8 rounded-full bg-gray-300 flex items-center justify-center">
                      <span class="text-xs font-medium text-gray-600">{{ ticker.ticker.charAt(0) }}</span>
                    </div>
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="flex flex-col sm:flex-row sm:items-center space-y-1 sm:space-y-0 sm:space-x-2">
                      <span class="font-bold text-gray-900 text-sm sm:text-base">{{ ticker.ticker }}</span>
                      <span
                        :class="{
                          'bg-green-100 text-green-800': ticker.type === 'stock',
                          'bg-purple-100 text-purple-800': ticker.type === 'crypto',
                          'bg-blue-100 text-blue-800': ticker.type === 'forex'
                        }"
                        class="px-2 py-1 text-xs font-medium rounded-full self-start sm:self-auto"
                      >
                        {{ ticker.type }}
                      </span>
                    </div>
                    <div class="text-xs sm:text-sm text-gray-600 truncate">{{ ticker.name }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="filteredTickers.length === 0" class="text-center py-8">
          <p class="text-gray-500 text-base sm:text-lg">No tickers found matching your search.</p>
        </div>
      </div>
    </div>
  </div>
</template> 