export type Budget = {
  id: number
  month: number
  year: number
  total_budget: number
  currency: string
  created_at: string
  updated_at: string
}

export type BudgetPayload = {
  month: number
  year: number
  total_budget: number
  currency: string
}

export type BudgetQueryParams = {
  skip?: number
  limit?: number
  month?: number
  year?: number
  sort_by?: 'created_at' | 'month' | 'year'
  sort_dir?: 'asc' | 'desc'
}
