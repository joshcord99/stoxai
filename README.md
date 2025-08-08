# StoxAI - Stock Analysis Platform

A comprehensive stock analysis platform built with Vue.js and deployed on Netlify with Neon database integration.

## Features

- User authentication and registration
- Real-time stock data visualization
- AI-powered chatbot for stock analysis
- Personalized watchlists
- Market headlines and news
- Portfolio tracking
- Responsive design with Tailwind CSS

## Tech Stack

- **Frontend**: Vue.js 3 with TypeScript
- **Backend**: Netlify Serverless Functions
- **Database**: Neon PostgreSQL
- **Styling**: Tailwind CSS
- **Charts**: Chart.js with vue-chartjs
- **Authentication**: JWT with bcryptjs

## Project Structure

```
stoxai/
├── src/                    # Vue.js source code
│   ├── components/         # Vue components
│   ├── pages/             # Page components
│   ├── connection/         # API connection layer
│   └── ...
├── netlify/
│   └── functions/         # Serverless functions
│       └── api.js         # Main API handler
├── netlify.toml           # Netlify configuration
└── package.json           # Dependencies
```

## Setup Instructions

### 1. Prerequisites

- Node.js 18+ installed
- Netlify account
- Neon database (already provisioned)

### 2. Local Development

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd stoxai
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory:

   ```
   VITE_USE_MOCK_AUTH=true
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

### 3. Netlify Deployment

1. **Connect to Netlify**:
   - Push your code to GitHub
   - Connect your repository to Netlify
   - Set the build command: `npm run build`
   - Set the publish directory: `dist`

2. **Environment Variables**:
   In your Netlify dashboard, set these environment variables:

   ```
   JWT_SECRET_KEY=your-jwt-secret-key
   NETLIFY_DATABASE_URL=your-neon-database-url
   NETLIFY_DATABASE_URL_UNPOOLED=your-neon-database-url-unpooled
   ```

3. **Neon Database Setup**:
   - Your Neon database is already provisioned
   - The serverless functions will automatically create the required tables
   - Make sure to claim your database to prevent expiration

### 4. Database Schema

The application automatically creates the following table:

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  watchlist TEXT[],
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints

### Authentication

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### User Management

- `GET /api/user/profile` - Get user profile
- `PUT /api/user/watchlist` - Update watchlist

### Chatbot

- `POST /api/ai_chatbot` - Send message to AI chatbot

### Stock Data

- `GET /api/available-assets` - Get available assets
- `GET /api/available-stocks` - Get available stocks

### Account Management

- `DELETE /api/account/delete` - Delete user account

### Health Check

- `GET /api/health` - API health check

## Development Notes

- The application uses JWT for authentication
- Passwords are hashed using bcryptjs
- The database connection uses Neon's serverless driver
- All API calls are routed through Netlify functions
- CORS is enabled for cross-origin requests

## Troubleshooting

1. **Database Connection Issues**:
   - Verify your Neon database URL in environment variables
   - Ensure the database is claimed and active

2. **Authentication Issues**:
   - Check that JWT_SECRET_KEY is set
   - Verify token expiration settings

3. **Build Issues**:
   - Ensure Node.js version is 18+
   - Clear node_modules and reinstall if needed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
