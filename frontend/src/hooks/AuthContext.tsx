import { type ReactNode, useEffect, useState } from 'react'

import { authApi } from '../api/authApi'
import type { LoginRequest, User } from '../types/auth'
import {
  clearTokens,
  getAccessToken,
  getRefreshToken,
  setTokens,
} from '../utils/storage'
import { AuthContext } from './auth-context'

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(() => Boolean(getAccessToken()))

  useEffect(() => {
    const accessToken = getAccessToken()

    if (!accessToken) {
      return
    }

    void authApi
      .getMe()
      .then((response) => setUser(response.data))
      .catch(() => {
        clearTokens()
        setUser(null)
      })
      .finally(() => setIsLoading(false))
  }, [])

  const login = async (payload: LoginRequest) => {
    const response = await authApi.login(payload)
    setTokens(response.data.access, response.data.refresh)
    setUser(response.data.user)
  }

  const logout = async () => {
    const refreshToken = getRefreshToken()

    try {
      if (refreshToken) {
        await authApi.logout({ refresh: refreshToken })
      }
    } finally {
      clearTokens()
      setUser(null)
    }
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: Boolean(user),
        isLoading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}
