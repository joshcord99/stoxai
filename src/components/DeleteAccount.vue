<script setup lang="ts">
import { ref, reactive } from "vue";
import { useUserStore } from "../userInfo.ts";
import { useRouter } from "vue-router";
import { authAPI } from "../connection/api.ts";
import Toast from "../tools/Toast.vue";

const user = useUserStore();
const router = useRouter();
const toastRef = ref();

const showDeleteModal = ref(false);
const isDeleting = ref(false);
interface AccountInfo {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  created_at: string;
  watchlist_count: number;
}

const accountInfo = ref<AccountInfo | null>(null);

const deleteForm = reactive({
  confirmEmail: "",
  confirmText: "",
  agreeToDelete: false,
});

const fetchAccountInfo = async () => {
  try {
    const response = await authAPI.getAccountInfo();
    if (response.success) {
      accountInfo.value = response.user_info;
    }
  } catch (error) {
    console.error("Failed to fetch account info:", error);
  }
};

const deleteAccount = async () => {
  if (!deleteForm.agreeToDelete) {
    if (toastRef.value) {
      toastRef.value.addToast("Please agree to delete your account", "error");
    }
    return;
  }

  if (deleteForm.confirmEmail !== user.user?.email) {
    if (toastRef.value) {
      toastRef.value.addToast("Email confirmation does not match", "error");
    }
    return;
  }

  if (deleteForm.confirmText !== "DELETE") {
    if (toastRef.value) {
      toastRef.value.addToast("Please type DELETE to confirm", "error");
    }
    return;
  }

  try {
    isDeleting.value = true;
    const response = await authAPI.deleteAccount();

    if (response.success) {
      if (toastRef.value) {
        toastRef.value.addToast("Account deleted successfully", "success");
      }
      await user.logout();
      router.push("/login");
    } else {
      if (toastRef.value) {
        toastRef.value.addToast(
          response.message || "Failed to delete account",
          "error"
        );
      }
    }
  } catch (error) {
    console.error("Delete failed:", error);
    if (toastRef.value) {
      toastRef.value.addToast("Failed to delete account", "error");
    }
  } finally {
    isDeleting.value = false;
  }
};

const openDeleteModal = () => {
  fetchAccountInfo();
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  console.log("closeDeleteModal called");
  showDeleteModal.value = false;
  deleteForm.confirmEmail = "";
  deleteForm.confirmText = "";
  deleteForm.agreeToDelete = false;
};
</script>

<template>
  <div>
    <button
      @click="openDeleteModal"
      class="w-full px-4 py-3 text-left text-sm text-red-600 hover:bg-red-50 transition-colors duration-200 flex items-center space-x-3"
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
          d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
        />
      </svg>
      <span>Delete Account</span>
    </button>

    <div
      v-if="showDeleteModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click="closeDeleteModal"
    >
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4" @click.stop>
        <div class="flex items-center justify-between mb-4 relative">
          <h3 class="text-lg font-semibold text-gray-900">Delete Account</h3>
          <button
            @click.stop="closeDeleteModal"
            class="relative z-10 p-4 -m-4 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors duration-200 touch-manipulation min-w-[48px] min-h-[48px] flex items-center justify-center border border-gray-200 bg-white"
            aria-label="Close modal"
            type="button"
          >
            <svg
              class="w-6 h-6 pointer-events-none"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        <div v-if="accountInfo" class="mb-4 p-4 bg-gray-50 rounded-lg">
          <h4 class="font-medium text-gray-900 mb-2">Account Information</h4>
          <div class="text-sm text-gray-600">
            <p><strong>Name:</strong> {{ accountInfo.full_name }}</p>
            <p><strong>Email:</strong> {{ accountInfo.email }}</p>
            <p>
              <strong>Member since:</strong>
              {{ new Date(accountInfo.created_at).toLocaleDateString() }}
            </p>
            <p>
              <strong>Watchlist items:</strong>
              {{ accountInfo.watchlist_count }}
            </p>
          </div>
        </div>

        <div class="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div class="flex items-center mb-2">
            <svg
              class="w-5 h-5 text-red-500 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
              />
            </svg>
            <span class="font-medium text-red-800">Warning</span>
          </div>
          <p class="text-sm text-red-700">
            This action cannot be undone. All your data including watchlist,
            preferences, and account information will be permanently deleted.
          </p>
        </div>

        <form @submit.prevent="deleteAccount" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Confirm your email address
            </label>
            <input
              v-model="deleteForm.confirmEmail"
              type="email"
              placeholder="Enter your email address"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Type DELETE to confirm
            </label>
            <input
              v-model="deleteForm.confirmText"
              type="text"
              placeholder="Type DELETE"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
              required
            />
          </div>

          <div class="flex items-center">
            <input
              v-model="deleteForm.agreeToDelete"
              type="checkbox"
              id="agree-delete"
              class="h-4 w-4 text-red-600 focus:ring-red-500 border-gray-300 rounded"
              required
            />
            <label for="agree-delete" class="ml-2 block text-sm text-gray-700">
              I understand that this action cannot be undone and I want to
              permanently delete my account
            </label>
          </div>

          <div class="flex space-x-3">
            <button
              type="button"
              @click="closeDeleteModal"
              class="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded-lg transition-colors duration-200"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="isDeleting || !deleteForm.agreeToDelete"
              class="flex-1 bg-red-600 hover:bg-red-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
            >
              <svg
                v-if="isDeleting"
                class="animate-spin w-4 h-4"
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
              <span>{{ isDeleting ? "Deleting..." : "Delete Account" }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <Toast ref="toastRef" />
  </div>
</template>
