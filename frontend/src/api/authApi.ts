import apiClient from './axios'
import type {
  CurrentUserResponse,
  LoginRequest,
  LoginResponse,
  LogoutRequest,
  LogoutResponse,
  RefreshTokenRequest,
  RefreshTokenResponse,
  RegisterRequest,
  RegisterResponse,
} from '../types/auth'

export const authApi = {
  register: async (payload: RegisterRequest) => {
    const response = await apiClient.post<RegisterResponse>('/auth/register/', payload)
    return response.data
  },

  login: async (payload: LoginRequest) => {
    const response = await apiClient.post<LoginResponse>('/auth/login/', payload)
    return response.data
  },

  refreshToken: async (payload: RefreshTokenRequest) => {
    const response = await apiClient.post<RefreshTokenResponse>(
      '/auth/token/refresh/',
      payload,
    )
    return response.data
  },

  logout: async (payload: LogoutRequest) => {
    const response = await apiClient.post<LogoutResponse>('/auth/logout/', payload)
    return response.data
  },

  getMe: async () => {
    const response = await apiClient.get<CurrentUserResponse>('/auth/me/')
    return response.data
  },
}
