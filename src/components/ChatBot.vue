<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { marked } from 'marked'
import { useUserStore } from '../userInfo'
import api from '../connection/api'

interface Message {
  text: string
  sender: 'user' | 'bot'
  loading?: boolean
}

const messages = ref<Message[]>([])
const input = ref('')
const isLoading = ref(false)
const userStore = useUserStore()
const chatContainer = ref<HTMLElement>()

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

watch(messages, () => {
  scrollToBottom()
}, { deep: true })

onMounted(() => {
  const userName =
    userStore.user?.full_name ||
    userStore.user?.first_name ||
    'User'
  messages.value = [
    { text: `Hello ${userName}! How can I help you today?`, sender: 'bot' }
  ]
})

const sendMessage = async () => {
  const userQuestion = input.value.trim()
  if (!userQuestion || isLoading.value) return

  messages.value.push({ text: userQuestion, sender: 'user' })
  messages.value.push({ text: 'Analyzing...', sender: 'bot', loading: true })

  input.value = ''
  isLoading.value = true

  try {
    const stockMappings: Record<string, string> = {
      google: 'GOOGL',
      alphabet: 'GOOGL',
      apple: 'AAPL',
      microsoft: 'MSFT',
      tesla: 'TSLA',
      amazon: 'AMZN',
      facebook: 'META',
      meta: 'META',
      nvidia: 'NVDA',
      netflix: 'NFLX',
      bitcoin: 'BTC',
      ethereum: 'ETH',
      cardano: 'ADA',
      solana: 'SOL',
      polkadot: 'DOT',
      chainlink: 'LINK',
      uniswap: 'UNI',
      polygon: 'MATIC',
      avalanche: 'AVAX',
      fantom: 'FTM',
      near: 'NEAR',
      cosmos: 'ATOM',
      filecoin: 'FIL',
      tezos: 'XTZ',
      theta: 'THETA',
      pancakeswap: 'CAKE',
      chiliz: 'CHZ',
      holochain: 'HOT',
      dogecoin: 'DOGE',
      shiba: 'SHIB',
      decentraland: 'MANA',
      sandbox: 'SAND',
      enjin: 'ENJ',
      axie: 'AXS',
      gala: 'GALA'
    }

    const stockSymbols = [
      'AAPL','GOOGL','MSFT','TSLA','AMZN','META','NVDA','NFLX',
      'BTC','ETH','ADA','SOL','DOT','LINK','UNI','MATIC','AVAX',
      'FTM','NEAR','ICP','FIL','XTZ','THETA','CAKE','CHZ','HOT',
      'DOGE','SHIB','MANA','SAND','ENJ','AXS','GALA'
    ]

    let isStockQuestion = false
    let detectedSymbol: string | null = null

    const questionLower = userQuestion.toLowerCase()

    for (const [companyName, symbol] of Object.entries(stockMappings)) {
      if (questionLower.includes(companyName)) {
        isStockQuestion = true
        detectedSymbol = symbol
        break
      }
    }

    if (!isStockQuestion) {
      for (const symbol of stockSymbols) {
        if (userQuestion.toUpperCase().includes(symbol)) {
          isStockQuestion = true
          detectedSymbol = symbol
          break
        }
      }
    }

    const investmentKeywords = [
      'invest','investment','buy','sell','hold','stock','shares',
      'trading','market','price','trend','analysis','performance',
      'doing','how is','should i'
    ]
    const hasInvestmentKeywords = investmentKeywords.some(k =>
      questionLower.includes(k)
    )

    let data: { success: boolean; response?: string; technical_data?: any; analysis_type?: string; symbol?: string } = { success: false }
    const authHeaders = userStore.token
      ? { Authorization: `Bearer ${userStore.token}` }
      : {}

    if ((isStockQuestion && detectedSymbol) || (hasInvestmentKeywords && detectedSymbol)) {
      try {
        // Get conversation context for better analysis
        const conversationContext = messages.value
          .filter(msg => msg.sender === 'user' && !msg.loading)
          .slice(-5) // Last 5 user messages for context
          .map(msg => msg.text)
          .join(' | ')

        const res = await api.post(
          '/stock-analysis',
          { 
            symbol: detectedSymbol, 
            question: userQuestion,
            conversation_context: conversationContext
          }
        )
        data = res.data
      } catch {
        const res = await api.post(
          '/ai_chatbot',
          { question: userQuestion }
        )
        data = res.data
      }
    } else {
      const res = await api.post(
        '/ai_chatbot',
        { question: userQuestion }
      )
      data = res.data
    }

    messages.value.pop()

    if (data.success && data.response) {
      // If we have technical data from stock analyzer, enhance the response
      if (data.technical_data && data.analysis_type === 'stock_analysis') {
        const enhancedResponse = enhanceStockResponse(data.response, data.technical_data, data.symbol || 'Unknown')
        messages.value.push({ text: enhancedResponse, sender: 'bot' })
      } else {
        messages.value.push({ text: data.response, sender: 'bot' })
      }
    } else {
      messages.value.push({
        text: "Sorry, I couldn't analyze your question right now.",
        sender: 'bot'
      })
    }
  } catch (err) {
    console.error('Chatbot error:', err)
    const last = messages.value[messages.value.length - 1]
    if (last?.loading) messages.value.pop()
    messages.value.push({
      text: 'Unable to connect to analysis service. Please try again later.',
      sender: 'bot'
    })
  } finally {
    isLoading.value = false
  }
}

