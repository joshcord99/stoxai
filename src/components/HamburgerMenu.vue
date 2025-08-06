<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '../userInfo.ts'
import { useRouter } from 'vue-router'
import DeleteAccount from './DeleteAccount.vue'

const user = useUserStore()
const router = useRouter()

const isMenuOpen = ref(false)

const handleLogout = async () => {
  try {
    await user.logout()
    router.push('/login')
  } catch (error) {
    user.logout()
    router.push('/login')
  }
}

let closeTimeout: number | null = null

const openMenu = () => {
  if (closeTimeout) {
    clearTimeout(closeTimeout)
    closeTimeout = null
  }
  isMenuOpen.value = true
}

const closeMenu = () => {
  closeTimeout = window.setTimeout(() => {
    isMenuOpen.value = false
  }, 150) 
}


const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && isMenuOpen.value) {
    closeMenu()
  }
}


onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <div class="relative hamburger-menu">
  
    <button
      @mouseenter="openMenu"
      @mouseleave="closeMenu"
      class="p-2 rounded-lg bg-gray-800 hover:bg-gray-700 text-white transition-colors duration-200"
      aria-label="Open menu"
    >
      <svg
        class="w-6 h-6"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          v-if="!isMenuOpen"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M4 6h16M4 12h16M4 18h16"
        />
        <path
          v-else
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M6 18L18 6M6 6l12 12"
        />
      </svg>
    </button>

 
    <div
      v-if="isMenuOpen"
      @mouseenter="openMenu"
      @mouseleave="closeMenu"
      class="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-200 z-50"
      @click.stop
    >

      <div class="p-4 border-b border-gray-200">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
            <span class="text-white font-semibold text-sm">
              {{ (user.displayName || user.fullName || 'U').charAt(0).toUpperCase() }}
            </span>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-900 truncate">
              {{ user.displayName || user.fullName || 'User' }}
            </p>
            <p class="text-xs text-gray-500 truncate">
              {{ user.user?.email }}
            </p>
          </div>
        </div>
      </div>

     
      <div class="py-2">
      
        <div class="px-4 py-2 text-xs text-gray-500">
          Account Information
        </div>
        
     
        <button
          @click="handleLogout"
          class="w-full px-4 py-3 text-left text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-200 flex items-center space-x-3"
        >
          <svg
            class="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
            />
          </svg>
          <span>Logout</span>
        </button>

     
        <div class="border-t border-gray-200 my-2"></div>


        <div class="px-4 py-2 text-xs text-red-600 font-medium">
          Danger Zone
        </div>

       
        <div class="px-4 py-2">
          <DeleteAccount />
        </div>
      </div>
    </div>

  </div>
</template> 