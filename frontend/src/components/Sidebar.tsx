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
        <NavLink className="nav-link" to="/notes">
          Notes
        </NavLink>
        <NavLink className="nav-link" to="/reminders">
          Reminders
        </NavLink>
        <NavLink className="nav-link" to="/budgets">
          Budgets
        </NavLink>
        <NavLink className="nav-link" to="/expenses">
          Expenses
        </NavLink>
        <NavLink className="nav-link" to="/ai-tools">
          AI Tools
        </NavLink>
      </nav>
    </aside>
  )
}
