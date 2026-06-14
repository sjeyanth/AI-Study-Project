import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <section className="page-shell">
      <h1>Page Not Found</h1>
      <p>The page you requested does not exist.</p>
      <Link to="/dashboard" className="primary-link">
        Go to dashboard
      </Link>
    </section>
  )
}
