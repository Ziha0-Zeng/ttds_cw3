// used to create the router of the whole project

import VueRouter from 'vue-router'
import SearchInput from '../pages/SearchInput'
import MainSearchInterface from '../pages/MainSearchInterface'

export default new VueRouter({
    mode: 'history',
    routes:[
        { 
            path:'',
            component: SearchInput
        },
        {
            name:'searchPage',
            path:'/search',
            component: MainSearchInterface
        }
    ]
})