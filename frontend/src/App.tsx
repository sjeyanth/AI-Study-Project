import { useMemo, useState } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'

import Navbar from './components/Navbar'
import ProtectedRoute from './components/ProtectedRoute'
import Sidebar from './components/Sidebar'
import {useAuth } from './context/useAuth'
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'
import NotFound from './pages/NotFound'
import Register from './pages/Register'

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const auth = useAuth()

  const homeRoute = useMemo(() => {
    return auth.isAuthenticated ? '/dashboard' : '/login'
  }, [auth.isAuthenticated])

  return (
    <div className="app-shell">
      <Navbar
        isAuthenticated={auth.isAuthenticated}
        onLogout={auth.logout}
        onToggleSidebar={() => setSidebarOpen(true)}
      />

      <div className="layout">
        {auth.isAuthenticated && (
          <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        )}

        <main className="content" onClick={() => sidebarOpen && setSidebarOpen(false)}>
          <Routes>
            <Route path="/" element={<Navigate to={homeRoute} replace />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            <Route element={<ProtectedRoute />}>
              <Route path="/dashboard" element={<Dashboard />} />
            </Route>

            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
      </div>
    </div>
  )
}

export default App
