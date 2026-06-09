import { useEffect, useState, type FormEvent } from 'react'

import {
  createGoal,
  deleteGoal,
  getGoals,
  updateGoal,
} from '../api/goalsApi'
import { EmptyState } from '../components/EmptyState'
import { PageState } from '../components/PageState'
import type { Goal, GoalStatus } from '../types/goal'

type GoalFormState = {
  title: string
  description: string
  targetDate: string
  status: GoalStatus
  progress: number
}

const goalPageSize = 10

const emptyGoalForm: GoalFormState = {
  title: '',
  description: '',
  targetDate: '',
  status: 'not_started',
  progress: 0,
}

const statusLabels: Record<GoalStatus, string> = {
  not_started: 'Not started',
  in_progress: 'In progress',
  completed: 'Completed',
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
  }).format(new Date(value))
}

function toDateInputValue(value: string) {
  return value.slice(0, 10)
}

function toGoalPayload(formState: GoalFormState) {
  return {
    title: formState.title.trim(),
    description: formState.description.trim() || null,
    target_date: new Date(`${formState.targetDate}T00:00:00`).toISOString(),
    status: formState.status,
    progress: Number(formState.progress),
  }
}

export function Goals() {
  const [goals, setGoals] = useState<Goal[]>([])
  const [formState, setFormState] = useState<GoalFormState>(emptyGoalForm)
  const [editingGoalId, setEditingGoalId] = useState<number | null>(null)
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState<GoalStatus | ''>('')
  const [page, setPage] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  async function loadGoals(nextPage = page) {
    setIsLoading(true)
    setError('')

    try {
      const data = await getGoals({
        skip: nextPage * goalPageSize,
        limit: goalPageSize,
        search: search.trim() || undefined,
        status: statusFilter,
        sort_by: 'created_at',
        sort_dir: 'desc',
      })
      setGoals(data)
    } catch {
      setError('Unable to load goals.')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    let isMounted = true

    async function loadCurrentGoals() {
      await Promise.resolve()
      setIsLoading(true)
      setError('')

      try {
        const data = await getGoals({
          skip: page * goalPageSize,
          limit: goalPageSize,
          search: search.trim() || undefined,
          status: statusFilter,
          sort_by: 'created_at',
          sort_dir: 'desc',
        })

        if (isMounted) {
          setGoals(data)
        }
      } catch {
        if (isMounted) {
          setError('Unable to load goals.')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    loadCurrentGoals()

    return () => {
      isMounted = false
    }
  }, [page, search, statusFilter])

  async function handleSearchSubmit(event: FormEvent<HTMLFormElement>) {
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
      const payload = toGoalPayload(formState)

      if (editingGoalId) {
        await updateGoal(editingGoalId, payload)
      } else {
        await createGoal(payload)
      }

      setFormState(emptyGoalForm)
      setEditingGoalId(null)
      await loadGoals()
    } catch {
      setError('Unable to save goal.')
    } finally {
      setIsSubmitting(false)
    }
  }

  function handleEdit(goal: Goal) {
    setEditingGoalId(goal.id)
    setFormState({
      title: goal.title,
      description: goal.description ?? '',
      targetDate: toDateInputValue(goal.target_date),
      status: goal.status,
      progress: goal.progress,
    })
  }

  async function handleDelete(goalId: number) {
    setError('')

    try {
      await deleteGoal(goalId)
      await loadGoals()
    } catch {
      setError('Unable to delete goal.')
    }
  }

  function handleCancelEdit() {
    setEditingGoalId(null)
    setFormState(emptyGoalForm)
  }

  return (
    <>
      <div className="page-header">
        <h1>Goals</h1>
        <p>Plan outcomes, monitor progress, and keep milestones visible.</p>
      </div>

      {error ? <PageState message={error} tone="error" /> : null}

      <section className="resource-layout">
        <form className="resource-form" onSubmit={handleSubmit}>
          <h2>{editingGoalId ? 'Edit goal' : 'Create goal'}</h2>
          <div className="field">
            <label htmlFor="goal-title">Title</label>
            <input
              id="goal-title"
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
          <div className="field">
            <label htmlFor="goal-description">Description</label>
            <textarea
              id="goal-description"
              value={formState.description}
              onChange={(event) =>
                setFormState((current) => ({
                  ...current,
                  description: event.target.value,
                }))
              }
              rows={4}
            />
          </div>
          <div className="form-grid">
            <div className="field">
              <label htmlFor="goal-target-date">Target date</label>
              <input
                id="goal-target-date"
                type="date"
                value={formState.targetDate}
                onChange={(event) =>
                  setFormState((current) => ({
                    ...current,
                    targetDate: event.target.value,
                  }))
                }
                required
              />
            </div>
            <div className="field">
              <label htmlFor="goal-status">Status</label>
              <select
                id="goal-status"
                value={formState.status}
                onChange={(event) =>
                  setFormState((current) => ({
                    ...current,
                    status: event.target.value as GoalStatus,
                  }))
                }
              >
                <option value="not_started">Not started</option>
                <option value="in_progress">In progress</option>
                <option value="completed">Completed</option>
              </select>
            </div>
          </div>
          <div className="field">
            <label htmlFor="goal-progress">Progress: {formState.progress}%</label>
            <input
              id="goal-progress"
              type="range"
              min="0"
              max="100"
              value={formState.progress}
              onChange={(event) =>
                setFormState((current) => ({
                  ...current,
                  progress: Number(event.target.value),
                }))
              }
            />
          </div>
          <div className="form-actions">
            <button className="primary-button" type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Saving...' : editingGoalId ? 'Save goal' : 'Create goal'}
            </button>
            {editingGoalId ? (
              <button className="ghost-button" type="button" onClick={handleCancelEdit}>
                Cancel
              </button>
            ) : null}
          </div>
        </form>

        <section className="resource-list" aria-label="Goal list">
          <form className="resource-toolbar" onSubmit={handleSearchSubmit}>
            <input
              className="search-input"
              type="search"
              placeholder="Search goals"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
            <select
              className="filter-select"
              value={statusFilter}
              onChange={(event) => setStatusFilter(event.target.value as GoalStatus | '')}
            >
              <option value="">All statuses</option>
              <option value="not_started">Not started</option>
              <option value="in_progress">In progress</option>
              <option value="completed">Completed</option>
            </select>
            <button className="ghost-button" type="submit">
              Search
            </button>
          </form>

          {isLoading ? <PageState message="Loading goals..." /> : null}
          {!isLoading && goals.length === 0 ? (
            <EmptyState
              title="No goals found"
              description="Create your first goal or adjust your filters."
            />
          ) : null}
          {!isLoading
            ? goals.map((goal) => (
                <article className="resource-card" key={goal.id}>
                  <div className="resource-card-main">
                    <div>
                      <h2>{goal.title}</h2>
                      <p>{goal.description || 'No description added.'}</p>
                    </div>
                    <span
                      className={
                        goal.status === 'completed'
                          ? 'status-pill status-success'
                          : 'status-pill'
                      }
                    >
                      {statusLabels[goal.status]}
                    </span>
                  </div>
                  <div className="goal-meta">
                    <span>Target: {formatDate(goal.target_date)}</span>
                    <span>{goal.progress}% complete</span>
                  </div>
                  <div className="progress-track" aria-label={`${goal.progress}% complete`}>
                    <span style={{ width: `${goal.progress}%` }} />
                  </div>
                  <div className="resource-actions">
                    <button className="ghost-button" type="button" onClick={() => handleEdit(goal)}>
                      Edit
                    </button>
                    <button
                      className="danger-button"
                      type="button"
                      onClick={() => handleDelete(goal.id)}
                    >
                      Delete
                    </button>
                  </div>
                </article>
              ))
            : null}

          <div className="pagination-bar">
            <button
              className="ghost-button"
              type="button"
              disabled={page === 0 || isLoading}
              onClick={() => setPage((current) => Math.max(0, current - 1))}
            >
              Previous
            </button>
            <span>Page {page + 1}</span>
            <button
              className="ghost-button"
              type="button"
              disabled={goals.length < goalPageSize || isLoading}
              onClick={() => setPage((current) => current + 1)}
            >
              Next
            </button>
          </div>
        </section>
      </section>
    </>
  )
}
