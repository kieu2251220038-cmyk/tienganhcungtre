import { Link } from 'react-router-dom'

function HomePage() {
  return (
    <main className="home-page">
      <section className="home-panel" aria-labelledby="home-title">
        <p className="health-eyebrow">English Kids</p>
        <h1 id="home-title">Learn, play, and grow.</h1>
        <p className="health-description">
          The foundation is ready. Check the system connection before building
          the learning experience.
        </p>
        <Link className="health-link" to="/health">
          Open system health
        </Link>
      </section>
    </main>
  )
}

export default HomePage
