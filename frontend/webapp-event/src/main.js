import './assets/main.css'
import cors from 'cors'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(cors)

app.use(router)

app.mount('#app')
