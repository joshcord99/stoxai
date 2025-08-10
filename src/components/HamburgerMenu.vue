<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { useUserStore } from "../userInfo.ts";
import { useRouter } from "vue-router";
import DeleteAccount from "./DeleteAccount.vue";

const user = useUserStore();
const router = useRouter();

const isMenuOpen = ref(false);
const isHovering = ref(false);

const handleLogout = async () => {
  try {
    await user.logout();
    router.push("/login");
  } catch (error) {
    user.logout();
    router.push("/login");
  }
};

let closeTimeout: number | null = null;

const openMenu = () => {
  if (closeTimeout) {
    clearTimeout(closeTimeout);
    closeTimeout = null;
  }
  isMenuOpen.value = true;
};

const closeMenu = () => {
  closeTimeout = window.setTimeout(() => {
    if (!isHovering.value) {
      isMenuOpen.value = false;
    }
  }, 150);
};

const toggleMenu = () => {
  // Clear any pending close timeout
  if (closeTimeout) {
    clearTimeout(closeTimeout);
    closeTimeout = null;
  }

  if (isMenuOpen.value) {
    closeMenu();
  } else {
    openMenu();
  }
};

const handleMouseEnter = () => {
  isHovering.value = true;
  openMenu();
};

const handleMouseLeave = () => {
  isHovering.value = false;
  closeMenu();
};

const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === "Escape" && isMenuOpen.value) {
    closeMenu();
  }
};

onMounted(() => {
  document.addEventListener("keydown", handleKeydown);
});

onUnmounted(() => {
  document.removeEventListener("keydown", handleKeydown);
});
</script>

<template>
  <div class="relative hamburger-menu">
    <button
      @click="toggleMenu"
      @mouseenter="handleMouseEnter"
      @mouseleave="handleMouseLeave"
      class="p-2 rounded-lg bg-gray-800 hover:bg-gray-700 text-white transition-colors duration-200"
      aria-label="Open menu"
    >
      <svg
        class="w-5 h-5 sm:w-6 sm:h-6"
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
      @mouseenter="handleMouseEnter"
      @mouseleave="handleMouseLeave"
      class="absolute right-0 mt-2 w-56 sm:w-64 bg-white rounded-lg shadow-lg border border-gray-200 z-50"
      @click.stop
    >
      <div class="p-3 sm:p-4 border-b border-gray-200">
        <div class="flex items-center space-x-2 sm:space-x-3">
          <div
            class="w-8 h-8 sm:w-10 sm:h-10 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0"
          >
            <span class="text-white font-semibold text-xs sm:text-sm">
              {{ (user.user?.first_name || "U").charAt(0).toUpperCase() }}
            </span>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-xs sm:text-sm font-medium text-gray-900 truncate">
              {{
                (user.user?.first_name || "") +
                  " " +
                  (user.user?.last_name || "") || "User"
              }}
            </p>
            <p class="text-xs text-gray-500 truncate">
              {{ user.user?.email }}
            </p>
          </div>
        </div>
      </div>

      <div class="py-2">
        <div class="px-3 sm:px-4 py-2 text-xs text-gray-500">
          Account Information
        </div>

        <button
          @click="handleLogout"
          class="w-full px-3 sm:px-4 py-2 sm:py-3 text-left text-xs sm:text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-200 flex items-center space-x-2 sm:space-x-3"
        >
          <svg
            class="w-3 h-3 sm:w-4 sm:h-4 flex-shrink-0"
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

        <div class="px-3 sm:px-4 py-2 text-xs text-red-600 font-medium">
          Danger Zone
        </div>

        <div class="px-3 sm:px-4 py-2">
          <DeleteAccount />
        </div>
      </div>
    </div>
  </div>
</template>
