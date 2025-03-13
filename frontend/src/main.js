import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import '@/assets/css/style.scss'
import VueLazyload from 'vue-lazyload'
import loadingImage from '@/assets/image/loading.webp'
import { createPinia } from 'pinia'


// 自動登録用の関数
function registerGlobalComponents(app) {
  // src/components 配下の .vue をすべて読み込む
  const modules = import.meta.glob('@/components/*.vue', { eager: true });
  Object.entries(modules).forEach(([path, definition]) => {
    // ファイル名から拡張子を取り除いてコンポーネント名にする
    const componentName = path.split('/').pop().replace(/\.\w+$/, '');
    app.component(componentName, definition.default);
  });
}

const pinia = createPinia()
const app = createApp(App);

app.use(pinia)
app.use(router);
app.use(VueLazyload, {
  preload: 1.3,
  loading: loadingImage,
  attempt: 1
})


// コンポーネントを自動登録
registerGlobalComponents(app);
app.mount('#app');
