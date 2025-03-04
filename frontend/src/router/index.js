import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/pages/Home.vue';
import PostList from '@/pages/PostList.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/posts', component: PostList }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
