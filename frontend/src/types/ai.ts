export interface NoteSummaryRequest {
  content: string
}

export interface NoteSummaryResponse {
  summary: string
}

export interface EmailGenerationRequest {
  purpose: string
}

export interface EmailGenerationResponse {
  email: string
}

export interface TaskBreakdownRequest {
  goal: string
}

export interface TaskBreakdownResponse {
  tasks: string
}

export interface BudgetInsightsRequest {
  budget_summary: string
}

export interface BudgetInsightsResponse {
  insights: string
}
