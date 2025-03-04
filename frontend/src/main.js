import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import DonateButton from '@/components/DonateButton.vue';
import FooterButton from '@/components/FooterButton.vue';


const app = createApp(App);
app.use(router);

app.component('FooterButton', FooterButton);
app.component('DonateButton', DonateButton);
app.mount('#app');