import axios from 'axios';

const config = {
    headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Credentials': '*'
    }
}
export default {
    login(username, password) {
        config.auth = {username: username, password: password}
        return new Promise((resolve, reject) => {
            axios.get('/login', config)
                .then(res => {
                    resolve(res.data['token']);
                })
                .catch(error => {
                    reject(error);
                })
        })
    }
}