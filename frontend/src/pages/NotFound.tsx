import { Link } from 'react-router-dom'

export function NotFound() {
  return (
    <main className="not-found">
      <section>
        <h1>Page not found</h1>
        <p>The page you requested does not exist.</p>
        <Link className="ghost-button" to="/dashboard">
          Back to dashboard
        </Link>
      </section>
    </main>
  )
}
