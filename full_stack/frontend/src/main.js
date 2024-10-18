
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import Vue3Toastify from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

// import '../src/resources/css/bootstrap.css'


// const options: ToastContainerOptions = {
//     position: "top-right",
//     autoClose: 3000,
//     pauseOnHover: true,
//     draggable: true,
//     closeOnClick: true
//   };

// createApp(App).use(router).mount('#app')


const app = createApp(App);
app.use(router);


// Use the plugin with options
app.use(Vue3Toastify);

app.mount('#app');