const enhanceStockResponse = (baseResponse: string, technicalData: any, symbol: string) => {
  let enhancedResponse = baseResponse

  // Add technical insights if available
  if (technicalData) {
    enhancedResponse += '\n\n**Technical Insights:**\n'
    
    if (technicalData.current_price) {
      enhancedResponse += `• Current Price: $${technicalData.current_price}\n`
    }
    
    if (technicalData.trend) {
      enhancedResponse += `• Trend: ${technicalData.trend}\n`
    }
    
    if (technicalData.recommendation) {
      enhancedResponse += `• Recommendation: ${technicalData.recommendation}\n`
    }
    
    if (technicalData.risk_score) {
      enhancedResponse += `• Risk Score: ${technicalData.risk_score}/10\n`
    }
  }

  // Add contextual advice based on the conversation
  const recentMessages = messages.value
    .filter(msg => msg.sender === 'user' && !msg.loading)
    .slice(-3)
    .map(msg => msg.text.toLowerCase())

  const hasAskedAboutTrend = recentMessages.some(msg => 
    msg.includes('trend') || msg.includes('going') || msg.includes('direction')
  )
  
  const hasAskedAboutRisk = recentMessages.some(msg => 
    msg.includes('risk') || msg.includes('safe') || msg.includes('dangerous')
  )
  
  const hasAskedAboutInvestment = recentMessages.some(msg => 
    msg.includes('buy') || msg.includes('sell') || msg.includes('invest')
  )

  if (hasAskedAboutTrend && technicalData?.trend) {
    enhancedResponse += '\n**Trend Analysis:** Based on your interest in trends, '
    if (technicalData.trend.includes('UP')) {
      enhancedResponse += `${symbol || 'this stock'} is showing positive momentum. Consider this in your investment strategy.`
    } else if (technicalData.trend.includes('DOWN')) {
      enhancedResponse += `${symbol || 'this stock'} is showing negative momentum. Exercise caution and consider waiting for a reversal.`
    } else {
      enhancedResponse += `${symbol || 'this stock'} is moving sideways. This might be a good time to accumulate or wait for a breakout.`
    }
  }

  if (hasAskedAboutRisk && technicalData?.risk_score) {
    enhancedResponse += '\n**Risk Context:** '
    if (technicalData.risk_score <= 3) {
      enhancedResponse += 'This appears to be a relatively low-risk investment opportunity.'
    } else if (technicalData.risk_score <= 6) {
      enhancedResponse += 'This investment carries moderate risk. Consider your risk tolerance.'
    } else {
      enhancedResponse += 'This is a high-risk investment. Only invest what you can afford to lose.'
    }
  }

  if (hasAskedAboutInvestment && technicalData?.recommendation) {
    enhancedResponse += '\n**Investment Context:** '
    if (technicalData.recommendation.includes('BUY')) {
      enhancedResponse += 'The technical analysis suggests this could be a good entry point.'
    } else if (technicalData.recommendation.includes('SELL')) {
      enhancedResponse += 'Consider taking profits or waiting for better entry conditions.'
    } else {
      enhancedResponse += 'The signals are mixed. Consider waiting for clearer direction.'
    }
  }

  return enhancedResponse
}

const getAvailableAssets = async () => {
  return
}

const renderMarkdown = (text: string) => {
  try {
    return marked.parse(text)
  } catch {
    return text
  }
}

getAvailableAssets()
</script>

<template>
  <div class="bg-white shadow-lg p-3 sm:p-4 rounded-lg w-full">
    <h2 class="text-lg sm:text-xl font-bold mb-4 text-center">Stock & Crypto Chat Assistant</h2>

    <div ref="chatContainer" class="h-48 sm:h-64 overflow-y-auto border p-2 sm:p-3 mb-4 bg-gray-50 rounded">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="{
          'text-right text-blue-700': msg.sender === 'user',
          'text-left text-gray-800': msg.sender === 'bot'
        }"
        class="mb-2"
      >
        <div
          class="inline-block px-2 sm:px-3 py-1 sm:py-2 rounded-lg shadow text-xs sm:text-sm max-w-full"
          :class="{
            'bg-blue-100': msg.sender === 'user',
            'bg-gray-200': msg.sender === 'bot',
            'bg-yellow-100 animate-pulse': msg.loading
          }"
        >
          <span v-if="msg.loading" class="inline-block animate-spin mr-1 sm:mr-2">⏳</span>
          <div v-if="msg.sender === 'bot'" v-html="renderMarkdown(msg.text)" class="prose prose-xs sm:prose-sm max-w-none break-words"></div>
          <div v-else class="break-words">{{ msg.text }}</div>
        </div>
      </div>
    </div>

    <div class="flex items-center gap-2">
      <input
        v-model="input"
        @keydown.enter="sendMessage"
        type="text"
        placeholder="Ask about stocks or crypto..."
        class="flex-1 px-2 sm:px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 text-sm sm:text-base"
        :disabled="isLoading"
      />
      <button
        @click="sendMessage"
        :disabled="isLoading"
        class="bg-blue-600 text-white px-3 sm:px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 text-sm sm:text-base whitespace-nowrap"
      >
        {{ isLoading ? 'Analyzing...' : 'Send' }}
      </button>
    </div>
  </div>
</template>