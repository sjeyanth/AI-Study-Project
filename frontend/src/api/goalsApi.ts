import { apiClient } from './client'
import type { Goal, GoalPayload, GoalQueryParams } from '../types/goal'

export async function getGoals(params: GoalQueryParams = {}) {
  const response = await apiClient.get<Goal[]>('/goals', { params })
  return response.data
}

export async function createGoal(payload: GoalPayload) {
  const response = await apiClient.post<Goal>('/goals', payload)
  return response.data
}

export async function updateGoal(goalId: number, payload: GoalPayload) {
  const response = await apiClient.put<Goal>(`/goals/${goalId}`, payload)
  return response.data
}

export async function deleteGoal(goalId: number) {
  await apiClient.delete(`/goals/${goalId}`)
}
