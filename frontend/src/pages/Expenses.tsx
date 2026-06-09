import { useEffect, useMemo, useState, type FormEvent } from 'react'

import {
  createExpense,
  deleteExpense,
  getExpenses,
  updateExpense,
} from '../api/expensesApi'
import { EmptyState } from '../components/EmptyState'
import { PageState } from '../components/PageState'
import { PaginationBar } from '../components/PaginationBar'
import type { Expense, ExpenseQueryParams } from '../types/expense'

type ExpenseFormState = {
  title: string
  amount: string
  category: string
  notes: string
  expenseDate: string
}

type ExpenseSortBy = NonNullable<ExpenseQueryParams['sort_by']>
type ExpenseSortDir = NonNullable<ExpenseQueryParams['sort_dir']>

const expensePageSize = 10

const emptyExpenseForm: ExpenseFormState = {
  title: '',
  amount: '',
  category: '',
  notes: '',
  expenseDate: '',
}

function formatAmount(value: number) {
  return new Intl.NumberFormat(undefined, {
    maximumFractionDigits: 2,
  }).format(value)
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
  }).format(new Date(value))
}

function toDateInputValue(value: string) {
  return value.slice(0, 10)
}

function toExpensePayload(formState: ExpenseFormState) {
  return {
    title: formState.title.trim(),
    amount: Number(formState.amount),
    category: formState.category.trim(),
    notes: formState.notes.trim() || null,
    expense_date: new Date(`${formState.expenseDate}T00:00:00`).toISOString(),
  }
}

function toDateTimeQuery(value: string, edge: 'start' | 'end') {
  if (!value) {
    return undefined
  }

  const suffix = edge === 'start' ? 'T00:00:00' : 'T23:59:59'
  return new Date(`${value}${suffix}`).toISOString()
}

