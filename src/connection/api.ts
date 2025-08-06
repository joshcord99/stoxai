import axios from "axios";

// Get backend URL from environment or default to localhost
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:5003";

const api = axios.create({
  baseURL: `${BACKEND_URL}/api`,
  headers: {
    "Content-Type": "application/json",
  },
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
    const response = await api.post("/auth/login", credentials);
    return response.data;
  },

  register: async (userData: {
    email: string;
    password: string;
    first_name: string;
    last_name: string;
  }) => {
    const response = await api.post("/auth/register", userData);
    return response.data;
  },

  getProfile: async () => {
    const response = await api.get("/auth/profile");
    return response.data;
  },

  verifyToken: async () => {
    const response = await api.get("/auth/verify-token");
    return response.data;
  },

  logout: async () => {
    const response = await api.post("/auth/logout");
    return response.data;
  },

  getWatchlist: async () => {
    const response = await api.get("/auth/watchlist");
    return response.data;
  },

  addToWatchlist: async (ticker: string) => {
    const response = await api.post("/auth/watchlist/add", { ticker });
    return response.data;
  },

  removeFromWatchlist: async (ticker: string) => {
    const response = await api.post("/auth/watchlist/remove", { ticker });
    return response.data;
  },

  getAccountInfo: async () => {
    const response = await api.get("/account/info");
    return response.data;
  },

  exportAccountData: async () => {
    const response = await api.get("/account/export");
    return response.data;
  },

  deleteAccount: async () => {
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
