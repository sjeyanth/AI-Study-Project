import { useEffect, useState, type FormEvent } from 'react'

import {
  createReminder,
  deleteReminder,
  getReminders,
  updateReminder,
} from '../api/remindersApi'
import { EmptyState } from '../components/EmptyState'
import { PageState } from '../components/PageState'
import { PaginationBar } from '../components/PaginationBar'
import type { Reminder } from '../types/reminder'

type ReminderFormState = {
  title: string
  description: string
  tags: string
  dueDate: string
  completed: boolean
}

const reminderPageSize = 10

const emptyReminderForm: ReminderFormState = {
  title: '',
  description: '',
  tags: '',
  dueDate: '',
  completed: false,
}

function toReminderPayload(formState: ReminderFormState) {
  return {
    title: formState.title.trim(),
    description: formState.description.trim() || null,
    tags: formState.tags.trim() || null,
    due_date: formState.dueDate
      ? new Date(formState.dueDate).toISOString()
      : null,
    completed: formState.completed,
  }
}

function toDateTimeInputValue(value: string | null) {
  if (!value) {
    return ''
  }

  const date = new Date(value)
  const timezoneOffset = date.getTimezoneOffset() * 60_000
  return new Date(date.getTime() - timezoneOffset).toISOString().slice(0, 16)
}

function formatDateTime(value: string | null) {
  if (!value) {
    return 'No date set'
  }

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}

