import { Link } from 'react-router-dom'

type NavbarProps = {
  isAuthenticated: boolean
  onLogout: () => void
  onToggleSidebar: () => void
}

export default function Navbar({
  isAuthenticated,
  onLogout,
  onToggleSidebar,
}: NavbarProps) {
  return (
    <header className="navbar">
      {isAuthenticated ? (
        <button
          type="button"
          className="menu-button"
          onClick={onToggleSidebar}
          aria-label="Open navigation"
        >
          <span />
          <span />
          <span />
        </button>
      ) : (
        <div style={{ width: 40, height: 40 }} aria-hidden="true" />
      )}

      <Link to="/dashboard" className="brand">
        AI Study Project
      </Link>

      <nav className="navbar-links">
        {isAuthenticated ? (
          <button type="button" className="logout-button" onClick={onLogout}>
            Logout
          </button>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </nav>
    </header>
  )
}
