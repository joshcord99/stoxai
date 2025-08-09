<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { marked } from 'marked'
import { useUserStore } from '../userInfo'

interface Message {
  text: string
  sender: 'user' | 'bot'
  loading?: boolean
}

const messages = ref<Message[]>([])
const input = ref('')
const isLoading = ref(false)
const userStore = useUserStore()

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

    let data: { success: boolean; response?: string } = { success: false }
    const authHeaders = userStore.token
      ? { Authorization: `Bearer ${userStore.token}` }
      : {}

    if ((isStockQuestion && detectedSymbol) || (hasInvestmentKeywords && detectedSymbol)) {
      const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5003'
      try {
        const res = await axios.post(
          `${BACKEND_URL}/api/stock-analysis`,
          { symbol: detectedSymbol, question: userQuestion },
          { headers: authHeaders }
        )
        data = res.data
      } catch {
        const res = await axios.post(
          '/.netlify/functions/api/ai_chatbot',
          { question: userQuestion },
          { headers: authHeaders }
        )
        data = res.data
      }
    } else {
      const res = await axios.post(
        '/.netlify/functions/api/ai_chatbot',
        { question: userQuestion },
        { headers: authHeaders }
      )
      data = res.data
    }

    messages.value.pop()

    if (data.success && data.response) {
      messages.value.push({ text: data.response, sender: 'bot' })
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
  <div class="bg-white shadow-lg p-4 rounded-lg max-w-2xl mx-auto mt-[-15px]">
            <h2 class="text-xl font-bold mb-4 text-center">Stock & Crypto Chat Assistant</h2>

    <div class="h-64 overflow-y-auto border p-3 mb-4 bg-gray-50 rounded">
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
          class="inline-block px-3 py-2 rounded-lg shadow text-sm"
          :class="{
            'bg-blue-100': msg.sender === 'user',
            'bg-gray-200': msg.sender === 'bot',
            'bg-yellow-100 animate-pulse': msg.loading
          }"
        >
          <span v-if="msg.loading" class="inline-block animate-spin mr-2">⏳</span>
          <div v-if="msg.sender === 'bot'" v-html="renderMarkdown(msg.text)" class="prose prose-sm max-w-none"></div>
          <div v-else>{{ msg.text }}</div>
        </div>
      </div>
    </div>

    <div class="flex items-center gap-2">
      <input
        v-model="input"
        @keydown.enter="sendMessage"
        type="text"
        placeholder="Ask about stocks or crypto (e.g., 'Should I invest in Bitcoin?')"
        class="flex-1 px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500"
        :disabled="isLoading"
      />
      <button
        @click="sendMessage"
        :disabled="isLoading"
        class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
      >
        {{ isLoading ? 'Analyzing...' : 'Send' }}
      </button>
    </div>
  </div>
</template>