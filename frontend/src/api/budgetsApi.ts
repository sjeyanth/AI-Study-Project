import { apiClient } from './client'
import type { Budget, BudgetPayload, BudgetQueryParams } from '../types/budget'

export async function getBudgets(params: BudgetQueryParams = {}) {
  const response = await apiClient.get<Budget[]>('/budgets', { params })
  return response.data
}

export async function createBudget(payload: BudgetPayload) {
  const response = await apiClient.post<Budget>('/budgets', payload)
  return response.data
}

export async function updateBudget(budgetId: number, payload: BudgetPayload) {
  const response = await apiClient.put<Budget>(`/budgets/${budgetId}`, payload)
  return response.data
}

export async function deleteBudget(budgetId: number) {
  await apiClient.delete(`/budgets/${budgetId}`)
}
