import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/pages/Home.vue';
import PostList from '@/pages/PostList.vue';
import PostDetail from '@/pages/PostDetail.vue';
import PaymentSuccess from '@/pages/PaymentSuccess.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/posts', component: PostList },
  { path: '/posts/:slug', component: PostDetail },
  { path: '/payments/success', component: PaymentSuccess }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
