# Stock Analyst Frontend

A Vue.js 3 frontend application for the Stock Analyst platform with real-time market data, portfolio management, and AI-powered chatbot integration.

## Features

- **Modern Vue.js 3** with TypeScript and Composition API
- **Real-time Market Data** with live stock prices and charts
- **Portfolio Management** with watchlist functionality
- **AI Chatbot Integration** for stock analysis and investment advice
- **Responsive Design** with Tailwind CSS
- **User Authentication** with JWT tokens
- **Chart.js Integration** for data visualization

## Quick Start

### Prerequisites

- Node.js >= 16.0.0
- npm >= 8.0.0

### Installation

```bash
# Install dependencies
npm install

# Create environment file
cp env.example .env
# Edit .env with your backend URL

# Start development server
npm run dev
```

## Environment Configuration

The frontend can connect to different backend environments by setting the `VITE_BACKEND_URL` environment variable.

### Development (Local Backend)

```env
VITE_BACKEND_URL=http://localhost:5003
```

### Production (Deployed Backend)

```env
VITE_BACKEND_URL=https://your-backend-api.com
```

### Environment Files

- `env.example` - Template with default values
- `env.development` - Development environment settings
- `env.production` - Production environment settings

## Available Scripts

### Development

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

### Code Quality

- `npm run lint` - Lint code with ESLint
- `npm run format` - Format code with Prettier
- `npm run test` - Run tests with Vitest

### Build & Deploy

- `npm run build` - Build the application
- `npm run serve` - Serve the built application

## Project Structure

```
frontend/
├── src/
│   ├── components/      # Vue components
│   │   ├── ChatBot.vue
│   │   ├── Header.vue
│   │   ├── Footer.vue
│   │   └── ...
│   ├── pages/          # Vue pages/routes
│   │   ├── Dashboard.vue
│   │   ├── Login.vue
│   │   ├── Registration.vue
│   │   └── ...
│   ├── connection/     # API services
│   │   └── api.ts      # Backend API client
│   ├── services/       # External API services
│   │   ├── finnhubApi.ts
│   │   ├── twelveDataApi.ts
│   │   └── currencyLayerApi.ts
│   ├── tools/          # Utility components
│   ├── routes/         # Vue Router configuration
│   ├── userInfo.ts     # User state management
│   ├── App.vue         # Root component
│   └── main.ts         # Application entry point
├── public/             # Static assets
├── css/               # Global styles
└── package.json       # Dependencies and scripts
```

## Backend Integration

The frontend connects to the Stock Analyst Backend API. Make sure your backend is running and accessible at the URL specified in your environment variables.

### API Endpoints Used

- **Authentication**: `/api/auth/*`
- **User Profile**: `/api/auth/profile`
- **Watchlist**: `/api/auth/watchlist/*`
- **Chatbot**: `/api/user-chatbot`
- **Health Check**: `/api/health`

## Development

### Local Development

1. **Start Backend**: Ensure your backend is running on port 5003
2. **Start Frontend**: Run `npm run dev`
3. **Access**: Open http://localhost:5173

### Connecting to External Backend

1. **Set Environment**: Update `VITE_BACKEND_URL` in your `.env` file
2. **Start Frontend**: Run `npm run dev`
3. **Verify Connection**: Check browser console for API connection status

## Building for Production

```bash
# Build the application
npm run build

# Preview the build
npm run preview

# Deploy the dist/ folder to your hosting service
```

## Dependencies

### Core Dependencies

- **Vue.js 3.5.17** - Progressive JavaScript framework
- **TypeScript 5.8.3** - Type safety
- **Vite 7.0.4** - Build tool and dev server
- **Vue Router 4.5.1** - Client-side routing
- **Pinia 3.0.3** - State management

### UI & Styling

- **Tailwind CSS 3.4.17** - Utility-first CSS framework
- **Chart.js 4.5.0** - Data visualization
- **vue-chartjs 5.3.2** - Vue wrapper for Chart.js

### HTTP & Data

- **Axios 1.11.0** - HTTP client
- **Marked 16.1.1** - Markdown processing

### Development

- **ESLint** - Code linting
- **Prettier** - Code formatting
- **Vitest** - Unit testing

## Troubleshooting

### Common Issues

- **Backend Connection Error**: Check `VITE_BACKEND_URL` in your `.env` file
- **CORS Issues**: Ensure backend CORS is configured for your frontend domain
- **Build Errors**: Run `npm run lint` to check for code issues

### Environment Variables

Make sure your `.env` file contains:

```env
VITE_BACKEND_URL=http://localhost:5003
```

## License

This project is licensed under the MIT License.
