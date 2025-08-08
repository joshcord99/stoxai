<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-900">
    <div class="w-full max-w-md bg-white p-8 rounded-lg shadow-md">
      <h3 class="text-[30px] font-medium text-center mb-2 text-gray-600">Sign Up</h3>
      <h2 class="text-2xl font-semibold text-center mb-6 text-gray-800">Create Your Account</h2>


      <div v-if="error" class="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
        {{ error }}
      </div>


      <div v-if="success" class="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
        {{ success }}
      </div>

      <form @submit.prevent="submitRegister">
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label class="block text-gray-700 mb-1" for="firstName">First Name</label>
            <input
              v-model="form.firstName"
              type="text"
              id="firstName"
              required
              :disabled="loading"
              class="w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              placeholder="Enter first name"
            />
          </div>

          <div>
            <label class="block text-gray-700 mb-1" for="lastName">Last Name</label>
            <input
              v-model="form.lastName"
              type="text"
              id="lastName"
              required
              :disabled="loading"
              class="w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              placeholder="Enter last name"
            />
          </div>
        </div>

        <div class="mb-4">
          <label class="block text-gray-700 mb-1" for="email">Email</label>
          <input
            v-model="form.email"
            type="email"
            id="email"
            required
            :disabled="loading"
            class="w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
            placeholder="Enter email"
          />
        </div>

        <div class="mb-4">
          <label class="block text-gray-700 mb-1" for="password">Password</label>
          <div class="relative">
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="form.password"
              id="password"
              required
              :disabled="loading"
              class="w-full px-4 py-2 pr-10 border rounded-md focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
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

        <div class="mb-6">
          <label class="block text-gray-700 mb-1" for="confirmPassword">Confirm Password</label>
          <div class="relative">
            <input
              :type="showConfirmPassword ? 'text' : 'password'"
              v-model="form.confirmPassword"
              id="confirmPassword"
              required
              :disabled="loading"
              class="w-full px-4 py-2 pr-10 border rounded-md focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              placeholder="Confirm password"
            />
            <button
              type="button"
              @click="toggleConfirmPassword"
              class="absolute inset-y-0 right-0 pr-3 flex items-center"
              :disabled="loading"
            >
              <svg
                v-if="showConfirmPassword"
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
          class="w-full bg-green-600 text-white py-2 rounded-md hover:bg-green-700 transition duration-200 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center"
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
          {{ loading ? 'Creating Account...' : 'Create Account' }}
        </button>
      </form>

      <p class="mt-4 text-center text-sm text-gray-500">
        Already have an account?
        <router-link to="/login" class="text-green-600 hover:underline">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../userInfo';

const router = useRouter();
const userStore = useUserStore();

const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
});

const loading = ref(false);
const error = ref('');
const success = ref('');
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const togglePassword = () => {
  showPassword.value = !showPassword.value;
};

const toggleConfirmPassword = () => {
  showConfirmPassword.value = !showConfirmPassword.value;
};

const validateForm = () => {
  if (form.password !== form.confirmPassword) {
    error.value = 'Passwords do not match.';
    return false;
  }

  if (form.password.length < 6) {
    error.value = 'Password must be at least 6 characters long.';
    return false;
  }

  if (form.firstName.trim().length < 1) {
    error.value = 'First name is required.';
    return false;
  }

  if (form.lastName.trim().length < 1) {
    error.value = 'Last name is required.';
    return false;
  }

  return true;
};

const submitRegister = async () => {
  if (loading.value) return;

  error.value = '';
  success.value = '';

  if (!validateForm()) {
    return;
  }

  loading.value = true;

  try {
    await userStore.register({
      email: form.email,
      password: form.password,
      first_name: form.firstName,
      last_name: form.lastName,
    });

    success.value = 'Account created successfully! Redirecting to dashboard...';
    
    setTimeout(() => {
      router.push('/dashboard');
    }, 1500);

  } catch (err: any) {
    console.error('Registration error:', err);
    
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
  