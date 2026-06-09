import { NavLink } from 'react-router-dom'

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand">
        <span className="brand-mark">AI</span>
        <span>Productivity</span>
      </div>
      <nav className="nav-list" aria-label="Primary navigation">
        <NavLink className="nav-link" to="/dashboard">
          Dashboard
        </NavLink>
        <NavLink className="nav-link" to="/tasks">
          Tasks
        </NavLink>
        <NavLink className="nav-link" to="/goals">
          Goals
        </NavLink>
      </nav>
    </aside>
  )
}
