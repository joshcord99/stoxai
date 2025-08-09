import axios, { AxiosRequestConfig, AxiosResponse } from "axios";
import { mockAuthAPI } from "./mockAuth";

declare module "axios" {
  export interface AxiosRequestConfig {
    _retry?: boolean;
  }
}

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "";
const USE_MOCK_AUTH = import.meta.env.VITE_USE_MOCK_AUTH === "true";

const api = axios.create({
  baseURL: BACKEND_URL ? `${BACKEND_URL}/api` : "/.netlify/functions/api",
  headers: { "Content-Type": "application/json" },
  timeout: 10000,
  withCredentials: false,
});

api.interceptors.request.use(
  (config) => {
    const token = typeof localStorage !== "undefined" ? localStorage.getItem("access_token") : null;
    if (!config.headers) config.headers = {};
    if (token) (config.headers as Record<string, string>).Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error) => {
    const originalRequest = error.config as AxiosRequestConfig;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = typeof localStorage !== "undefined" ? localStorage.getItem("refresh_token") : null;
        if (refreshToken) {
          const refreshUrl = BACKEND_URL
            ? `${BACKEND_URL}/api/auth/refresh`
            : "/.netlify/functions/api/auth/refresh";

          const response = await axios.post(
            refreshUrl,
            {},
            { headers: { Authorization: `Bearer ${refreshToken}` } }
          );

          const { access_token } = response.data || {};
          if (access_token && typeof localStorage !== "undefined") {
            localStorage.setItem("access_token", access_token);
            originalRequest.headers = {
              ...(originalRequest.headers as Record<string, string>),
              Authorization: `Bearer ${access_token}`,
            };
            return api(originalRequest);
          }
        }
      } catch {
        if (typeof localStorage !== "undefined") {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
        }
        if (typeof window !== "undefined") {
          window.location.href = "/login";
        }
      }
    }

    return Promise.reject(error);
  }
);

export const authAPI = {
  login: async (credentials: { email: string; password: string }) => {
    if (USE_MOCK_AUTH) return await mockAuthAPI.login(credentials);
    const { data } = await api.post("/auth/login", credentials);
    return data;
  },

  register: async (userData: {
    email: string;
    password: string;
    firstName: string;
    lastName: string;
  }) => {
    if (USE_MOCK_AUTH) return await mockAuthAPI.register(userData);
    const { data } = await api.post("/auth/register", {
      email: userData.email,
      password: userData.password,
      first_name: userData.firstName,
      last_name: userData.lastName,
    });
    return data;
  },

  getProfile: async () => {
    if (USE_MOCK_AUTH) return await mockAuthAPI.getProfile();
    const { data } = await api.get("/user/profile");
    return data;
  },

  verifyToken: async () => {
    if (USE_MOCK_AUTH) return await mockAuthAPI.verifyToken();
    const { data } = await api.get("/user/profile");
    return data;
  },

  logout: async () => {
    if (USE_MOCK_AUTH) return await mockAuthAPI.logout();
    if (typeof localStorage !== "undefined") localStorage.removeItem("access_token");
    return { message: "Logged out successfully" };
  },

  getWatchlist: async () => {
    if (USE_MOCK_AUTH) return { watchlist: (await mockAuthAPI.getWatchlist()) ?? [] };
    const { data } = await api.get("/user/profile");
    return { watchlist: data.user?.watchlist ?? [] };
  },

  updateWatchlist: async (watchlist: string[]) => {
    if (USE_MOCK_AUTH) return await (mockAuthAPI as any).updateWatchlist?.(watchlist);
    const { data } = await api.put("/user/watchlist", { watchlist });
    return data;
  },

  addToWatchlist: async (ticker: string) => {
    if (USE_MOCK_AUTH) return await mockAuthAPI.addToWatchlist(ticker);
    const { data: current } = await api.get("/user/profile");
    const currentWatchlist: string[] = current.user?.watchlist ?? [];
    const newWatchlist = Array.from(new Set([...currentWatchlist, ticker]));
    const { data } = await api.put("/user/watchlist", { watchlist: newWatchlist });
    return data;
  },

  removeFromWatchlist: async (ticker: string) => {
    if (USE_MOCK_AUTH) return await mockAuthAPI.removeFromWatchlist(ticker);
    const { data: current } = await api.get("/user/profile");
    const currentWatchlist: string[] = current.user?.watchlist ?? [];
    const newWatchlist = currentWatchlist.filter((t: string) => t !== ticker);
    const { data } = await api.put("/user/watchlist", { watchlist: newWatchlist });
    return data;
  },

  getAccountInfo: async () => {
    if (USE_MOCK_AUTH) return { user: await mockAuthAPI.getProfile() };
    const { data } = await api.get("/user/profile");
    return data;
  },

  exportAccountData: async () => {
    if (USE_MOCK_AUTH) return { user: await mockAuthAPI.getProfile(), exportData: "Mock export data" };
    const { data } = await api.get("/user/profile");
    return { user: data.user, exportData: "Account data export" };
  },

  deleteAccount: async () => {
    if (USE_MOCK_AUTH) {
      await mockAuthAPI.logout();
      return { message: "Account deleted successfully" };
    }
    const { data } = await api.delete("/account/delete");
    return data;
  },
};

export const healthAPI = {
  check: async () => {
    const { data } = await api.get("/health");
    return data;
  },
};

export const chatbotAPI = {
  sendMessage: async (question: string) => {
    const { data } = await api.post("/ai_chatbot", { question });
    return data;
  },
};

export const stockAPI = {
  analyze: async (symbol: string, question: string) => {
    const { data } = await api.post("/stock-analysis", { symbol, question });
    return data;
  },

  getAvailableAssets: async () => {
    const { data } = await api.get("/available-assets");
    return data;
  },

  getAvailableStocks: async () => {
    const { data } = await api.get("/available-stocks");
    return data;
  },
};

export default api;