# StoxAI - Stock Analysis Platform

A comprehensive stock analysis platform that combines real-time market data, AI-powered chatbot assistance, and portfolio management tools.

## Features

- Real-time Market Data
- AI Chatbot for stock analysis
- Portfolio Management
- Market Headlines
- User Authentication
- Responsive Design

## Interface Screenshots

### Landing Page
![Interface 1](assets/interface-1.png)

### Dashboard - Stock Analysis & Chatbot
![Interface 2](assets/interface-2.png)

## Tech Stack

- **Frontend**: Vue.js 3, TypeScript, Tailwind CSS
- **Backend**: Flask, SQLAlchemy, JWT
- **AI**: OpenAI API
- **Data**: yfinance, Pandas
- **Deployment**: Netlify, Docker

## Quick Start

### Frontend
```bash
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run_server.py
```

## Environment Setup

Create `.env` file in backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/stoxai
JWT_SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Testing Credentials

Use these accounts for testing:

**Account 1:**
- Email: sunny@gmail.com
- Password: SunnyApple123

**Account 2:**
- Email: willy@gmail.com
- Password: WillyWonka123

## Usage

1. Register/Login with the provided credentials
2. Explore the dashboard for live market data
3. Use the AI chatbot for stock analysis
4. Manage your portfolio
5. Stay updated with market headlines

## Project Structure

```
stoxai/
├── src/                    # Vue.js frontend
├── backend/               # Flask backend
├── netlify/               # Netlify configuration
└── assets/                # Static assets
```

## Deployment

- **Frontend**: Deploy to Netlify
- **Backend**: Use Docker for containerization

## License

MIT License

---

*Last updated: December 2024*
