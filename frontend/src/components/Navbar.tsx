import { useAuth } from '../context/useAuth'

export function Navbar() {
  const { logout, user } = useAuth()

  return (
    <header className="navbar">
      <div className="navbar-title">
        <strong>Dashboard</strong>
        <span>Productivity overview</span>
      </div>
      <div className="navbar-actions">
        <span className="user-chip">{user?.username}</span>
        <button className="ghost-button" type="button" onClick={logout}>
          Sign out
        </button>
      </div>
    </header>
  )
}
