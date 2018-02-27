import Vue from 'vue'
import Router from 'vue-router'
import home from '@/components/home'
import indexs from '@/components/index'

Vue.use(Router)

export default new Router({
    routes: [{
        path: '/',
        name: 'indexs',
        component: indexs
    }, {

        path: '/home',
        name: 'home',
        component: home
    }]
})