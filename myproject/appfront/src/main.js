// import Vue
import Vue from 'vue'
// import APP
import App from './App.vue'
// import vue-router plugin
import VueRouter from 'vue-router'

Vue.config.productionTip = false
// import router
import router from './router'

import Element from 'element-ui';

import 'element-ui/lib/theme-chalk/index.css';
import locale from 'element-ui/lib/locale/lang/en'

Vue.use(Element, { locale, size: 'small', zIndex: 3000 } );

Vue.use(VueRouter)
new Vue({
  el:'#app',
  render: h => h(App),
  router: router,
  beforeCreate() {
    Vue.prototype.$bus = this
  },
}).$mount('#app')
