import Vue from 'vue'
import App from './App.vue'

import { BootstrapVue } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import Vuex from 'vuex'
Vue.use(Vuex)

Vue.config.productionTip = false

Vue.use(BootstrapVue)

const store = new Vuex.Store({
  state: {
    iris: {}
  },
  mutations: {
    setIris (state, iris) {
      state.iris = iris;
    }
  }
})

new Vue({
  render: h => h(App),
  store: store,
}).$mount('#app')
