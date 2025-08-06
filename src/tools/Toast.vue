<script setup lang="ts">
import { ref } from 'vue'

interface ToastMessage {
  id: string
  message: string
  type: 'error' | 'success' | 'warning'
  duration?: number
}

const toasts = ref<ToastMessage[]>([])

const addToast = (message: string, type: 'error' | 'success' | 'warning' = 'error', duration: number = 5000) => {
  const id = Date.now().toString()
  const toast: ToastMessage = {
    id,
    message,
    type,
    duration
  }
  
  toasts.value.push(toast)
  
  setTimeout(() => {
    removeToast(id)
  }, duration)
}

const removeToast = (id: string) => {
  const index = toasts.value.findIndex(toast => toast.id === id)
  if (index > -1) {
    toasts.value.splice(index, 1)
  }
}

defineExpose({
  addToast
})
</script>

<template>
  <div class="fixed top-4 right-4 z-[9999] space-y-2" style="pointer-events: auto;">
    <div
      v-for="toast in toasts"
      :key="toast.id"
      :class="{
        'bg-red-500 text-white': toast.type === 'error',
        'bg-green-500 text-white': toast.type === 'success',
        'bg-yellow-500 text-white': toast.type === 'warning'
      }"
      class="px-4 py-3 rounded-lg shadow-lg max-w-sm flex items-center justify-between"
      style="min-width: 300px;"
    >
      <span class="text-sm font-medium">{{ toast.message }}</span>
      <button
        @click="removeToast(toast.id)"
        class="ml-3 text-white hover:text-gray-200 font-bold text-lg"
      >
        ×
      </button>
    </div>
  </div>
</template>

<style scoped>
</style> 