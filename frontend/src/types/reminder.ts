export type Reminder = {
  id: number
  title: string
  description: string | null
  tags: string | null
  due_date: string | null
  completed: boolean
  created_at: string
  updated_at: string
}

export type ReminderPayload = {
  title: string
  description: string | null
  tags: string | null
  due_date: string | null
  completed: boolean
}

export type ReminderQueryParams = {
  skip?: number
  limit?: number
  search?: string
  sort_by?: 'created_at' | 'updated_at' | 'due_date' | 'title'
  sort_dir?: 'asc' | 'desc'
}
