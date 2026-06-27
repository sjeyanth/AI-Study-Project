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

export type DifficultyLevel = 'Easy' | 'Medium' | 'Hard'
export type StudySessionLength = 30 | 45 | 60 | 90
export type StudySessionType = 'study' | 'revision' | 'assignment' | 'break'

export interface StudySubjectRequest {
  name: string
  exam_date: string
  difficulty: DifficultyLevel
}

export interface AssignmentDeadlineRequest {
  title: string
  subject?: string
  due_date: string
}

export interface StudyPlannerRequest {
  subjects: StudySubjectRequest[]
  assignment_deadlines: AssignmentDeadlineRequest[]
  available_hours_per_day: number
  preferred_session_length: StudySessionLength
  notes?: string
}

export interface StudyScheduleItem {
  subject: string
  duration_minutes: number
  activity: string
  type: StudySessionType
}

export interface WeeklyStudyDay {
  day: string
  total_minutes: number
  sessions: StudyScheduleItem[]
}

export interface DailyStudyPlan {
  date: string
  focus: string
  sessions: StudyScheduleItem[]
}

export interface SubjectPriority {
  subject: string
  reason: string
  rank: number
}

export interface RecommendedStudyDuration {
  subject: string
  minutes_per_week: number
  reason: string
}

export interface RevisionItem {
  subject: string
  date: string
  focus: string
}

export interface StudyPlannerResponse {
  weekly_schedule: WeeklyStudyDay[]
  daily_plan: DailyStudyPlan[]
  priority_order: SubjectPriority[]
  recommended_study_duration: RecommendedStudyDuration[]
  revision_schedule: RevisionItem[]
  break_suggestions: string[]
  study_tips: string[]
  explanation: string
}
