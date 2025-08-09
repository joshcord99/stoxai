# Stock Analyst Backend API

A Flask-based REST API with AI-powered chatbot for stock analysis and portfolio management.

## Features

- **User Authentication**: JWT-based authentication with refresh tokens
- **AI Chatbot**: OpenAI-powered stock analysis and investment advice
- **Portfolio Management**: Watchlist management and stock tracking
- **Stock Analysis**: Technical analysis using historical data
- **Multi-sector Coverage**: Stocks across Technology, Healthcare, Financial, Energy, and more
- **Cryptocurrency Support**: Real-time crypto data and analysis

## Quick Start

### Prerequisites

- Python >= 3.8.0
- Node.js >= 16.0.0 (for npm scripts)
- PostgreSQL (or SQLite for development)

### Installation

#### Option 1: Quick Start with Virtual Environment (Recommended)

```bash
# Clone the repository
git clone <your-backend-repo-url>
cd stock-analyst-backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cp env.example .env
# Edit .env with your configuration

# Start backend server
./start_backend.sh  # On Windows: python run_server.py
```

#### Option 2: Using npm scripts (Legacy)

```bash
# Install dependencies
npm run setup

# Start development server
npm run dev
```

## Available Scripts

### Development

- `npm run dev` - Start both server and chatbot in development mode
- `npm run server` - Start Flask server only
- `npm run chatbot` - Start AI chatbot service only

### Production

- `npm start` - Start in production mode
- `npm run production` - Start both server and chatbot in production mode

### Setup & Testing

- `npm run setup` - Create virtual environment and install dependencies
- `npm run install-deps` - Install Python dependencies
- `npm run test` - Run backend tests
- `npm run lint` - Lint Python code
- `npm run format` - Format Python code with Black
- `npm run clean` - Clean Python artifacts

### Health Checks

- `npm run health` - Check backend health (port 5003)
- `npm run chatbot-health` - Check chatbot health (port 5002)

## Architecture

### New Hybrid Architecture (Recommended)

**Frontend**: Netlify (Vue.js)

- **User Management**: Netlify Functions (login, registration, profile)
- **Stock Analysis**: Python Backend (direct access to CSV data and technical analysis)

**Backend**: Python Flask

- **Stock Analysis**: Direct integration with StockAnalyzer class
- **Market Data**: Access to local CSV files with historical data
- **Technical Indicators**: SMA, EMA, RSI, MACD, Bollinger Bands

### Ports

- **Backend API**: 5003
- **Chatbot API**: 5002

### Technology Stack

- **Framework**: Flask (Python)
- **Database**: SQLAlchemy with PostgreSQL/SQLite
- **Authentication**: Flask-JWT-Extended
- **AI Chatbot**: OpenAI API + Custom stock analysis models
- **Data Sources**: Multiple financial APIs (Finnhub, Twelve Data, Currency Layer)
- **CORS**: Flask-CORS for cross-origin requests

## API Endpoints

### Authentication

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/profile` - Get user profile
- `GET /api/auth/verify-token` - Verify JWT token
- `POST /api/auth/refresh` - Refresh JWT token

### Watchlist Management

- `GET /api/auth/watchlist` - Get user watchlist
- `POST /api/auth/watchlist/add` - Add stock to watchlist
- `POST /api/auth/watchlist/remove` - Remove stock from watchlist

### Chatbot & Analysis

- `POST /api/ai_chatbot` - AI-powered chatbot for general questions
- `POST /api/stock-analysis` - **NEW**: Direct stock analysis using Python StockAnalyzer
- `POST /api/user-chatbot` - User-specific chatbot with watchlist context

- `POST /api/ai_chatbot` - AI chatbot endpoint
- `POST /api/test-chatbot` - Test chatbot without authentication
- `POST /api/user-chatbot` - Authenticated chatbot with user context
- `POST /api/stock-analysis` - Basic stock analysis

### Account Management

- `GET /api/account/info` - Get account information
- `GET /api/account/export` - Export user data
- `DELETE /api/account/delete` - Delete user account

### Health & Assets

- `GET /api/health` - Health check
- `GET /api/available-assets` - Get available assets
- `GET /api/available-stocks` - Get available stocks

## Environment Variables

Create a `.env` file based on `env.example`:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/stock_analyst
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DATABASE=stock_analyst

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key
SECRET_KEY=your-secret-key

# OpenAI Configuration (for AI chatbot)
OPENAI_API_KEY=your-openai-api-key-here

# API Keys for Financial Data
FINNHUB_API_KEY=your-finnhub-api-key
TWELVE_DATA_API_KEY=your-twelve-data-api-key
CURRENCY_LAYER_API_KEY=your-currency-layer-api-key

# Development Settings
FLASK_ENV=development
DEBUG=True
```

## Project Structure

```
backend/
├── app/                    # Flask application
│   ├── main.py            # Main Flask app and routes
│   ├── models/            # Database models
│   │   └── user.py        # User model
│   ├── routes/            # API routes
│   │   └── auth.py        # Authentication routes
│   └── utils/             # Utilities
│       └── config.py      # Configuration
├── chatbot/               # AI chatbot services
│   ├── chat_response_router.py  # Chatbot API server
│   ├── ai_chatbot.py     # OpenAI integration
│   ├── basic_chatbot.py  # Basic chatbot fallback
│   └── stock_analyzer_model/  # Stock analysis models
├── tools/                 # Utility tools
│   └── account_manager.py # Account management utilities
├── stock-data-collector/  # Market data collection
│   └── market_data/       # Historical stock data
├── run_server.py          # Server entry point
├── requirements.txt       # Python dependencies
├── package.json           # NPM scripts and config
└── env.example           # Environment template
```

## Dependencies

### Python Dependencies (requirements.txt)

- Flask>=3.0.0,<4.0.0
- Flask-SQLAlchemy>=3.0.0,<4.0.0
- Flask-JWT-Extended>=4.5.0,<5.0.0
- Flask-CORS>=4.0.0,<5.0.0
- Werkzeug>=3.0.0,<4.0.0
- requests>=2.30.0,<3.0.0
- psycopg2-binary>=2.9.0
- openai>=1.0.0
- pandas>=2.0.0
- numpy>=1.20.0
- yfinance>=0.2.0
- python-dotenv>=1.0.0

### Development Dependencies

- pytest (testing)
- flake8 (linting)
- black (code formatting)

## Testing

```bash
# Run all tests
npm run test

# Run specific test file
python3 -m pytest tests/test_auth.py
```

## Code Quality

```bash
# Format code
npm run format

# Lint code
npm run lint
```

## Deployment

### Production Deployment

```bash
# Install dependencies
npm run setup

# Set production environment variables
# Edit .env with production values

# Start production server
npm start
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5003 5002

CMD ["npm", "start"]
```

## Health Monitoring

```bash
# Check backend health
curl http://localhost:5003/api/health

# Check chatbot health
curl http://localhost:5002/api/health
```

## Troubleshooting

### Common Issues

- **Port conflicts**: Use `lsof -ti:5002 5003 | xargs kill -9` to clear occupied ports
- **Python environment issues**: Use `npm run clean && npm run setup` to reset environment
- **Database connection**: Ensure PostgreSQL is running and credentials are correct
- **OpenAI API**: Verify your OpenAI API key is valid and has sufficient credits

### Reset Everything

```bash
# Clean everything and start fresh
npm run clean
npm run setup
npm run dev
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
