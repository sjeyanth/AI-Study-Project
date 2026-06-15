import { useEffect, useState } from 'react'

import { getDashboardData } from '../api/dashboardApi'
import { DashboardCard } from '../components/DashboardCard'
import type { DashboardResponse } from '../types/dashboard'

const amountFormatter = new Intl.NumberFormat(undefined, {
  maximumFractionDigits: 2,
  minimumFractionDigits: 0,
})

function formatAmount(value: number) {
  return amountFormatter.format(value)
}

function formatProgress(value: number) {
  return `${Math.round(value)}%`
}

export function Dashboard() {
  const [dashboardData, setDashboardData] = useState<DashboardResponse | null>(
    null,
  )
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let isMounted = true

    async function loadDashboardData() {
      try {
        const data = await getDashboardData()

        if (isMounted) {
          setDashboardData(data)
          setError('')
        }
      } catch {
        if (isMounted) {
          setError('Unable to load dashboard analytics.')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    loadDashboardData()

    return () => {
      isMounted = false
    }
  }, [])

  return (
    <>
      <div className="page-header">
        <h1>Dashboard</h1>
        <p>Your productivity and finance analytics at a glance.</p>
      </div>

      {isLoading ? (
        <section className="dashboard-state" aria-live="polite">
          Loading dashboard analytics...
        </section>
      ) : null}

      {error ? (
        <section className="dashboard-state dashboard-state-error" role="alert">
          {error}
        </section>
      ) : null}

      {dashboardData ? (
        <div className="dashboard-sections">
          <section className="dashboard-section" aria-labelledby="tasks-title">
            <div className="section-heading">
              <h2 id="tasks-title">Tasks</h2>
            </div>
            <div className="dashboard-card-grid">
              <DashboardCard label="Total Tasks" value={dashboardData.total_tasks} />
              <DashboardCard
                label="Completed Tasks"
                value={dashboardData.completed_tasks}
              />
              <DashboardCard
                label="Pending Tasks"
                value={dashboardData.pending_tasks}
              />
            </div>
          </section>

          <section className="dashboard-section" aria-labelledby="goals-title">
            <div className="section-heading">
              <h2 id="goals-title">Goals</h2>
            </div>
            <div className="dashboard-card-grid">
              <DashboardCard label="Total Goals" value={dashboardData.total_goals} />
              <DashboardCard
                label="Completed Goals"
                value={dashboardData.completed_goals}
              />
              <DashboardCard
                label="Average Goal Progress"
                value={formatProgress(dashboardData.average_goal_progress)}
              />
            </div>
          </section>

          <section className="dashboard-section" aria-labelledby="notes-title">
            <div className="section-heading">
              <h2 id="notes-title">Notes</h2>
            </div>
            <div className="dashboard-card-grid dashboard-card-grid-compact">
              <DashboardCard label="Total Notes" value={dashboardData.total_notes} />
            </div>
          </section>

          <section className="dashboard-section" aria-labelledby="reminders-title">
            <div className="section-heading">
              <h2 id="reminders-title">Reminders</h2>
            </div>
            <div className="dashboard-card-grid dashboard-card-grid-compact">
              <DashboardCard
                label="Total Reminders"
                value={dashboardData.total_reminders}
              />
            </div>
          </section>

          <section className="dashboard-section" aria-labelledby="finance-title">
            <div className="section-heading">
              <h2 id="finance-title">Finance</h2>
            </div>
            <div className="dashboard-card-grid">
              <DashboardCard
                label="Total Budget"
                value={formatAmount(dashboardData.total_budget)}
              />
              <DashboardCard
                label="Total Spent"
                value={formatAmount(dashboardData.total_spent)}
              />
              <DashboardCard
                label="Remaining Budget"
                value={formatAmount(dashboardData.remaining_budget)}
              />
            </div>
          </section>
        </div>
      ) : null}
    </>
  )
}
