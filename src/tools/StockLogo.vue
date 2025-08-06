<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Props {
  ticker: string
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md'
})

const logoUrl = ref<string | null>(null)
const logoError = ref(false)
const imageLoaded = ref(false)

const stockLogos: Record<string, string> = {
  'AAPL': 'https://logo.clearbit.com/apple.com',
  'MSFT': 'https://logo.clearbit.com/microsoft.com',
  'GOOGL': 'https://logo.clearbit.com/google.com',
  'AMZN': 'https://logo.clearbit.com/amazon.com',
  'TSLA': 'https://logo.clearbit.com/tesla.com',
  'META': 'https://logo.clearbit.com/meta.com',
  'NVDA': 'https://logo.clearbit.com/nvidia.com',
  'NFLX': 'https://logo.clearbit.com/netflix.com',
  'CRM': 'https://logo.clearbit.com/salesforce.com',
  'ADBE': 'https://logo.clearbit.com/adobe.com',
  'PYPL': 'https://logo.clearbit.com/paypal.com',
  'INTC': 'https://logo.clearbit.com/intel.com',
  'AMD': 'https://logo.clearbit.com/amd.com',
  'CSCO': 'https://logo.clearbit.com/cisco.com',
  'ORCL': 'https://logo.clearbit.com/oracle.com',
  'IBM': 'https://logo.clearbit.com/ibm.com',
  'QCOM': 'https://logo.clearbit.com/qualcomm.com',
  'TXN': 'https://logo.clearbit.com/ti.com',
  'AVGO': 'https://logo.clearbit.com/broadcom.com',
  'MU': 'https://logo.clearbit.com/micron.com',
  'AMAT': 'https://logo.clearbit.com/appliedmaterials.com',
  'KLAC': 'https://logo.clearbit.com/lamresearch.com',
  'LRCX': 'https://logo.clearbit.com/lamresearch.com',
  'ASML': 'https://logo.clearbit.com/asml.com',
  'ADI': 'https://logo.clearbit.com/analog.com',
  'MCHP': 'https://logo.clearbit.com/microchip.com',
  'TSM': 'https://logo.clearbit.com/tsmc.com',
  'JPM': 'https://logo.clearbit.com/jpmorganchase.com',
  'BAC': 'https://logo.clearbit.com/bankofamerica.com',
  'WFC': 'https://logo.clearbit.com/wellsfargo.com',
  'GS': 'https://logo.clearbit.com/goldmansachs.com',
  'MS': 'https://logo.clearbit.com/morganstanley.com',
  'C': 'https://logo.clearbit.com/citigroup.com',
  'COF': 'https://logo.clearbit.com/capitalone.com',
  'USB': 'https://logo.clearbit.com/usbank.com',
  'PNC': 'https://logo.clearbit.com/pnc.com',
  'TFC': 'https://logo.clearbit.com/truist.com',
  'JNJ': 'https://logo.clearbit.com/jnj.com',
  'PFE': 'https://logo.clearbit.com/pfizer.com',
  'UNH': 'https://logo.clearbit.com/unitedhealthgroup.com',
  'ABBV': 'https://logo.clearbit.com/abbvie.com',
  'ABT': 'https://logo.clearbit.com/abbott.com',
  'MRK': 'https://logo.clearbit.com/merck.com',
  'TMO': 'https://logo.clearbit.com/thermofisher.com',
  'DHR': 'https://logo.clearbit.com/danaher.com',
  'BMY': 'https://logo.clearbit.com/bms.com',
  'AMGN': 'https://logo.clearbit.com/amgen.com',
  'PEP': 'https://logo.clearbit.com/pepsico.com',
  'KO': 'https://logo.clearbit.com/coca-cola.com',
  'PG': 'https://logo.clearbit.com/pg.com',
  'WMT': 'https://logo.clearbit.com/walmart.com',
  'HD': 'https://logo.clearbit.com/homedepot.com',
  'MCD': 'https://logo.clearbit.com/mcdonalds.com',
  'DIS': 'https://logo.clearbit.com/disney.com',
  'NKE': 'https://logo.clearbit.com/nike.com',
  'SBUX': 'https://logo.clearbit.com/starbucks.com',
  'TGT': 'https://logo.clearbit.com/target.com',
  'LOW': 'https://logo.clearbit.com/lowes.com',
  'COST': 'https://logo.clearbit.com/costco.com',
  'XOM': 'https://logo.clearbit.com/exxonmobil.com',
  'CVX': 'https://logo.clearbit.com/chevron.com',
  'COP': 'https://logo.clearbit.com/conocophillips.com',
  'EOG': 'https://logo.clearbit.com/eogresources.com',
  'SLB': 'https://logo.clearbit.com/slb.com',
  'VLO': 'https://logo.clearbit.com/valero.com',
  'MPC': 'https://logo.clearbit.com/marathonpetroleum.com',
  'PSX': 'https://logo.clearbit.com/phillips66.com',
  'HAL': 'https://logo.clearbit.com/halliburton.com',
  'BKR': 'https://logo.clearbit.com/bakerhughes.com',
}

