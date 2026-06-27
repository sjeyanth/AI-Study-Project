import { apiClient } from './client'


import type {
  BudgetInsightsResponse,
  EmailGenerationResponse,
  TaskBreakdownResponse,
  NoteSummaryResponse
} from '../types/ai'

export const summarizeNote = async (
  content: string
): Promise<NoteSummaryResponse> => {
  const response = await apiClient.post(
    '/ai/summarize-note',
    {
      content,
    }
  )

  return response.data
}

export const generateEmail = async (
  purpose: string
): Promise<EmailGenerationResponse> => {
  const response = await apiClient.post(
    '/ai/generate-mail',
    {
      purpose,
    }
  )

  return response.data
}

export const taskBreakdown = async (
  goal: string
): Promise<TaskBreakdownResponse> => {
  const response = await apiClient.post(
    '/ai/task-breakdown',
    {
      goal,
    }
  )

  return response.data
}

export const budgetInsights = async (
  budgetSummary: string
): Promise<BudgetInsightsResponse> => {
  const response = await apiClient.post(
    '/ai/budget-insights',
    {
      budget_summary: budgetSummary,
    }
  )

  return response.data
}
