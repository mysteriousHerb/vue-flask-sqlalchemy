import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    session_id: '',
    user_name_in_key: ''
  },
  getters:{
    },
  mutations: {
    generate_session_id (state) {
      var random_id = [...Array(50)]
      .map(_ => ((Math.random(this.id_length) * 36) | 0).toString(36))
      .join(``);
      state.session_id = random_id
    },
    update_user_name_in_key(state, user_name){
      state.user_name_in_key = user_name
    },
  },
  actions: {
    generate_session_id ({ commit }) {
      commit('generate_session_id')
    },
    update_user_name_in_key({commit}, user_name){
      commit('update_user_name_in_key', user_name)
    },
  }
})
