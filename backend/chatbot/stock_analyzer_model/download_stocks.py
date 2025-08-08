import yfinance as yf
import os

tickers = {
    "Tech": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "ADBE", "CRM",
             "PYPL", "INTC", "AMD", "ORCL", "CSCO", "IBM", "QCOM", "TXN", "AVGO", "MU",
             "AMAT", "KLAC", "LRCX", "ADI", "MCHP", "ASML", "TSM"],
    "Telecommunications": ["TMUS", "VZ", "T", "CMCSA", "CHTR", "DISH", "LUMN", "CTL", "VZ", "T"],
    "Financial": ["JPM", "BAC", "WFC", "GS", "MS", "C", "USB", "PNC", "TFC", "COF"],
    "Healthcare": ["JNJ", "PFE", "UNH", "ABBV", "MRK", "TMO", "ABT", "DHR", "BMY", "AMGN"],
    "Energy": ["XOM", "CVX", "COP", "EOG", "SLB", "PSX", "VLO", "MPC", "HAL", "BKR"],
    "ConsumerRetail": ["DIS", "NKE", "HD", "LOW", "COST", "TGT", "WMT", "SBUX", "MCD", "KO", "PEP", "PG"],
    "Industrial": ["BA", "CAT", "GE", "MMM", "HON", "UPS", "FDX", "RTX", "LMT", "NOC"],
    "RealEstate": ["SPG", "PLD", "AMT", "CCI", "EQIX", "DLR", "PSA", "O", "WELL", "VICI"],
    "Materials": ["LIN", "APD", "FCX", "NEM", "BLL", "SHW", "ECL", "APD", "NUE", "X"],
    "Utilities": ["NEE", "DUK", "SO", "D", "AEP", "SRE", "XEL", "DTE", "WEC", "ED"],
    "ConsumerDiscretionary": ["AMZN", "TSLA", "HD", "MCD", "NKE", "SBUX", "LOW", "TJX", "BKNG", "MAR"],
    "ConsumerStaples": ["PG", "KO", "PEP", "WMT", "COST", "PM", "MO", "CL", "GIS", "KMB"],
    "CommunicationServices": ["GOOGL", "META", "NFLX", "DIS", "CMCSA", "CHTR", "VZ", "T", "TMUS", "DISH"],
    "StaticMarket": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "ADBE", "CRM",
                     "PYPL", "INTC", "AMD", "ORCL", "CSCO"],
    "BackendStock": ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "META", "NVDA"],
    "Crypto": [
        "BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD", "XRP-USD", "DOT-USD", "LINK-USD", "LTC-USD",
        "BCH-USD", "UNI-USD", "ATOM-USD", "VET-USD", "TRX-USD", "ETC-USD", "ALGO-USD", "SOL-USD",
        "MATIC-USD", "AVAX-USD", "FTM-USD", "NEAR-USD", "ICP-USD", "FIL-USD", "XTZ-USD",
        "THETA-USD", "CAKE-USD", "CHZ-USD", "HOT-USD", "DOGE-USD", "SHIB-USD", "MANA-USD",
        "SAND-USD", "ENJ-USD", "AXS-USD", "GALA-USD"
    ]
}

base_dir = 'market_data'
os.makedirs(base_dir, exist_ok=True)

for category, symbols in tickers.items():
    category_dir = os.path.join(base_dir, category)
    os.makedirs(category_dir, exist_ok=True)
    for symbol in symbols:
        print(f"Downloading {symbol} in {category}...")
        try:
            data = yf.download(symbol, start='2000-01-01', end='2025-08-01', interval='1d')
            if not data.empty:
                data.to_csv(os.path.join(category_dir, f"{symbol.replace('-', '_')}_history.csv"))
            else:
                print(f"No data returned for {symbol}")
        except Exception as e:
            print(f"Failed to download {symbol}: {e}")

print("All stock and crypto data downloaded.")
