from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = Flask(__name__)
CORS(app)


try:
    from chat_gpt_model.ai_chatbot import AIChatbot
    ai_chatbot = AIChatbot()
    enhanced_chatbot = ai_chatbot
    ai_available = True
    print("AI Chatbot loaded successfully")
except Exception as e:
    print(f"Failed to load AI Chatbot: {e}")
    ai_available = False


from stock_analyzer_model.basic_chatbot import BasicChatbot
basic_chatbot = BasicChatbot()
enhanced_chatbot = basic_chatbot

@app.route('/api/ai_chatbot', methods=['POST'])
def analyze_stock_enhanced():
    """Enhanced stock analysis with AI or basic fallback"""
    try:
        data = request.get_json()
        user_question = data.get('question', '')
        
        if not user_question:
            return jsonify({
                'error': 'No question provided',
                'response': 'Please provide a question about a stock or cryptocurrency.'
            }), 400
        
  
        if ai_available:
            try:
                response = ai_chatbot.process_question(user_question)
                return jsonify({
                    'question': user_question,
                    'response': response,
                    'success': True,
                    'enhanced': True,
                    'ai_enabled': True
                })
            except Exception as ai_error:
                print(f"AI chatbot error: {ai_error}")
                response = basic_chatbot.process_question(user_question)
                return jsonify({
                    'question': user_question,
                    'response': response,
                    'success': True,
                    'enhanced': False,
                    'ai_enabled': False
                })
        else:
      
            response = basic_chatbot.process_question(user_question)
            return jsonify({
                'question': user_question,
                'response': response,
                'success': True,
                'enhanced': False,
                'ai_enabled': False
            })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'response': 'Sorry, I encountered an error processing your request. Please try again.',
            'success': False
        }), 500

@app.route('/api/available-assets', methods=['GET'])
def get_available_assets():
    """Get list of available assets"""
    try:
        assets = basic_chatbot.get_available_assets()
        return jsonify({
            'assets': assets,
            'count': len(assets),
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Enhanced Stock Analysis API is running',
        'features': [
            'OpenAI-powered question interpretation',
            'Contextual market analysis',
            'Macroeconomic insights',
            'Human-like investment advice',
            'Conversation memory and context awareness'
        ]
    })

@app.route('/api/fallback-analysis', methods=['POST'])
def fallback_analysis():
    """Fallback to basic analysis if OpenAI fails"""
    try:
        data = request.get_json()
        user_question = data.get('question', '')
        
        if not user_question:
            return jsonify({
                'error': 'No question provided',
                'response': 'Please provide a question about a stock or cryptocurrency.'
            }), 400
        
        response = basic_chatbot.process_question(user_question)
        
        return jsonify({
            'question': user_question,
            'response': response,
            'success': True,
            'enhanced': False,
            'fallback': True
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'response': 'Sorry, I encountered an error processing your request.',
            'success': False
        }), 500

@app.route('/api/conversation-history', methods=['GET'])
def get_conversation_history():
    """Get current conversation history"""
    try:
        history = enhanced_chatbot.conversation_history
        return jsonify({
            'history': history,
            'count': len(history),
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/clear-conversation', methods=['POST'])
def clear_conversation():
    """Clear conversation history"""
    try:
        enhanced_chatbot.clear_history()
        return jsonify({
            'message': 'Conversation history cleared',
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002) 