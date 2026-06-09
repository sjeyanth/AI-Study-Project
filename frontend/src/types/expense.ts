export type Expense = {
  id: number
  title: string
  amount: number
  category: string
  notes: string | null
  expense_date: string
  created_at: string
  updated_at: string
}

export type ExpensePayload = {
  title: string
  amount: number
  category: string
  notes: string | null
  expense_date: string
}

export type ExpenseQueryParams = {
  skip?: number
  limit?: number
  category?: string
  start_date?: string
  end_date?: string
  sort_by?: 'created_at' | 'expense_date' | 'amount'
  sort_dir?: 'asc' | 'desc'
  search?: string
}
