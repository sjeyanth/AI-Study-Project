import { apiClient } from './client'
import type { Note, NotePayload, NoteQueryParams } from '../types/note'

export async function getNotes(params: NoteQueryParams = {}) {
  const response = await apiClient.get<Note[]>('/notes', { params })
  return response.data
}

export async function createNote(payload: NotePayload) {
  const response = await apiClient.post<Note>('/notes', payload)
  return response.data
}

export async function updateNote(noteId: number, payload: NotePayload) {
  const response = await apiClient.put<Note>(`/notes/${noteId}`, payload)
  return response.data
}

export async function deleteNote(noteId: number) {
  await apiClient.delete(`/notes/${noteId}`)
}
