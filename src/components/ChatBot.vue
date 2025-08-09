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