const { neon } = require("@neondatabase/serverless");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs");
const fetch = require("node-fetch");

let sql;
try {
  const databaseUrl = process.env.DATABASE_URL;
  sql = neon(databaseUrl);
} catch (error) {
  throw error;
}

const JWT_SECRET = process.env.JWT_SECRET_KEY || "your-jwt-secret-key";
const JWT_EXPIRES_IN = "7d";

function createToken(userId) {
  return jwt.sign({ userId }, JWT_SECRET, { expiresIn: JWT_EXPIRES_IN });
}

function verifyToken(token) {
  try {
    return jwt.verify(token, JWT_SECRET);
  } catch (error) {
    return null;
  }
}

async function hashPassword(password) {
  return await bcrypt.hash(password, 10);
}

async function comparePassword(password, hashedPassword) {
  return await bcrypt.compare(password, hashedPassword);
}

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

    try {
      await sql`ALTER TABLE users ADD COLUMN IF NOT EXISTS watchlist TEXT[]`;
    } catch (migrationError) {}

    try {
      await sql`ALTER TABLE users ALTER COLUMN first_name DROP NOT NULL`;
      await sql`ALTER TABLE users ALTER COLUMN last_name DROP NOT NULL`;
    } catch (migrationError) {}
  } catch (error) {
    throw error;
  }
}

exports.handler = async (event, context) => {
  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Content-Type": "application/json",
  };

  if (event.httpMethod === "OPTIONS") {
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({}),
    };
  }

  try {
    await initializeDatabase();

    const path = event.path.replace("/.netlify/functions/api", "");
    const method = event.httpMethod;

    let body = {};
    if (event.body) {
      try {
        body = JSON.parse(event.body);
      } catch (error) {}
    }

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
          INSERT INTO users (email, password_hash, first_name, last_name, created_at, updated_at)
          VALUES (${email}, ${hashedPassword}, ${first_name || null}, ${last_name || null}, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
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
              full_name:
                `${user.first_name || ""} ${user.last_name || ""}`.trim(),
              created_at: user.created_at,
              is_active: true,
              watchlist: [],
            },
            access_token: token,
            refresh_token: token,
          }),
        };
      } catch (error) {
        if (error.code === "23505") {
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
              full_name:
                `${user.first_name || ""} ${user.last_name || ""}`.trim(),
              watchlist: user.watchlist || [],
              created_at: user.created_at,
              is_active: true,
            },
            access_token: token,
            refresh_token: token,
          }),
        };
      } catch (error) {
        throw error;
      }
    }

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
              full_name:
                `${user.first_name || ""} ${user.last_name || ""}`.trim(),
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

      const userResult = await sql`
        SELECT first_name, last_name, watchlist
        FROM users WHERE id = ${decoded.userId}
      `;

      const user = userResult[0];

      try {
        const openaiApiKey = process.env.OPENAI_API_KEY;

        if (!openaiApiKey) {
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

        const response = await fetch(
          "https://api.openai.com/v1/chat/completions",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${openaiApiKey}`,
            },
            body: JSON.stringify({
              model: "gpt-4o",
              messages: [
                { role: "system", content: systemPrompt },
                { role: "user", content: question },
              ],
              max_tokens: 500,
              temperature: 0.7,
            }),
          }
        );

        if (!response.ok) {
          throw new Error(
            `OpenAI API error: ${response.status} ${response.statusText}`
          );
        }

        const data = await response.json();
        const aiResponse = data.choices[0].message.content;

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
        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            success: true,
            response: `Hello ${user.first_name}! I can see you have ${(user.watchlist || []).length} items in your watchlist: ${(user.watchlist || []).join(", ") || "None"}.\n\nI'm experiencing some technical difficulties with my AI analysis right now. Please try again later for enhanced insights.`,
            user_context: {
              name: `${user.first_name} ${user.last_name}`,
              watchlist: user.watchlist || [],
            },
            ai_enabled: false,
          }),
        };
      }
    }

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

    return {
      statusCode: 404,
      headers,
      body: JSON.stringify({
        success: false,
        error: "Endpoint not found",
      }),
    };
  } catch (error) {
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
