import sys
import os
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta
import requests


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'stock-data-collector'))

from app.utils.config import Config
from app.models.user import db, User
from app.routes.auth import auth_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    with app.app_context():
        db.create_all()
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'message': 'Stock Analyst API is running'}
    
    @app.route('/api/ai_chatbot', methods=['POST'])
    def ai_chatbot():
        """Proxy to AI chatbot service"""
        try:
        
            response = requests.post(
                'http://localhost:5002/api/ai_chatbot',
                json=request.get_json(),
                timeout=30
            )
            return response.json(), response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify({
                'success': False, 
                'error': 'AI chatbot service unavailable',
                'message': 'Please ensure the AI chatbot service is running on port 5002'
            }), 503
    
    @app.route('/api/stock-analysis', methods=['POST'])
    def stock_analysis():
        try:
            data = request.get_json()
            symbol = data.get('symbol', '')
            question = data.get('question', '')
            
            if not symbol or not question:
                return jsonify({'success': False, 'error': 'Symbol and question are required'}), 400
            
            # Import and use your Python stock analyzer
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'chatbot'))
            from stock_analyzer_model.stock_analyzer import StockAnalyzer
            
            print(f"Stock analysis requested for symbol: {symbol}")
            print(f"Question: {question}")
            
            analyzer = StockAnalyzer()
            print("StockAnalyzer instance created successfully")
            
            # Generate investment advice
            advice = analyzer.generate_investment_advice(symbol)
            print(f"Investment advice generated: {advice}")
            
            if advice and not advice.get('error'):
                # Determine question type for better formatting
                question_type = "general"
                if 'trend' in question.lower() or 'going' in question.lower():
                    question_type = "trend_analysis"
                elif any(word in question.lower() for word in ['buy', 'sell', 'hold', 'invest', 'investment']):
                    question_type = "should_i_buy"
                elif any(word in question.lower() for word in ['risk', 'safe', 'dangerous']):
                    question_type = "risk_assessment"
                
                print(f"Question type detected: {question_type}")
                
                # Get formatted investment insight
                response = analyzer.get_investment_insight(symbol, question_type)
                print(f"Response generated: {response}")
                
                return jsonify({
                    'success': True,
                    'response': response,
                    'analysis_type': 'stock_analysis',
                    'symbol': symbol,
                    'technical_data': {
                        'current_price': advice.get('current_price'),
                        'trend': advice.get('trend'),
                        'recommendation': advice.get('recommendation'),
                        'risk_score': advice.get('risk_score')
                    }
                })
            else:
                return jsonify({
                    'success': False,
                    'error': f'Unable to analyze {symbol}. Please check if data is available.'
                }), 400
                
        except Exception as e:
            print(f"Stock analysis error: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/available-assets', methods=['GET'])
    def available_assets():
        try:
            assets = [
                'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX',
                'BTC', 'ETH', 'ADA', 'DOT', 'LINK', 'LTC', 'BCH', 'UNI', 'ATOM',
                'EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 'USD/CAD'
            ]
            
            return jsonify({
                'success': True,
                'assets': assets
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/available-stocks', methods=['GET'])
    def available_stocks():
        try:
            stocks = [
                'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX',
                'ADBE', 'CRM', 'ORCL', 'PYPL', 'INTC', 'AMD', 'CSCO', 'IBM'
            ]
            
            return jsonify({
                'success': True,
                'stocks': stocks
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/test-chatbot', methods=['POST'])
    def test_chatbot():
        """Test chatbot without authentication"""
        try:
            data = request.get_json()
            question = data.get('question', '')
            
            if not question:
                return jsonify({'success': False, 'error': 'Question is required'}), 400
 
            user_context = f"""
User Information:
- Name: Gillian
- Email: gillian@example.com
- Watchlist: AAPL, TSLA

User Question: {question}

Please provide personalized analysis considering the user's watchlist and preferences.
"""
            
            response = requests.post(
                'http://localhost:5002/api/ai_chatbot',
                json={'question': user_context},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return jsonify({
                    'success': True,
                    'response': result.get('response', 'Sorry, I encountered an error processing your request.'),
                    'ai_enabled': result.get('ai_enabled', False)
                })
            else:
                return jsonify({
                    'success': True,
                    'response': f"Hello {user.get_full_name()}! This is a test response. For enhanced AI analysis, please ensure the chatbot service is running.",
                    'ai_enabled': False
                })
                
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/user-chatbot', methods=['POST'])
    @jwt_required()
    def user_chatbot():
        """Enhanced chatbot with user database access"""
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            data = request.get_json()
            question = data.get('question', '')
            
            if not question:
                return jsonify({'success': False, 'error': 'Question is required'}), 400
            

            try:
                
                user_context = f"""
User Information:
- Name: {user.get_full_name()}
- Email: {user.email}
- Watchlist: {', '.join(user.get_watchlist()) if user.get_watchlist() else 'None'}

User Question: {question}

Please provide personalized analysis considering the user's watchlist and preferences.
"""
                
                response = requests.post(
                    'http://localhost:5002/api/ai_chatbot',
                    json={'question': user_context},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return jsonify({
                        'success': True,
                        'response': result.get('response', 'Sorry, I encountered an error processing your request.'),
                        'user_context': {
                            'name': user.get_full_name(),
                            'watchlist': user.get_watchlist(),
                            'email': user.email
                        },
                        'ai_enabled': result.get('ai_enabled', False)
                    })
                else:
             
                    return jsonify({
                        'success': True,
                        'response': f"Hello {user.get_full_name()}! I can see you have {len(user.get_watchlist())} items in your watchlist: {', '.join(user.get_watchlist()) if user.get_watchlist() else 'None'}.\n\nThis is a basic response. For enhanced AI analysis, please ensure the chatbot service is running.",
                        'user_context': {
                            'name': user.get_full_name(),
                            'watchlist': user.get_watchlist(),
                            'email': user.email
                        },
                        'ai_enabled': False
                    })
                
            except ImportError:
                try:
                    from chatbot.stock_analyzer_model.basic_chatbot import BasicChatbot
                    chatbot = BasicChatbot()
                    
      
                    user_context = f"""
User Information:
- Name: {user.get_full_name()}
- Email: {user.email}
- Watchlist: {', '.join(user.get_watchlist()) if user.get_watchlist() else 'None'}

User Question: {question}

Please provide personalized analysis considering the user's watchlist and preferences.
"""
                    
                    response = chatbot.process_question(user_context)
                    
                    return jsonify({
                        'success': True,
                        'response': response,
                        'user_context': {
                            'name': user.get_full_name(),
                            'watchlist': user.get_watchlist(),
                            'email': user.email
                        },
                        'ai_enabled': False
                    })
                except Exception as basic_error:
                
                    return jsonify({
                        'success': True,
                        'response': f"Hello {user.get_full_name()}! I can see you have {len(user.get_watchlist())} items in your watchlist: {', '.join(user.get_watchlist()) if user.get_watchlist() else 'None'}.\n\nThis is a basic response. For enhanced AI analysis, please ensure the chatbot service is running.",
                        'user_context': {
                            'name': user.get_full_name(),
                            'watchlist': user.get_watchlist(),
                            'email': user.email
                        },
                        'ai_enabled': False
                    })
                
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Endpoint not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
   
    @app.route('/api/account/info', methods=['GET'])
    @jwt_required()
    def get_account_info():
        """Get current user account information"""
        try:
            user_id = get_jwt_identity()
            
            from tools.account_manager import AccountManager
            account_manager = AccountManager()
            
            result = account_manager.get_account_info(user_id)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 404
                
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/account/export', methods=['GET'])
    @jwt_required()
    def export_account_data():
        """Export user data before account deletion"""
        try:
            user_id = get_jwt_identity()
            
            from tools.account_manager import AccountManager
            account_manager = AccountManager()
            
            result = account_manager.export_user_data(user_id)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 404
                
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/account/delete', methods=['DELETE'])
    @jwt_required()
    def delete_account():
        """Delete user account and all associated data"""
        try:
            user_id = get_jwt_identity()
            
            from tools.account_manager import AccountManager
            account_manager = AccountManager()
            
            result = account_manager.delete_user_account(user_id)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
