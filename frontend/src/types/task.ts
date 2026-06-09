export type Task = {
  id: number
  title: string
  description: string | null
  completed: boolean
}

export type TaskPayload = {
  title: string
  description: string | null
  completed: boolean
}
