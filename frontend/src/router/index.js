import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/pages/Home.vue';
import PostList from '@/pages/PostList.vue';
import PostDetail from '@/pages/PostDetail.vue';
import PaymentSuccess from '@/pages/PaymentSuccess.vue';
import Signup from '@/pages/Signup.vue'
import Login from '@/pages/Login.vue';
import Dashboard from '@/pages/Dashboard.vue';
import ConfirmSuccess from '@/pages/ConfirmSuccess.vue';
import Settings from '@/pages/Settings.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/posts', component: PostList },
  { path: '/posts/:slug', component: PostDetail },
  { path: '/payments/success', component: PaymentSuccess },
  { path: '/signup', component: Signup },
  { path: '/confirm-success', component: ConfirmSuccess },
  { path: '/login', name: 'login', component: Login },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  { path: '/dashboard/settings', name: 'Settings', component: Settings, meta: { requiresAuth: true }},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 毎回トップへスクロール
    return { top: 0 }
  }
});

router.beforeEach((to, from, next) => {
  // "accessToken" があるかどうかでログイン判定
  const isLoggedIn = !!localStorage.getItem('authToken')
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isLoggedIn) {
      // 未ログインならログインページへ
      return next({ name: 'login' });
    }
  }
  next();
});

export default router;
