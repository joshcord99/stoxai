import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import json

class StockAnalyzer:
    def __init__(self, data_dir=None):
        if data_dir is None:
         
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(current_dir, '..', '..', 'stock-data-collector', 'market_data')
        self.data_dir = data_dir
        self.analysis_cache = {}
    
    def load_stock_data(self, symbol, category=None):
        """Load stock/crypto data from CSV file"""
        try:
            if '-' in symbol:
                symbol = symbol.replace('-', '_')
            
            if category:
                file_path = os.path.join(self.data_dir, category, f"{symbol}_history.csv")
            else:
                for cat in os.listdir(self.data_dir):
                    cat_path = os.path.join(self.data_dir, cat)
                    if os.path.isdir(cat_path):
                        possible_paths = [
                            os.path.join(cat_path, f"{symbol}_history.csv"),
                            os.path.join(cat_path, f"{symbol}_USD_history.csv"),
                            os.path.join(cat_path, f"{symbol.replace('_', '')}_USD_history.csv")
                        ]
                        
                        for file_path in possible_paths:
                            if os.path.exists(file_path):
                                break
                        else:
                            continue
                        break
                else:
                    return None
            
            if os.path.exists(file_path):
                df = pd.read_csv(file_path, skiprows=3)
                df.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
                
                df = df.dropna(subset=['Date'])
                
                df['Date'] = pd.to_datetime(df['Date'])
                df.set_index('Date', inplace=True)
                
                for col in ['Close', 'High', 'Low', 'Open', 'Volume']:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                df = df.dropna()
                
                return df
            return None
        except Exception as e:
            print(f"Error loading data for {symbol}: {e}")
            return None
    
    def is_crypto(self, symbol):
        """Check if symbol is a crypto currency"""
        crypto_symbols = [
            'BTC', 'ETH', 'BNB', 'ADA', 'XRP', 'DOT', 'LINK', 'LTC', 'BCH', 'UNI',
            'ATOM', 'VET', 'TRX', 'ETC', 'ALGO', 'SOL', 'MATIC', 'AVAX', 'FTM', 'NEAR',
            'ICP', 'FIL', 'XTZ', 'THETA', 'CAKE', 'CHZ', 'HOT', 'DOGE', 'SHIB', 'MANA',
            'SAND', 'ENJ', 'AXS', 'GALA'
        ]
        return symbol.upper() in crypto_symbols
    
    def calculate_technical_indicators(self, df):
        """Calculate technical indicators"""
        if df is None or df.empty:
            return {}
        
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['EMA_12'] = df['Close'].ewm(span=12).mean()
        df['EMA_26'] = df['Close'].ewm(span=26).mean()
        
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        df['Volume_SMA'] = df['Volume'].rolling(window=20).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume_SMA']
        
        return df
    
    def analyze_trend(self, df, period_days=30):
        """Analyze recent trend"""
        if df is None or df.empty:
            return {}
        
        recent_data = df.tail(period_days)
        if recent_data.empty:
            return {}
        
        current_price = recent_data['Close'].iloc[-1]
        start_price = recent_data['Close'].iloc[0]
        price_change = current_price - start_price
        price_change_pct = (price_change / start_price) * 100
        
        if price_change_pct > 5:
            trend = "STRONG_UPTREND"
        elif price_change_pct > 2:
            trend = "UPTREND"
        elif price_change_pct < -5:
            trend = "STRONG_DOWNTREND"
        elif price_change_pct < -2:
            trend = "DOWNTREND"
        else:
            trend = "SIDEWAYS"
        
        volatility = recent_data['Close'].pct_change().std() * np.sqrt(252) * 100
        
        resistance = recent_data['High'].max()
        support = recent_data['Low'].min()
        
        return {
            'trend': trend,
            'price_change': price_change,
            'price_change_pct': price_change_pct,
            'current_price': current_price,
            'volatility': volatility,
            'resistance': resistance,
            'support': support,
            'period_days': period_days
        }
    
    def analyze_technical_signals(self, df):
        """Analyze technical indicators for buy/sell signals"""
        if df is None or df.empty:
            return {}
        
        recent_data = df.tail(20)
        if recent_data.empty:
            return {}
        
        signals = {
            'macd_bullish': False,
            'macd_bearish': False,
            'rsi_overbought': False,
            'rsi_oversold': False,
            'price_above_sma': False,
            'volume_spike': False,
            'bollinger_position': 'middle'
        }
        
        if len(recent_data) >= 2:
            current_macd = recent_data['MACD'].iloc[-1]
            prev_macd = recent_data['MACD'].iloc[-2]
            current_signal = recent_data['MACD_Signal'].iloc[-1]
            prev_signal = recent_data['MACD_Signal'].iloc[-2]
            
            if prev_macd <= prev_signal and current_macd > current_signal:
                signals['macd_bullish'] = True
            
            if prev_macd >= prev_signal and current_macd < current_signal:
                signals['macd_bearish'] = True
        
        current_rsi = recent_data['RSI'].iloc[-1]
        if current_rsi > 70:
            signals['rsi_overbought'] = True
        elif current_rsi < 30:
            signals['rsi_oversold'] = True
        
        current_price = recent_data['Close'].iloc[-1]
        current_sma = recent_data['SMA_20'].iloc[-1]
        if current_price > current_sma:
            signals['price_above_sma'] = True
        
        current_volume = recent_data['Volume'].iloc[-1]
        avg_volume = recent_data['Volume'].iloc[-5:].mean()
        if current_volume > avg_volume * 1.5:
            signals['volume_spike'] = True
        
        current_price = recent_data['Close'].iloc[-1]
        bb_upper = recent_data['BB_Upper'].iloc[-1]
        bb_lower = recent_data['BB_Lower'].iloc[-1]
        
        if current_price > bb_upper:
            signals['bollinger_position'] = 'above'
        elif current_price < bb_lower:
            signals['bollinger_position'] = 'below'
        else:
            signals['bollinger_position'] = 'middle'
        
        return signals
    
    def generate_investment_advice(self, symbol, analysis_period=30):
        """Generate investment advice based on analysis"""
        df = self.load_stock_data(symbol)
        if df is None:
            return {
                'error': f'No data available for {symbol}',
                'recommendation': 'UNAVAILABLE'
            }
        
        df = self.calculate_technical_indicators(df)
        trend_analysis = self.analyze_trend(df, analysis_period)
        technical_signals = self.analyze_technical_signals(df)
        
        recommendation = self._generate_recommendation(trend_analysis, technical_signals)
        
        risk_score = self._calculate_risk_score(trend_analysis, technical_signals)
        
        return {
            'symbol': symbol,
            'current_price': trend_analysis.get('current_price', 0),
            'trend': trend_analysis.get('trend', 'UNKNOWN'),
            'price_change_pct': trend_analysis.get('price_change_pct', 0),
            'volatility': trend_analysis.get('volatility', 0),
            'support': trend_analysis.get('support', 0),
            'resistance': trend_analysis.get('resistance', 0),
            'technical_signals': technical_signals,
            'recommendation': recommendation,
            'risk_score': risk_score,
            'analysis_period': analysis_period,
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_recommendation(self, trend_analysis, technical_signals):
        """Generate buy/sell/hold recommendation"""
        trend = trend_analysis.get('trend', 'UNKNOWN')
        price_change_pct = trend_analysis.get('price_change_pct', 0)
        
        bullish_signals = 0
        bearish_signals = 0
        
        if technical_signals.get('macd_bullish'):
            bullish_signals += 1
        if technical_signals.get('macd_bearish'):
            bearish_signals += 1
        if technical_signals.get('rsi_oversold'):
            bullish_signals += 1
        if technical_signals.get('rsi_overbought'):
            bearish_signals += 1
        if technical_signals.get('price_above_sma'):
            bullish_signals += 1
        if technical_signals.get('volume_spike'):
            bullish_signals += 1
        if technical_signals.get('bollinger_position') == 'below':
            bullish_signals += 1
        elif technical_signals.get('bollinger_position') == 'above':
            bearish_signals += 1
        
        if trend in ['STRONG_UPTREND', 'STRONG_DOWNTREND']:
            if trend == 'STRONG_UPTREND':
                return 'STRONG_BUY'
            else:
                return 'STRONG_SELL'
        
        if bullish_signals > bearish_signals + 1:
            return 'BUY'
        elif bearish_signals > bullish_signals + 1:
            return 'SELL'
        else:
            return 'HOLD'
    
    def _calculate_risk_score(self, trend_analysis, technical_signals):
        """Calculate risk score from 1-10"""
        risk_score = 5
        
        volatility = trend_analysis.get('volatility', 0)
        if volatility > 50:
            risk_score += 3
        elif volatility > 30:
            risk_score += 2
        elif volatility > 20:
            risk_score += 1
        
        trend = trend_analysis.get('trend', 'UNKNOWN')
        if trend in ['STRONG_UPTREND', 'STRONG_DOWNTREND']:
            risk_score += 2
        elif trend in ['UPTREND', 'DOWNTREND']:
            risk_score += 1
        
        if technical_signals.get('rsi_overbought') or technical_signals.get('rsi_oversold'):
            risk_score += 1
        
        if technical_signals.get('volume_spike'):
            risk_score += 1
        
        return max(1, min(10, risk_score))
    
    def get_investment_insight(self, symbol, question_type="general"):
        """Get investment insight for chatbot"""
        advice = self.generate_investment_advice(symbol)
        
        if 'error' in advice:
            return f"I don't have enough data to analyze {symbol}. Please check if the stock symbol is correct."
        

        if question_type == "should_i_buy":
            return self._format_buy_advice(advice)
        elif question_type == "trend_analysis":
            return self._format_trend_analysis(advice)
        elif question_type == "risk_assessment":
            return self._format_risk_assessment(advice)
        elif question_type == "price_analysis":
            return self._format_price_analysis(advice)
        else:
            return self._format_general_advice(advice)
    
    def _format_buy_advice(self, advice):
        """Format advice for buy/sell decisions"""
        symbol = advice['symbol']
        recommendation = advice['recommendation']
        current_price = advice['current_price']
        price_change_pct = advice['price_change_pct']
        risk_score = advice['risk_score']
        
        response = f"Based on my analysis of {symbol}:\n\n"
        response += f"Current Price: ${current_price:.2f}\n"
        response += f"Recent Change: {price_change_pct:+.2f}%\n"
        response += f"Recommendation: {recommendation}\n"
        response += f"Risk Level: {risk_score}/10\n\n"
        
        if recommendation in ['STRONG_BUY', 'BUY']:
            response += "This appears to be a good time to consider buying. "
            if recommendation == 'STRONG_BUY':
                response += "Technical indicators are strongly bullish."
            else:
                response += "Technical indicators are moderately bullish."
        elif recommendation in ['STRONG_SELL', 'SELL']:
            response += "This might not be the best time to buy. "
            if recommendation == 'STRONG_SELL':
                response += "Technical indicators are strongly bearish."
            else:
                response += "Technical indicators are moderately bearish."
        else:
            response += "The stock is showing mixed signals. Consider waiting for clearer trends."
        
        return response
    
    def _format_trend_analysis(self, advice):
        """Format trend analysis"""
        symbol = advice['symbol']
        trend = advice['trend']
        price_change_pct = advice['price_change_pct']
        volatility = advice['volatility']
        
        response = f"Trend Analysis for {symbol}:\n\n"
        response += f"Current Trend: {trend}\n"
        response += f"Price Change: {price_change_pct:+.2f}%\n"
        response += f"Volatility: {volatility:.1f}%\n\n"
        
        if trend == 'STRONG_UPTREND':
            response += "The stock is in a strong upward trend with significant momentum."
        elif trend == 'UPTREND':
            response += "The stock is showing positive momentum with an upward trend."
        elif trend == 'STRONG_DOWNTREND':
            response += "The stock is in a strong downward trend with significant selling pressure."
        elif trend == 'DOWNTREND':
            response += "The stock is showing negative momentum with a downward trend."
        else:
            response += "The stock is moving sideways with no clear directional trend."
        
        return response
    
    def _format_risk_assessment(self, advice):
        """Format risk assessment"""
        symbol = advice['symbol']
        risk_score = advice['risk_score']
        volatility = advice['volatility']
        support = advice['support']
        resistance = advice['resistance']
        
        response = f"Risk Assessment for {symbol}:\n\n"
        response += f"Risk Score: {risk_score}/10\n"
        response += f"Volatility: {volatility:.1f}%\n"
        response += f"Support Level: ${support:.2f}\n"
        response += f"Resistance Level: ${resistance:.2f}\n\n"
        
        if risk_score <= 3:
            response += "Low risk investment with stable price movements."
        elif risk_score <= 6:
            response += "Moderate risk with some price volatility."
        else:
            response += "High risk investment with significant price volatility."
        
        return response
    
    def _format_general_advice(self, advice):
        """Format general investment advice"""
        return self._format_buy_advice(advice)

    def _format_price_analysis(self, advice):
        """Format price analysis and valuation insights"""
        symbol = advice['symbol']
        current_price = advice['current_price']
        price_change_pct = advice['price_change_pct']
        support = advice['support']
        resistance = advice['resistance']
        volatility = advice['volatility']
        
        response = f"Price Analysis for {symbol}:\n\n"
        response += f"Current Price: ${current_price:.2f}\n"
        response += f"Recent Change: {price_change_pct:+.2f}%\n"
        response += f"Support Level: ${support:.2f}\n"
        response += f"Resistance Level: ${resistance:.2f}\n"
        response += f"Volatility: {volatility:.1f}%\n\n"
        
        # Price position analysis
        price_position = (current_price - support) / (resistance - support) if resistance > support else 0.5
        
        if price_position < 0.3:
            response += "The stock is trading near support levels, which could indicate a potential buying opportunity."
        elif price_position > 0.7:
            response += "The stock is trading near resistance levels, which could indicate a potential selling opportunity."
        else:
            response += "The stock is trading in the middle range between support and resistance levels."
        
        # Volatility assessment
        if volatility > 20:
            response += " High volatility suggests significant price swings are possible."
        elif volatility < 10:
            response += " Low volatility suggests relatively stable price movements."
        else:
            response += " Moderate volatility indicates balanced risk and opportunity."
        
        return response

 