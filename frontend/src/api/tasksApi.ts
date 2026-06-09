import { apiClient } from './client'
import type { Task, TaskPayload } from '../types/task'

export async function getTasks() {
  const response = await apiClient.get<Task[]>('/tasks')
  return response.data
}

export async function createTask(payload: TaskPayload) {
  const response = await apiClient.post<Task>('/tasks', payload)
  return response.data
}

export async function updateTask(taskId: number, payload: TaskPayload) {
  const response = await apiClient.put<Task>(`/tasks/${taskId}`, payload)
  return response.data
}

export async function deleteTask(taskId: number) {
  await apiClient.delete(`/tasks/${taskId}`)
}
