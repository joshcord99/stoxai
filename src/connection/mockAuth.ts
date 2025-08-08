// Mock authentication system for development
// This simulates a backend API for user authentication

interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  watchlist: string[];
}

interface AuthResponse {
  access_token: string;
  refresh_token: string;
  user: User;
}

// Mock user database
const mockUsers: User[] = [];
const mockTokens = new Map<string, string>(); // token -> email

const generateToken = (): string => {
  return "mock_token_" + Math.random().toString(36).substr(2, 9);
};

const findUserByEmail = (email: string): User | undefined => {
  return mockUsers.find((user) => user.email === email);
};

const createUser = (userData: {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}): User => {
  const user: User = {
    id: Date.now().toString(),
    email: userData.email,
    first_name: userData.first_name,
    last_name: userData.last_name,
    full_name: `${userData.first_name} ${userData.last_name}`,
    watchlist: [],
  };

  mockUsers.push(user);
  return user;
};

export const mockAuthAPI = {
  login: async (credentials: {
    email: string;
    password: string;
  }): Promise<AuthResponse> => {
    // Simulate network delay
    await new Promise((resolve) => setTimeout(resolve, 500));

    const user = findUserByEmail(credentials.email);
    if (!user) {
      throw new Error("User not found. Please register first.");
    }

    // In a real app, you'd verify the password
    if (credentials.password.length < 6) {
      throw new Error("Invalid credentials");
    }

    const access_token = generateToken();
    const refresh_token = generateToken();

    mockTokens.set(access_token, user.email);

    return {
      access_token,
      refresh_token,
      user,
    };
  },

  register: async (userData: {
    email: string;
    password: string;
    first_name: string;
    last_name: string;
  }): Promise<AuthResponse> => {
    // Simulate network delay
    await new Promise((resolve) => setTimeout(resolve, 500));

    const existingUser = findUserByEmail(userData.email);
    if (existingUser) {
      throw new Error("User with this email already exists");
    }

    if (userData.password.length < 6) {
      throw new Error("Password must be at least 6 characters long");
    }

    const user = createUser(userData);
    const access_token = generateToken();
    const refresh_token = generateToken();

    mockTokens.set(access_token, user.email);

    return {
      access_token,
      refresh_token,
      user,
    };
  },

  getProfile: async (): Promise<User> => {
    await new Promise((resolve) => setTimeout(resolve, 300));

    // In a real app, you'd get the user from the token
    const token = localStorage.getItem("access_token");
    if (!token || !mockTokens.has(token)) {
      throw new Error("Unauthorized");
    }

    const email = mockTokens.get(token);
    const user = findUserByEmail(email!);

    if (!user) {
      throw new Error("User not found");
    }

    return user;
  },

  verifyToken: async (): Promise<{ valid: boolean; user?: User }> => {
    await new Promise((resolve) => setTimeout(resolve, 200));

    const token = localStorage.getItem("access_token");
    if (!token || !mockTokens.has(token)) {
      return { valid: false };
    }

    const email = mockTokens.get(token);
    const user = findUserByEmail(email!);

    return { valid: true, user };
  },

  logout: async (): Promise<void> => {
    await new Promise((resolve) => setTimeout(resolve, 200));

    const token = localStorage.getItem("access_token");
    if (token) {
      mockTokens.delete(token);
    }
  },

  getWatchlist: async (): Promise<{ watchlist: string[] }> => {
    await new Promise((resolve) => setTimeout(resolve, 300));

    const token = localStorage.getItem("access_token");
    if (!token || !mockTokens.has(token)) {
      throw new Error("Unauthorized");
    }

    const email = mockTokens.get(token);
    const user = findUserByEmail(email!);

    return { watchlist: user?.watchlist || [] };
  },

  addToWatchlist: async (ticker: string): Promise<void> => {
    await new Promise((resolve) => setTimeout(resolve, 300));

    const token = localStorage.getItem("access_token");
    if (!token || !mockTokens.has(token)) {
      throw new Error("Unauthorized");
    }

    const email = mockTokens.get(token);
    const user = findUserByEmail(email!);

    if (user && !user.watchlist.includes(ticker)) {
      user.watchlist.push(ticker);
    }
  },

  removeFromWatchlist: async (ticker: string): Promise<void> => {
    await new Promise((resolve) => setTimeout(resolve, 300));

    const token = localStorage.getItem("access_token");
    if (!token || !mockTokens.has(token)) {
      throw new Error("Unauthorized");
    }

    const email = mockTokens.get(token);
    const user = findUserByEmail(email!);

    if (user) {
      user.watchlist = user.watchlist.filter((t) => t !== ticker);
    }
  },
};
