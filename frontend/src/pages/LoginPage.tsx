import axios from 'axios'
import { type FormEvent, useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'

import { useAuth } from '../hooks/useAuth'

function LoginPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { login } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const registrationMessage =
    typeof location.state?.message === 'string' ? location.state.message : ''

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError('')

    if (!email.trim() || !password) {
      setError('Email and password are required.')
      return
    }

    setIsSubmitting(true)

    try {
      await login({
        email: email.trim(),
        password,
      })
      navigate('/')
    } catch (requestError: unknown) {
      if (axios.isAxiosError(requestError)) {
        const message = requestError.response?.data?.message
        setError(
          typeof message === 'string'
            ? message
            : 'Unable to sign in with these credentials.',
        )
      } else {
        setError('Unable to sign in. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-panel" aria-labelledby="login-title">
        <p className="health-eyebrow">English Kids</p>
        <h1 id="login-title">Welcome back</h1>
        <p className="health-description">Sign in to continue learning.</p>

        {registrationMessage && (
          <p className="auth-success" role="status">
            {registrationMessage}
          </p>
        )}

        <form className="auth-form" onSubmit={handleSubmit}>
          <label htmlFor="login-email">Email</label>
          <input
            id="login-email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            autoComplete="email"
            required
          />

          <label htmlFor="login-password">Password</label>
          <input
            id="login-password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="current-password"
            required
          />

          {error && (
            <p className="auth-error" role="alert">
              {error}
            </p>
          )}

          <button type="submit" className="auth-submit" disabled={isSubmitting}>
            {isSubmitting ? 'Signing in...' : 'Sign in'}
          </button>
        </form>

        <Link className="auth-secondary-link" to="/">
          Back to home
        </Link>
        <Link className="auth-secondary-link" to="/register">
          Create an account
        </Link>
      </section>
    </main>
  )
}

export default LoginPage
