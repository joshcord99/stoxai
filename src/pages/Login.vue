<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-900">

    <div class="absolute top-0 left-0 right-0">
      <StaticNewsTicker />
    </div>

    <div class="absolute top-8 left-1/2 transform -translate-x-1/2">
      <h1 class="text-white text-[50px] font-bold">Stock Analyst</h1>
    </div>
    
    <div class="flex w-full max-w-6xl gap-8">

      <div class="w-1/2 bg-white p-8 rounded-lg shadow-md">
        <h3 class="text-[30px] font-medium text-center mb-2 text-gray-600">Welcome Back</h3>
        <h2 class="text-2xl font-semibold text-center mb-6 text-gray-800">Login to Stock Analyst</h2>
        

        <div v-if="error" class="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {{ error }}
        </div>


        <div v-if="success" class="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
          {{ success }}
        </div>
        
        <form @submit.prevent="submitLogin">
          <div class="mb-4">
            <label class="block text-gray-700 mb-1" for="email">Email</label>
            <input
              type="email"
              id="email"
              v-model="form.email"
              required
              :disabled="loading"
              class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              placeholder="Enter your email"
            />
          </div>

          <div class="mb-6">
            <label class="block text-gray-700 mb-1" for="password">Password</label>
            <div class="relative">
              <input
                :type="showPassword ? 'text' : 'password'"
                id="password"
                v-model="form.password"
                required
                :disabled="loading"
                class="w-full px-4 py-2 pr-10 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
                placeholder="Enter password"
              />
              <button
                type="button"
                @click="togglePassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
                :disabled="loading"
              >
                <svg
                  v-if="showPassword"
                  class="h-5 w-5 text-gray-400 hover:text-gray-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"
                  />
                </svg>
                <svg
                  v-else
                  class="h-5 w-5 text-gray-400 hover:text-gray-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                  />
                </svg>
              </button>
            </div>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition duration-200 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center"
          >
            <svg
              v-if="loading"
              class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>
        </form>

        <p class="mt-4 text-center text-sm text-gray-500">
          Don't have an account? <router-link to="/registration" class="text-blue-600 hover:underline">Register</router-link>
        </p>


      </div>

      <div class="w-1/2 bg-white rounded-lg shadow-md p-6">
        <div class="text-center mb-4">
          <h3 class="text-xl font-semibold text-gray-800 mb-2">Market Data</h3>
          <p class="text-gray-600 text-sm">Sample Market Information</p>
        </div>
        <div class="bg-gray-50 rounded-lg p-4">
          <StaticMarketData />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../userInfo';
import StaticMarketData from '../components/StaticMarketData.vue';
import StaticNewsTicker from '../components/StaticNewsTicker.vue';

const router = useRouter();
const userStore = useUserStore();

const form = reactive({
  email: '',
  password: ''
});

const loading = ref(false);
const error = ref('');
const success = ref('');
const showPassword = ref(false);

const togglePassword = () => {
  showPassword.value = !showPassword.value;
};

const submitLogin = async () => {
  if (loading.value) return;

  loading.value = true;
  error.value = '';
  success.value = '';

  try {
    console.log('=== DEBUG: Attempting login ===');
    const response = await userStore.login({
      email: form.email,
      password: form.password
    });
    console.log('=== DEBUG: Login response ===', response);
    console.log('=== DEBUG: User store state ===', {
      isAuthenticated: userStore.isAuthenticated,
      user: userStore.user,
      token: userStore.token
    });

    success.value = 'Login successful! Redirecting...';
    
    setTimeout(() => {
      console.log('=== DEBUG: Redirecting to dashboard ===');
      router.push('/dashboard');
    }, 1000);

  } catch (err: any) {
    console.error('Login error:', err);
    
    if (err.code === 'ECONNABORTED' || err.message?.includes('timeout')) {
      error.value = 'Network timeout. Please check your connection and try again.';
    } else if (err.response?.status === 404) {
      error.value = 'Backend service not found. Please contact support.';
    } else if (err.response?.status === 500) {
      error.value = 'Server error. Please try again later.';
    } else if (err.response?.data?.error) {
      error.value = err.response.data.error;
    } else if (err.message) {
      error.value = err.message;
    } else {
      error.value = 'Network error. Unable to connect to the server.';
    }
  } finally {
    loading.value = false;
  }
};
</script>
  