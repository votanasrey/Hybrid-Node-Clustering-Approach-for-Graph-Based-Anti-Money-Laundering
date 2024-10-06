import { API_ENDPOINTS } from '../../../configs/apiEndpoints'
import { API } from '../base'
import { AuthResponse, ISignInParams } from './types'

export const AUTH_API = {
    async signIn(params: ISignInParams): Promise<AuthResponse> {
        const { data } = await API.post(API_ENDPOINTS.AUTH.SIGN_IN, params)
        return data
    }
}
