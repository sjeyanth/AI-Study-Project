export type Note = {
  id: number
  title: string
  content: string
  tags: string | null
  created_at: string
  updated_at: string
}

export type NotePayload = {
  title: string
  content: string
  tags: string | null
}

export type NoteQueryParams = {
  skip?: number
  limit?: number
  search?: string
  sort_by?: 'created_at' | 'updated_at' | 'title'
  sort_dir?: 'asc' | 'desc'
}
