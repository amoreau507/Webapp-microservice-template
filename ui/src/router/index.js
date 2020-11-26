import Vue from 'vue'
import VueRouter from 'vue-router'

import Login from '../views/Login'
import Home from '../views/Home'
// import store from '../store'

Vue.use(VueRouter)

const routes = [
    {
        path: '/Login',
        name: 'Login',
        component: Login,
        meta: {authorize: []}
    },
    {
        path: '/',
        name: 'Home',
        component: Home,
        meta: {authorize: []}
    },
    {
        path: '*',
        redirect: '/',
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

router.beforeEach((to, from, next) => {

    if (to.name !== 'Login' && !sessionStorage.getItem('token')) {
        return next({name: 'Login'});
    } else {
        next();
    }
})

export default router
