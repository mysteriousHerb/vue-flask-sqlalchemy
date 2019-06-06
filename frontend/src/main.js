import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'



Vue.config.productionTip = false

Vue.use(Vuetify)

// as axios is not a vue plugin, cannot use Vue.use(axios)
// how to only import axios once
// https://vuejs.org/v2/guide/plugins.html
// https://dev.to/heftyhead/lets-talk-about-an-unnecessary-but-popular-vue-plugin-1ied
Vue.prototype.axios = axios




new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
