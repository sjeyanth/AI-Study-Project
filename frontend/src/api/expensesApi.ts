import { apiClient } from './client'
import type {
  Expense,
  ExpensePayload,
  ExpenseQueryParams,
} from '../types/expense'

export async function getExpenses(params: ExpenseQueryParams = {}) {
  const response = await apiClient.get<Expense[]>('/expenses', { params })
  return response.data
}

export async function createExpense(payload: ExpensePayload) {
  const response = await apiClient.post<Expense>('/expenses', payload)
  return response.data
}

export async function updateExpense(expenseId: number, payload: ExpensePayload) {
  const response = await apiClient.put<Expense>(
    `/expenses/${expenseId}`,
    payload,
  )
  return response.data
}

export async function deleteExpense(expenseId: number) {
  await apiClient.delete(`/expenses/${expenseId}`)
}
