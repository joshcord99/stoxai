import os
import sys
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))


from chatbot.stock_analyzer_model.stock_analyzer import StockAnalyzer

class BasicChatbot:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.market_data_path = os.path.abspath(
            os.path.join(current_dir, '..', 'stock-data-collector', 'market_data')
        )
        self.analyzer = StockAnalyzer(data_dir=self.market_data_path)
        self.conversation_history = []
        self.max_history_length = 10

    def process_question(self, question):
        """Process user question with basic technical analysis"""
        try:
            if self._is_general_conversation(question):
                return self._handle_general_conversation(question)
            
    
            symbol = self._extract_symbol_from_input(question)
            
            if symbol:
                data = self.analyzer.generate_investment_advice(symbol)
                if data and 'error' not in data:
                    prediction = self._generate_market_prediction(data, symbol)
                    
                    return (
                        f"**Technical Analysis**\n\n"
                        f"{self._format_basic_analysis(data)}\n\n"
                        f"**Market Prediction**:\n{prediction}\n\n"
                        f"**Note**: This analysis is based on technical indicators and historical data."
                    )
                else:
                    return (
                        f"**Analysis**\n\n"
                        f"I couldn't find data for {symbol}. "
                        f"Available symbols include: AAPL, MSFT, GOOGL, TSLA, BTC, ETH, and more.\n\n"
                        f"Please try asking about a specific stock symbol and I'll provide technical analysis."
                    )
            else:
                return (
                    f"**Technical Analysis**\n\n"
                    f"I can provide technical analysis using historical data.\n\n"
                    f"Available symbols: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA, BTC, ETH, and more.\n\n"
                    f"Please ask about a specific stock or crypto symbol for detailed analysis."
                )
                
        except Exception as e:
            print("[ERROR] Basic chatbot error:", e)
            return (
                f"**Technical Analysis**\n\n"
                f"I can provide technical analysis using historical data.\n\n"
                f"Available symbols: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA, BTC, ETH, and more.\n\n"
                f"Please ask about a specific stock or crypto symbol for detailed analysis."
            )

    def _is_general_conversation(self, q):
        return any(p in q.lower() for p in ['hi', 'hello', 'bye', 'thanks', 'thank you'])

    def _handle_general_conversation(self, q):
        return (
            f"**Technical Analysis Assistant**\n\n"
            f"Hello! I'm your technical analysis assistant. I can provide comprehensive stock and crypto analysis "
            f"using historical data and technical indicators.\n\n"
            f"Available symbols: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA, BTC, ETH, and more.\n\n"
            f"Ask me about any stock or cryptocurrency for detailed technical analysis!"
        )

    def _format_basic_analysis(self, data):
        return (
            f"**{data.get('symbol', 'Symbol')} Technical Analysis**\n\n"
            f"**Price Information:**\n"
            f"   • Current Price: ${data.get('current_price', 0):.2f}\n"
            f"   • Price Change: {data.get('price_change_pct', 0):+.2f}% (${data.get('price_change', 0):+.2f})\n"
            f"   • 52-Week Range: ${data.get('low_52w', 0):.2f} - ${data.get('high_52w', 0):.2f}\n\n"
            f"**Technical Analysis:**\n"
            f"   • Trend Direction: {data.get('trend', 'N/A')}\n"
            f"   • Volatility: {data.get('volatility', 0):.2f}%\n"
            f"   • Support Level: ${data.get('support', 0):.2f}\n"
            f"   • Resistance Level: ${data.get('resistance', 0):.2f}\n\n"
            f"**Investment Assessment:**\n"
            f"   • Recommendation: {data.get('recommendation', 'N/A')}\n"
            f"   • Risk Score: {data.get('risk_score', 'N/A')}/10\n"
            f"   • P/E Ratio: {data.get('pe_ratio', 'N/A')}\n"
            f"   • Market Cap: {data.get('market_cap', 'N/A')}\n\n"
            f"**Key Insights:**\n"
            f"   • This analysis is based on technical indicators and historical data\n"
            f"   • Consider your investment goals and risk tolerance\n"
            f"   • Always diversify your portfolio and never invest more than you can afford to lose\n"
            f"   • For more detailed analysis, try asking specific questions about this stock"
        )

    def _generate_market_prediction(self, data, symbol):
        """Generate market prediction based on technical analysis"""
        try:
            trend = data.get('trend', 'UNKNOWN')
            volatility = data.get('volatility', 0)
            risk_score = data.get('risk_score', 5)
            recommendation = data.get('recommendation', 'HOLD')
            
            prediction = ""
            
            if trend == 'STRONG_UPTREND':
                prediction += f"**Bullish Outlook**: {symbol} shows strong upward momentum with technical indicators supporting continued growth.\n"
            elif trend == 'UPTREND':
                prediction += f"**Moderate Growth**: {symbol} is trending upward with positive technical signals.\n"
            elif trend == 'STRONG_DOWNTREND':
                prediction += f"**Bearish Outlook**: {symbol} shows strong downward pressure with technical indicators suggesting further decline.\n"
            elif trend == 'DOWNTREND':
                prediction += f"**Moderate Decline**: {symbol} is trending downward with negative technical signals.\n"
            else:
                prediction += f"**Sideways Movement**: {symbol} shows mixed signals with no clear directional trend.\n"
            
            if recommendation == 'STRONG_BUY':
                prediction += f"**Recommendation**: Strong buy signal based on technical analysis.\n"
            elif recommendation == 'BUY':
                prediction += f"**Recommendation**: Buy signal with positive technical indicators.\n"
            elif recommendation == 'STRONG_SELL':
                prediction += f"**Recommendation**: Strong sell signal based on technical analysis.\n"
            elif recommendation == 'SELL':
                prediction += f"**Recommendation**: Sell signal with negative technical indicators.\n"
            else:
                prediction += f"**Recommendation**: Hold position, monitor for clearer signals.\n"
            
            if volatility > 20:
                prediction += f"**High Volatility**: Expect significant price swings. Consider position sizing.\n"
            elif volatility > 10:
                prediction += f"**Moderate Volatility**: Normal market fluctuations expected.\n"
            else:
                prediction += f"**Low Volatility**: Relatively stable price movements.\n"
            
            if risk_score >= 7:
                prediction += f"**High Risk**: Consider smaller position sizes and strict stop-losses.\n"
            elif risk_score >= 4:
                prediction += f"**Moderate Risk**: Standard risk management recommended.\n"
            else:
                prediction += f"**Lower Risk**: Generally safer investment with lower volatility.\n"
            
            return prediction
            
        except Exception as e:
            print("[ERROR] _generate_market_prediction:", e)
            return "**Technical Analysis**: Based on historical data and technical indicators."

    def _extract_symbol_from_input(self, user_input):
        common_symbols = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'CRM', 'ADBE',
            'PYPL', 'INTC', 'AMD', 'CSCO', 'ORCL', 'IBM', 'QCOM', 'AVGO', 'TXN', 'MU',
            'TMUS', 'VZ', 'T', 'CMCSA', 'CHTR', 'DISH', 'LUMN', 'CTL',
            'JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'USB', 'PNC', 'TFC', 'COF',
            'JNJ', 'PFE', 'UNH', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'BMY', 'AMGN',
            'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'PSX', 'VLO', 'MPC', 'HAL', 'BKR',
            'DIS', 'NKE', 'HD', 'LOW', 'COST', 'TGT', 'WMT', 'SBUX', 'MCD', 'KO', 'PEP', 'PG',
            'BA', 'CAT', 'GE', 'MMM', 'HON', 'UPS', 'FDX', 'RTX', 'LMT', 'NOC',
            'SPG', 'PLD', 'AMT', 'CCI', 'EQIX', 'DLR', 'PSA', 'WELL', 'VICI',
            'LIN', 'APD', 'FCX', 'NEM', 'BLL', 'SHW', 'ECL', 'NUE', 'X',
            'NEE', 'DUK', 'SO', 'D', 'AEP', 'SRE', 'XEL', 'DTE', 'WEC', 'ED',
            'TJX', 'BKNG', 'MAR', 'PM', 'MO', 'CL', 'GIS', 'KMB',
            'BTC', 'ETH', 'ADA', 'DOT', 'LINK', 'LTC', 'BCH', 'XRP', 'BNB', 'SOL',
            'MATIC', 'AVAX', 'UNI', 'ATOM', 'FTM', 'NEAR', 'ALGO', 'VET', 'MANA', 'SAND'
        ]
        
        company_to_symbol = {
            'APPLE': 'AAPL',
            'MICROSOFT': 'MSFT',
            'GOOGLE': 'GOOGL',
            'AMAZON': 'AMZN',
            'TESLA': 'TSLA',
            'FACEBOOK': 'META',
            'META': 'META',
            'NVIDIA': 'NVDA',
            'NETFLIX': 'NFLX',
            'SALESFORCE': 'CRM',
            'ADOBE': 'ADBE',
            'PAYPAL': 'PYPL',
            'INTEL': 'INTC',
            'AMD': 'AMD',
            'CISCO': 'CSCO',
            'ORACLE': 'ORCL',
            'IBM': 'IBM',
            'QUALCOMM': 'QCOM',
            'BROADCOM': 'AVGO',
            'TEXAS INSTRUMENTS': 'TXN',
            'MICRON': 'MU',
            'T-MOBILE': 'TMUS',
            'TMUS': 'TMUS',
            'VERIZON': 'VZ',
            'VZ': 'VZ',
            'AT&T': 'T',
            'COMCAST': 'CMCSA',
            'CHARTER': 'CHTR',
            'DISH': 'DISH',
            'LUMEN': 'LUMN',
            'CENTURYLINK': 'CTL',
            'JPMORGAN': 'JPM',
            'BANK OF AMERICA': 'BAC',
            'WELLS FARGO': 'WFC',
            'GOLDMAN SACHS': 'GS',
            'MORGAN STANLEY': 'MS',
            'CITIGROUP': 'C',
            'US BANCORP': 'USB',
            'PNC': 'PNC',
            'TRUIST': 'TFC',
            'CAPITAL ONE': 'COF',
            'JOHNSON & JOHNSON': 'JNJ',
            'PFIZER': 'PFE',
            'UNITEDHEALTH': 'UNH',
            'ABBVIE': 'ABBV',
            'MERCK': 'MRK',
            'THERMO FISHER': 'TMO',
            'ABBOTT': 'ABT',
            'DANAHER': 'DHR',
            'BRISTOL MYERS': 'BMY',
            'AMGEN': 'AMGN',
            'EXXON': 'XOM',
            'CHEVRON': 'CVX',
            'CONOCOPHILLIPS': 'COP',
            'EOG': 'EOG',
            'SCHLUMBERGER': 'SLB',
            'PHILLIPS 66': 'PSX',
            'VALERO': 'VLO',
            'MARATHON': 'MPC',
            'HALLIBURTON': 'HAL',
            'BAKER HUGHES': 'BKR',
            'DISNEY': 'DIS',
            'NIKE': 'NKE',
            'HOME DEPOT': 'HD',
            'LOWES': 'LOW',
            'COSTCO': 'COST',
            'TARGET': 'TGT',
            'WALMART': 'WMT',
            'STARBUCKS': 'SBUX',
            'MCDONALDS': 'MCD',
            'COCA COLA': 'KO',
            'PEPSICO': 'PEP',
            'PROCTER & GAMBLE': 'PG',
            'BOEING': 'BA',
            'CATERPILLAR': 'CAT',
            'GENERAL ELECTRIC': 'GE',
            '3M': 'MMM',
            'HONEYWELL': 'HON',
            'UPS': 'UPS',
            'FEDEX': 'FDX',
            'RAYTHEON': 'RTX',
            'LOCKHEED': 'LMT',
            'NORTHROP': 'NOC',
            'SIMON PROPERTY': 'SPG',
            'PROLOGIS': 'PLD',
            'AMERICAN TOWER': 'AMT',
            'CROWN CASTLE': 'CCI',
            'EQUINIX': 'EQIX',
            'DIGITAL REALTY': 'DLR',
            'PUBLIC STORAGE': 'PSA',
            'REALTY INCOME': 'O',
            'WELLTOWER': 'WELL',
            'VICI': 'VICI',
            'LINDE': 'LIN',
            'AIR PRODUCTS': 'APD',
            'FREEPORT': 'FCX',
            'NEWMONT': 'NEM',
            'BALL': 'BLL',
            'SHERWIN WILLIAMS': 'SHW',
            'ECOLAB': 'ECL',
            'NUCOR': 'NUE',
            'US STEEL': 'X',
            'NEXTERA': 'NEE',
            'DUKE ENERGY': 'DUK',
            'SOUTHERN': 'SO',
            'DOMINION': 'D',
            'AMERICAN ELECTRIC': 'AEP',
            'SEMPRA': 'SRE',
            'XCEL': 'XEL',
            'DTE': 'DTE',
            'WEC': 'WEC',
            'CONSOLIDATED EDISON': 'ED',
            'TJX': 'TJX',
            'BOOKING': 'BKNG',
            'MARRIOTT': 'MAR',
            'PHILIP MORRIS': 'PM',
            'ALTRIA': 'MO',
            'COLGATE': 'CL',
            'GENERAL MILLS': 'GIS',
            'KIMBERLY CLARK': 'KMB',
            'BITCOIN': 'BTC',
            'ETHEREUM': 'ETH',
            'CARDANO': 'ADA',
            'POLKADOT': 'DOT',
            'CHAINLINK': 'LINK',
            'LITECOIN': 'LTC',
            'BITCOIN CASH': 'BCH',
            'RIPPLE': 'XRP',
            'BINANCE COIN': 'BNB',
            'SOLANA': 'SOL',
            'POLYGON': 'MATIC',
            'AVALANCHE': 'AVAX',
            'UNISWAP': 'UNI',
            'COSMOS': 'ATOM',
            'FANTOM': 'FTM',
            'NEAR': 'NEAR',
            'ALGORAND': 'ALGO',
            'VE CHAIN': 'VET',
            'DECENTRALAND': 'MANA',
            'SAND': 'SAND'
        }
        
        user_input_upper = user_input.upper()
        

  
        sorted_symbols = sorted(common_symbols, key=len, reverse=True)
        
        for symbol in sorted_symbols:
            if symbol in user_input_upper:
                return symbol
        

        for company, symbol in company_to_symbol.items():
            if company in user_input_upper:
                return symbol
        
        
        for company, symbol in company_to_symbol.items():
            if company.lower() in user_input.lower():
                return symbol
        
        return None

    def _add_to_history(self, question, response):
        self.conversation_history.append({
            "user": question,
            "bot": response,
            "timestamp": datetime.now().isoformat()
        })
        self.conversation_history = self.conversation_history[-self.max_history_length:]

    def clear_history(self):
        self.conversation_history = []

    def get_available_assets(self):
        return [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'CRM', 'ADBE',
            'PYPL', 'INTC', 'AMD', 'CSCO', 'ORCL', 'IBM', 'QCOM', 'AVGO', 'TXN', 'MU',
            'TMUS', 'VZ', 'T', 'CMCSA', 'CHTR', 'DISH', 'LUMN', 'CTL',
            'JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'USB', 'PNC', 'TFC', 'COF',
            'JNJ', 'PFE', 'UNH', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'BMY', 'AMGN',
            'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'PSX', 'VLO', 'MPC', 'HAL', 'BKR',
            'DIS', 'NKE', 'HD', 'LOW', 'COST', 'TGT', 'WMT', 'SBUX', 'MCD', 'KO', 'PEP', 'PG',
            'BA', 'CAT', 'GE', 'MMM', 'HON', 'UPS', 'FDX', 'RTX', 'LMT', 'NOC',
            'SPG', 'PLD', 'AMT', 'CCI', 'EQIX', 'DLR', 'PSA', 'O', 'WELL', 'VICI',
            'LIN', 'APD', 'FCX', 'NEM', 'BLL', 'SHW', 'ECL', 'NUE', 'X',
            'NEE', 'DUK', 'SO', 'D', 'AEP', 'SRE', 'XEL', 'DTE', 'WEC', 'ED',
            'TJX', 'BKNG', 'MAR', 'PM', 'MO', 'CL', 'GIS', 'KMB',
            'BTC', 'ETH', 'ADA', 'DOT', 'LINK', 'LTC', 'BCH', 'XRP', 'BNB', 'SOL',
            'MATIC', 'AVAX', 'UNI', 'ATOM', 'FTM', 'NEAR', 'ALGO', 'VET', 'MANA', 'SAND'
        ] 