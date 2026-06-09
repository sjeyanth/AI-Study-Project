import { useEffect, useMemo, useState, type FormEvent } from 'react'

import {
  createTask,
  deleteTask,
  getTasks,
  updateTask,
} from '../api/tasksApi'
import { EmptyState } from '../components/EmptyState'
import { PageState } from '../components/PageState'
import type { Task } from '../types/task'

type TaskFormState = {
  title: string
  description: string
  completed: boolean
}

const emptyTaskForm: TaskFormState = {
  title: '',
  description: '',
  completed: false,
}

function toTaskPayload(formState: TaskFormState) {
  return {
    title: formState.title.trim(),
    description: formState.description.trim() || null,
    completed: formState.completed,
  }
}

export function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [formState, setFormState] = useState<TaskFormState>(emptyTaskForm)
  const [editingTaskId, setEditingTaskId] = useState<number | null>(null)
  const [search, setSearch] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  async function loadTasks() {
    setIsLoading(true)
    setError('')

    try {
      const data = await getTasks()
      setTasks(data)
    } catch {
      setError('Unable to load tasks.')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    let isMounted = true

    async function loadInitialTasks() {
      await Promise.resolve()
      setError('')

      try {
        const data = await getTasks()

        if (isMounted) {
          setTasks(data)
        }
      } catch {
        if (isMounted) {
          setError('Unable to load tasks.')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    loadInitialTasks()

    return () => {
      isMounted = false
    }
  }, [])

  const filteredTasks = useMemo(() => {
    const query = search.trim().toLowerCase()

    if (!query) {
      return tasks
    }

    return tasks.filter((task) => {
      return (
        task.title.toLowerCase().includes(query) ||
        (task.description ?? '').toLowerCase().includes(query)
      )
    })
  }, [search, tasks])

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsSubmitting(true)
    setError('')

    try {
      const payload = toTaskPayload(formState)

      if (editingTaskId) {
        await updateTask(editingTaskId, payload)
      } else {
        await createTask(payload)
      }

      setFormState(emptyTaskForm)
      setEditingTaskId(null)
      await loadTasks()
    } catch {
      setError('Unable to save task.')
    } finally {
      setIsSubmitting(false)
    }
  }

  function handleEdit(task: Task) {
    setEditingTaskId(task.id)
    setFormState({
      title: task.title,
      description: task.description ?? '',
      completed: task.completed,
    })
  }

  async function handleToggleCompleted(task: Task) {
    setError('')

    try {
      await updateTask(task.id, {
        title: task.title,
        description: task.description,
        completed: !task.completed,
      })
      await loadTasks()
    } catch {
      setError('Unable to update task.')
    }
  }

  async function handleDelete(taskId: number) {
    setError('')

    try {
      await deleteTask(taskId)
      await loadTasks()
    } catch {
      setError('Unable to delete task.')
    }
  }

  function handleCancelEdit() {
    setEditingTaskId(null)
    setFormState(emptyTaskForm)
  }

  return (
    <>
      <div className="page-header resource-header">
        <div>
          <h1>Tasks</h1>
          <p>Create, track, and complete your day-to-day work.</p>
        </div>
        <input
          className="search-input"
          type="search"
          placeholder="Search tasks"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
      </div>

      {error ? <PageState message={error} tone="error" /> : null}

      <section className="resource-layout">
        <form className="resource-form" onSubmit={handleSubmit}>
          <h2>{editingTaskId ? 'Edit task' : 'Create task'}</h2>
          <div className="field">
            <label htmlFor="task-title">Title</label>
            <input
              id="task-title"
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
            <label htmlFor="task-description">Description</label>
            <textarea
              id="task-description"
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
              {isSubmitting ? 'Saving...' : editingTaskId ? 'Save task' : 'Create task'}
            </button>
            {editingTaskId ? (
              <button className="ghost-button" type="button" onClick={handleCancelEdit}>
                Cancel
              </button>
            ) : null}
          </div>
        </form>

        <section className="resource-list" aria-label="Task list">
          {isLoading ? <PageState message="Loading tasks..." /> : null}
          {!isLoading && filteredTasks.length === 0 ? (
            <EmptyState
              title="No tasks found"
              description="Create your first task or adjust the search term."
            />
          ) : null}
          {!isLoading
            ? filteredTasks.map((task) => (
                <article className="resource-card" key={task.id}>
                  <div className="resource-card-main">
                    <div>
                      <h2>{task.title}</h2>
                      <p>{task.description || 'No description added.'}</p>
                    </div>
                    <span className={task.completed ? 'status-pill status-success' : 'status-pill'}>
                      {task.completed ? 'Completed' : 'Pending'}
                    </span>
                  </div>
                  <div className="resource-actions">
                    <button
                      className="ghost-button"
                      type="button"
                      onClick={() => handleToggleCompleted(task)}
                    >
                      {task.completed ? 'Mark pending' : 'Mark completed'}
                    </button>
                    <button className="ghost-button" type="button" onClick={() => handleEdit(task)}>
                      Edit
                    </button>
                    <button
                      className="danger-button"
                      type="button"
                      onClick={() => handleDelete(task.id)}
                    >
                      Delete
                    </button>
                  </div>
                </article>
              ))
            : null}
        </section>
      </section>
    </>
  )
}
