import axios from 'axios'
import { type FormEvent, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { authApi } from '../api/authApi'

function RegisterPage() {
  const navigate = useNavigate()
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [passwordConfirm, setPasswordConfirm] = useState('')
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError('')

    if (password !== passwordConfirm) {
      setError('Passwords do not match.')
      return
    }

    setIsSubmitting(true)

    try {
      await authApi.register({
        first_name: firstName.trim(),
        last_name: lastName.trim(),
        email: email.trim(),
        password,
        password_confirm: passwordConfirm,
      })
      navigate('/login', {
        state: { message: 'Registration successful. Please sign in.' },
      })
    } catch (requestError: unknown) {
      if (axios.isAxiosError(requestError)) {
        const message = requestError.response?.data?.message
        setError(
          typeof message === 'string'
            ? message
            : 'Unable to create your account.',
        )
      } else {
        setError('Unable to create your account. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-panel" aria-labelledby="register-title">
        <p className="health-eyebrow">English Kids</p>
        <h1 id="register-title">Create account</h1>
        <p className="health-description">
          Create an account to start your learning journey.
        </p>

        <form className="auth-form" onSubmit={handleSubmit}>
          <label htmlFor="register-first-name">First name</label>
          <input
            id="register-first-name"
            type="text"
            value={firstName}
            onChange={(event) => setFirstName(event.target.value)}
            autoComplete="given-name"
            required
          />

          <label htmlFor="register-last-name">Last name</label>
          <input
            id="register-last-name"
            type="text"
            value={lastName}
            onChange={(event) => setLastName(event.target.value)}
            autoComplete="family-name"
            required
          />

          <label htmlFor="register-email">Email</label>
          <input
            id="register-email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            autoComplete="email"
            required
          />

          <label htmlFor="register-password">Password</label>
          <input
            id="register-password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="new-password"
            required
          />

          <label htmlFor="register-password-confirm">Confirm password</label>
          <input
            id="register-password-confirm"
            type="password"
            value={passwordConfirm}
            onChange={(event) => setPasswordConfirm(event.target.value)}
            autoComplete="new-password"
            required
          />

          {error && (
            <p className="auth-error" role="alert">
              {error}
            </p>
          )}

          <button type="submit" className="auth-submit" disabled={isSubmitting}>
            {isSubmitting ? 'Creating account...' : 'Create account'}
          </button>
        </form>

        <Link className="auth-secondary-link" to="/login">
          Already have an account? Sign in
        </Link>
      </section>
    </main>
  )
}

export default RegisterPage
