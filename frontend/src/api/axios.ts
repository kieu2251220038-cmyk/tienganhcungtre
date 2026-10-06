import axios, { type InternalAxiosRequestConfig } from 'axios'

import type { RefreshTokenResponse } from '../types/auth'
import {
  clearTokens,
  getAccessToken,
  getRefreshToken,
  setAccessToken,
} from '../utils/storage'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

apiClient.interceptors.request.use((config) => {
  const accessToken = getAccessToken()

  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`
  }

  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  async (error: unknown) => {
    if (!axios.isAxiosError(error) || !error.config || !error.response) {
      return Promise.reject(error)
    }

    const originalRequest = error.config as InternalAxiosRequestConfig & {
      _retry?: boolean
    }
    const requestUrl = originalRequest.url ?? ''
    const isAuthRequest = requestUrl.includes('/auth/')

    if (error.response.status !== 401 || originalRequest._retry || isAuthRequest) {
      return Promise.reject(error)
    }

    const refreshToken = getRefreshToken()

    if (!refreshToken) {
      clearTokens()
      return Promise.reject(error)
    }

    originalRequest._retry = true

    try {
      const response = await axios.post<RefreshTokenResponse>(
        `${import.meta.env.VITE_API_URL}/auth/token/refresh/`,
        { refresh: refreshToken },
      )
      const accessToken = response.data.data.access

      setAccessToken(accessToken)
      originalRequest.headers.Authorization = `Bearer ${accessToken}`

      return apiClient(originalRequest)
    } catch (refreshError: unknown) {
      clearTokens()
      return Promise.reject(refreshError)
    }
  },
)

export default apiClient
