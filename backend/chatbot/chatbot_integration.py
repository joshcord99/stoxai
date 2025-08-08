import json
import re
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from stock_analyzer_model.stock_analyzer import StockAnalyzer 


class StockChatbot:
    def __init__(self):
        self.analyzer = StockAnalyzer()
        
    def process_question(self, user_question):
        """Process user question and return investment advice"""
        user_question = user_question.lower()
        
        stock_symbol = self._extract_stock_symbol(user_question)
        if not stock_symbol:
            return "I couldn't identify a stock symbol in your question. Please mention a stock symbol like AAPL, MSFT, etc."
        
        question_type = self._determine_question_type(user_question)
        
        try:
            insight = self.analyzer.get_investment_insight(stock_symbol, question_type)
            return insight
        except Exception as e:
            return f"Sorry, I encountered an error analyzing {stock_symbol}: {str(e)}"
    
    def _extract_stock_symbol(self, question):
        """Extract stock/crypto symbol from question"""
        stock_symbols = [
            'GOOGL', 'MSFT', 'AAPL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'ADBE', 'CRM',
            'PYPL', 'INTC', 'AMD', 'ORCL', 'CSCO', 'IBM', 'QCOM', 'TXN', 'AVGO', 'MU',
            'AMAT', 'KLAC', 'LRCX', 'ADI', 'MCHP', 'ASML', 'TSM', 'JPM', 'BAC', 'WFC',
            'GS', 'MS', 'USB', 'PNC', 'TFC', 'COF', 'JNJ', 'PFE', 'UNH',
            'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'BMY', 'AMGN', 'XOM', 'CVX', 'COP',
            'EOG', 'SLB', 'PSX', 'VLO', 'MPC', 'HAL', 'BKR', 'DIS', 'NKE', 'HD',
            'LOW', 'COST', 'TGT', 'WMT', 'SBUX', 'MCD', 'KO', 'PEP', 'PG'
        ]
        
        crypto_symbols = [
            'BTC', 'ETH', 'BNB', 'ADA', 'XRP', 'DOT', 'LINK', 'LTC', 'BCH', 'UNI',
            'ATOM', 'VET', 'TRX', 'ETC', 'ALGO', 'SOL', 'MATIC', 'AVAX', 'FTM', 'NEAR',
            'ICP', 'FIL', 'XTZ', 'THETA', 'CAKE', 'CHZ', 'HOT', 'DOGE', 'SHIB', 'MANA',
            'SAND', 'ENJ', 'AXS', 'GALA'
        ]
        
        all_symbols = stock_symbols + crypto_symbols
        
        question_upper = question.upper()
        for symbol in all_symbols:
            if symbol in question_upper:
                return symbol
        
        asset_names = {
            'apple': 'AAPL',
            'microsoft': 'MSFT',
            'google': 'GOOGL',
            'amazon': 'AMZN',
            'tesla': 'TSLA',
            'facebook': 'META',
            'meta': 'META',
            'nvidia': 'NVDA',
            'netflix': 'NFLX',
            'adobe': 'ADBE',
            'salesforce': 'CRM',
            'paypal': 'PYPL',
            'intel': 'INTC',
            'amd': 'AMD',
            'oracle': 'ORCL',
            'cisco': 'CSCO',
            'ibm': 'IBM',
            'qualcomm': 'QCOM',
            'texas instruments': 'TXN',
            'broadcom': 'AVGO',
            'micron': 'MU',
            'applied materials': 'AMAT',
            'kla': 'KLAC',
            'lam research': 'LRCX',
            'analog devices': 'ADI',
            'microchip': 'MCHP',
            'asml': 'ASML',
            'tsmc': 'TSM',
            'jpmorgan': 'JPM',
            'bank of america': 'BAC',
            'wells fargo': 'WFC',
            'goldman sachs': 'GS',
            'morgan stanley': 'MS',
            'citigroup': 'C',
            'us bancorp': 'USB',
            'pnc': 'PNC',
            'truist': 'TFC',
            'capital one': 'COF',
            'johnson & johnson': 'JNJ',
            'pfizer': 'PFE',
            'unitedhealth': 'UNH',
            'abbvie': 'ABBV',
            'merck': 'MRK',
            'thermo fisher': 'TMO',
            'abbott': 'ABT',
            'danaher': 'DHR',
            'bristol myers': 'BMY',
            'amgen': 'AMGN',
            'exxon': 'XOM',
            'chevron': 'CVX',
            'conocophillips': 'COP',
            'eog resources': 'EOG',
            'schlumberger': 'SLB',
            'phillips 66': 'PSX',
            'valero': 'VLO',
            'marathon petroleum': 'MPC',
            'halliburton': 'HAL',
            'baker hughes': 'BKR',
            'disney': 'DIS',
            'nike': 'NKE',
            'home depot': 'HD',
            'lowes': 'LOW',
            'costco': 'COST',
            'target': 'TGT',
            'walmart': 'WMT',
            'starbucks': 'SBUX',
            'mcdonalds': 'MCD',
            'coca cola': 'KO',
            'pepsi': 'PEP',
            'procter & gamble': 'PG',
            
            'bitcoin': 'BTC',
            'btc': 'BTC',
            'ethereum': 'ETH',
            'eth': 'ETH',
            'binance coin': 'BNB',
            'bnb': 'BNB',
            'cardano': 'ADA',
            'ada': 'ADA',
            'ripple': 'XRP',
            'xrp': 'XRP',
            'polkadot': 'DOT',
            'dot': 'DOT',
            'chainlink': 'LINK',
            'link': 'LINK',
            'litecoin': 'LTC',
            'ltc': 'LTC',
            'bitcoin cash': 'BCH',
            'bch': 'BCH',
            'uniswap': 'UNI',
            'uni': 'UNI',
            'cosmos': 'ATOM',
            'atom': 'ATOM',
            'vechain': 'VET',
            'vet': 'VET',
            'tron': 'TRX',
            'trx': 'TRX',
            'ethereum classic': 'ETC',
            'etc': 'ETC',
            'algorand': 'ALGO',
            'algo': 'ALGO',
            'solana': 'SOL',
            'sol': 'SOL',
            'polygon': 'MATIC',
            'matic': 'MATIC',
            'avalanche': 'AVAX',
            'avax': 'AVAX',
            'fantom': 'FTM',
            'ftm': 'FTM',
            'near': 'NEAR',
            'internet computer': 'ICP',
            'icp': 'ICP',
            'filecoin': 'FIL',
            'fil': 'FIL',
            'tezos': 'XTZ',
            'xtz': 'XTZ',
            'theta': 'THETA',
            'pancakeswap': 'CAKE',
            'cake': 'CAKE',
            'chiliz': 'CHZ',
            'chz': 'CHZ',
            'holochain': 'HOT',
            'hot': 'HOT',
            'dogecoin': 'DOGE',
            'doge': 'DOGE',
            'shiba inu': 'SHIB',
            'shib': 'SHIB',
            'decentraland': 'MANA',
            'mana': 'MANA',
            'sandbox': 'SAND',
            'sand': 'SAND',
            'enjin': 'ENJ',
            'enj': 'ENJ',
            'axie infinity': 'AXS',
            'axs': 'AXS',
            'gala': 'GALA'
        }
        
        for name, symbol in asset_names.items():
            if name in question:
                return symbol
        
        return None
    
    def _determine_question_type(self, question):
        """Determine the type of investment question"""
        if any(word in question for word in ['buy', 'invest', 'purchase', 'should i buy']):
            return 'should_i_buy'
        elif any(word in question for word in ['trend', 'direction', 'moving', 'going']):
            return 'trend_analysis'
        elif any(word in question for word in ['risk', 'volatile', 'safe', 'dangerous']):
            return 'risk_assessment'
        else:
            return 'general'
    
    def get_available_stocks(self):
        """Get list of available stocks and crypto for analysis"""
        stocks = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'ADBE', 'CRM',
            'PYPL', 'INTC', 'AMD', 'ORCL', 'CSCO', 'IBM', 'QCOM', 'TXN', 'AVGO', 'MU',
            'AMAT', 'KLAC', 'LRCX', 'ADI', 'MCHP', 'ASML', 'TSM', 'JPM', 'BAC', 'WFC',
            'GS', 'MS', 'USB', 'PNC', 'TFC', 'COF', 'JNJ', 'PFE', 'UNH',
            'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'BMY', 'AMGN', 'XOM', 'CVX', 'COP',
            'EOG', 'SLB', 'PSX', 'VLO', 'MPC', 'HAL', 'BKR', 'DIS', 'NKE', 'HD',
            'LOW', 'COST', 'TGT', 'WMT', 'SBUX', 'MCD', 'KO', 'PEP', 'PG'
        ]
        
        crypto = [
            'BTC', 'ETH', 'BNB', 'ADA', 'XRP', 'DOT', 'LINK', 'LTC', 'BCH', 'UNI',
            'ATOM', 'VET', 'TRX', 'ETC', 'ALGO', 'SOL', 'MATIC', 'AVAX', 'FTM', 'NEAR',
            'ICP', 'FIL', 'XTZ', 'THETA', 'CAKE', 'CHZ', 'HOT', 'DOGE', 'SHIB', 'MANA',
            'SAND', 'ENJ', 'AXS', 'GALA'
        ]
        
        return stocks + crypto

 