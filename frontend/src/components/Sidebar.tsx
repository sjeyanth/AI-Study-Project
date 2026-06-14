import { Link, useLocation } from 'react-router-dom'

type SidebarProps = {
  isOpen: boolean
  onClose: () => void
}

const navItems = [
  { to: '/dashboard', label: 'Dashboard' },
]

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const location = useLocation()

  return (
    <>
      <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h2>Navigation</h2>
          <button type="button" className="close-sidebar" onClick={onClose}>
            Close
          </button>
        </div>

        <nav>
          {navItems.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className={location.pathname === item.to ? 'active' : ''}
              onClick={onClose}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>

      {isOpen && <button className="backdrop" type="button" onClick={onClose} aria-label="Close menu" />}
    </>
  )
}
