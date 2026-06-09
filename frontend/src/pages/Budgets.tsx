import { useEffect, useState, type FormEvent } from 'react'

import {
  createBudget,
  deleteBudget,
  getBudgets,
  updateBudget,
} from '../api/budgetsApi'
import { getDashboardData } from '../api/dashboardApi'
import { DashboardCard } from '../components/DashboardCard'
import { EmptyState } from '../components/EmptyState'
import { PageState } from '../components/PageState'
import { PaginationBar } from '../components/PaginationBar'
import type { Budget } from '../types/budget'
import type { DashboardResponse } from '../types/dashboard'

type BudgetFormState = {
  month: string
  year: string
  totalBudget: string
  currency: string
}

const budgetPageSize = 10
const monthNames = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
]

const emptyBudgetForm: BudgetFormState = {
  month: String(new Date().getMonth() + 1),
  year: String(new Date().getFullYear()),
  totalBudget: '',
  currency: 'INR',
}

function formatAmount(value: number, currency?: string) {
  return `${currency ? `${currency} ` : ''}${new Intl.NumberFormat(undefined, {
    maximumFractionDigits: 2,
  }).format(value)}`
}

function toBudgetPayload(formState: BudgetFormState) {
  return {
    month: Number(formState.month),
    year: Number(formState.year),
    total_budget: Number(formState.totalBudget),
    currency: formState.currency.trim().toUpperCase(),
  }
}

