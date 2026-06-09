import { useEffect, useState, type FormEvent } from 'react'

import {
  createNote,
  deleteNote,
  getNotes,
  updateNote,
} from '../api/notesApi'
import { EmptyState } from '../components/EmptyState'
import { PageState } from '../components/PageState'
import { PaginationBar } from '../components/PaginationBar'
import type { Note } from '../types/note'

type NoteFormState = {
  title: string
  content: string
  tags: string
}

const notePageSize = 10

const emptyNoteForm: NoteFormState = {
  title: '',
  content: '',
  tags: '',
}

function toNotePayload(formState: NoteFormState) {
  return {
    title: formState.title.trim(),
    content: formState.content.trim(),
    tags: formState.tags.trim() || null,
  }
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
  }).format(new Date(value))
}

export function Notes() {
  const [notes, setNotes] = useState<Note[]>([])
  const [formState, setFormState] = useState<NoteFormState>(emptyNoteForm)
  const [editingNoteId, setEditingNoteId] = useState<number | null>(null)
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  async function loadNotes(nextPage = page) {
    setIsLoading(true)
    setError('')

    try {
      const data = await getNotes({
        skip: nextPage * notePageSize,
        limit: notePageSize,
        search: search.trim() || undefined,
        sort_by: 'updated_at',
        sort_dir: 'desc',
      })
      setNotes(data)
    } catch {
      setError('Unable to load notes.')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    let isMounted = true

    async function loadCurrentNotes() {
      await Promise.resolve()
      setIsLoading(true)
      setError('')

      try {
        const data = await getNotes({
          skip: page * notePageSize,
          limit: notePageSize,
          search: search.trim() || undefined,
          sort_by: 'updated_at',
          sort_dir: 'desc',
        })

        if (isMounted) {
          setNotes(data)
        }
      } catch {
        if (isMounted) {
          setError('Unable to load notes.')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    loadCurrentNotes()

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
      const payload = toNotePayload(formState)

      if (editingNoteId) {
        await updateNote(editingNoteId, payload)
      } else {
        await createNote(payload)
      }

      setFormState(emptyNoteForm)
      setEditingNoteId(null)
      await loadNotes()
    } catch {
      setError('Unable to save note.')
    } finally {
      setIsSubmitting(false)
    }
  }

  function handleEdit(note: Note) {
    setEditingNoteId(note.id)
    setFormState({
      title: note.title,
      content: note.content,
      tags: note.tags ?? '',
    })
  }

  async function handleDelete(noteId: number) {
    setError('')

    try {
      await deleteNote(noteId)
      await loadNotes()
    } catch {
      setError('Unable to delete note.')
    }
  }

  function handleCancelEdit() {
    setEditingNoteId(null)
    setFormState(emptyNoteForm)
  }

  return (
    <>
      <div className="page-header">
        <h1>Notes</h1>
        <p>Capture ideas, study material, and action details.</p>
      </div>

      {error ? <PageState message={error} tone="error" /> : null}

      <section className="resource-layout">
        <form className="resource-form" onSubmit={handleSubmit}>
          <h2>{editingNoteId ? 'Edit note' : 'Create note'}</h2>
          <div className="field">
            <label htmlFor="note-title">Title</label>
            <input
              id="note-title"
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
            <label htmlFor="note-content">Content</label>
            <textarea
              id="note-content"
              value={formState.content}
              onChange={(event) =>
                setFormState((current) => ({
                  ...current,
                  content: event.target.value,
                }))
              }
              rows={8}
              required
            />
          </div>
          <div className="field">
            <label htmlFor="note-tags">Tags</label>
            <input
              id="note-tags"
              value={formState.tags}
              onChange={(event) =>
                setFormState((current) => ({
                  ...current,
                  tags: event.target.value,
                }))
              }
              placeholder="study, work, ideas"
            />
          </div>
          <div className="form-actions">
            <button className="primary-button" type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Saving...' : editingNoteId ? 'Save note' : 'Create note'}
            </button>
            {editingNoteId ? (
              <button className="ghost-button" type="button" onClick={handleCancelEdit}>
                Cancel
              </button>
            ) : null}
          </div>
        </form>

        <section className="resource-list" aria-label="Note list">
          <form className="resource-toolbar" onSubmit={handleSearchSubmit}>
            <input
              className="search-input"
              type="search"
              placeholder="Search notes"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
            <button className="ghost-button" type="submit">
              Search
            </button>
          </form>

          {isLoading ? <PageState message="Loading notes..." /> : null}
          {!isLoading && notes.length === 0 ? (
            <EmptyState
              title="No notes found"
              description="Create your first note or adjust the search term."
            />
          ) : null}
          {!isLoading
            ? notes.map((note) => (
                <article className="resource-card" key={note.id}>
                  <div className="resource-card-main">
                    <div>
                      <h2>{note.title}</h2>
                      <p className="note-preview">{note.content}</p>
                    </div>
                    <span className="status-pill">Updated {formatDate(note.updated_at)}</span>
                  </div>
                  {note.tags ? <div className="tag-list">{note.tags}</div> : null}
                  <div className="resource-actions">
                    <button className="ghost-button" type="button" onClick={() => handleEdit(note)}>
                      Edit
                    </button>
                    <button
                      className="danger-button"
                      type="button"
                      onClick={() => handleDelete(note.id)}
                    >
                      Delete
                    </button>
                  </div>
                </article>
              ))
            : null}

          <PaginationBar
            page={page}
            hasNextPage={notes.length === notePageSize}
            isLoading={isLoading}
            onPrevious={() => setPage((current) => Math.max(0, current - 1))}
            onNext={() => setPage((current) => current + 1)}
          />
        </section>
      </section>
    </>
  )
}
