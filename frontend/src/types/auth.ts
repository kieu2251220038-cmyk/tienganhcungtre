export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
}

export interface ApiErrorResponse {
  success: false
  message: string
  errors: Record<string, string[] | string>
}

export interface ApiSuccessResponse<T> {
  success: true
  message: string
  data: T
}

export interface RegisterRequest {
  email: string
  password: string
  password_confirm: string
  first_name: string
  last_name: string
}

export interface RegisterData {
  user: User
}

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginData {
  access: string
  refresh: string
  user: User
}

export interface RefreshTokenRequest {
  refresh: string
}

export interface RefreshTokenData {
  access: string
}

export interface LogoutRequest {
  refresh: string
}

export interface AuthResponse<T> extends ApiSuccessResponse<T> {}
export type RegisterResponse = AuthResponse<RegisterData>
export type LoginResponse = AuthResponse<LoginData>
export type RefreshTokenResponse = AuthResponse<RefreshTokenData>
export type CurrentUserResponse = AuthResponse<User>
export type LogoutResponse = AuthSuccessResponse<null>

export interface AuthSuccessResponse<T> extends ApiSuccessResponse<T> {}
