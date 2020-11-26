import axios from 'axios';

const config = {
    headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Credentials': '*'
    }
}
export default {
    generate() {
        return new Promise((resolve, reject) => {
            // config.headers.Authorization = sessionStorage.getItem('token')
            axios.get('/', config)
                .then(res => {
                    resolve(res.data);
                })
                .catch(error => {
                    reject(error);
                })
        })
    },
}