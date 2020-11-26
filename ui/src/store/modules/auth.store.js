import authService from '../../services/auth.service'
// import router from '../../router/router.js' // Vue router instance

import {LOGIN, LOGOUT} from '../actions.type'
import {SET_TOKEN} from '../mutations.type'
import {GET_TOKEN} from "@/store/mutations.type";

let user = JSON.parse(sessionStorage.getItem('user'));
const initialUserState = user ? user : {};

const state = {
    errors: '',
    user: initialUserState
}

/**************************************************************************
 * GETTERS
 **************************************************************************/
const getters = {
    getUser: state => state.user,
    getErrors: state => state.errors
}

const actions = {
    async [LOGIN](state, payload) {
        await authService.login(payload.username, payload.password)
            .then((token) => {
                state.commit(SET_TOKEN, token)
                this.isValid = true;
            })
            .catch((error) => {
                this.hasError = true;
                this.errorMsg = error.message;
            });
    },
    async [LOGOUT]() {
        sessionStorage.removeItem('token')
    },
    [GET_TOKEN]() {
        return sessionStorage.getItem('token')
    }
}
const mutations = {
    [SET_TOKEN](state, token) {
        sessionStorage.setItem('token', token);
    }
}

/**************************************************************************
 * EXPORTS
 **************************************************************************/
export default {
    state,
    actions,
    mutations,
    getters
}