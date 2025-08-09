#!/usr/bin/env python3
"""
Test script to verify stock analyzer integration
Run this from the backend directory: python test_stock_analyzer.py
"""

import sys
import os

# Add the chatbot directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'chatbot', 'stock_analyzer_model'))

try:
    from stock_analyzer import StockAnalyzer
    
    print("✅ StockAnalyzer imported successfully!")
    
    # Test the analyzer
    analyzer = StockAnalyzer()
    print("✅ StockAnalyzer instance created!")
    
    # Test with a known symbol
    test_symbol = "AAPL"
    print(f"\n🔍 Testing analysis for {test_symbol}...")
    
    advice = analyzer.generate_investment_advice(test_symbol)
    
    if advice and not advice.get('error'):
        print("✅ Stock analysis successful!")
        print(f"Current Price: ${advice.get('current_price', 'N/A')}")
        print(f"Trend: {advice.get('trend', 'N/A')}")
        print(f"Recommendation: {advice.get('recommendation', 'N/A')}")
        print(f"Risk Score: {advice.get('risk_score', 'N/A')}/10")
        
        # Test question-specific formatting
        print(f"\n📊 Testing trend analysis formatting...")
        trend_insight = analyzer.get_investment_insight(test_symbol, "trend")
        print(f"Trend insight length: {len(trend_insight)} characters")
        
    else:
        print("❌ Stock analysis failed!")
        print(f"Error: {advice.get('error', 'Unknown error')}")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the backend directory")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n�� Test completed!")
