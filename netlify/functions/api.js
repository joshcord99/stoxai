const { neon } = require("@neondatabase/serverless");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs");



// Initialize database connection
let sql;
try {
  const databaseUrl = process.env.DATABASE_URL;
  sql = neon(databaseUrl);
} catch (error) {
  throw error;
}

// JWT configuration
const JWT_SECRET = process.env.JWT_SECRET_KEY || "your-jwt-secret-key";
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
        first_name VARCHAR(100) DEFAULT NULL,
        last_name VARCHAR(100) DEFAULT NULL,
        watchlist TEXT[],
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `;
    
    // Add watchlist column if it doesn't exist (migration)
    try {
      await sql`ALTER TABLE users ADD COLUMN IF NOT EXISTS watchlist TEXT[]`;
    } catch (migrationError) {
      // Column already exists
    }
    
    // Update first_name and last_name columns to allow NULL (migration)
    try {
      await sql`ALTER TABLE users ALTER COLUMN first_name DROP NOT NULL`;
      await sql`ALTER TABLE users ALTER COLUMN last_name DROP NOT NULL`;
    } catch (migrationError) {
      // Columns already allow NULL
    }
  } catch (error) {
    throw error;
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
      const { email, password, firstName, lastName } = body;

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
          INSERT INTO users (email, password_hash, first_name, last_name, created_at, updated_at)
          VALUES (${email}, ${hashedPassword}, ${firstName || null}, ${lastName || null}, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
          RETURNING id, email, first_name, last_name, created_at, updated_at
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
              full_name: `${user.first_name || ''} ${user.last_name || ''}`.trim(),
              created_at: user.created_at,
              is_active: true,
              watchlist: [],
            },
            access_token: token,
            refresh_token: token, // For simplicity, using same token as refresh
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
          SELECT id, email, password_hash, first_name, last_name, watchlist, created_at
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
              full_name: `${user.first_name || ''} ${user.last_name || ''}`.trim(),
              watchlist: user.watchlist || [],
              created_at: user.created_at,
              is_active: true,
            },
            access_token: token,
            refresh_token: token, // For simplicity, using same token as refresh
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
              full_name: `${user.first_name || ''} ${user.last_name || ''}`.trim(),
              watchlist: user.watchlist || [],
              created_at: user.created_at,
              is_active: true,
            },
          }),
        };
      } catch (error) {
        throw error;
      }
    }

    if (path === "/user/profile" && method === "PUT") {
      const { first_name, last_name } = body;

      try {
        await sql`
          UPDATE users 
          SET first_name = ${first_name}, last_name = ${last_name}, updated_at = CURRENT_TIMESTAMP
          WHERE id = ${decoded.userId}
        `;

        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            success: true,
            message: "Profile updated successfully",
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
      
      try {
        // Check if OpenAI API key is available
        const openaiApiKey = process.env.OPENAI_API_KEY;
        
        console.log("OpenAI API Key check:", {
          hasKey: !!openaiApiKey,
          keyLength: openaiApiKey ? openaiApiKey.length : 0,
          keyStart: openaiApiKey ? openaiApiKey.substring(0, 7) + "..." : "None"
        });
        
        if (!openaiApiKey) {
          console.log("No OpenAI API key found, using fallback response");
          // Fallback to basic response if no API key
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

        // Use OpenAI API for AI-powered responses
        const OpenAI = require('openai');
        const openai = new OpenAI({
          apiKey: openaiApiKey,
        });

        // Create a context-aware prompt
        const systemPrompt = `You are an expert financial analyst and AI assistant specializing in stock and cryptocurrency analysis. 
You have access to real-time market data and can provide comprehensive investment insights.

User Information:
- Name: ${user.first_name} ${user.last_name}
- Watchlist: ${(user.watchlist || []).join(", ") || "None"}

Your capabilities include:
- Technical analysis of stocks and cryptocurrencies
- Price trend analysis and predictions
- Risk assessment and investment recommendations
- Market sentiment analysis
- Portfolio optimization advice

Provide personalized, helpful financial analysis based on the user's question. If they ask about specific stocks or crypto, give detailed insights. If they ask general questions, provide educational financial advice.`;

        const completion = await openai.chat.completions.create({
          model: "gpt-3.5-turbo",
          messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: question }
          ],
          max_tokens: 500,
          temperature: 0.7,
        });

        const aiResponse = completion.choices[0].message.content;

        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            success: true,
            response: aiResponse,
            user_context: {
              name: `${user.first_name} ${user.last_name}`,
              watchlist: user.watchlist || [],
            },
            ai_enabled: true,
          }),
        };

      } catch (error) {
        console.error("AI chatbot error:", error);
        console.error("Error details:", {
          message: error.message,
          stack: error.stack,
          openaiKey: openaiApiKey ? "Present" : "Missing",
          openaiKeyLength: openaiApiKey ? openaiApiKey.length : 0
        });
        
        // Fallback response on error
        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            success: true,
            response: `Hello ${user.first_name}! I can see you have ${(user.watchlist || []).length} items in your watchlist: ${(user.watchlist || []).join(", ") || "None"}.\n\nI'm experiencing some technical difficulties with my AI analysis right now. Please try again later for enhanced insights.\n\nDebug: ${error.message}`,
            user_context: {
              name: `${user.first_name} ${user.last_name}`,
              watchlist: user.watchlist || [],
            },
            ai_enabled: false,
            error: error.message,
          }),
        };
      }
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
