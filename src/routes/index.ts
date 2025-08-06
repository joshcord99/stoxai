import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "../userInfo";
import Register from "../pages/Registration.vue";
import Login from "../pages/Login.vue";
import dashboard from "../pages/Dashboard.vue";

import Tickers from "../pages/Tickers.vue";
import MarketLingo from "../pages/MarketLingo.vue";

const routes = [
  { path: "/", redirect: "/login" },
  {
    path: "/registration",
    name: "Register",
    component: Register,
    meta: { requiresGuest: true },
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: { requiresGuest: true },
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: dashboard,
    meta: { requiresAuth: true },
  },

  {
    path: "/tickers",
    name: "tickers",
    component: Tickers,
    meta: { requiresAuth: true },
  },
  {
    path: "/market-lingo",
    name: "market-lingo",
    component: MarketLingo,
    meta: { requiresAuth: true },
  },
  { path: "/:pathMatch(.*)*", redirect: "/dashboard" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, _from, next) => {
  const userStore = useUserStore();

  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next("/login");
    return;
  }

  if (to.meta.requiresGuest && userStore.isAuthenticated) {
    next("/dashboard");
    return;
  }

  next();
});

export default router;
