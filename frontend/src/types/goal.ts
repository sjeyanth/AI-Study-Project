export type GoalStatus = 'not_started' | 'in_progress' | 'completed'

export type Goal = {
  id: number
  user_id: number
  title: string
  description: string | null
  target_date: string
  status: GoalStatus
  progress: number
  created_at: string
  updated_at: string
}

export type GoalPayload = {
  title: string
  description: string | null
  target_date: string
  status: GoalStatus
  progress: number
}

export type GoalQueryParams = {
  skip?: number
  limit?: number
  search?: string
  status?: GoalStatus | ''
  sort_by?: 'created_at' | 'updated_at' | 'target_date' | 'title' | 'status' | 'progress'
  sort_dir?: 'asc' | 'desc'
}
