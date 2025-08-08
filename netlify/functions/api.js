const { neon } = require("@neondatabase/serverless");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs");

// Initialize database connection
const sql = neon();

// JWT configuration
const JWT_SECRET =
  process.env.JWT_SECRET_KEY || "your-jwt-secret-key";
const JWT_EXPIRES_IN = "7d";

// Helper function to create JWT token
function createToken(userId) {
  return jwt.sign({ userId }, JWT_SECRET, { expiresIn: JWT_EXPIRES_IN });
}

// Helper function to verify JWT token
function verifyToken(token) {
  try {
    return jwt.verify(token, JWT_SECRET);
  } catch (error) {
    return null;
  }
}

// Helper function to hash password
async function hashPassword(password) {
  return await bcrypt.hash(password, 10);
}

// Helper function to compare password
async function comparePassword(password, hashedPassword) {
  return await bcrypt.compare(password, hashedPassword);
}

// Initialize database tables
async function initializeDatabase() {
  try {
    await sql`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        watchlist TEXT[],
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `;
  } catch (error) {
    console.error("Database initialization error:", error);
  }
}

// Main handler function
exports.handler = async (event, context) => {
  // Enable CORS
  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Content-Type": "application/json",
  };

  // Handle preflight requests
  if (event.httpMethod === "OPTIONS") {
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({}),
    };
  }

  try {
    // Initialize database
    await initializeDatabase();

    const path = event.path.replace("/.netlify/functions/api", "");
    const method = event.httpMethod;

    // Parse request body
    let body = {};
    if (event.body) {
      try {
        body = JSON.parse(event.body);
      } catch (error) {
        console.error("Error parsing request body:", error);
      }
    }

    // Route handling
    if (path === "/health" && method === "GET") {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          status: "healthy",
          message: "Stock Analyst API is running",
        }),
      };
    }

    // Authentication routes
    if (path === "/auth/register" && method === "POST") {
      const { email, password, first_name, last_name } = body;

      if (!email || !password) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({
            success: false,
            error: "Email and password are required",
          }),
        };
      }

      try {
        const hashedPassword = await hashPassword(password);

        const result = await sql`
          INSERT INTO users (email, password_hash, first_name, last_name)
          VALUES (${email}, ${hashedPassword}, ${first_name || null}, ${last_name || null})
          RETURNING id, email, first_name, last_name
        `;

        const user = result[0];
        const token = createToken(user.id);

        return {
          statusCode: 201,
          headers,
          body: JSON.stringify({
            success: true,
            message: "User registered successfully",
            user: {
              id: user.id,
              email: user.email,
              first_name: user.first_name,
              last_name: user.last_name,
            },
            token,
          }),
        };
      } catch (error) {
        if (error.code === "23505") {
          // Unique constraint violation
          return {
            statusCode: 400,
            headers,
            body: JSON.stringify({
              success: false,
              error: "Email already exists",
            }),
          };
        }
        throw error;
      }
    }

    if (path === "/auth/login" && method === "POST") {
      const { email, password } = body;

      if (!email || !password) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({
            success: false,
            error: "Email and password are required",
          }),
        };
      }

      try {
        const result = await sql`
          SELECT id, email, password_hash, first_name, last_name, watchlist
          FROM users WHERE email = ${email}
        `;

        if (result.length === 0) {
          return {
            statusCode: 401,
            headers,
            body: JSON.stringify({
              success: false,
              error: "Invalid credentials",
            }),
          };
        }

        const user = result[0];
        const isValidPassword = await comparePassword(
          password,
          user.password_hash
        );

        if (!isValidPassword) {
          return {
            statusCode: 401,
            headers,
            body: JSON.stringify({
              success: false,
              error: "Invalid credentials",
            }),
          };
        }

        const token = createToken(user.id);

        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            success: true,
            message: "Login successful",
            user: {
              id: user.id,
              email: user.email,
              first_name: user.first_name,
              last_name: user.last_name,
              watchlist: user.watchlist || [],
            },
            token,
          }),
        };
      } catch (error) {
        throw error;
      }
    }

    // Protected routes - require authentication
    const authHeader =
      event.headers.authorization || event.headers.Authorization;
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return {
        statusCode: 401,
        headers,
        body: JSON.stringify({
          success: false,
          error: "Authentication required",
        }),
      };
    }

    const token = authHeader.replace("Bearer ", "");
    const decoded = verifyToken(token);

    if (!decoded) {
      return {
        statusCode: 401,
        headers,
        body: JSON.stringify({
          success: false,
          error: "Invalid or expired token",
        }),
      };
    }

    // User-specific routes
    if (path === "/user/profile" && method === "GET") {
      try {
        const result = await sql`
          SELECT id, email, first_name, last_name, watchlist, created_at
          FROM users WHERE id = ${decoded.userId}
        `;

        if (result.length === 0) {
          return {
            statusCode: 404,
            headers,
            body: JSON.stringify({
              success: false,
              error: "User not found",
            }),
          };
        }

        const user = result[0];
        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            success: true,
            user: {
              id: user.id,
              email: user.email,
              first_name: user.first_name,
              last_name: user.last_name,
              watchlist: user.watchlist || [],
              created_at: user.created_at,
            },
          }),
        };
      } catch (error) {
        throw error;
      }
    }

    if (path === "/user/watchlist" && method === "PUT") {
      const { watchlist } = body;

      if (!Array.isArray(watchlist)) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({
            success: false,
            error: "Watchlist must be an array",
          }),
        };
      }

      try {
        await sql`
          UPDATE users 
          SET watchlist = ${watchlist}, updated_at = CURRENT_TIMESTAMP
          WHERE id = ${decoded.userId}
        `;

        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            success: true,
            message: "Watchlist updated successfully",
            watchlist,
          }),
        };
      } catch (error) {
        throw error;
      }
    }

    // Chatbot routes
    if (path === "/ai_chatbot" && method === "POST") {
      const { question } = body;

      if (!question) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({
            success: false,
            error: "Question is required",
          }),
        };
      }

      // Get user context
      const userResult = await sql`
        SELECT first_name, last_name, watchlist
        FROM users WHERE id = ${decoded.userId}
      `;

      const user = userResult[0];
      const userContext = `
User Information:
- Name: ${user.first_name} ${user.last_name}
- Watchlist: ${(user.watchlist || []).join(", ")}

User Question: ${question}

Please provide personalized analysis considering the user's watchlist and preferences.
      `;

      // For now, return a basic response
      // In production, you would integrate with OpenAI or another AI service
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          response: `Hello ${user.first_name}! I can see you have ${(user.watchlist || []).length} items in your watchlist: ${(user.watchlist || []).join(", ") || "None"}.\n\nThis is a basic response. For enhanced AI analysis, please configure an AI service integration.`,
          user_context: {
            name: `${user.first_name} ${user.last_name}`,
            watchlist: user.watchlist || [],
          },
          ai_enabled: false,
        }),
      };
    }

    // Stock data routes
    if (path === "/available-assets" && method === "GET") {
      const assets = [
        "AAPL",
        "GOOGL",
        "MSFT",
        "AMZN",
        "TSLA",
        "META",
        "NVDA",
        "NFLX",
        "BTC",
        "ETH",
        "ADA",
        "DOT",
        "LINK",
        "LTC",
        "BCH",
        "UNI",
        "ATOM",
        "EUR/USD",
        "GBP/USD",
        "USD/JPY",
        "AUD/USD",
        "USD/CAD",
      ];

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          assets,
        }),
      };
    }

    if (path === "/available-stocks" && method === "GET") {
      const stocks = [
        "AAPL",
        "GOOGL",
        "MSFT",
        "AMZN",
        "TSLA",
        "META",
        "NVDA",
        "NFLX",
        "ADBE",
        "CRM",
        "ORCL",
        "PYPL",
        "INTC",
        "AMD",
        "CSCO",
        "IBM",
      ];

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          stocks,
        }),
      };
    }

    // Account management routes
    if (path === "/account/delete" && method === "DELETE") {
      try {
        await sql`
          DELETE FROM users WHERE id = ${decoded.userId}
        `;

        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            success: true,
            message: "Account deleted successfully",
          }),
        };
      } catch (error) {
        throw error;
      }
    }

    // Default response for unmatched routes
    return {
      statusCode: 404,
      headers,
      body: JSON.stringify({
        success: false,
        error: "Endpoint not found",
      }),
    };
  } catch (error) {
    console.error("Server error:", error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: "Internal server error",
      }),
    };
  }
};
