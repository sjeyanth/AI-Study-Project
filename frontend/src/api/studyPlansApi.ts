import { apiClient } from './client'
import type {
  CreateStudyPlanPayload,
  StudyPlan,
  StudyPlanSummary,
} from '../types/studyPlan'

export async function createStudyPlan(payload: CreateStudyPlanPayload) {
  const response = await apiClient.post<StudyPlan>('/study-planner', payload)
  return response.data
}

export async function getStudyPlans() {
  const response = await apiClient.get<StudyPlanSummary[]>('/study-planner')
  return response.data
}

export async function getStudyPlan(studyPlanId: number) {
  const response = await apiClient.get<StudyPlan>(`/study-planner/${studyPlanId}`)
  return response.data
}

export async function deleteStudyPlan(studyPlanId: number) {
  await apiClient.delete(`/study-planner/${studyPlanId}`)
}
