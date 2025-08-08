#!/usr/bin/env node

import https from "https";
import http from "http";

// Update this URL to match your backend
const BACKEND_URL =
  process.env.BACKEND_URL || "https://stoxai-backend.onrender.com";

console.log("Testing your backend connection...");
console.log(`URL: ${BACKEND_URL}`);

function testEndpoint(path) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, BACKEND_URL);
    const client = url.protocol === "https:" ? https : http;

    const req = client.get(url, (res) => {
      let data = "";

      res.on("data", (chunk) => {
        data += chunk;
      });

      res.on("end", () => {
        resolve({
          status: res.statusCode,
          headers: res.headers,
          data: data,
        });
      });
    });

    req.on("error", (err) => {
      reject(err);
    });

    req.setTimeout(10000, () => {
      req.destroy();
      reject(new Error("Request timeout"));
    });
  });
}

async function runTests() {
  const endpoints = [
    // Root endpoints
    "/",
    "/api",
    "/api/health",
    "/health",
    "/status",

    // Auth endpoints (different patterns)
    "/api/auth",
    "/auth",
    "/api/auth/login",
    "/auth/login",
    "/api/auth/register",
    "/auth/register",
    "/api/auth/profile",
    "/auth/profile",
    "/api/auth/verify-token",
    "/auth/verify-token",
    "/api/auth/logout",
    "/auth/logout",

    // Watchlist endpoints
    "/api/auth/watchlist",
    "/auth/watchlist",
    "/api/watchlist",
    "/watchlist",

    // Chatbot endpoints
    "/api/user-chatbot",
    "/api/chatbot",
    "/user-chatbot",
    "/chatbot",

    // Other common patterns
    "/api/users",
    "/users",
    "/api/user",
    "/user",
  ];

  console.log("\nTesting endpoints on your backend:");

  for (const endpoint of endpoints) {
    try {
      console.log(`\nTesting: ${endpoint}`);
      const result = await testEndpoint(endpoint);
      console.log(`Status: ${result.status}`);
      if (result.status === 200) {
        console.log(`Response: ${result.data.substring(0, 200)}...`);
      }
    } catch (error) {
      console.log(`Error: ${error.message}`);
    }
  }

  console.log("\nSummary:");
  console.log("- If you see 200 status codes, your backend is working!");
  console.log(
    "- If you see 404 errors, those endpoints need to be implemented"
  );
  console.log(
    "- If you see connection errors, check if your backend is running"
  );
}

runTests().catch(console.error);
