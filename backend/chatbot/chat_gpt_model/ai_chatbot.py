import os
import sys
import json
import openai
from datetime import datetime
from dotenv import load_dotenv


current_dir = os.path.dirname(os.path.abspath(__file__))
chatbot_dir = os.path.abspath(os.path.join(current_dir, '..'))
env_path = os.path.join(chatbot_dir, '.env')
print("Looking for .env at:", env_path)
print(".env exists:", os.path.exists(env_path))
load_dotenv(env_path, override=True)

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    openai.api_key = api_key
    print("OpenAI API key loaded from .env file")
else:
    print("WARNING: No OPENAI_API_KEY found in .env file")


sys.path.append(os.path.dirname(current_dir))

from stock_analyzer_model.stock_analyzer import StockAnalyzer

class AIChatbot:
    def __init__(self, openai_api_key=None):
        self.market_data_path = os.path.abspath(
            os.path.join(current_dir, '..', '..', 'stock-data-collector', 'market_data')
        )

        self.analyzer = StockAnalyzer(data_dir=self.market_data_path)

        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.use_openai = bool(self.api_key)
        if self.use_openai:
            openai.api_key = self.api_key
        else:
            pass

        self.conversation_history = []
        self.max_history_length = 10

    def process_question(self, question):
        try:
            if not self.use_openai:
                return self._fallback_response(question)

            question_type = self._classify_question_type(question)
            print(f"[DEBUG] Question classified as: {question_type}")
            
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
  
                print(f"[DEBUG] AI classification returned '{question_type}', trying fallback...")
                fallback_type = self._fallback_classification(question)
                print(f"[DEBUG] Fallback classification: {fallback_type}")
                
                if fallback_type == "WATCHLIST_QUERY":
                    return self._handle_watchlist_question(question)
                elif fallback_type == "GENERAL_CONVERSATION":
                    return self._handle_general_conversation(question)
                elif fallback_type == "STOCK_ANALYSIS":
                    return self._handle_stock_analysis(question)
                elif fallback_type == "ACCOUNT_INFO":
                    return self._handle_account_question(question)
                else:
                    return self._handle_unknown_question(question)
                
        except Exception as e:
            print("[ERROR] Main process_question error:", e)
            return self._fallback_response(question)

    def _is_general_conversation(self, q):
        """Legacy method - now handled by AI classification"""
        general_keywords = [
            'hi', 'hello', 'bye', 'thanks', 'thank you', 'how are you', 'good morning', 
            'good afternoon', 'good evening', 'weather', 'temperature', 'hot', 'cold',
            'nice day', 'beautiful day', 'weekend', 'holiday', 'vacation', 'work',
            'family', 'friend', 'home', 'food', 'dinner', 'lunch', 'breakfast',
            'coffee', 'tea', 'water', 'exercise', 'gym', 'sports', 'movie', 'music',
            'book', 'reading', 'sleep', 'rest', 'relax', 'stress', 'busy', 'tired',
            'name', 'know', 'my name', 'your name', 'who are you', 'what is your name'
        ]
        return any(keyword in q.lower() for keyword in general_keywords)

    def _handle_general_conversation(self, q):
        
        user_info = self._extract_user_info(q)
        
        if user_info:
            prompt = (
                f"You're an expert financial analyst and AI assistant. The user's name is {user_info['name']} and they have "
                f"a watchlist with: {user_info['watchlist']}. "
                "You have access to real-time market data and can provide comprehensive investment insights. "
                "Your capabilities include:\n"
                "- Technical analysis of stocks and cryptocurrencies\n"
                "- Price trend analysis and predictions\n"
                "- Risk assessment and investment recommendations\n"
                "- Market sentiment analysis\n"
                "- Portfolio optimization advice\n\n"
                f"Greet {user_info['name']} warmly by name and explain how you can help with their investment decisions. "
                f"Mention their watchlist items and specific examples like 'AAPL', 'TSLA', 'BTC', or 'ETH' to show your expertise. "
                f"If the user asks about non-financial topics (weather, personal life, etc.), politely redirect them to financial topics. "
                f"Use their name naturally in conversation when appropriate.\n\n"
                f"IMPORTANT: Do NOT include formal closings like 'Best regards', 'Sincerely', 'Thank you', etc. "
                f"Keep responses conversational and direct."
            )
        else:
            prompt = (
                "You're an expert financial analyst and AI assistant specializing in stock and cryptocurrency analysis. "
                "You have access to real-time market data and can provide comprehensive investment insights. "
                "Your capabilities include:\n"
                "- Technical analysis of stocks and cryptocurrencies\n"
                "- Price trend analysis and predictions\n"
                "- Risk assessment and investment recommendations\n"
                "- Market sentiment analysis\n"
                "- Portfolio optimization advice\n\n"
                "Greet the user warmly and explain how you can help them with their investment decisions. "
                "Mention specific examples like 'AAPL', 'TSLA', 'BTC', or 'ETH' to show your expertise. "
                "If the user asks about non-financial topics (weather, personal life, etc.), politely redirect them to financial topics.\n\n"
                "IMPORTANT: Do NOT include formal closings like 'Best regards', 'Sincerely', 'Thank you', etc. "
                "Keep responses conversational and direct."
            )
        
        return self._chat_with_openai(prompt, q, 300)

    def _handle_general_financial_question(self, q):
        prompt = (
            "You're a senior financial analyst with 15+ years of experience in investment management and market analysis. "
            "Provide comprehensive, well-researched responses to financial questions. Include:\n"
            "- Detailed analysis with supporting reasoning\n"
            "- Current market context and trends\n"
            "- Risk considerations and mitigation strategies\n"
            "- Actionable investment advice\n"
            "- Educational insights to help the user understand the concepts\n\n"
            "Use specific examples and data when relevant. Be thorough but accessible.\n\n"
            "CRITICAL: Do NOT include any of the following in your response:\n"
            "- Personal greetings or salutations\n"
            "- User names or personal references\n"
            "- Email signatures or closings like 'Best regards', 'Sincerely', 'Thank you', etc.\n"
            "- Formal letter endings\n"
            "- Any closing phrases\n\n"
            "Focus purely on the financial analysis and advice. Keep responses direct and professional."
        )
        return self._chat_with_openai(prompt, q, 600)

    def _handle_no_data_response(self, q, symbol):
        return f"Sorry, I couldn't find data for {symbol}. Try another like AAPL, TSLA, BTC, or ETH."

    def interpret_question(self, q):
        if not self.use_openai:
            return self._fallback_interpretation(q)
        try:
            prompt = (
                "You are an expert financial analyst specializing in stock and cryptocurrency analysis. "
                "Extract detailed information from the user's question to provide the most relevant analysis.\n\n"
                "Extract the following from the user's question:\n"
                "- asset_symbol (stock or crypto symbol like AAPL, TSLA, BTC, ETH)\n"
                "- analysis_type (trend, buy/sell, risk, technical, fundamental, general)\n"
                "- user_concerns (what they're worried about or interested in)\n"
                "- timeframe (short_term, medium_term, long_term)\n"
                "- context_hints (any additional context like market conditions, news, etc.)\n"
                "- investment_goal (growth, income, speculation, hedging)\n"
                "- risk_tolerance (conservative, moderate, aggressive)\n\n"
                "Return as JSON like:\n"
                '{ "asset_symbol": "AAPL", "analysis_type": "trend", "user_concerns": ["volatility"], "timeframe": "short_term", "context_hints": ["market uncertainty"], "investment_goal": "growth", "risk_tolerance": "moderate" }'
            )
            client = openai.OpenAI(api_key=openai.api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": prompt}, {"role": "user", "content": q}],
                temperature=0.3
            )

            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print("[ERROR] interpret_question:", e)
            return self._fallback_interpretation(q)

    def generate_insight(self, data, q):
        if not self.use_openai:
            return self._format_basic_analysis(data)
        
        summary = (
            f"COMPREHENSIVE STOCK ANALYSIS DATA:\n"
            f"Symbol: {data.get('symbol')}\n"
            f"Current Price: ${data.get('current_price', 0):.2f}\n"
            f"Price Change: {data.get('price_change_pct', 0):+.2f}%\n"
            f"Price Change Amount: ${data.get('price_change', 0):+.2f}\n"
            f"Trend Direction: {data.get('trend')}\n"
            f"Volatility: {data.get('volatility', 0):.2f}%\n"
            f"Risk Score: {data.get('risk_score', 'N/A')}/10\n"
            f"Recommendation: {data.get('recommendation', 'N/A')}\n"
            f"Support Level: ${data.get('support', 0):.2f}\n"
            f"Resistance Level: ${data.get('resistance', 0):.2f}\n"
            f"Volume: {data.get('volume', 'N/A')}\n"
            f"Market Cap: {data.get('market_cap', 'N/A')}\n"
            f"P/E Ratio: {data.get('pe_ratio', 'N/A')}\n"
            f"52-Week High: ${data.get('high_52w', 0):.2f}\n"
            f"52-Week Low: ${data.get('low_52w', 0):.2f}\n"
        )
        
        prompt = (
            "You're a senior investment analyst with expertise in technical and fundamental analysis. "
            "Analyze the provided stock data and provide a comprehensive investment analysis. Include:\n\n"
            "1. **Technical Analysis**:\n"
            "   - Price trend interpretation and momentum\n"
            "   - Support and resistance level analysis\n"
            "   - Volatility assessment and implications\n\n"
            "2. **Investment Recommendation**:\n"
            "   - Clear buy/sell/hold recommendation with reasoning\n"
            "   - Risk assessment and management strategies\n"
            "   - Short-term vs long-term outlook\n\n"
            "3. **Market Context**:\n"
            "   - Sector and market correlation analysis\n"
            "   - Macroeconomic factors to consider\n"
            "   - Competitive positioning insights\n\n"
            "4. **Actionable Advice**:\n"
            "   - Entry and exit strategies\n"
            "   - Position sizing recommendations\n"
            "   - Portfolio diversification considerations\n\n"
            "CRITICAL: Do NOT include any of the following in your response:\n"
            "- Personal greetings or salutations\n"
            "- User names or personal references\n"
            "- Email signatures or closings like 'Best regards', 'Sincerely', 'Thank you', etc.\n"
            "- Formal letter endings\n"
            "- Any closing phrases\n\n"
            "Focus purely on the financial analysis and investment advice. "
            "Provide specific, actionable insights that help the investor make informed decisions. "
            "Use the user's original question to tailor the response appropriately.\n\n"
            f"USER QUESTION: {q}\n\n"
            f"STOCK DATA:\n{summary}"
        )
        return self._chat_with_openai(prompt, "", 800)

    def _chat_with_openai(self, sys_prompt, user_input, max_tokens):
        try:
            client = openai.OpenAI(api_key=openai.api_key)
            res = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=max_tokens
            )

            return res.choices[0].message.content.strip()
        except Exception as e:
            print("[ERROR] chat_with_openai:", e)
            return self._fallback_response(user_input)

    def _fallback_interpretation(self, q):
        return {
            "asset_symbol": self._extract_symbol_from_input(q),
            "analysis_type": "general",
            "user_concerns": [],
            "timeframe": "medium_term",
            "context_hints": []
        }

    def _format_basic_analysis(self, data):
        return (
            f"**{data.get('symbol', 'Symbol')} Comprehensive Analysis**\n\n"
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
            f"   • This analysis is based on technical indicators and market data\n"
            f"   • Consider your investment goals and risk tolerance\n"
            f"   • Always diversify your portfolio and never invest more than you can afford to lose\n"
            f"   • For more detailed analysis, try asking specific questions about this stock"
        )

    def _fallback_response(self, q):
        """Fall back to basic analysis when AI is not available"""
        try:
            symbol = self._extract_symbol_from_input(q)
            
            if symbol:
                data = self.analyzer.generate_investment_advice(symbol)
                if data and 'error' not in data:
                    prediction = self._generate_market_prediction(data, symbol)
                    
                    return (
                        f"**Technical Analysis - Offline Mode**\n\n"
                        f"I'm currently offline but can provide comprehensive analysis using historical data.\n\n"
                        f"{self._format_basic_analysis(data)}\n\n"
                        f"**Market Prediction**:\n{prediction}\n\n"
                        f"**Note**: This analysis is based on technical indicators and historical data. "
                        f"For real-time AI insights, please connect to the internet."
                    )
                else:
                    return (
                        f"**Offline Mode**\n\n"
                        f"I'm currently offline and couldn't find data for {symbol}. "
                        f"Available symbols include: AAPL, MSFT, GOOGL, TSLA, BTC, ETH, and more.\n\n"
                        f"Please try asking about a specific stock symbol and I'll provide technical analysis."
                    )
            else:
                return (
                    f"**Offline Mode**\n\n"
                    f"I'm currently offline but can provide technical analysis using historical data.\n\n"
                    f"Available symbols: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA, BTC, ETH, and more.\n\n"
                    f"Please ask about a specific stock or crypto symbol for detailed analysis."
                )
        except Exception as e:
            print("[ERROR] _fallback_response:", e)
            return (
                f"**Offline Mode**\n\n"
                f"I'm currently offline but can provide technical analysis using historical data.\n\n"
                f"Available symbols: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA, BTC, ETH, and more.\n\n"
                f"Please ask about a specific stock or crypto symbol for detailed analysis."
            )

    def _generate_market_prediction(self, data, symbol):
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

    def _extract_user_question(self, question):
        """Extract just the user's question from the context"""
        try:
            if "User Question:" in question:
               
                lines = question.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith("User Question:"):
                        return line.replace("User Question:", "").strip()
            return question  
        except Exception as e:
            print("[ERROR] _extract_user_question:", e)
            return question

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
                    print(f"[DEBUG] Extracted user info: {user_info}")
                    return user_info
            print(f"[DEBUG] No 'User Information:' found in question or missing name")
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
        """Use AI to classify the question type"""
        try:
            prompt = """
            Classify this user question into one of these categories:
            
            - GENERAL_CONVERSATION: greetings, casual chat, personal questions, how are you, hello, hi
            - WATCHLIST_QUERY: questions about user's watchlist, portfolio, items count, "how many items", "my watchlist", "my stocks", "should i invest in those both", "analyze my watchlist", "compare my stocks"
            - STOCK_ANALYSIS: questions about specific stocks/crypto for investment advice, technical analysis, price predictions
            - FINANCIAL_ADVICE: general financial questions, market trends, investment strategies, economic questions
            - ACCOUNT_INFO: questions about user account, settings, preferences, profile information
            - UNKNOWN: anything that doesn't fit above categories
            
            IMPORTANT: 
            - If the user is asking about their watchlist, portfolio, or items count, classify as WATCHLIST_QUERY
            - If the user asks about multiple stocks from their watchlist (like "both", "all", "those"), classify as WATCHLIST_QUERY
            - If the user asks "should i invest in those both" or similar, classify as WATCHLIST_QUERY
            
            Return ONLY the category name, nothing else.
            
            Question: {question}
            """
            
            client = openai.OpenAI(api_key=openai.api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0.1,
                max_tokens=50
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[ERROR] Question classification failed: {e}")
            return self._fallback_classification(question)

    def _fallback_classification(self, question):
        """Fallback to keyword-based classification if AI fails"""
        q_lower = question.lower()
    
        watchlist_keywords = [
            'watchlist', 'how many items', 'my stocks', 'portfolio', 'my list', 'items count', 
            'items in your watchlist', 'those both', 'both', 'all', 'these', 'those', 'them',
            'should i invest in', 'analyze my', 'compare my'
        ]
        if any(keyword in q_lower for keyword in watchlist_keywords):
            return "WATCHLIST_QUERY"
        
       
        general_keywords = [
            'hi', 'hello', 'bye', 'thanks', 'thank you', 'how are you', 'good morning', 
            'good afternoon', 'good evening', 'weather', 'temperature', 'hot', 'cold',
            'nice day', 'beautiful day', 'weekend', 'holiday', 'vacation', 'work',
            'family', 'friend', 'home', 'food', 'dinner', 'lunch', 'breakfast',
            'coffee', 'tea', 'water', 'exercise', 'gym', 'sports', 'movie', 'music',
            'book', 'reading', 'sleep', 'rest', 'relax', 'stress', 'busy', 'tired',
            'name', 'know', 'my name', 'your name', 'who are you', 'what is your name'
        ]
        if any(keyword in q_lower for keyword in general_keywords):
            return "GENERAL_CONVERSATION"
        
        
        common_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'BTC', 'ETH', 'ADA', 'DOT', 'LINK']
        if any(symbol in question.upper() for symbol in common_symbols):
            return "STOCK_ANALYSIS"
        
       
        account_keywords = ['account', 'profile', 'settings', 'preferences', 'my info', 'user info']
        if any(keyword in q_lower for keyword in account_keywords):
            return "ACCOUNT_INFO"
        
        return "FINANCIAL_ADVICE"

    def _handle_watchlist_question(self, question):
        """Handle watchlist-specific questions"""
        print(f"[DEBUG] Handling watchlist question: {question[:200]}...")
        
       
        if self._is_multiple_stock_question(question):
            return self._handle_multiple_stock_analysis(question)
        
        user_info = self._extract_user_info(question)
        
        if user_info and user_info.get('watchlist'):
            watchlist_text = user_info['watchlist']
            if watchlist_text != "no items" and watchlist_text != "None":
                watchlist_items = [item.strip() for item in watchlist_text.split(',')]
                count = len(watchlist_items)
                
                prompt = f"""
                The user is asking about their watchlist. They have {count} items: {user_info['watchlist']}
                
                Answer their question about their watchlist specifically. If they ask about count, mention the number.
                If they ask about specific items, provide analysis. Be helpful and specific to their watchlist.
                If they ask "how many items", tell them they have {count} items and list them.
                
                User question: {question}
                """
                
                return self._chat_with_openai(prompt, question, 400)
            else:
                return f"Hello {user_info.get('name', 'there')}! You currently have no items in your watchlist. You can add stocks or cryptocurrencies to your watchlist to track them."
        else:
            
            print(f"[DEBUG] User info extraction failed. Trying manual parsing...")
            try:
               
                if "Watchlist:" in question:
                    lines = question.split('\n')
                    for line in lines:
                        if line.strip().startswith("- Watchlist:"):
                            watchlist_text = line.replace("- Watchlist:", "").strip()
                            if watchlist_text != "None" and watchlist_text:
                                watchlist_items = [item.strip() for item in watchlist_text.split(',')]
                                count = len(watchlist_items)
                                return f"You have {count} items in your watchlist: {watchlist_text}. I can provide analysis for any of these stocks if you'd like!"
                            else:
                                return "You currently have no items in your watchlist. You can add stocks or cryptocurrencies to your watchlist to track them."
                
                
                if "Name:" in question:
                    lines = question.split('\n')
                    for line in lines:
                        if line.strip().startswith("- Name:"):
                            name = line.replace("- Name:", "").strip()
                            return f"Hello {name}! I can see your watchlist information, but I'm having trouble accessing the specific items. Please try asking again or contact support."
                
                return "I don't have access to your watchlist information right now. Please try asking again or contact support."
            except Exception as e:
                print(f"[ERROR] Manual parsing failed: {e}")
                return "I don't have access to your watchlist information right now. Please try asking again or contact support."

    def _handle_account_question(self, question):
        """Handle account-related questions"""
        user_info = self._extract_user_info(question)
        
        prompt = f"""
        The user is asking about their account information. They are {user_info.get('name', 'User')}.
        
        Answer questions about their account, settings, or preferences. Be helpful but don't share sensitive information.
        If they ask about their profile, mention their name and email.
        
        User question: {question}
        """
        
        return self._chat_with_openai(prompt, question, 300)

    def _handle_stock_analysis(self, question):
        """Handle stock/crypto analysis questions"""
       
        if self._is_multiple_stock_question(question):
            return self._handle_multiple_stock_analysis(question)
        
        interpretation = self.interpret_question(question)
        symbol = interpretation.get("asset_symbol")

        if symbol:
            data = self.analyzer.generate_investment_advice(symbol)
            if data and 'error' not in data:
                try:
                    return self.generate_insight(data, question)
                except Exception as ai_error:
                    print("[ERROR] AI insight generation failed:", ai_error)
                    return self._fallback_response(question)
            return self._handle_no_data_response(question, symbol)
        else:
            return self._handle_general_financial_question(question)

    def _is_multiple_stock_question(self, question):
        """Check if user is asking about multiple stocks from their watchlist"""
        q_lower = question.lower()
        multiple_stock_keywords = [
            'both', 'all', 'these', 'those', 'them', 'my stocks', 'my watchlist',
            'should i invest in', 'analyze', 'compare', 'which one'
        ]
        
        
        has_multiple_keywords = any(keyword in q_lower for keyword in multiple_stock_keywords)
        
       
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
            
            symbol = watchlist_items[0]
            return f"I can see you have {symbol} in your watchlist. Let me analyze it for you:\n\n" + self._analyze_single_stock(symbol)
        
       
        prompt = f"""
        The user is asking about investing in multiple stocks from their watchlist: {watchlist_text}
        
        Provide a comprehensive analysis comparing these stocks. Include:
        1. Brief overview of each company
        2. Risk assessment for each
        3. Investment recommendations
        4. Diversification advice
        5. Which might be better for different investment goals
        
        Be specific about their watchlist stocks and provide actionable advice.
        
        CRITICAL: Do NOT include any of the following in your response:
        - Personal greetings or salutations
        - User names or personal references
        - Email signatures or closings like 'Best regards', 'Sincerely', 'Thank you', etc.
        - Formal letter endings
        - Any closing phrases
        
        Keep responses direct and professional.
        
        User question: {question}
        """
        
        return self._chat_with_openai(prompt, question, 600)

    def _analyze_single_stock(self, symbol):
        """Analyze a single stock and return formatted response"""
        try:
            data = self.analyzer.generate_investment_advice(symbol)
            if data and 'error' not in data:
                return self.generate_insight(data, f"Analyze {symbol}")
            else:
                return f"I couldn't find data for {symbol}. Please try another stock like AAPL, TSLA, or GOOGL."
        except Exception as e:
            print(f"[ERROR] Single stock analysis failed for {symbol}: {e}")
            return f"I encountered an error analyzing {symbol}. Please try asking about a specific stock individually."

    def _handle_unknown_question(self, question):
        """Handle questions that don't fit other categories"""
        return self._chat_with_openai(
            "You're a helpful AI assistant. Answer the user's question as best you can.",
            question, 
            400
        ) 