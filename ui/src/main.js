import Vue from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import store from './store';
import axios from 'axios';

axios.defaults.baseURL = 'https://localhost:5000';
axios.defaults.headers.common['Authorization'] = sessionStorage.getItem('token')
// axios.defaults.withCredentials = true

Vue.config.productionTip = false

new Vue({
    store,
    router,
    vuetify,
    render: h => h(App)
}).$mount('#app')
