import { createApp } from 'vue'
//import './style.css'
import App from './App.vue'

import router from './router'; // Importa tu configuración de Vue Router

const app = createApp(App);

app.use(router); // Utiliza Vue Router en tu aplicación

app.mount('#app');
