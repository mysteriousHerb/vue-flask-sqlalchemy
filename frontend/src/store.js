import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    session_id: ''
  },
  getters:{
    session_id: state => {
      return state.session_id
    }
  },
  mutations: {
    generate_session_id (state) {
      var random_id = [...Array(50)]
      .map(_ => ((Math.random(this.id_length) * 36) | 0).toString(36))
      .join(``);
      state.session_id = random_id
    }
  },
  actions: {
    generate_session_id ({ commit }) {
      commit('generate_session_id')
    }
  }
})
