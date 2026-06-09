import { Navigate, Route, Routes } from 'react-router-dom'

import { AppLayout } from '../components/AppLayout'
import { Budgets } from '../pages/Budgets'
import { GuestRoute } from '../components/GuestRoute'
import { ProtectedRoute } from '../components/ProtectedRoute'
import { Dashboard } from '../pages/Dashboard'
import { Expenses } from '../pages/Expenses'
import { Goals } from '../pages/Goals'
import { Login } from '../pages/Login'
import { Notes } from '../pages/Notes'
import { NotFound } from '../pages/NotFound'
import { Register } from '../pages/Register'
import { Reminders } from '../pages/Reminders'
import { Tasks } from '../pages/Tasks'

export function AppRoutes() {
  return (
    <Routes>
      <Route element={<GuestRoute />}>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Route>

      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/tasks" element={<Tasks />} />
          <Route path="/goals" element={<Goals />} />
          <Route path="/notes" element={<Notes />} />
          <Route path="/reminders" element={<Reminders />} />
          <Route path="/budgets" element={<Budgets />} />
          <Route path="/expenses" element={<Expenses />} />
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
        </Route>
      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}
