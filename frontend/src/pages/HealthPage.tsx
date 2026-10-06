import { useEffect, useState } from 'react'

import apiClient from '../api/axios'
import type {
  ApiResponse,
  DatabaseHealthData,
  HealthData,
  HealthStatus,
} from '../types/health'

function statusLabel(status: HealthStatus) {
  if (status === 'checking') {
    return 'Checking...'
  }

  return status === 'connected' ? 'Connected' : 'Disconnected'
}

function HealthPage() {
  const [apiStatus, setApiStatus] = useState<HealthStatus>('checking')
  const [databaseStatus, setDatabaseStatus] =
    useState<HealthStatus>('checking')

  useEffect(() => {
    let isMounted = true

    const loadHealthStatus = async () => {
      const results = await Promise.allSettled([
        apiClient.get<ApiResponse<HealthData>>('/health/'),
        apiClient.get<ApiResponse<DatabaseHealthData>>('/health/db/'),
      ])

      if (!isMounted) {
        return
      }

      const [apiResult, databaseResult] = results
      setApiStatus(
        apiResult.status === 'fulfilled' && apiResult.value.data.success
          ? 'connected'
          : 'disconnected',
      )
      setDatabaseStatus(
        databaseResult.status === 'fulfilled' &&
          databaseResult.value.data.success
          ? 'connected'
          : 'disconnected',
      )
    }

    void loadHealthStatus()

    return () => {
      isMounted = false
    }
  }, [])

  return (
    <main className="health-page">
      <section className="health-panel" aria-labelledby="health-title">
        <p className="health-eyebrow">English Kids</p>
        <h1 id="health-title">System Health</h1>
        <p className="health-description">
          Check the connection between the frontend, backend, and database.
        </p>

        <div className="health-status-grid">
          <article className="health-status-card">
            <span className="health-status-label">Backend API</span>
            <strong className={`status status-${apiStatus}`}>
              {statusLabel(apiStatus)}
            </strong>
          </article>
          <article className="health-status-card">
            <span className="health-status-label">Database</span>
            <strong className={`status status-${databaseStatus}`}>
              {statusLabel(databaseStatus)}
            </strong>
          </article>
        </div>
      </section>
    </main>
  )
}

export default HealthPage