const cryptoLogos: Record<string, string> = {
  'BTC': 'https://assets.coingecko.com/coins/images/1/large/bitcoin.png',
  'ETH': 'https://assets.coingecko.com/coins/images/279/large/ethereum.png',
  'ADA': 'https://assets.coingecko.com/coins/images/975/large/cardano.png',
  'DOT': 'https://assets.coingecko.com/coins/images/12171/large/polkadot_new_logo.png',
  'LINK': 'https://assets.coingecko.com/coins/images/877/large/chainlink.png',
  'LTC': 'https://assets.coingecko.com/coins/images/2/large/litecoin.png',
  'BCH': 'https://assets.coingecko.com/coins/images/780/large/bitcoin-cash-circle.png',
  'UNI': 'https://assets.coingecko.com/coins/images/12504/large/uniswap-uni.png',
  'ATOM': 'https://assets.coingecko.com/coins/images/1481/large/cosmos_hub.png',
  'VET': 'https://assets.coingecko.com/coins/images/1167/large/vechain.png',
  'TRX': 'https://assets.coingecko.com/coins/images/1094/large/tron.png',
  'ETC': 'https://assets.coingecko.com/coins/images/453/large/ethereum-classic.png',
  'ALGO': 'https://assets.coingecko.com/coins/images/4380/large/algo.png',
  'BNB': 'https://assets.coingecko.com/coins/images/825/large/bnb-icon2_2x.png',
  'XRP': 'https://assets.coingecko.com/coins/images/44/large/xrp-symbol-white-128.png',
  'SOL': 'https://assets.coingecko.com/coins/images/4128/large/solana.png',
  'MATIC': 'https://assets.coingecko.com/coins/images/4713/large/matic-token-icon.png',
  'AVAX': 'https://assets.coingecko.com/coins/images/12559/large/avalanche-avax-red-white.png',
  'FTM': 'https://assets.coingecko.com/coins/images/4001/large/Fantom.png',
  'NEAR': 'https://assets.coingecko.com/coins/images/10365/large/near.png',
  'ICP': 'https://assets.coingecko.com/coins/images/14495/large/Internet_Computer_logo.png',
  'FIL': 'https://assets.coingecko.com/coins/images/12817/large/filecoin.png',
  'XTZ': 'https://assets.coingecko.com/coins/images/9768/large/Tezos-logo.png',
  'THETA': 'https://assets.coingecko.com/coins/images/2538/large/theta-token-logo.png',
  'CAKE': 'https://assets.coingecko.com/coins/images/12632/large/logo.png',
  'CHZ': 'https://assets.coingecko.com/coins/images/9712/large/Chiliz.png',
  'HOT': 'https://assets.coingecko.com/coins/images/5998/large/holochain.png',
  'DOGE': 'https://assets.coingecko.com/coins/images/5/large/dogecoin.png',
  'SHIB': 'https://assets.coingecko.com/coins/images/11939/large/shiba.png',
  'MANA': 'https://assets.coingecko.com/coins/images/878/large/decentraland-mana.png',
  'SAND': 'https://assets.coingecko.com/coins/images/12129/large/sandbox.png',
  'ENJ': 'https://assets.coingecko.com/coins/images/1102/large/enjin-coin-logo.png',
  'AXS': 'https://assets.coingecko.com/coins/images/13025/large/axie_infinity_logo.png',
  'GALA': 'https://assets.coingecko.com/coins/images/12493/large/GALA-COINGECKO.png',
}

const getLogoUrl = (symbol: string) => {
  const upperSymbol = symbol.toUpperCase()
  
  if (cryptoLogos[upperSymbol]) {
    return cryptoLogos[upperSymbol]
  }
  
  if (stockLogos[upperSymbol]) {
    return stockLogos[upperSymbol]
  }
  
  if (upperSymbol.includes('/') || upperSymbol.includes('USD') || upperSymbol.includes('EUR') ||
      upperSymbol.includes('GBP') || upperSymbol.includes('JPY') || upperSymbol.includes('CHF') ||
      upperSymbol.includes('AUD') || upperSymbol.includes('CAD') || upperSymbol.includes('NZD')) {
    return 'https://cdn-icons-png.flaticon.com/512/2830/2830312.png'
  }
  
  if (upperSymbol.includes('USDT')) {
    const baseSymbol = upperSymbol.replace('USDT', '')
    if (cryptoLogos[baseSymbol]) {
      return cryptoLogos[baseSymbol]
    }
  }
  
  return `https://logo.clearbit.com/${upperSymbol.toLowerCase()}.com`
}

const handleLogoError = () => {
  logoError.value = true
  imageLoaded.value = false
}

const handleLogoLoad = () => {
  imageLoaded.value = true
  logoError.value = false
}

const getTickerDisplay = () => {
  const ticker = props.ticker.toUpperCase()
  return ticker.length > 3 ? ticker.substring(0, 3) : ticker
}

const sizeClasses = {
  sm: 'w-6 h-6',
  md: 'w-8 h-8',
  lg: 'w-12 h-12'
}

const textSizeClasses = {
  sm: 'text-xs',
  md: 'text-sm',
  lg: 'text-lg'
}

onMounted(() => {
  logoUrl.value = getLogoUrl(props.ticker)
})
</script>

<template>
  <div class="flex-shrink-0">
    <div :class="[sizeClasses[size], 'rounded-full bg-gray-600 border border-gray-500 flex items-center justify-center overflow-hidden']">

      <img
        v-if="logoUrl && !logoError"
        :src="logoUrl"
        :alt="`${ticker} logo`"
        class="w-full h-full object-contain"
        @error="handleLogoError"
        @load="handleLogoLoad"
      />

      <span 
        v-else 
        :class="[textSizeClasses[size], 'text-white font-bold text-center']"
        class="text-white font-bold text-center"
      >
        {{ getTickerDisplay() }}
      </span>
    </div>
  </div>
</template> 