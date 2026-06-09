import { apiClient } from './client'
import type { DashboardResponse } from '../types/dashboard'

export async function getDashboardData() {
  const response = await apiClient.get<DashboardResponse>('/dashboard/')
  return response.data
}
