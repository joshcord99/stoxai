import axios from "axios";
import { mockAuthAPI } from "./mockAuth";

// Get backend URL from environment or default to localhost
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:5003";

// Log the backend URL for debugging
console.log("Backend URL:", BACKEND_URL);

// Check if we should use mock authentication
const USE_MOCK_AUTH = import.meta.env.VITE_USE_MOCK_AUTH === 'true';

if (USE_MOCK_AUTH) {
  console.log("Using mock authentication system");
}

const api = axios.create({
  baseURL: `${BACKEND_URL}/api`,
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
    const response = await api.get("/auth/profile");
    return response.data;
  },

  verifyToken: async () => {
    if (USE_MOCK_AUTH) {
      return await mockAuthAPI.verifyToken();
    }
    const response = await api.get("/auth/verify-token");
    return response.data;
  },

  logout: async () => {
    if (USE_MOCK_AUTH) {
      return await mockAuthAPI.logout();
    }
    const response = await api.post("/auth/logout");
    return response.data;
  },

  getWatchlist: async () => {
    if (USE_MOCK_AUTH) {
      return await mockAuthAPI.getWatchlist();
    }
    const response = await api.get("/auth/watchlist");
    return response.data;
  },

  addToWatchlist: async (ticker: string) => {
    if (USE_MOCK_AUTH) {
      return await mockAuthAPI.addToWatchlist(ticker);
    }
    const response = await api.post("/auth/watchlist/add", { ticker });
    return response.data;
  },

  removeFromWatchlist: async (ticker: string) => {
    if (USE_MOCK_AUTH) {
      return await mockAuthAPI.removeFromWatchlist(ticker);
    }
    const response = await api.post("/auth/watchlist/remove", { ticker });
    return response.data;
  },

  getAccountInfo: async () => {
    if (USE_MOCK_AUTH) {
      const user = await mockAuthAPI.getProfile();
      return { user };
    }
    const response = await api.get("/account/info");
    return response.data;
  },

  exportAccountData: async () => {
    if (USE_MOCK_AUTH) {
      const user = await mockAuthAPI.getProfile();
      return { user, exportData: "Mock export data" };
    }
    const response = await api.get("/account/export");
    return response.data;
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

export default api;
