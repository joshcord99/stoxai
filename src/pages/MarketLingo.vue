<script setup lang="ts">
import { ref, computed } from 'vue'

interface LingoTerm {
  term: string
  definition: string
  category: 'trading' | 'technical' | 'fundamental' | 'crypto' | 'forex' | 'general'
  example?: string
}

const searchQuery = ref('')
const activeCategory = ref<'all' | 'trading' | 'technical' | 'fundamental' | 'crypto' | 'forex' | 'general'>('all')

const marketLingo: LingoTerm[] = [

  { term: 'Bull Market', definition: 'A market condition where prices are rising or expected to rise.', category: 'trading', example: 'The stock market has been in a bull market for the past 5 years.' },
  { term: 'Bear Market', definition: 'A market condition where prices are falling or expected to fall.', category: 'trading', example: 'During the 2008 financial crisis, we experienced a severe bear market.' },
  { term: 'Long Position', definition: 'Buying an asset with the expectation that its price will rise.', category: 'trading', example: 'I went long on AAPL at $150, expecting it to reach $200.' },
  { term: 'Short Position', definition: 'Selling an asset you don\'t own, expecting to buy it back at a lower price.', category: 'trading', example: 'I shorted TSLA at $800, hoping to cover at $600.' },
  { term: 'Liquidity', definition: 'How easily an asset can be bought or sold without affecting its price.', category: 'trading', example: 'Large-cap stocks like AAPL have high liquidity compared to penny stocks.' },
  { term: 'Volatility', definition: 'The rate at which the price of an asset increases or decreases.', category: 'trading', example: 'Crypto markets are known for their high volatility.' },
  { term: 'Spread', definition: 'The difference between the bid (buy) and ask (sell) price of an asset.', category: 'trading', example: 'The spread on major forex pairs is usually very tight.' },
  { term: 'Slippage', definition: 'The difference between the expected price and the actual executed price of a trade.', category: 'trading', example: 'High volatility can cause significant slippage on large orders.' },
  { term: 'Market Order', definition: 'An order to buy or sell immediately at the current market price.', category: 'trading', example: 'I placed a market order to buy 100 shares of MSFT.' },
  { term: 'Limit Order', definition: 'An order to buy or sell at a specific price or better.', category: 'trading', example: 'I set a limit order to buy AAPL at $150 or lower.' },
  { term: 'Stop Loss', definition: 'An order to sell an asset when it reaches a certain price to limit losses.', category: 'trading', example: 'I set a stop loss at $140 to protect my AAPL position.' },
  { term: 'Take Profit', definition: 'An order to sell an asset when it reaches a target price to secure gains.', category: 'trading', example: 'I set a take profit order at $200 for my AAPL shares.' },
  { term: 'Day Trading', definition: 'Buying and selling securities within the same trading day.', category: 'trading', example: 'Day traders close all positions before the market closes.' },
  { term: 'Swing Trading', definition: 'Holding positions for several days to weeks to capture medium-term moves.', category: 'trading', example: 'Swing traders analyze weekly charts for entry and exit points.' },
  { term: 'Position Sizing', definition: 'Determining how much of your capital to risk on a single trade.', category: 'trading', example: 'I risk 2% of my account on each trade for proper position sizing.' },
  { term: 'Risk/Reward Ratio', definition: 'The ratio of potential profit to potential loss on a trade.', category: 'trading', example: 'I only take trades with a risk/reward ratio of at least 1:2.' },


  { term: 'Support', definition: 'A price level where an asset tends to stop falling and bounce back up.', category: 'technical', example: 'AAPL found support at the $150 level multiple times.' },
  { term: 'Resistance', definition: 'A price level where an asset tends to stop rising and fall back down.', category: 'technical', example: 'The $200 level has been strong resistance for TSLA.' },
  { term: 'Moving Average', definition: 'An average of prices over a specific period, used to identify trends.', category: 'technical', example: 'The 50-day moving average is often used as a trend indicator.' },
  { term: 'RSI (Relative Strength Index)', definition: 'A momentum oscillator that measures the speed and change of price movements.', category: 'technical', example: 'RSI above 70 indicates overbought conditions.' },
  { term: 'MACD', definition: 'Moving Average Convergence Divergence - a trend-following momentum indicator.', category: 'technical', example: 'MACD crossover signals can indicate buy or sell opportunities.' },
  { term: 'Bollinger Bands', definition: 'A volatility indicator consisting of a moving average and two standard deviation bands.', category: 'technical', example: 'Price touching the upper Bollinger Band may indicate overbought conditions.' },
  { term: 'Candlestick', definition: 'A chart element showing the open, high, low, and close prices for a period.', category: 'technical', example: 'A doji candlestick indicates indecision in the market.' },
  { term: 'Breakout', definition: 'When price moves above resistance or below support with significant volume.', category: 'technical', example: 'The stock broke out above $200 with high volume.' },
  { term: 'Breakdown', definition: 'When price falls below a support level, often leading to further declines.', category: 'technical', example: 'The breakdown below $150 triggered a sell-off.' },
  { term: 'Gap', definition: 'A space between the previous day\'s close and the current day\'s open.', category: 'technical', example: 'The stock gapped up 5% on positive earnings news.' },
  { term: 'Volume', definition: 'The number of shares or contracts traded in a security or market.', category: 'technical', example: 'High volume confirms the strength of a price move.' },
  { term: 'Divergence', definition: 'When price and an indicator move in opposite directions.', category: 'technical', example: 'Bearish divergence occurs when price makes higher highs but RSI makes lower highs.' },
  { term: 'Fibonacci Retracement', definition: 'A tool used to identify potential reversal levels based on Fibonacci ratios.', category: 'technical', example: 'The 61.8% Fibonacci retracement level often acts as support.' },
  { term: 'Head and Shoulders', definition: 'A reversal pattern with three peaks, the middle one being the highest.', category: 'technical', example: 'The head and shoulders pattern completed, signaling a trend reversal.' },
  { term: 'Double Top', definition: 'A reversal pattern with two peaks at approximately the same price level.', category: 'technical', example: 'The double top at $200 suggests the uptrend may be ending.' },
  { term: 'Golden Cross', definition: 'When a shorter-term moving average crosses above a longer-term moving average.', category: 'technical', example: 'The golden cross of the 50-day above the 200-day MA is bullish.' },
  { term: 'Death Cross', definition: 'When a shorter-term moving average crosses below a longer-term moving average.', category: 'technical', example: 'The death cross of the 50-day below the 200-day MA is bearish.' },


  { term: 'P/E Ratio', definition: 'Price-to-Earnings ratio - measures a company\'s stock price relative to its earnings.', category: 'fundamental', example: 'A P/E ratio of 15 means investors pay $15 for every $1 of earnings.' },
  { term: 'EPS (Earnings Per Share)', definition: 'A company\'s profit divided by the number of outstanding shares.', category: 'fundamental', example: 'AAPL reported EPS of $5.67 for the quarter.' },
  { term: 'Market Cap', definition: 'The total value of a company\'s shares of stock.', category: 'fundamental', example: 'Apple has a market cap of over $2 trillion.' },
  { term: 'Dividend Yield', definition: 'Annual dividend payment as a percentage of the stock price.', category: 'fundamental', example: 'A stock with a 3% dividend yield pays $3 annually for every $100 invested.' },
  { term: 'Revenue', definition: 'The total amount of money a company receives from its business activities.', category: 'fundamental', example: 'Tesla reported revenue of $81.5 billion in 2022.' },
  { term: 'Net Income', definition: 'A company\'s total earnings after deducting all expenses and taxes.', category: 'fundamental', example: 'Net income is also called the bottom line.' },
  { term: 'ROE (Return on Equity)', definition: 'Net income divided by shareholders\' equity, measuring profitability.', category: 'fundamental', example: 'A ROE of 15% means the company generates 15% return on shareholders\' equity.' },
  { term: 'Debt-to-Equity Ratio', definition: 'Total debt divided by shareholders\' equity, measuring financial leverage.', category: 'fundamental', example: 'A high debt-to-equity ratio indicates higher financial risk.' },
  { term: 'Free Cash Flow', definition: 'Cash generated by a company after accounting for capital expenditures.', category: 'fundamental', example: 'Free cash flow is used for dividends, buybacks, and growth investments.' },
  { term: 'Book Value', definition: 'The value of a company\'s assets minus its liabilities.', category: 'fundamental', example: 'A stock trading below book value may be undervalued.' },
  { term: 'Intrinsic Value', definition: 'The true value of an asset based on fundamental analysis.', category: 'fundamental', example: 'Warren Buffett focuses on finding stocks trading below their intrinsic value.' },
  { term: 'Growth Stock', definition: 'A stock expected to grow earnings at an above-average rate.', category: 'fundamental', example: 'Tech companies like TSLA are often considered growth stocks.' },
  { term: 'Value Stock', definition: 'A stock that appears to trade for less than its intrinsic value.', category: 'fundamental', example: 'Value investors look for stocks with low P/E ratios.' },
  { term: 'Blue Chip', definition: 'A large, well-established, and financially sound company.', category: 'fundamental', example: 'Companies like AAPL, MSFT, and JNJ are considered blue chips.' },
  { term: 'Earnings Call', definition: 'A conference call where company executives discuss quarterly results.', category: 'fundamental', example: 'Analysts ask questions during earnings calls to understand company performance.' },
  { term: 'Guidance', definition: 'A company\'s forecast of future financial performance.', category: 'fundamental', example: 'The company lowered its guidance for the next quarter.' },


  { term: 'Blockchain', definition: 'A decentralized digital ledger that records transactions across multiple computers.', category: 'crypto', example: 'Bitcoin\'s blockchain records all BTC transactions since 2009.' },
  { term: 'Mining', definition: 'The process of validating transactions and adding them to the blockchain.', category: 'crypto', example: 'Bitcoin miners compete to solve complex mathematical problems.' },
  { term: 'Staking', definition: 'Holding cryptocurrency to help secure a network and earn rewards.', category: 'crypto', example: 'ETH holders can stake their coins to earn staking rewards.' },
  { term: 'DeFi', definition: 'Decentralized Finance - financial services built on blockchain technology.', category: 'crypto', example: 'DeFi platforms allow users to lend, borrow, and trade without intermediaries.' },
  { term: 'NFT', definition: 'Non-Fungible Token - a unique digital asset that cannot be replaced.', category: 'crypto', example: 'NFTs can represent digital art, collectibles, or real estate.' },
  { term: 'Smart Contract', definition: 'Self-executing contracts with terms written in code on the blockchain.', category: 'crypto', example: 'Smart contracts automatically execute when conditions are met.' },
  { term: 'Gas Fee', definition: 'The cost of processing a transaction on the Ethereum network.', category: 'crypto', example: 'High network congestion leads to higher gas fees.' },
  { term: 'HODL', definition: 'A misspelling of "hold" that became a crypto meme meaning to hold long-term.', category: 'crypto', example: 'Many Bitcoiners believe in HODLing through market volatility.' },
  { term: 'Whale', definition: 'An individual or entity that holds a large amount of cryptocurrency.', category: 'crypto', example: 'Whales can significantly impact market prices with large transactions.' },
  { term: 'Altcoin', definition: 'Any cryptocurrency other than Bitcoin.', category: 'crypto', example: 'Ethereum, Cardano, and Solana are popular altcoins.' },
  { term: 'ICO', definition: 'Initial Coin Offering - a fundraising method for new cryptocurrency projects.', category: 'crypto', example: 'Many projects raised funds through ICOs in 2017-2018.' },
  { term: 'FOMO', definition: 'Fear Of Missing Out - buying due to fear of missing potential gains.', category: 'crypto', example: 'FOMO often leads to buying at market peaks.' },
  { term: 'FUD', definition: 'Fear, Uncertainty, and Doubt - negative information that may affect prices.', category: 'crypto', example: 'Regulatory FUD often causes crypto market sell-offs.' },
  { term: 'DYOR', definition: 'Do Your Own Research - advice to research before investing.', category: 'crypto', example: 'Never invest based on social media tips - always DYOR.' },
  { term: 'Moon', definition: 'When a cryptocurrency\'s price increases dramatically.', category: 'crypto', example: 'Bitcoin mooned to $69,000 in November 2021.' },
  { term: 'Diamond Hands', definition: 'Holding through market volatility and not selling.', category: 'crypto', example: 'Diamond hands held through the 2018 crypto winter.' },
  { term: 'Paper Hands', definition: 'Selling quickly when prices drop or at the first sign of profit.', category: 'crypto', example: 'Paper hands sold Bitcoin during the March 2020 crash.' },


  { term: 'Pip', definition: 'The smallest price move in forex trading, typically 0.0001 for most pairs.', category: 'forex', example: 'A 10-pip move in EUR/USD equals a $10 profit on a standard lot.' },
  { term: 'Lot', definition: 'A standardized unit of trading in forex markets.', category: 'forex', example: 'A standard lot equals 100,000 units of the base currency.' },
  { term: 'Base Currency', definition: 'The first currency in a forex pair, the one being bought or sold.', category: 'forex', example: 'In EUR/USD, EUR is the base currency.' },
  { term: 'Quote Currency', definition: 'The second currency in a forex pair, the one used to price the base currency.', category: 'forex', example: 'In EUR/USD, USD is the quote currency.' },
  { term: 'Spread', definition: 'The difference between the bid and ask price in forex.', category: 'forex', example: 'Major pairs typically have spreads of 1-3 pips.' },
  { term: 'Leverage', definition: 'Borrowed money used to increase potential returns on investment.', category: 'forex', example: '100:1 leverage allows trading $100,000 with $1,000 margin.' },
  { term: 'Margin', definition: 'The amount of money required to open and maintain a leveraged position.', category: 'forex', example: 'Margin requirements vary by broker and currency pair.' },
  { term: 'Margin Call', definition: 'A broker\'s demand for additional funds to maintain open positions.', category: 'forex', example: 'A margin call occurs when account equity falls below required margin.' },
  { term: 'Swap', definition: 'The interest paid or earned for holding a position overnight.', category: 'forex', example: 'Positive swap is earned when holding a high-interest currency.' },
  { term: 'Carry Trade', definition: 'Borrowing in a low-interest currency to invest in a high-interest currency.', category: 'forex', example: 'Borrowing JPY to invest in AUD is a popular carry trade.' },
  { term: 'Major Pairs', definition: 'The most traded currency pairs involving the US dollar.', category: 'forex', example: 'EUR/USD, GBP/USD, USD/JPY, and USD/CHF are major pairs.' },
  { term: 'Minor Pairs', definition: 'Currency pairs that don\'t include the US dollar.', category: 'forex', example: 'EUR/GBP, EUR/JPY, and GBP/JPY are minor pairs.' },
  { term: 'Exotic Pairs', definition: 'Currency pairs involving one major currency and one from a developing economy.', category: 'forex', example: 'USD/TRY, EUR/PLN, and GBP/ZAR are exotic pairs.' },
  { term: 'Central Bank', definition: 'The institution responsible for monetary policy in a country.', category: 'forex', example: 'The Federal Reserve is the central bank of the United States.' },
  { term: 'Interest Rate', definition: 'The cost of borrowing money, set by central banks.', category: 'forex', example: 'Higher interest rates typically strengthen a currency.' },
  { term: 'Economic Calendar', definition: 'A schedule of important economic events and data releases.', category: 'forex', example: 'Traders watch the economic calendar for GDP and employment data.' },
  { term: 'NFP', definition: 'Non-Farm Payrolls - monthly US employment report that affects forex markets.', category: 'forex', example: 'NFP data is released on the first Friday of each month.' },
  { term: 'Risk Sentiment', definition: 'Market attitude toward risk, affecting currency movements.', category: 'forex', example: 'During risk-off periods, safe-haven currencies like JPY strengthen.' },


  { term: 'Asset', definition: 'Anything of value that can be owned or controlled to produce positive economic value.', category: 'general', example: 'Stocks, bonds, real estate, and commodities are all assets.' },
  { term: 'Portfolio', definition: 'A collection of financial investments like stocks, bonds, and cash.', category: 'general', example: 'A diversified portfolio reduces overall investment risk.' },
  { term: 'Diversification', definition: 'Spreading investments across different assets to reduce risk.', category: 'general', example: 'Diversification across sectors and countries reduces portfolio volatility.' },
  { term: 'Risk Management', definition: 'The process of identifying, assessing, and controlling financial risks.', category: 'general', example: 'Stop losses and position sizing are key risk management tools.' },
  { term: 'Liquidity', definition: 'How quickly an asset can be converted to cash without affecting its price.', category: 'general', example: 'Cash and large-cap stocks are highly liquid assets.' },
  { term: 'Volatility', definition: 'The degree of variation in trading price over time.', category: 'general', example: 'High volatility means large price swings in short periods.' },
  { term: 'Market Cap', definition: 'The total value of a company\'s shares of stock.', category: 'general', example: 'Market cap = share price × number of outstanding shares.' },
  { term: 'Dividend', definition: 'A distribution of profits by a corporation to its shareholders.', category: 'general', example: 'Many companies pay quarterly dividends to shareholders.' },
  { term: 'Yield', definition: 'The income return on an investment, expressed as a percentage.', category: 'general', example: 'A bond with 5% yield pays $50 annually on a $1,000 investment.' },
  { term: 'Index', definition: 'A statistical measure of change in a securities market.', category: 'general', example: 'The S&P 500 is an index of 500 large US companies.' },
  { term: 'ETF', definition: 'Exchange-Traded Fund - a basket of securities that trades like a stock.', category: 'general', example: 'SPY is an ETF that tracks the S&P 500 index.' },
  { term: 'Mutual Fund', definition: 'A type of investment vehicle consisting of a portfolio of stocks, bonds, or other securities.', category: 'general', example: 'Mutual funds are managed by professional fund managers.' },
  { term: 'Bond', definition: 'A debt security that represents a loan made by an investor to a borrower.', category: 'general', example: 'Government bonds are considered safer than corporate bonds.' },
  { term: 'Commodity', definition: 'A basic good used in commerce that is interchangeable with other goods of the same type.', category: 'general', example: 'Gold, oil, and wheat are examples of commodities.' },
  { term: 'Derivative', definition: 'A financial contract whose value is derived from an underlying asset.', category: 'general', example: 'Options and futures are types of derivatives.' },
  { term: 'Hedge', definition: 'An investment made to reduce the risk of adverse price movements.', category: 'general', example: 'Investors hedge by buying put options to protect against stock declines.' },
  { term: 'Arbitrage', definition: 'The practice of taking advantage of price differences in different markets.', category: 'general', example: 'Arbitrageurs profit from price differences between exchanges.' },
  { term: 'Market Maker', definition: 'A firm that quotes both a buy and sell price for a security.', category: 'general', example: 'Market makers provide liquidity to financial markets.' },
  { term: 'Bid', definition: 'The price a buyer is willing to pay for a security.', category: 'general', example: 'The bid price is always lower than the ask price.' },
  { term: 'Ask', definition: 'The price a seller is willing to accept for a security.', category: 'general', example: 'The ask price is always higher than the bid price.' },
  { term: 'Spread', definition: 'The difference between the bid and ask prices.', category: 'general', example: 'Tight spreads indicate high liquidity in a market.' },
  { term: 'Commission', definition: 'A fee charged by a broker for executing a trade.', category: 'general', example: 'Many online brokers now offer commission-free stock trading.' },
  { term: 'Settlement', definition: 'The process of transferring securities from seller to buyer.', category: 'general', example: 'Stock trades typically settle two business days after the trade date.' },
  { term: 'Market Order', definition: 'An order to buy or sell immediately at the current market price.', category: 'general', example: 'Market orders execute quickly but may have price slippage.' },
  { term: 'Limit Order', definition: 'An order to buy or sell at a specific price or better.', category: 'general', example: 'Limit orders may not execute if the market doesn\'t reach the specified price.' },
  { term: 'Stop Order', definition: 'An order that becomes a market order when a specified price is reached.', category: 'general', example: 'Stop orders are often used to limit losses or protect profits.' }
]

