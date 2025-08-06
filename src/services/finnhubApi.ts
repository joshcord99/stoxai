import axios from "axios";

// Function to get API key at runtime to prevent embedding in build
const getFinnhubApiKey = (): string | undefined => {
  // Only access environment variable if we're in a browser environment
  if (typeof window !== 'undefined') {
    return import.meta.env.VITE_FINNHUB_API_KEY;
  }
  return undefined;
};

const BASE_URL = "https://finnhub.io/api/v1";

interface StockQuote {
  symbol: string;
  currentPrice: number;
  change: number;
  changePercent: number;
  high: number;
  low: number;
  open: number;
  previousClose: number;
  type: "stock";
}

interface FinnhubQuoteResponse {
  c: number;
  d: number;
  dp: number
  h: number;
  l: number;
  o: number;
  pc: number;
}

interface NewsItem {
  headline: string;
  category: string;
  datetime: number;
  id: number;
  image: string;
  related: string;
  source: string;
  summary: string;
  url: string;
}

export const finnhubApi = {
  hasApiKey(): boolean {
    const FINNHUB_API_KEY = getFinnhubApiKey();
    return !!(
      FINNHUB_API_KEY &&
      FINNHUB_API_KEY !== "your_finnhub_api_key_here" &&
      FINNHUB_API_KEY !== "unknown" &&
      FINNHUB_API_KEY !== "undefined" &&
      FINNHUB_API_KEY !== ""
    );
  },

  async getStockQuote(symbol: string): Promise<StockQuote | null> {
    if (!this.hasApiKey()) {
      return null;
    }

    const FINNHUB_API_KEY = getFinnhubApiKey();

    try {
      const response = await axios.get<FinnhubQuoteResponse>(
        `${BASE_URL}/quote`,
        {
          params: {
            symbol: symbol,
            token: FINNHUB_API_KEY,
          },
        }
      );

      if (response.data && response.data.c) {
        return {
          symbol: symbol,
          currentPrice: response.data.c,
          change: response.data.d,
          changePercent: response.data.dp,
          high: response.data.h,
          low: response.data.l,
          open: response.data.o,
          previousClose: response.data.pc,
          type: "stock",
        };
      }
      return null;
    } catch (error) {
      console.error(`Error fetching stock quote for ${symbol}:`, error);
      return null;
    }
  },

  async getMultipleStockQuotes(symbols: string[]): Promise<StockQuote[]> {
    const quotes: StockQuote[] = [];

    for (const symbol of symbols) {
      const quote = await this.getStockQuote(symbol);
      if (quote) {
        quotes.push(quote);
      }
  
      await new Promise((resolve) => setTimeout(resolve, 100));
    }

    return quotes;
  },

  async getMarketNews(
    categories: string[] = ["forex", "crypto", "general"]
  ): Promise<string[]> {
    if (!this.hasApiKey()) {
      return [];
    }

    try {
      let allNews: NewsItem[] = [];

      for (const category of categories) {
        try {
          const response = await axios.get<NewsItem[]>(`${BASE_URL}/news`, {
            params: {
              category: category,
              token: getFinnhubApiKey(),
            },
          });

          if (response.data && Array.isArray(response.data)) {
            allNews = allNews.concat(response.data);
          }
        } catch (error) {
          console.error(`Error fetching news for category ${category}:`, error);
        }
      }

      if (allNews.length > 0) {
        const marketKeywords = [
          "stock",
          "market",
          "trading",
          "invest",
          "earnings",
          "revenue",
          "profit",
          "loss",
          "crypto",
          "bitcoin",
          "ethereum",
          "blockchain",
          "forex",
          "currency",
          "dollar",
          "fed",
          "federal reserve",
          "interest rate",
          "inflation",
          "economy",
          "economic",
          "nasdaq",
          "dow",
          "s&p",
          "sp500",
          "nyse",
          "exchange",
          "shares",
          "equity",
          "bond",
          "treasury",
          "yield",
          "dividend",
          "ipo",
          "merger",
          "acquisition",
          "bull",
          "bear",
          "rally",
          "crash",
          "volatility",
          "volatile",
          "rally",
          "dip",
          "commodity",
          "oil",
          "gold",
          "silver",
          "copper",
          "aluminum",
          "natural gas",
          "central bank",
          "monetary policy",
          "quantitative easing",
          "tapering",
          "securities",
          "derivatives",
          "options",
          "futures",
          "hedge fund",
          "mutual fund",
          "etf",
          "index fund",
          "portfolio",
          "asset allocation",
          "risk management",
          "market cap",
          "valuation",
          "pe ratio",
          "price target",
          "analyst rating",
          "short selling",
          "margin trading",
          "leverage",
          "liquidity",
          "market maker",
        ];

        const marketRelatedNews = allNews.filter((item: NewsItem) => {
          const headline = item.headline.toLowerCase();
          return marketKeywords.some((keyword) => headline.includes(keyword));
        });

        return marketRelatedNews.slice(0, 15).map((item) => item.headline);
      }

      return [];
    } catch (error) {
      console.error("Error fetching market news:", error);
      return [];
    }
  },

  getDemoStockQuotes(): StockQuote[] {
    return [
      {
        symbol: "AAPL",
        currentPrice: 150.25,
        change: 2.15,
        changePercent: 1.45,
        high: 152.0,
        low: 148.5,
        open: 149.1,
        previousClose: 148.1,
        type: "stock",
      },
      {
        symbol: "MSFT",
        currentPrice: 320.5,
        change: -1.2,
        changePercent: -0.37,
        high: 322.0,
        low: 318.0,
        open: 321.7,
        previousClose: 321.7,
        type: "stock",
      },
      {
        symbol: "GOOGL",
        currentPrice: 2800.75,
        change: 15.3,
        changePercent: 0.55,
        high: 2810.0,
        low: 2785.0,
        open: 2785.45,
        previousClose: 2785.45,
        type: "stock",
      },
    ];
  },
};