export function Expenses() {
  const [expenses, setExpenses] = useState<Expense[]>([])
  const [formState, setFormState] =
    useState<ExpenseFormState>(emptyExpenseForm)
  const [editingExpenseId, setEditingExpenseId] = useState<number | null>(null)
  const [search, setSearch] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [sortBy, setSortBy] = useState<ExpenseSortBy>('expense_date')
  const [sortDir, setSortDir] = useState<ExpenseSortDir>('desc')
  const [page, setPage] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  const categories = useMemo(() => {
    return Array.from(new Set(expenses.map((expense) => expense.category))).sort()
  }, [expenses])

  async function loadExpenses(nextPage = page) {
    setIsLoading(true)
    setError('')

    try {
      const data = await getExpenses({
        skip: nextPage * expensePageSize,
        limit: expensePageSize,
        search: search.trim() || undefined,
        category: categoryFilter.trim() || undefined,
        start_date: toDateTimeQuery(startDate, 'start'),
        end_date: toDateTimeQuery(endDate, 'end'),
        sort_by: sortBy,
        sort_dir: sortDir,
      })
      setExpenses(data)
    } catch {
      setError('Unable to load expenses.')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    let isMounted = true

    async function loadCurrentExpenses() {
      await Promise.resolve()
      setIsLoading(true)
      setError('')

      try {
        const data = await getExpenses({
          skip: page * expensePageSize,
          limit: expensePageSize,
          search: search.trim() || undefined,
          category: categoryFilter.trim() || undefined,
          start_date: toDateTimeQuery(startDate, 'start'),
          end_date: toDateTimeQuery(endDate, 'end'),
          sort_by: sortBy,
          sort_dir: sortDir,
        })

        if (isMounted) {
          setExpenses(data)
        }
      } catch {
        if (isMounted) {
          setError('Unable to load expenses.')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    loadCurrentExpenses()

    return () => {
      isMounted = false
    }
  }, [categoryFilter, endDate, page, search, sortBy, sortDir, startDate])

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
      const payload = toExpensePayload(formState)

      if (editingExpenseId) {
        await updateExpense(editingExpenseId, payload)
      } else {
        await createExpense(payload)
      }

      setFormState(emptyExpenseForm)
      setEditingExpenseId(null)
      await loadExpenses()
    } catch {
      setError('Unable to save expense.')
    } finally {
      setIsSubmitting(false)
    }
  }

  function handleEdit(expense: Expense) {
    setEditingExpenseId(expense.id)
    setFormState({
      title: expense.title,
      amount: String(expense.amount),
      category: expense.category,
      notes: expense.notes ?? '',
      expenseDate: toDateInputValue(expense.expense_date),
    })
  }

  async function handleDelete(expenseId: number) {
    setError('')

    try {
      await deleteExpense(expenseId)
      await loadExpenses()
    } catch {
      setError('Unable to delete expense.')
    }
  }

  function handleCancelEdit() {
    setEditingExpenseId(null)
    setFormState(emptyExpenseForm)
  }

  return (
    <>
      <div className="page-header">
        <h1>Expenses</h1>
        <p>Track spending, categories, and financial activity over time.</p>
      </div>

      {error ? <PageState message={error} tone="error" /> : null}

      <section className="resource-layout">
        <form className="resource-form" onSubmit={handleSubmit}>
          <h2>{editingExpenseId ? 'Edit expense' : 'Create expense'}</h2>
          <div className="field">
            <label htmlFor="expense-title">Title</label>
            <input
              id="expense-title"
              value={formState.title}
              onChange={(event) =>
                setFormState((current) => ({
                  ...current,
                  title: event.target.value,
                }))
              }
              required
            />
          </div>
          <div className="form-grid">
            <div className="field">
              <label htmlFor="expense-amount">Amount</label>
              <input
                id="expense-amount"
                type="number"
                min="0.01"
                step="0.01"
                value={formState.amount}
                onChange={(event) =>
                  setFormState((current) => ({
                    ...current,
                    amount: event.target.value,
                  }))
                }
                required
              />
            </div>
            <div className="field">
              <label htmlFor="expense-date">Date</label>
              <input
                id="expense-date"
                type="date"
                value={formState.expenseDate}
                onChange={(event) =>
                  setFormState((current) => ({
                    ...current,
                    expenseDate: event.target.value,
                  }))
                }
                required
              />
            </div>
          </div>
          <div className="field">
            <label htmlFor="expense-category">Category</label>
            <input
              id="expense-category"
              value={formState.category}
              onChange={(event) =>
                setFormState((current) => ({
                  ...current,
                  category: event.target.value,
                }))
              }
              required
            />
          </div>
          <div className="field">
            <label htmlFor="expense-notes">Notes</label>
            <textarea
              id="expense-notes"
              value={formState.notes}
              onChange={(event) =>
                setFormState((current) => ({
                  ...current,
                  notes: event.target.value,
                }))
              }
              rows={4}
            />
          </div>
          <div className="form-actions">
            <button className="primary-button" type="submit" disabled={isSubmitting}>
              {isSubmitting
                ? 'Saving...'
                : editingExpenseId
                  ? 'Save expense'
                  : 'Create expense'}
            </button>
            {editingExpenseId ? (
              <button className="ghost-button" type="button" onClick={handleCancelEdit}>
                Cancel
              </button>
            ) : null}
          </div>
        </form>

        <section className="resource-list" aria-label="Expense list">
          <form className="resource-toolbar" onSubmit={handleFilterSubmit}>
            <input
              className="search-input"
              type="search"
              placeholder="Search expenses"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
            <input
              className="filter-select"
              list="expense-categories"
              placeholder="Category"
              value={categoryFilter}
              onChange={(event) => setCategoryFilter(event.target.value)}
            />
            <datalist id="expense-categories">
              {categories.map((category) => (
                <option key={category} value={category} />
              ))}
            </datalist>
            <input
              className="filter-select"
              type="date"
              value={startDate}
              onChange={(event) => setStartDate(event.target.value)}
            />
            <input
              className="filter-select"
              type="date"
              value={endDate}
              onChange={(event) => setEndDate(event.target.value)}
            />
            <select
              className="filter-select"
              value={sortBy}
              onChange={(event) => setSortBy(event.target.value as ExpenseSortBy)}
            >
              <option value="expense_date">Date</option>
              <option value="amount">Amount</option>
              <option value="created_at">Created</option>
            </select>
            <select
              className="filter-select"
              value={sortDir}
              onChange={(event) => setSortDir(event.target.value as ExpenseSortDir)}
            >
              <option value="desc">Desc</option>
              <option value="asc">Asc</option>
            </select>
            <button className="ghost-button" type="submit">
              Apply
            </button>
          </form>

          {isLoading ? <PageState message="Loading expenses..." /> : null}
          {!isLoading && expenses.length === 0 ? (
            <EmptyState
              title="No expenses found"
              description="Create your first expense or adjust your filters."
            />
          ) : null}
          {!isLoading
            ? expenses.map((expense) => (
                <article className="resource-card" key={expense.id}>
                  <div className="resource-card-main">
                    <div>
                      <h2>{expense.title}</h2>
                      <p>{expense.notes || 'No notes added.'}</p>
                    </div>
                    <span className="status-pill">{expense.category}</span>
                  </div>
                  <div className="goal-meta">
                    <span>{formatDate(expense.expense_date)}</span>
                    <span>{formatAmount(expense.amount)}</span>
                  </div>
                  <div className="resource-actions">
                    <button
                      className="ghost-button"
                      type="button"
                      onClick={() => handleEdit(expense)}
                    >
                      Edit
                    </button>
                    <button
                      className="danger-button"
                      type="button"
                      onClick={() => handleDelete(expense.id)}
                    >
                      Delete
                    </button>
                  </div>
                </article>
              ))
            : null}

          <PaginationBar
            page={page}
            hasNextPage={expenses.length === expensePageSize}
            isLoading={isLoading}
            onPrevious={() => setPage((current) => Math.max(0, current - 1))}
            onNext={() => setPage((current) => current + 1)}
          />
        </section>
      </section>
    </>
  )
}
