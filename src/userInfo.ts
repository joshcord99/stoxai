import { defineStore } from "pinia";
import { authAPI } from "./connection/api";

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  created_at: string;
  is_active: boolean;
  watchlist?: string[];
}

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null as User | null,
    token: "",
    refreshToken: "",
    isAuthenticated: false,
    watchlist: [] as string[],
    stockDataCache: {} as Record<string, any>,
  }),

  getters: {
    fullName: (state) => {
      if (!state.user) return "";
      return state.user.full_name;
    },

    displayName: (state) => {
      if (!state.user) return "";
      return state.user.full_name;
    },
  },

  actions: {
    async login(credentials: { email: string; password: string }) {
      try {
        const response = await authAPI.login(credentials);

        this.token = response.access_token;
        this.refreshToken = response.refresh_token;
        this.user = response.user;
        this.isAuthenticated = true;
        this.watchlist = response.user.watchlist || [];

        localStorage.setItem("access_token", response.access_token);
        localStorage.setItem("refresh_token", response.refresh_token);
        localStorage.setItem("user", JSON.stringify(response.user));
        localStorage.setItem("watchlist", JSON.stringify(this.watchlist));

        return response;
      } catch (error) {
        throw error;
      }
    },

    async register(userData: {
      email: string;
      password: string;
      first_name: string;
      last_name: string;
    }) {
      try {
        const response = await authAPI.register(userData);

        this.token = response.access_token;
        this.refreshToken = response.refresh_token;
        this.user = response.user;
        this.isAuthenticated = true;
        this.watchlist = response.user.watchlist || [];

        localStorage.setItem("access_token", response.access_token);
        localStorage.setItem("refresh_token", response.refresh_token);
        localStorage.setItem("user", JSON.stringify(response.user));
        localStorage.setItem("watchlist", JSON.stringify(this.watchlist));

        return response;
      } catch (error) {
        throw error;
      }
    },

    async logout() {
      try {
        if (this.isAuthenticated) {
          await authAPI.logout();
        }
      } catch (error) {
      } finally {
        this.user = null;
        this.token = "";
        this.refreshToken = "";
        this.isAuthenticated = false;
        this.watchlist = [];

        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");
        localStorage.removeItem("watchlist");
      }
    },

    initializeAuth() {
      const token = localStorage.getItem("access_token");
      const refreshToken = localStorage.getItem("refresh_token");
      const userStr = localStorage.getItem("user");
      const watchlistStr = localStorage.getItem("watchlist");

      if (token && refreshToken && userStr) {
        try {
          this.token = token;
          this.refreshToken = refreshToken;
          this.user = JSON.parse(userStr);
          this.isAuthenticated = true;

          if (watchlistStr) {
            this.watchlist = JSON.parse(watchlistStr);
          }
        } catch (error) {
          this.logout();
        }
      }
    },

    clearAllCache() {
      this.watchlist = [];
      this.stockDataCache = {};
      localStorage.removeItem("watchlist");
    },

    async verifyToken() {
      try {
        const response = await authAPI.verifyToken();
        this.user = response.user;
        this.isAuthenticated = true;
        this.watchlist = response.user.watchlist || [];
        return true;
      } catch (error) {
        this.logout();
        return false;
      }
    },

    async getProfile() {
      try {
        const response = await authAPI.getProfile();
        this.user = response.user;
        this.watchlist = response.user.watchlist || [];
        return response;
      } catch (error) {
        throw error;
      }
    },

    async loadWatchlist() {
      try {
        const response = await authAPI.getWatchlist();
        this.watchlist = response.watchlist;
        localStorage.setItem("watchlist", JSON.stringify(this.watchlist));
        return response;
      } catch (error) {
        throw error;
      }
    },

    async addStock(ticker: string) {
      try {
        const response = await authAPI.addToWatchlist(ticker);

        if (response.watchlist) {
          this.watchlist = response.watchlist;
          localStorage.setItem("watchlist", JSON.stringify(this.watchlist));
        }

        return response;
      } catch (error) {
        throw error;
      }
    },

    async removeStock(ticker: string) {
      try {
        const response = await authAPI.removeFromWatchlist(ticker);

        if (response.watchlist) {
          this.watchlist = response.watchlist;
          localStorage.setItem("watchlist", JSON.stringify(this.watchlist));
        }

        delete this.stockDataCache[ticker.toUpperCase()];

        return response;
      } catch (error) {
        throw error;
      }
    },

    getCachedStockData(ticker: string) {
      return this.stockDataCache[ticker.toUpperCase()] || null;
    },

    setCachedStockData(ticker: string, data: any) {
      this.stockDataCache[ticker.toUpperCase()] = {
        ...data,
        cachedAt: Date.now(),
      };
    },

    clearStockDataCache() {
      this.stockDataCache = {};
    },

    isStockDataCached(ticker: string) {
      const cached = this.stockDataCache[ticker.toUpperCase()];
      if (!cached) return false;

      const cacheAge = Date.now() - cached.cachedAt;
      return cacheAge < 5 * 60 * 1000;
    },
  },
});
