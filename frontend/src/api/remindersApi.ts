import { apiClient } from './client'
import type {
  Reminder,
  ReminderPayload,
  ReminderQueryParams,
} from '../types/reminder'

export async function getReminders(params: ReminderQueryParams = {}) {
  const response = await apiClient.get<Reminder[]>('/reminders', { params })
  return response.data
}

export async function createReminder(payload: ReminderPayload) {
  const response = await apiClient.post<Reminder>('/reminders', payload)
  return response.data
}

export async function updateReminder(
  reminderId: number,
  payload: ReminderPayload,
) {
  const response = await apiClient.put<Reminder>(
    `/reminders/${reminderId}`,
    payload,
  )
  return response.data
}

export async function deleteReminder(reminderId: number) {
  await apiClient.delete(`/reminders/${reminderId}`)
}
