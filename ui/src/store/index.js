import Vue from 'vue'
import Vuex from 'vuex'

import auth from './modules/auth.store';
import uuid from './modules/uuid.store';

Vue.use(Vuex)

export default new Vuex.Store({
    state: {},
    mutations: {},
    actions: {},
    modules: {
        auth,
        uuid
    }
})
