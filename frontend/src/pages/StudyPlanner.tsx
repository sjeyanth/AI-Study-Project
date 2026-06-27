import { useMemo, useState, type FormEvent } from 'react'

import { generateStudyPlan } from '../api/aiApi'
import { EmptyState } from '../components/EmptyState'
import type {
  AssignmentDeadlineRequest,
  DifficultyLevel,
  StudyPlannerResponse,
  StudySessionLength,
  StudySubjectRequest,
} from '../types/ai'

const sessionLengths: StudySessionLength[] = [30, 45, 60, 90]
const difficultyLevels: DifficultyLevel[] = ['Easy', 'Medium', 'Hard']

const createSubject = (): StudySubjectRequest => ({
  name: '',
  exam_date: '',
  difficulty: 'Medium',
})

const createDeadline = (): AssignmentDeadlineRequest => ({
  title: '',
  subject: '',
  due_date: '',
})

const todayInputValue = new Date().toISOString().slice(0, 10)

export function StudyPlanner() {
  const [subjects, setSubjects] = useState<StudySubjectRequest[]>([createSubject()])
  const [deadlines, setDeadlines] = useState<AssignmentDeadlineRequest[]>([])
  const [availableHours, setAvailableHours] = useState(2)
  const [sessionLength, setSessionLength] = useState<StudySessionLength>(60)
  const [notes, setNotes] = useState('')
  const [plan, setPlan] = useState<StudyPlannerResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const subjectNames = useMemo(
    () => subjects.map((subject) => subject.name.trim()).filter(Boolean),
    [subjects]
  )

  function updateSubject(index: number, field: keyof StudySubjectRequest, value: string) {
    setSubjects((currentSubjects) =>
      currentSubjects.map((subject, subjectIndex) =>
        subjectIndex === index
          ? {
              ...subject,
              [field]: value,
            }
          : subject
      )
    )
  }

  function updateDeadline(index: number, field: keyof AssignmentDeadlineRequest, value: string) {
    setDeadlines((currentDeadlines) =>
      currentDeadlines.map((deadline, deadlineIndex) =>
        deadlineIndex === index
          ? {
              ...deadline,
              [field]: value,
            }
          : deadline
      )
    )
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      const cleanedDeadlines = deadlines.filter(
        (deadline) => deadline.title.trim() && deadline.due_date
      )
      const data = await generateStudyPlan({
        subjects,
        assignment_deadlines: cleanedDeadlines,
        available_hours_per_day: availableHours,
        preferred_session_length: sessionLength,
        notes: notes.trim() || undefined,
      })

      setPlan(data)
    } catch {
      setError('Unable to generate a study plan. Check your inputs and try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      <div className="page-header study-planner-header">
        <div>
          <h1>Study Planner</h1>
          <p>Build a balanced AI-generated schedule around exams, deadlines, and study time.</p>
        </div>
      </div>

      <section className="study-planner-layout">
        <form className="resource-form study-planner-form" onSubmit={handleSubmit}>
          <div>
            <h2>Planning inputs</h2>
            <p>Subjects, dates, study capacity, and preferences.</p>
          </div>

          <section className="study-form-section">
            <div className="section-heading">
              <h3>Subjects</h3>
              <button
                className="ghost-button"
                type="button"
                onClick={() => setSubjects((currentSubjects) => [...currentSubjects, createSubject()])}
              >
                Add Subject
              </button>
            </div>

            <div className="study-dynamic-list">
              {subjects.map((subject, index) => (
                <div className="study-input-group" key={`subject-${index}`}>
                  <div className="field">
                    <label htmlFor={`subject-name-${index}`}>Subject</label>
                    <input
                      id={`subject-name-${index}`}
                      type="text"
                      value={subject.name}
                      onChange={(event) => updateSubject(index, 'name', event.target.value)}
                      placeholder="Database Systems"
                      required
                    />
                  </div>

                  <div className="form-grid">
                    <div className="field">
                      <label htmlFor={`exam-date-${index}`}>Exam date</label>
                      <input
                        id={`exam-date-${index}`}
                        type="date"
                        min={todayInputValue}
                        value={subject.exam_date}
                        onChange={(event) => updateSubject(index, 'exam_date', event.target.value)}
                        required
                      />
                    </div>

                    <div className="field">
                      <label htmlFor={`difficulty-${index}`}>Difficulty</label>
                      <select
                        id={`difficulty-${index}`}
                        value={subject.difficulty}
                        onChange={(event) =>
                          updateSubject(index, 'difficulty', event.target.value as DifficultyLevel)
                        }
                      >
                        {difficultyLevels.map((difficulty) => (
                          <option key={difficulty} value={difficulty}>
                            {difficulty}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>

                  {subjects.length > 1 ? (
                    <button
                      className="danger-button"
                      type="button"
                      onClick={() =>
                        setSubjects((currentSubjects) =>
                          currentSubjects.filter((_, subjectIndex) => subjectIndex !== index)
                        )
                      }
                    >
                      Remove
                    </button>
                  ) : null}
                </div>
              ))}
            </div>
          </section>

          <section className="study-form-section">
            <div className="section-heading">
              <h3>Assignments</h3>
              <button
                className="ghost-button"
                type="button"
                onClick={() => setDeadlines((currentDeadlines) => [...currentDeadlines, createDeadline()])}
              >
                Add Deadline
              </button>
            </div>

            {deadlines.length ? (
              <div className="study-dynamic-list">
                {deadlines.map((deadline, index) => (
                  <div className="study-input-group" key={`deadline-${index}`}>
                    <div className="field">
                      <label htmlFor={`deadline-title-${index}`}>Assignment</label>
                      <input
                        id={`deadline-title-${index}`}
                        type="text"
                        value={deadline.title}
                        onChange={(event) => updateDeadline(index, 'title', event.target.value)}
                        placeholder="Research report"
                      />
                    </div>

                    <div className="form-grid">
                      <div className="field">
                        <label htmlFor={`deadline-subject-${index}`}>Subject</label>
                        <select
                          id={`deadline-subject-${index}`}
                          value={deadline.subject}
                          onChange={(event) => updateDeadline(index, 'subject', event.target.value)}
                        >
                          <option value="">Unassigned</option>
                          {subjectNames.map((subjectName) => (
                            <option key={subjectName} value={subjectName}>
                              {subjectName}
                            </option>
                          ))}
                        </select>
                      </div>

                      <div className="field">
                        <label htmlFor={`deadline-date-${index}`}>Due date</label>
                        <input
                          id={`deadline-date-${index}`}
                          type="date"
                          min={todayInputValue}
                          value={deadline.due_date}
                          onChange={(event) => updateDeadline(index, 'due_date', event.target.value)}
                        />
                      </div>
                    </div>

                    <button
                      className="danger-button"
                      type="button"
                      onClick={() =>
                        setDeadlines((currentDeadlines) =>
                          currentDeadlines.filter((_, deadlineIndex) => deadlineIndex !== index)
                        )
                      }
                    >
                      Remove
                    </button>
                  </div>
                ))}
              </div>
            ) : (
              <p className="ai-empty-copy">No assignment deadlines added.</p>
            )}
          </section>

          <div className="form-grid">
            <div className="field">
              <label htmlFor="available-hours">Hours per day</label>
              <input
                id="available-hours"
                type="number"
                min="0.5"
                max="16"
                step="0.5"
                value={availableHours}
                onChange={(event) => setAvailableHours(Number(event.target.value))}
                required
              />
            </div>

            <div className="field">
              <label htmlFor="session-length">Session length</label>
              <select
                id="session-length"
                value={sessionLength}
                onChange={(event) => setSessionLength(Number(event.target.value) as StudySessionLength)}
              >
                {sessionLengths.map((length) => (
                  <option key={length} value={length}>
                    {length} minutes
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="field">
            <label htmlFor="study-notes">Notes</label>
            <textarea
              id="study-notes"
              rows={4}
              value={notes}
              onChange={(event) => setNotes(event.target.value)}
              placeholder="Topics to emphasize, weak areas, preferred study days..."
            />
          </div>

          {error ? <div className="error-message">{error}</div> : null}

          <button className="primary-button" type="submit" disabled={isLoading}>
            {isLoading ? 'Generating Plan...' : 'Generate Study Plan'}
          </button>
        </form>

        <div className="study-results">
          {isLoading ? (
            <section className="resource-state study-loading-state" aria-live="polite">
              <span className="loading-spinner" />
              Generating a balanced study plan...
            </section>
          ) : plan ? (
            <StudyPlanResults plan={plan} />
          ) : (
            <EmptyState
              title="No study plan yet"
              description="Add your subjects and availability to generate a personalized weekly schedule."
            />
          )}
        </div>
      </section>
    </>
  )
}

function StudyPlanResults({ plan }: { plan: StudyPlannerResponse }) {
  return (
    <div className="study-plan-stack">
      <section className="resource-card">
        <h2>Weekly overview</h2>
        <div className="weekly-schedule-grid">
          {plan.weekly_schedule.map((day) => (
            <article className="study-day-card" key={day.day}>
              <div className="study-day-card-header">
                <strong>{day.day}</strong>
                <span>{formatMinutes(day.total_minutes)}</span>
              </div>
              <div className="study-session-list">
                {day.sessions.map((session, index) => (
                  <StudySessionPill session={session} key={`${day.day}-${index}`} />
                ))}
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="resource-card">
        <h2>Daily timeline</h2>
        <div className="daily-timeline">
          {plan.daily_plan.map((day) => (
            <article className="timeline-day" key={day.date}>
              <div className="timeline-date">
                <strong>{formatDate(day.date)}</strong>
                <span>{day.focus}</span>
              </div>
              <div className="timeline-sessions">
                {day.sessions.map((session, index) => (
                  <div className="timeline-session" key={`${day.date}-${index}`}>
                    <span className={`session-type session-type-${session.type}`}>{session.type}</span>
                    <div>
                      <strong>{session.subject}</strong>
                      <p>{session.activity}</p>
                    </div>
                    <span>{formatMinutes(session.duration_minutes)}</span>
                  </div>
                ))}
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="study-result-grid">
        <article className="resource-card">
          <h2>Priority order</h2>
          <ol className="study-priority-list">
            {plan.priority_order.map((priority) => (
              <li key={`${priority.rank}-${priority.subject}`}>
                <strong>{priority.subject}</strong>
                <p>{priority.reason}</p>
              </li>
            ))}
          </ol>
        </article>

        <article className="resource-card">
          <h2>Recommended duration</h2>
          <div className="study-duration-list">
            {plan.recommended_study_duration.map((duration) => (
              <div className="duration-row" key={duration.subject}>
                <strong>{duration.subject}</strong>
                <span>{formatMinutes(duration.minutes_per_week)} / week</span>
                <p>{duration.reason}</p>
              </div>
            ))}
          </div>
        </article>
      </section>

      <section className="study-result-grid">
        <article className="resource-card">
          <h2>Revision schedule</h2>
          <div className="revision-list">
            {plan.revision_schedule.map((revision) => (
              <div className="revision-row" key={`${revision.subject}-${revision.date}`}>
                <strong>{formatDate(revision.date)}</strong>
                <span>{revision.subject}</span>
                <p>{revision.focus}</p>
              </div>
            ))}
          </div>
        </article>

        <article className="resource-card">
          <h2>Breaks and tips</h2>
          <ul className="ai-list">
            {[...plan.break_suggestions, ...plan.study_tips].map((tip) => (
              <li key={tip}>{tip}</li>
            ))}
          </ul>
        </article>
      </section>

      <section className="resource-card study-explanation-card">
        <h2>AI explanation</h2>
        <p>{plan.explanation}</p>
      </section>
    </div>
  )
}

function StudySessionPill({ session }: { session: { subject: string; duration_minutes: number; activity: string; type: string } }) {
  return (
    <div className={`study-session-pill session-type-${session.type}`}>
      <strong>{session.subject}</strong>
      <span>{formatMinutes(session.duration_minutes)}</span>
      <p>{session.activity}</p>
    </div>
  )
}

function formatMinutes(minutes: number) {
  if (minutes < 60) {
    return `${minutes} min`
  }

  const hours = Math.floor(minutes / 60)
  const remainingMinutes = minutes % 60

  return remainingMinutes ? `${hours}h ${remainingMinutes}m` : `${hours}h`
}

function formatDate(value: string) {
  const date = new Date(`${value}T00:00:00`)

  if (Number.isNaN(date.getTime())) {
    return value
  }

  return new Intl.DateTimeFormat(undefined, {
    month: 'short',
    day: 'numeric',
  }).format(date)
}