const filteredLingo = computed(() => {
  let filtered = marketLingo.filter(term => {
    const matchesSearch = term.term.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         term.definition.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    if (activeCategory.value === 'all') {
      return matchesSearch
    } else {
      return term.category === activeCategory.value && matchesSearch
    }
  })
  
  return filtered.sort((a, b) => a.term.localeCompare(b.term))
})

const getCategoryCount = (category: 'trading' | 'technical' | 'fundamental' | 'crypto' | 'forex' | 'general') => {
  return marketLingo.filter(term => term.category === category).length
}
</script>

<template>
  <div class="min-h-screen bg-gray-900">
    <div class="container mx-auto px-4 py-8">
      <div class="bg-white rounded-lg shadow-lg p-6">
        <h1 class="text-3xl font-bold text-gray-900 mb-6 text-center">Market Lingo Dictionary</h1>
        
        <div class="mb-6">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search terms or definitions..."
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        
        <div class="flex flex-wrap gap-2 mb-6">
          <button
            @click="activeCategory = 'all'"
            :class="activeCategory === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
            class="px-4 py-2 rounded-lg font-medium transition-colors"
          >
            All ({{ marketLingo.length }})
          </button>
          <button
            @click="activeCategory = 'trading'"
            :class="activeCategory === 'trading' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
            class="px-4 py-2 rounded-lg font-medium transition-colors"
          >
            Trading ({{ getCategoryCount('trading') }})
          </button>
          <button
            @click="activeCategory = 'technical'"
            :class="activeCategory === 'technical' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
            class="px-4 py-2 rounded-lg font-medium transition-colors"
          >
            Technical ({{ getCategoryCount('technical') }})
          </button>
          <button
            @click="activeCategory = 'fundamental'"
            :class="activeCategory === 'fundamental' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
            class="px-4 py-2 rounded-lg font-medium transition-colors"
          >
            Fundamental ({{ getCategoryCount('fundamental') }})
          </button>
          <button
            @click="activeCategory = 'crypto'"
            :class="activeCategory === 'crypto' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
            class="px-4 py-2 rounded-lg font-medium transition-colors"
          >
            Crypto ({{ getCategoryCount('crypto') }})
          </button>
          <button
            @click="activeCategory = 'forex'"
            :class="activeCategory === 'forex' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
            class="px-4 py-2 rounded-lg font-medium transition-colors"
          >
            Forex ({{ getCategoryCount('forex') }})
          </button>
          <button
            @click="activeCategory = 'general'"
            :class="activeCategory === 'general' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
            class="px-4 py-2 rounded-lg font-medium transition-colors"
          >
            General ({{ getCategoryCount('general') }})
          </button>
        </div>
        
        <div class="space-y-4">
          <div
            v-for="term in filteredLingo"
            :key="`${term.term}-${term.category}`"
            class="bg-gray-50 rounded-lg p-6 border border-gray-200 hover:shadow-md transition-shadow"
          >
            <div class="flex items-start justify-between mb-3">
              <h3 class="text-xl font-bold text-gray-900">{{ term.term }}</h3>
              <span
                :class="{
                  'bg-green-100 text-green-800': term.category === 'trading',
                  'bg-blue-100 text-blue-800': term.category === 'technical',
                  'bg-purple-100 text-purple-800': term.category === 'fundamental',
                  'bg-orange-100 text-orange-800': term.category === 'crypto',
                  'bg-red-100 text-red-800': term.category === 'forex',
                  'bg-gray-100 text-gray-800': term.category === 'general'
                }"
                class="px-3 py-1 text-xs font-medium rounded-full"
              >
                {{ term.category }}
              </span>
            </div>
            <p class="text-gray-700 mb-3">{{ term.definition }}</p>
            <div v-if="term.example" class="bg-blue-50 border-l-4 border-blue-400 p-3 rounded">
              <p class="text-sm text-blue-800">
                <span class="font-semibold">Example:</span> {{ term.example }}
              </p>
            </div>
          </div>
        </div>
        
        <div v-if="filteredLingo.length === 0" class="text-center py-8">
          <p class="text-gray-500 text-lg">No terms found matching your search.</p>
        </div>
      </div>
    </div>
  </div>
</template> 