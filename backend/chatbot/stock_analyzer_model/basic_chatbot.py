import os
import sys
from datetime import datetime


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))


from .stock_analyzer import StockAnalyzer

class BasicChatbot:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.market_data_path = os.path.abspath(
            os.path.join(current_dir, '..', '..', 'stock-data-collector', 'market_data')
        )
        self.analyzer = StockAnalyzer(data_dir=self.market_data_path)
        self.conversation_history = []
        self.max_history_length = 10

    def process_question(self, question):
        """Process user question with basic technical analysis"""
        try:
            # AI-powered question classification
            question_type = self._classify_question_type(question)
            
            # Route based on AI classification
            if question_type == "GENERAL_CONVERSATION":
                return self._handle_general_conversation(question)
            elif question_type == "WATCHLIST_QUERY":
                return self._handle_watchlist_question(question)
            elif question_type == "STOCK_ANALYSIS":
                return self._handle_stock_analysis(question)
            elif question_type == "ACCOUNT_INFO":
                return self._handle_account_question(question)
            elif question_type == "FINANCIAL_ADVICE":
                return self._handle_general_financial_question(question)
            else:
                return self._handle_unknown_question(question)
                
        except Exception as e:
            print("[ERROR] Basic chatbot error:", e)
            return (
                f"**Technical Analysis**\n\n"
                f"I can provide technical analysis using historical data.\n\n"
                f"Available symbols: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA, BTC, ETH, and more.\n\n"
                f"Please ask about a specific stock or crypto symbol for detailed analysis."
            )

    def _is_general_conversation(self, q):
        """Legacy method - now handled by AI classification"""
        general_keywords = [
            'hi', 'hello', 'bye', 'thanks', 'thank you', 'how are you', 'good morning', 
            'good afternoon', 'good evening', 'weather', 'temperature', 'hot', 'cold',
            'nice day', 'beautiful day', 'weekend', 'holiday', 'vacation', 'work',
            'family', 'friend', 'home', 'food', 'dinner', 'lunch', 'breakfast',
            'coffee', 'tea', 'water', 'exercise', 'gym', 'sports', 'movie', 'music',
            'book', 'reading', 'sleep', 'rest', 'relax', 'stress', 'busy', 'tired'
        ]
        return any(keyword in q.lower() for keyword in general_keywords)

    def _handle_general_conversation(self, q):
        user_info = self._extract_user_info(q)
        user_name = user_info['name'] if user_info else 'there'
        
        q_lower = q.lower()
        
        if any(word in q_lower for word in ['weather', 'temperature', 'hot', 'cold', 'nice day', 'beautiful day']):
            return (
                f"**Weather Chat**\n\n"
                f"Hello {user_name}! I'm actually a financial analysis assistant, so I can't provide weather information. "
                f"But I'd be happy to help you with investment analysis!\n\n"
                f"**What I can help with:**\n"
                f"• Stock analysis (AAPL, TSLA, GOOGL, etc.)\n"
                f"• Cryptocurrency insights (BTC, ETH, etc.)\n"
                f"• Investment recommendations\n"
                f"• Market trends and predictions\n\n"
                f"Try asking me about stocks or crypto instead!"
            )
        elif any(word in q_lower for word in ['how are you', 'how you doing', 'how do you do']):
            return (
                f"**Greeting**\n\n"
                f"Hello {user_name}! I'm doing well, thank you for asking! I'm your financial analysis assistant "
                f"and I'm ready to help you with investment decisions.\n\n"
                f"**What I can help with:**\n"
                f"• Stock analysis and recommendations\n"
                f"• Cryptocurrency insights\n"
                f"• Market trends and predictions\n"
                f"• Investment strategies\n\n"
                f"Ask me about any stock or crypto for detailed analysis!"
            )
        elif any(word in q_lower for word in ['work', 'job', 'busy', 'tired', 'stress']):
            return (
                f"**Work Life**\n\n"
                f"Hello {user_name}! I understand work can be busy and stressful. "
                f"While I can't help with work-related questions, I can help you with financial planning "
                f"and investment decisions that might improve your financial situation!\n\n"
                f"**Financial topics I can help with:**\n"
                f"• Stock investment analysis\n"
                f"• Cryptocurrency insights\n"
                f"• Portfolio optimization\n"
                f"• Risk management strategies\n\n"
                f"Try asking me about stocks or crypto instead!"
            )
        else:

            return (
                f"**Financial Analysis Assistant**\n\n"
                f"Hello {user_name}! I'm your financial analysis assistant. I can provide comprehensive stock and crypto analysis "
                f"using historical data and technical indicators.\n\n"
                f"{'Your watchlist: ' + user_info['watchlist'] if user_info else ''}\n\n"
                f"**What I can help with:**\n"
                f"• Stock analysis (AAPL, TSLA, GOOGL, etc.)\n"
                f"• Cryptocurrency insights (BTC, ETH, etc.)\n"
                f"• Investment recommendations\n"
                f"• Market trends and predictions\n\n"
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
        """Extract stock symbol from user input"""
    
        common_symbols = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'CRM', 'ADBE',
            'PYPL', 'INTC', 'AMD', 'CSCO', 'ORCL', 'IBM', 'QCOM', 'AVGO', 'TXN', 'MU',
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
      
        for symbol in common_symbols:
            if symbol in user_input_upper:
                return symbol
        
       
        for company, symbol in company_to_symbol.items():
            if company in user_input_upper:
                return symbol
        
       
        for company, symbol in company_to_symbol.items():
            if company.lower() in user_input.lower():
                return symbol
        
        return None

    def _extract_user_info(self, question):
        """Extract user information from the question context"""
        try:
          
            if "User Information:" in question:
                lines = question.split('\n')
                user_info = {}
                
                for line in lines:
                    line = line.strip()
                    if line.startswith("- Name:"):
                        user_info['name'] = line.replace("- Name:", "").strip()
                    elif line.startswith("- Watchlist:"):
                        watchlist_text = line.replace("- Watchlist:", "").strip()
                        if watchlist_text != "None":
                            user_info['watchlist'] = watchlist_text
                        else:
                            user_info['watchlist'] = "no items"
                    elif line.startswith("- Email:"):
                        user_info['email'] = line.replace("- Email:", "").strip()
                
                if 'name' in user_info:
                    return user_info
            return None
        except Exception as e:
            print("[ERROR] _extract_user_info:", e)
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
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX',
            'BTC', 'ETH', 'ADA', 'DOT', 'LINK', 'LTC', 'BCH', 'UNI', 'ATOM',
            'EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 'USD/CAD'
        ] 

    def _classify_question_type(self, question):
        """Classify question type using keyword matching (basic version)"""
        q_lower = question.lower()
        
        # Check for watchlist keywords
        watchlist_keywords = ['watchlist', 'how many items', 'my stocks', 'portfolio', 'my list', 'items count']
        if any(keyword in q_lower for keyword in watchlist_keywords):
            return "WATCHLIST_QUERY"
        
        # Check for general conversation keywords
        general_keywords = [
            'hi', 'hello', 'bye', 'thanks', 'thank you', 'how are you', 'good morning', 
            'good afternoon', 'good evening', 'weather', 'temperature', 'hot', 'cold',
            'nice day', 'beautiful day', 'weekend', 'holiday', 'vacation', 'work',
            'family', 'friend', 'home', 'food', 'dinner', 'lunch', 'breakfast',
            'coffee', 'tea', 'water', 'exercise', 'gym', 'sports', 'movie', 'music',
            'book', 'reading', 'sleep', 'rest', 'relax', 'stress', 'busy', 'tired'
        ]
        if any(keyword in q_lower for keyword in general_keywords):
            return "GENERAL_CONVERSATION"
        
        # Check for stock symbols
        common_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'BTC', 'ETH', 'ADA', 'DOT', 'LINK']
        if any(symbol in question.upper() for symbol in common_symbols):
            return "STOCK_ANALYSIS"
        
        # Check for account keywords
        account_keywords = ['account', 'profile', 'settings', 'preferences', 'my info', 'user info']
        if any(keyword in q_lower for keyword in account_keywords):
            return "ACCOUNT_INFO"
        
        return "FINANCIAL_ADVICE"

    def _handle_watchlist_question(self, question):
        """Handle watchlist-specific questions"""
        user_info = self._extract_user_info(question)
        
        if user_info and user_info.get('watchlist'):
            watchlist_text = user_info['watchlist']
            if watchlist_text != "no items" and watchlist_text != "None":
                watchlist_items = [item.strip() for item in watchlist_text.split(',')]
                count = len(watchlist_items)
                
                return (
                    f"**Watchlist Information**\n\n"
                    f"Hello {user_info.get('name', 'there')}! You have {count} items in your watchlist:\n\n"
                    f"**Your Watchlist:**\n"
                    f"{', '.join(watchlist_items)}\n\n"
                    f"I can provide technical analysis for any of these stocks. Just ask about a specific symbol!"
                )
            else:
                return (
                    f"**Watchlist Information**\n\n"
                    f"Hello {user_info.get('name', 'there')}! You currently have no items in your watchlist.\n\n"
                    f"You can add stocks or cryptocurrencies to your watchlist to track them."
                )
        else:
            return "I don't have access to your watchlist information right now."

    def _handle_account_question(self, question):
        """Handle account-related questions"""
        user_info = self._extract_user_info(question)
        
        if user_info:
            return (
                f"**Account Information**\n\n"
                f"Hello {user_info.get('name', 'User')}! Here's your account information:\n\n"
                f"**Name:** {user_info.get('name', 'Not available')}\n"
                f"**Email:** {user_info.get('email', 'Not available')}\n"
                f"**Watchlist:** {user_info.get('watchlist', 'No items')}\n\n"
                f"I can help you with stock analysis and investment advice!"
            )
        else:
            return "I don't have access to your account information right now."

    def _handle_stock_analysis(self, question):
        """Handle stock/crypto analysis questions"""
        # Check if user is asking about multiple stocks from their watchlist
        if self._is_multiple_stock_question(question):
            return self._handle_multiple_stock_analysis(question)
        
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

    def _is_multiple_stock_question(self, question):
        """Check if user is asking about multiple stocks from their watchlist"""
        q_lower = question.lower()
        multiple_stock_keywords = [
            'both', 'all', 'these', 'those', 'them', 'my stocks', 'my watchlist',
            'should i invest in', 'analyze', 'compare', 'which one'
        ]
        
        # Check if question contains multiple stock keywords
        has_multiple_keywords = any(keyword in q_lower for keyword in multiple_stock_keywords)
        
        # Check if user has multiple stocks in watchlist
        user_info = self._extract_user_info(question)
        has_multiple_stocks = False
        if user_info and user_info.get('watchlist'):
            watchlist_text = user_info['watchlist']
            if watchlist_text != "no items" and watchlist_text != "None":
                watchlist_items = [item.strip() for item in watchlist_text.split(',')]
                has_multiple_stocks = len(watchlist_items) > 1
        
        return has_multiple_keywords and has_multiple_stocks

    def _handle_multiple_stock_analysis(self, question):
        """Handle analysis of multiple stocks from user's watchlist"""
        user_info = self._extract_user_info(question)
        
        if not user_info or not user_info.get('watchlist'):
            return "I can't access your watchlist information. Please ask about specific stocks individually."
        
        watchlist_text = user_info['watchlist']
        if watchlist_text == "no items" or watchlist_text == "None":
            return f"Hello {user_info.get('name', 'there')}! You don't have any stocks in your watchlist yet. Add some stocks first, then I can provide analysis."
        
        watchlist_items = [item.strip() for item in watchlist_text.split(',')]
        
        if len(watchlist_items) == 1:
            # Only one stock in watchlist
            symbol = watchlist_items[0]
            return f"I can see you have {symbol} in your watchlist. Let me analyze it for you:\n\n" + self._analyze_single_stock(symbol)
        
        # Multiple stocks - provide comparison
        analysis_parts = []
        for symbol in watchlist_items:
            try:
                data = self.analyzer.generate_investment_advice(symbol)
                if data and 'error' not in data:
                    analysis = self._format_basic_analysis(data)
                    prediction = self._generate_market_prediction(data, symbol)
                    analysis_parts.append(f"**{symbol} Analysis:**\n{analysis}\n**Prediction:** {prediction}\n")
                else:
                    analysis_parts.append(f"**{symbol}:** No data available for analysis.\n")
            except Exception as e:
                analysis_parts.append(f"**{symbol}:** Error analyzing this stock.\n")
        
        return (
            f"**Multi-Stock Analysis**\n\n"
            f"Here's an analysis of your watchlist stocks:\n\n"
            f"{''.join(analysis_parts)}\n"
            f"**Note**: This analysis is based on technical indicators and historical data. "
            f"Consider diversifying your portfolio across different sectors."
        )

    def _analyze_single_stock(self, symbol):
        """Analyze a single stock and return formatted response"""
        try:
            data = self.analyzer.generate_investment_advice(symbol)
            if data and 'error' not in data:
                analysis = self._format_basic_analysis(data)
                prediction = self._generate_market_prediction(data, symbol)
                return (
                    f"**{symbol} Analysis:**\n{analysis}\n"
                    f"**Prediction:** {prediction}\n"
                    f"**Note**: This analysis is based on technical indicators and historical data."
                )
            else:
                return f"I couldn't find data for {symbol}. Please try another stock like AAPL, TSLA, or GOOGL."
        except Exception as e:
            return f"I encountered an error analyzing {symbol}. Please try asking about a specific stock individually."

    def _handle_general_financial_question(self, question):
        """Handle general financial questions"""
        return (
            f"**Financial Analysis**\n\n"
            f"I can provide technical analysis and investment advice for stocks and cryptocurrencies.\n\n"
            f"**What I can help with:**\n"
            f"• Stock analysis (AAPL, TSLA, GOOGL, etc.)\n"
            f"• Cryptocurrency insights (BTC, ETH, etc.)\n"
            f"• Investment recommendations\n"
            f"• Market trends and predictions\n\n"
            f"Please ask about a specific stock or crypto for detailed analysis!"
        )

    def _handle_unknown_question(self, question):
        """Handle questions that don't fit other categories"""
        return (
            f"**Financial Analysis Assistant**\n\n"
            f"I'm here to help you with investment analysis and stock market insights.\n\n"
            f"**What I can help with:**\n"
            f"• Stock analysis and recommendations\n"
            f"• Cryptocurrency insights\n"
            f"• Market trends and predictions\n"
            f"• Investment strategies\n\n"
            f"Ask me about any stock or crypto for detailed analysis!"
        ) 