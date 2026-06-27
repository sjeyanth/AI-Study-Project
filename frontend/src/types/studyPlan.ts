import type { StudyPlannerRequest, StudyPlannerResponse, StudySubjectRequest } from './ai'

export type CreateStudyPlanPayload = StudyPlannerRequest & {
  title?: string
}

export type StudyPlanSummary = {
  id: number
  title: string
  subject_count: number
  created_at: string
  updated_at: string
}

export type StudyPlan = StudyPlanSummary & {
  subjects_json: StudySubjectRequest[]
  weekly_plan_json: StudyPlannerResponse
  ai_reasoning: string
}
