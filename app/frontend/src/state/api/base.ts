import axios from 'axios'
import Cookies from 'js-cookie'

import { ECookies } from '../../configs/constants'
import { API_ENDPOINTS } from '../../configs/apiEndpoints'

const API = axios.create({
    baseURL: API_ENDPOINTS.BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',

    }
})

API.interceptors.request.use(
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (config: any) => {
        const authToken = Cookies.get(ECookies.AUTH_TOKEN)
        if (authToken) {
            config.headers['x-access-token'] = `${authToken}`
        }
        return config
    },

    (error) => Promise.reject(error)
)

export { API }