export function Budgets() {
  const [budgets, setBudgets] = useState<Budget[]>([])
  const [summary, setSummary] = useState<DashboardResponse | null>(null)
  const [formState, setFormState] = useState<BudgetFormState>(emptyBudgetForm)
  const [editingBudgetId, setEditingBudgetId] = useState<number | null>(null)
  const [monthFilter, setMonthFilter] = useState('')
  const [yearFilter, setYearFilter] = useState('')
  const [page, setPage] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  async function loadBudgets(nextPage = page) {
    setIsLoading(true)
    setError('')

    try {
      const [budgetData, dashboardData] = await Promise.all([
        getBudgets({
          skip: nextPage * budgetPageSize,
          limit: budgetPageSize,
          month: monthFilter ? Number(monthFilter) : undefined,
          year: yearFilter ? Number(yearFilter) : undefined,
          sort_by: 'year',
          sort_dir: 'desc',
        }),
        getDashboardData(),
      ])
      setBudgets(budgetData)
      setSummary(dashboardData)
    } catch {
      setError('Unable to load budgets.')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    let isMounted = true

    async function loadCurrentBudgets() {
      await Promise.resolve()
      setIsLoading(true)
      setError('')

      try {
        const [budgetData, dashboardData] = await Promise.all([
          getBudgets({
            skip: page * budgetPageSize,
            limit: budgetPageSize,
            month: monthFilter ? Number(monthFilter) : undefined,
            year: yearFilter ? Number(yearFilter) : undefined,
            sort_by: 'year',
            sort_dir: 'desc',
          }),
          getDashboardData(),
        ])

        if (isMounted) {
          setBudgets(budgetData)
          setSummary(dashboardData)
        }
      } catch {
        if (isMounted) {
          setError('Unable to load budgets.')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    loadCurrentBudgets()

    return () => {
      isMounted = false
    }
  }, [monthFilter, page, yearFilter])

  async function handleFilterSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    if (page !== 0) {
      setPage(0)
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsSubmitting(true)
    setError('')

    try {
      const payload = toBudgetPayload(formState)

      if (editingBudgetId) {
        await updateBudget(editingBudgetId, payload)
      } else {
        await createBudget(payload)
      }

      setFormState(emptyBudgetForm)
      setEditingBudgetId(null)
      await loadBudgets()
    } catch {
      setError('Unable to save budget.')
    } finally {
      setIsSubmitting(false)
    }
  }

  function handleEdit(budget: Budget) {
    setEditingBudgetId(budget.id)
    setFormState({
      month: String(budget.month),
      year: String(budget.year),
      totalBudget: String(budget.total_budget),
      currency: budget.currency,
    })
  }

  async function handleDelete(budgetId: number) {
    setError('')

    try {
      await deleteBudget(budgetId)
      await loadBudgets()
    } catch {
      setError('Unable to delete budget.')
    }
  }

  function handleCancelEdit() {
    setEditingBudgetId(null)
    setFormState(emptyBudgetForm)
  }

  return (
    <>
      <div className="page-header">
        <h1>Budgets</h1>
        <p>Set monthly budgets and compare them against spending.</p>
      </div>

      {error ? <PageState message={error} tone="error" /> : null}

      {summary ? (
        <section className="dashboard-card-grid finance-summary" aria-label="Budget summary">
          <DashboardCard label="Total Budget" value={formatAmount(summary.total_budget)} />
          <DashboardCard label="Total Spent" value={formatAmount(summary.total_spent)} />
          <DashboardCard
            label="Remaining Budget"
            value={formatAmount(summary.remaining_budget)}
          />
        </section>
      ) : null}

      <section className="resource-layout">
        <form className="resource-form" onSubmit={handleSubmit}>
          <h2>{editingBudgetId ? 'Edit budget' : 'Create budget'}</h2>
          <div className="form-grid">
            <div className="field">
              <label htmlFor="budget-month">Month</label>
              <select
                id="budget-month"
                value={formState.month}
                onChange={(event) =>
                  setFormState((current) => ({
                    ...current,
                    month: event.target.value,
                  }))
                }
              >
                {monthNames.map((month, index) => (
                  <option key={month} value={index + 1}>
                    {month}
                  </option>
                ))}
              </select>
            </div>
            <div className="field">
              <label htmlFor="budget-year">Year</label>
              <input
                id="budget-year"
                type="number"
                min="2000"
                max="2100"
                value={formState.year}
                onChange={(event) =>
                  setFormState((current) => ({
                    ...current,
                    year: event.target.value,
                  }))
                }
                required
              />
            </div>
          </div>
          <div className="field">
            <label htmlFor="budget-total">Total budget</label>
            <input
              id="budget-total"
              type="number"
              min="0.01"
              step="0.01"
              value={formState.totalBudget}
              onChange={(event) =>
                setFormState((current) => ({
                  ...current,
                  totalBudget: event.target.value,
                }))
              }
              required
            />
          </div>
          <div className="field">
            <label htmlFor="budget-currency">Currency</label>
            <input
              id="budget-currency"
              maxLength={10}
              value={formState.currency}
              onChange={(event) =>
                setFormState((current) => ({
                  ...current,
                  currency: event.target.value,
                }))
              }
              required
            />
          </div>
          <div className="form-actions">
            <button className="primary-button" type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Saving...' : editingBudgetId ? 'Save budget' : 'Create budget'}
            </button>
            {editingBudgetId ? (
              <button className="ghost-button" type="button" onClick={handleCancelEdit}>
                Cancel
              </button>
            ) : null}
          </div>
        </form>

        <section className="resource-list" aria-label="Budget list">
          <form className="resource-toolbar" onSubmit={handleFilterSubmit}>
            <select
              className="filter-select"
              value={monthFilter}
              onChange={(event) => setMonthFilter(event.target.value)}
            >
              <option value="">All months</option>
              {monthNames.map((month, index) => (
                <option key={month} value={index + 1}>
                  {month}
                </option>
              ))}
            </select>
            <input
              className="filter-select"
              type="number"
              min="2000"
              max="2100"
              placeholder="Year"
              value={yearFilter}
              onChange={(event) => setYearFilter(event.target.value)}
            />
            <button className="ghost-button" type="submit">
              Apply
            </button>
          </form>

          {isLoading ? <PageState message="Loading budgets..." /> : null}
          {!isLoading && budgets.length === 0 ? (
            <EmptyState
              title="No budgets found"
              description="Create your first budget or adjust the filters."
            />
          ) : null}
          {!isLoading
            ? budgets.map((budget) => (
                <article className="resource-card" key={budget.id}>
                  <div className="resource-card-main">
                    <div>
                      <h2>
                        {monthNames[budget.month - 1]} {budget.year}
                      </h2>
                      <p>{formatAmount(budget.total_budget, budget.currency)}</p>
                    </div>
                    <span className="status-pill">{budget.currency}</span>
                  </div>
                  <div className="resource-actions">
                    <button
                      className="ghost-button"
                      type="button"
                      onClick={() => handleEdit(budget)}
                    >
                      Edit
                    </button>
                    <button
                      className="danger-button"
                      type="button"
                      onClick={() => handleDelete(budget.id)}
                    >
                      Delete
                    </button>
                  </div>
                </article>
              ))
            : null}

          <PaginationBar
            page={page}
            hasNextPage={budgets.length === budgetPageSize}
            isLoading={isLoading}
            onPrevious={() => setPage((current) => Math.max(0, current - 1))}
            onNext={() => setPage((current) => current + 1)}
          />
        </section>
      </section>
    </>
  )
}
