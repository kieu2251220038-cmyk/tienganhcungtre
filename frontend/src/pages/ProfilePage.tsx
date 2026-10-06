import { Link, useNavigate } from 'react-router-dom'

import { useAuth } from '../hooks/useAuth'

function ProfilePage() {
  const navigate = useNavigate()
  const { user, logout } = useAuth()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <main className="home-page">
      <section className="home-panel" aria-labelledby="profile-title">
        <p className="health-eyebrow">English Kids</p>
        <h1 id="profile-title">Your profile</h1>
        <p className="health-description">
          Signed in as {user?.first_name} {user?.last_name} ({user?.email}).
        </p>
        <button type="button" className="auth-submit" onClick={handleLogout}>
          Sign out
        </button>
        <Link className="health-link" to="/">
          Back to home
        </Link>
      </section>
    </main>
  )
}

export default ProfilePage
