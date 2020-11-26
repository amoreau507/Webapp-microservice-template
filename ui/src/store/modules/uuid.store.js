import uuidService from '../../services/uuid.service'


import {GENERATE_UUID} from '../actions.type'
import {SET_UUID} from '../mutations.type'

const state = {
    uuid: ''
}

/**************************************************************************
 * GETTERS
 **************************************************************************/
const getters = {
    getUUID: state => state.uuid
}

const actions = {
    async [GENERATE_UUID](state) {
        uuidService.generate()
            .then((uuid) => {
                state.commit(SET_UUID, uuid)
                this.isValid = true;
            })
            .catch((error) => {
                this.hasError = true;
                this.errorMsg = error.message;
            });
    },
}
const mutations = {
    [SET_UUID](state, uuid) {
        state.uuid = uuid
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