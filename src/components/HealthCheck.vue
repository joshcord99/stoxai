<template>
  <div class="fixed bottom-4 right-4 bg-white p-4 rounded-lg shadow-lg border max-w-sm">
    <h3 class="text-sm font-semibold mb-2">Backend Status</h3>
    <div class="space-y-2">
      <div class="flex items-center space-x-2">
        <div 
          :class="[
            'w-3 h-3 rounded-full',
            status === 'connected' ? 'bg-green-500' : 
            status === 'error' ? 'bg-red-500' : 'bg-yellow-500'
          ]"
        ></div>
        <span class="text-xs">{{ statusText }}</span>
      </div>
      <div v-if="error" class="text-xs text-red-600">{{ error }}</div>
      <button 
        @click="checkHealth" 
        class="text-xs text-blue-600 hover:underline"
        :disabled="checking"
      >
        {{ checking ? 'Checking...' : 'Test Connection' }}
      </button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const status = ref<'checking' | 'connected' | 'error'>('checking');
const statusText = ref('Checking connection...');
const error = ref('');
const checking = ref(false);

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:5003";

const checkHealth = async () => {
  checking.value = true;
  status.value = 'checking';
  statusText.value = 'Checking connection...';
  error.value = '';

  try {
    const response = await axios.get(`${BACKEND_URL}/api/health`, {
      timeout: 5000
    });
    
    if (response.status === 200) {
      status.value = 'connected';
      statusText.value = 'Backend connected';
    } else {
      status.value = 'error';
      statusText.value = 'Backend error';
      error.value = `Status: ${response.status}`;
    }
  } catch (err: any) {
    status.value = 'error';
    statusText.value = 'Backend unreachable';
    
    if (err.code === 'ECONNABORTED') {
      error.value = 'Connection timeout';
    } else if (err.response?.status === 404) {
      error.value = 'Endpoint not found';
    } else if (err.message) {
      error.value = err.message;
    } else {
      error.value = 'Unknown error';
    }
  } finally {
    checking.value = false;
  }
};

onMounted(() => {
  checkHealth();
});
</script> 