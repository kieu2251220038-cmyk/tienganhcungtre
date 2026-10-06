export type HealthStatus = 'checking' | 'connected' | 'disconnected'

export interface ApiResponse<T> {
  success: boolean
  message: string
  data: T | null
}

export interface HealthData {
  service: string
  version: string
}

export interface DatabaseHealthData {
  database: string
}
