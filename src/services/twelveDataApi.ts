import axios from "axios";
const getTwelveDataApiKey = (): string | undefined => {
  if (typeof window !== 'undefined') {
    return import.meta.env.VITE_TWELVE_DATA_API_KEY;
  }
  return undefined;
};

const BASE_URL = "https://api.twelvedata.com";

interface CryptoQuote {
  symbol: string;
  currentPrice: number;
  change: number;
  changePercent: number;
  high: number;
  low: number;
  open: number;
  previousClose: number;
  type: "crypto";
}

interface TwelveDataQuoteResponse {
  symbol: string;
  close: string;
  change: string;
  percent_change: string;
  high: string;
  low: string;
  open: string;
  previous_close: string;
}

interface SymbolSearchResponse {
  data: Array<{
    symbol: string;
    instrument_name: string;
    exchange: string;
    instrument_type: string;
    country: string;
    currency: string;
  }>;
}

export const twelveDataApi = {
  hasApiKey(): boolean {
    const TWELVE_DATA_API_KEY = getTwelveDataApiKey();
    return !!(
      TWELVE_DATA_API_KEY &&
      TWELVE_DATA_API_KEY !== "your_twelve_data_api_key_here" &&
      TWELVE_DATA_API_KEY !== "unknown" &&
      TWELVE_DATA_API_KEY !== "undefined" &&
      TWELVE_DATA_API_KEY !== ""
    );
  },

  async getCryptoQuote(symbol: string): Promise<CryptoQuote | null> {
    if (!this.hasApiKey()) {
      return null;
    }

    const TWELVE_DATA_API_KEY = getTwelveDataApiKey();

    try {
      const cleanSymbol = symbol.replace("BINANCE:", "");

      const response = await axios.get<TwelveDataQuoteResponse>(
        `${BASE_URL}/quote`,
        {
          params: {
            symbol: cleanSymbol,
            apikey: TWELVE_DATA_API_KEY,
          },
        }
      );

      if (
        response.data &&
        response.data.symbol &&
        response.data.close &&
        response.data.previous_close
      ) {
        const data = response.data;

        return {
          symbol: cleanSymbol,
          currentPrice: parseFloat(data.close),
          change: parseFloat(data.change),
          changePercent: parseFloat(data.percent_change),
          high: parseFloat(data.high),
          low: parseFloat(data.low),
          open: parseFloat(data.open),
          previousClose: parseFloat(data.previous_close),
          type: "crypto",
        };
      }
      return null;
    } catch (error) {
      console.warn(`Failed to fetch crypto data for ${symbol}:`, error);
      return null;
    }
  },

  async getMultipleCryptoQuotes(symbols: string[]): Promise<CryptoQuote[]> {
    const quotes: CryptoQuote[] = [];

    for (const symbol of symbols) {
      const quote = await this.getCryptoQuote(symbol);
      if (quote) {
        quotes.push(quote);
      }
     
      await new Promise((resolve) => setTimeout(resolve, 100));
    }

    return quotes;
  },

  async searchSymbols(
    query: string
  ): Promise<Array<{ symbol: string; name: string }>> {
    if (!this.hasApiKey()) {
      return [];
    }

    const TWELVE_DATA_API_KEY = getTwelveDataApiKey();

    try {
      const response = await axios.get<SymbolSearchResponse>(
        `${BASE_URL}/symbol_search`,
        {
          params: {
            symbol: query,
            apikey: TWELVE_DATA_API_KEY,
          },
        }
      );

      if (response.data && response.data.data) {
        return response.data.data.map((item) => ({
          symbol: item.symbol,
          name: item.instrument_name,
        }));
      }
      return [];
    } catch (error) {
      console.error("Error searching symbols:", error);
      return [];
    }
  },

  getDemoCryptoQuotes(): CryptoQuote[] {
    return [
      {
        symbol: "BTC",
        currentPrice: 45000.0,
        change: 500.0,
        changePercent: 1.12,
        high: 45200.0,
        low: 44800.0,
        open: 44500.0,
        previousClose: 44500.0,
        type: "crypto",
      },
      {
        symbol: "ETH",
        currentPrice: 3200.5,
        change: -25.0,
        changePercent: -0.77,
        high: 3250.0,
        low: 3180.0,
        open: 3225.5,
        previousClose: 3225.5,
        type: "crypto",
      },
    ];
  },
};
