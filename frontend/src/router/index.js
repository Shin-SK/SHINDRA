import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/IndexLayout.vue'), // ← ホーム専用レイアウト
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('@/pages/Index.vue')
      }
    ]
  },
  {
    path: '/',
    component: () => import('@/layouts/BaseLayout.vue'),
    children: [
      { 
        path: '/posts', 
        component: () => import('@/pages/PostList.vue')
      },
      { 
        path: '/posts/:slug', 
        component: () => import('@/pages/PostDetail.vue')
      },
      { 
        path: '/payments/success', 
        component: () => import('@/pages/PaymentSuccess.vue')
      },
      { 
        path: '/signup', 
        component: () => import('@/pages/Signup.vue')
      },
      { 
        path: '/confirm-success', 
        component: () => import('@/pages/ConfirmSuccess.vue')
      },
      { 
        path: '/confirm-email', 
        component: () => import('@/pages/ConfirmEmail.vue')
      },
      { 
        path: '/login', 
        name: 'login', 
        component: () => import('@/pages/Login.vue')
      },
      { 
        path: '/dashboard',
        name: 'dashboard',
        component: () => import('@/pages/Dashboard.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: '/dashboard/settings',
        name: 'Settings',
        component: () => import('@/pages/Settings.vue'),
        meta: { requiresAuth: true }
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 }
  }
});

router.beforeEach((to, from, next) => {
  // "accessToken" があるかどうかでログイン判定
  const isLoggedIn = !!localStorage.getItem('authToken');
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isLoggedIn) {
      // 未ログインならログインページへ
      return next({ name: 'login' });
    }
  }
  next();
});

export default router;
