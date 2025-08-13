# StoxAI - Stock Analysis Platform

A comprehensive stock analysis platform that combines real-time market data, AI-powered chatbot assistance, and portfolio management tools.

## Features

- **Real-time Market Data**: Live stock prices and market indices
- **AI Chatbot**: Intelligent stock analysis and market insights powered by OpenAI
- **Portfolio Management**: Track and manage your investment portfolio
- **Market Headlines**: Stay updated with latest financial news
- **Stock Analysis**: Detailed technical and fundamental analysis
- **User Authentication**: Secure login and registration system
- **Responsive Design**: Modern UI that works on desktop and mobile

## Tech Stack

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Fast build tool and dev server
- **Chart.js** - Interactive charts and graphs
- **Pinia** - State management

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - Database ORM
- **JWT** - Authentication
- **OpenAI API** - AI chatbot functionality
- **yfinance** - Stock data collection
- **Pandas** - Data manipulation

### Infrastructure
- **Netlify** - Frontend hosting and serverless functions
- **Docker** - Containerization
- **PostgreSQL** - Database

## Project Structure

```
stoxai/
├── src/                    # Vue.js frontend
│   ├── components/         # Vue components
│   ├── pages/             # Page components
│   ├── services/          # API services
│   └── types/             # TypeScript definitions
├── backend/               # Flask backend
│   ├── app/               # Main application
│   ├── chatbot/           # AI chatbot modules
│   └── stock-data-collector/ # Stock data collection
├── netlify/               # Netlify configuration
└── assets/                # Static assets
```

## Getting Started

### Prerequisites

- Node.js >= 20.0.0
- Python >= 3.8
- PostgreSQL database

### Frontend Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Build for production:
```bash
npm run build
```

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp env.example .env
# Edit .env with your configuration
```

5. Run the server:
```bash
python run_server.py
```

### Environment Variables

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/stoxai
JWT_SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Usage

1. **Registration/Login**: Create an account or sign in
2. **Dashboard**: View live market data and portfolio overview
3. **Chatbot**: Ask questions about stocks and get AI-powered analysis
4. **Portfolio**: Add stocks to your portfolio and track performance
5. **Market Data**: Explore real-time stock prices and market trends

## API Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/ai_chatbot` - AI chatbot requests
- `POST /api/stock-analysis` - Stock analysis

## Development

### Available Scripts

**Frontend:**
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

**Backend:**
- `python run_server.py` - Start Flask server
- `pytest` - Run tests

### Code Style

- Frontend: ESLint + Prettier
- Backend: Black + Flake8

## Deployment

### Frontend (Netlify)
1. Connect your repository to Netlify
2. Build command: `npm run build`
3. Publish directory: `dist`

### Backend
1. Use Docker for containerization
2. Deploy to your preferred cloud platform
3. Set up environment variables

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository.
