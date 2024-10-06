export interface ISignInParams {
    email: string
    password: string
}

export interface AuthResponse {
    data: UserParams
    message: string
}

export interface UserParams {
    token: string
}
