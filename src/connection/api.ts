import axios from "axios";
import { mockAuthAPI } from "./mockAuth";

// Get backend URL from environment or default to Netlify functions
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "";

// Log the backend URL for debugging
console.log("Backend URL:", BACKEND_URL);

// Check if we should use mock authentication
const USE_MOCK_AUTH = import.meta.env.VITE_USE_MOCK_AUTH === "true";

if (USE_MOCK_AUTH) {
  console.log("Using mock authentication system");
}

const api = axios.create({
  baseURL: BACKEND_URL ? `${BACKEND_URL}/api` : "/.netlify/functions/api",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000, // 10 second timeout
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem("refresh_token");
        if (refreshToken) {
          const response = await axios.post(
            `${BACKEND_URL}/api/auth/refresh`,
            {},
            {
              headers: {
                Authorization: `Bearer ${refreshToken}`,
              },
            }
          );

          const { access_token } = response.data;
          localStorage.setItem("access_token", access_token);
          originalRequest.headers.Authorization = `Bearer ${access_token}`;

          return api(originalRequest);
        }
      } catch (refreshError) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  }
);

export const authAPI = {
  login: async (credentials: { email: string; password: string }) => {
    if (USE_MOCK_AUTH) {
      return await mockAuthAPI.login(credentials);
    }
    const response = await api.post("/auth/login", credentials);
    return response.data;
  },

  register: async (userData: {
    email: string;
    password: string;
    first_name: string;
    last_name: string;
  }) => {
    if (USE_MOCK_AUTH) {
      return await mockAuthAPI.register(userData);
    }
    const response = await api.post("/auth/register", userData);
    return response.data;
  },

  getProfile: async () => {
    if (USE_MOCK_AUTH) {
      return await mockAuthAPI.getProfile();
    }
    const response = await api.get("/user/profile");
    return response.data;
  },

  verifyToken: async () => {
    if (USE_MOCK_AUTH) {
      return await mockAuthAPI.verifyToken();
    }
    const response = await api.get("/user/profile");
    return response.data;
  },

  logout: async () => {
    if (USE_MOCK_AUTH) {
      return await mockAuthAPI.logout();
    }
    // For JWT, logout is handled client-side by removing the token
    localStorage.removeItem("access_token");
    return { message: "Logged out successfully" };
  },

  getWatchlist: async () => {
    if (USE_MOCK_AUTH) {
      return await mockAuthAPI.getWatchlist();
    }
    const response = await api.get("/user/profile");
    return { watchlist: response.data.user.watchlist || [] };
  },

  updateWatchlist: async (watchlist: string[]) => {
    if (USE_MOCK_AUTH) {
      return await mockAuthAPI.addToWatchlist(watchlist[0]);
    }
    const response = await api.put("/user/watchlist", { watchlist });
    return response.data;
  },

  addToWatchlist: async (ticker: string) => {
    if (USE_MOCK_AUTH) {
      return await mockAuthAPI.addToWatchlist(ticker);
    }
    // Get current watchlist and add new ticker
    const currentResponse = await api.get("/user/profile");
    const currentWatchlist = currentResponse.data.user.watchlist || [];
    const newWatchlist = [...currentWatchlist, ticker];
    const response = await api.put("/user/watchlist", {
      watchlist: newWatchlist,
    });
    return response.data;
  },

  removeFromWatchlist: async (ticker: string) => {
    if (USE_MOCK_AUTH) {
      return await mockAuthAPI.removeFromWatchlist(ticker);
    }
    // Get current watchlist and remove ticker
    const currentResponse = await api.get("/user/profile");
    const currentWatchlist = currentResponse.data.user.watchlist || [];
    const newWatchlist = currentWatchlist.filter((t: string) => t !== ticker);
    const response = await api.put("/user/watchlist", {
      watchlist: newWatchlist,
    });
    return response.data;
  },

  getAccountInfo: async () => {
    if (USE_MOCK_AUTH) {
      const user = await mockAuthAPI.getProfile();
      return { user };
    }
    const response = await api.get("/user/profile");
    return response.data;
  },

  exportAccountData: async () => {
    if (USE_MOCK_AUTH) {
      const user = await mockAuthAPI.getProfile();
      return { user, exportData: "Mock export data" };
    }
    const response = await api.get("/user/profile");
    return { user: response.data.user, exportData: "Account data export" };
  },

  deleteAccount: async () => {
    if (USE_MOCK_AUTH) {
      await mockAuthAPI.logout();
      return { message: "Account deleted successfully" };
    }
    const response = await api.delete("/account/delete");
    return response.data;
  },
};

export const healthAPI = {
  check: async () => {
    const response = await api.get("/health");
    return response.data;
  },
};

export const chatbotAPI = {
  sendMessage: async (question: string) => {
    const response = await api.post("/ai_chatbot", { question });
    return response.data;
  },
};

export const stockAPI = {
  getAvailableAssets: async () => {
    const response = await api.get("/available-assets");
    return response.data;
  },

  getAvailableStocks: async () => {
    const response = await api.get("/available-stocks");
    return response.data;
  },
};

export default api;