export function Reminders() {
  const [reminders, setReminders] = useState<Reminder[]>([])
  const [formState, setFormState] =
    useState<ReminderFormState>(emptyReminderForm)
  const [editingReminderId, setEditingReminderId] = useState<number | null>(null)
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  async function loadReminders(nextPage = page) {
    setIsLoading(true)
    setError('')

    try {
      const data = await getReminders({
        skip: nextPage * reminderPageSize,
        limit: reminderPageSize,
        search: search.trim() || undefined,
        sort_by: 'due_date',
        sort_dir: 'asc',
      })
      setReminders(data)
    } catch {
      setError('Unable to load reminders.')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    let isMounted = true

    async function loadCurrentReminders() {
      await Promise.resolve()
      setIsLoading(true)
      setError('')

      try {
        const data = await getReminders({
          skip: page * reminderPageSize,
          limit: reminderPageSize,
          search: search.trim() || undefined,
          sort_by: 'due_date',
          sort_dir: 'asc',
        })

        if (isMounted) {
          setReminders(data)
        }
      } catch {
        if (isMounted) {
          setError('Unable to load reminders.')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    loadCurrentReminders()

    return () => {
      isMounted = false
    }
  }, [page, search])

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
      const payload = toReminderPayload(formState)

      if (editingReminderId) {
        await updateReminder(editingReminderId, payload)
      } else {
        await createReminder(payload)
      }

      setFormState(emptyReminderForm)
      setEditingReminderId(null)
      await loadReminders()
    } catch {
      setError('Unable to save reminder.')
    } finally {
      setIsSubmitting(false)
    }
  }

  function handleEdit(reminder: Reminder) {
    setEditingReminderId(reminder.id)
    setFormState({
      title: reminder.title,
      description: reminder.description ?? '',
      tags: reminder.tags ?? '',
      dueDate: toDateTimeInputValue(reminder.due_date),
      completed: reminder.completed,
    })
  }

  async function handleToggleCompleted(reminder: Reminder) {
    setError('')

    try {
      await updateReminder(reminder.id, {
        title: reminder.title,
        description: reminder.description,
        tags: reminder.tags,
        due_date: reminder.due_date,
        completed: !reminder.completed,
      })
      await loadReminders()
    } catch {
      setError('Unable to update reminder.')
    }
  }

  async function handleDelete(reminderId: number) {
    setError('')

    try {
      await deleteReminder(reminderId)
      await loadReminders()
    } catch {
      setError('Unable to delete reminder.')
    }
  }

  function handleCancelEdit() {
    setEditingReminderId(null)
    setFormState(emptyReminderForm)
  }

  return (
    <>
      <div className="page-header">
        <h1>Reminders</h1>
        <p>Keep upcoming dates and time-sensitive work visible.</p>
      </div>

      {error ? <PageState message={error} tone="error" /> : null}

      <section className="resource-layout">
        <form className="resource-form" onSubmit={handleSubmit}>
          <h2>{editingReminderId ? 'Edit reminder' : 'Create reminder'}</h2>
          <div className="field">
            <label htmlFor="reminder-title">Title</label>
            <input
              id="reminder-title"
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
            <label htmlFor="reminder-description">Description</label>
            <textarea
              id="reminder-description"
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
          <div className="field">
            <label htmlFor="reminder-due-date">Reminder date and time</label>
            <input
              id="reminder-due-date"
              type="datetime-local"
              value={formState.dueDate}
              onChange={(event) =>
                setFormState((current) => ({
                  ...current,
                  dueDate: event.target.value,
                }))
              }
            />
          </div>
          <div className="field">
            <label htmlFor="reminder-tags">Tags</label>
            <input
              id="reminder-tags"
              value={formState.tags}
              onChange={(event) =>
                setFormState((current) => ({
                  ...current,
                  tags: event.target.value,
                }))
              }
              placeholder="personal, follow-up"
            />
          </div>
          <label className="checkbox-field">
            <input
              type="checkbox"
              checked={formState.completed}
              onChange={(event) =>
                setFormState((current) => ({
                  ...current,
                  completed: event.target.checked,
                }))
              }
            />
            Completed
          </label>
          <div className="form-actions">
            <button className="primary-button" type="submit" disabled={isSubmitting}>
              {isSubmitting
                ? 'Saving...'
                : editingReminderId
                  ? 'Save reminder'
                  : 'Create reminder'}
            </button>
            {editingReminderId ? (
              <button className="ghost-button" type="button" onClick={handleCancelEdit}>
                Cancel
              </button>
            ) : null}
          </div>
        </form>

        <section className="resource-list" aria-label="Reminder list">
          <form className="resource-toolbar" onSubmit={handleSearchSubmit}>
            <input
              className="search-input"
              type="search"
              placeholder="Search reminders"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
            <button className="ghost-button" type="submit">
              Search
            </button>
          </form>

          {isLoading ? <PageState message="Loading reminders..." /> : null}
          {!isLoading && reminders.length === 0 ? (
            <EmptyState
              title="No reminders found"
              description="Create your first reminder or adjust the search term."
            />
          ) : null}
          {!isLoading
            ? reminders.map((reminder) => (
                <article className="resource-card" key={reminder.id}>
                  <div className="resource-card-main">
                    <div>
                      <h2>{reminder.title}</h2>
                      <p>{reminder.description || 'No description added.'}</p>
                    </div>
                    <span
                      className={
                        reminder.completed
                          ? 'status-pill status-success'
                          : 'status-pill'
                      }
                    >
                      {reminder.completed ? 'Completed' : 'Upcoming'}
                    </span>
                  </div>
                  <div className="goal-meta">
                    <span>{formatDateTime(reminder.due_date)}</span>
                    {reminder.tags ? <span>{reminder.tags}</span> : null}
                  </div>
                  <div className="resource-actions">
                    <button
                      className="ghost-button"
                      type="button"
                      onClick={() => handleToggleCompleted(reminder)}
                    >
                      {reminder.completed ? 'Mark upcoming' : 'Mark completed'}
                    </button>
                    <button
                      className="ghost-button"
                      type="button"
                      onClick={() => handleEdit(reminder)}
                    >
                      Edit
                    </button>
                    <button
                      className="danger-button"
                      type="button"
                      onClick={() => handleDelete(reminder.id)}
                    >
                      Delete
                    </button>
                  </div>
                </article>
              ))
            : null}

          <PaginationBar
            page={page}
            hasNextPage={reminders.length === reminderPageSize}
            isLoading={isLoading}
            onPrevious={() => setPage((current) => Math.max(0, current - 1))}
            onNext={() => setPage((current) => current + 1)}
          />
        </section>
      </section>
    </>
  )
}
