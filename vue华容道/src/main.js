import Vue from 'vue';
import App from './App.vue'

new Vue({
    //root是html中的一个元素，将app的内容渲染到root中去
    el: '#root',
    render: h => h(App)
});