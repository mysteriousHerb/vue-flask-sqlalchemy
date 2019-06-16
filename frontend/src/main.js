import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
// or import all icons if you don't care about bundle size
import 'vue-awesome/icons'

Vue.config.productionTip = false
// as axios is not a vue plugin, cannot use Vue.use(axios)
// how to only import axios once
// https://vuejs.org/v2/guide/plugins.html
// https://dev.to/heftyhead/lets-talk-about-an-unnecessary-but-popular-vue-plugin-1ied
Vue.prototype.axios = axios

// API server location, for deployment change IP address
// change for deployment
Vue.prototype.$API_URL = process.env.VUE_APP_API

// for the looks
Vue.use(Vuetify)



new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
