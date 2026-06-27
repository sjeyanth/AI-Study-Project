import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import {
  deleteStudyPlan,
  getStudyPlan,
  getStudyPlans,
} from '../api/studyPlansApi'
import { EmptyState } from '../components/EmptyState'
import { PageState } from '../components/PageState'
import { StudyPlanResults } from './StudyPlanner'
import type { StudyPlan, StudyPlanSummary } from '../types/studyPlan'

function formatDate(value: string) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
  }).format(new Date(value))
}

export function StudyPlans() {
  const [plans, setPlans] = useState<StudyPlanSummary[]>([])
  const [selectedPlan, setSelectedPlan] = useState<StudyPlan | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isOpening, setIsOpening] = useState(false)
  const [error, setError] = useState('')

  async function loadPlans() {
    setIsLoading(true)
    setError('')

    try {
      const data = await getStudyPlans()
      setPlans(data)
    } catch {
      setError('Unable to load study plans.')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    let isMounted = true

    async function loadCurrentPlans() {
      setIsLoading(true)
      setError('')

      try {
        const data = await getStudyPlans()

        if (isMounted) {
          setPlans(data)
        }
      } catch {
        if (isMounted) {
          setError('Unable to load study plans.')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    loadCurrentPlans()

    return () => {
      isMounted = false
    }
  }, [])

  async function handleOpen(studyPlanId: number) {
    setIsOpening(true)
    setError('')

    try {
      const data = await getStudyPlan(studyPlanId)
      setSelectedPlan(data)
    } catch {
      setError('Unable to open this study plan.')
    } finally {
      setIsOpening(false)
    }
  }

  async function handleDelete(studyPlanId: number) {
    setError('')

    try {
      await deleteStudyPlan(studyPlanId)

      if (selectedPlan?.id === studyPlanId) {
        setSelectedPlan(null)
      }

      await loadPlans()
    } catch {
      setError('Unable to delete this study plan.')
    }
  }

  return (
    <>
      <div className="page-header study-planner-header">
        <div>
          <h1>Study Plans</h1>
          <p>Open saved AI-generated study plans from your account.</p>
        </div>
        <Link className="primary-button study-header-button" to="/study-planner">
          Generate Plan
        </Link>
      </div>

      {error ? <PageState message={error} tone="error" /> : null}

      <section className="study-plans-layout">
        <div className="resource-list" aria-label="Saved study plans">
          {isLoading ? <PageState message="Loading study plans..." /> : null}
          {!isLoading && plans.length === 0 ? (
            <EmptyState
              title="No study plans found"
              description="Generate a study plan to save it to your account."
            />
          ) : null}

          {!isLoading
            ? plans.map((plan) => (
                <article className="resource-card" key={plan.id}>
                  <div className="resource-card-main">
                    <div>
                      <h2>{plan.title}</h2>
                      <p>{plan.subject_count} subjects</p>
                    </div>
                    <span className="status-pill">Created {formatDate(plan.created_at)}</span>
                  </div>

                  <div className="resource-actions">
                    <button
                      className="ghost-button"
                      type="button"
                      disabled={isOpening}
                      onClick={() => handleOpen(plan.id)}
                    >
                      Open
                    </button>
                    <button
                      className="danger-button"
                      type="button"
                      onClick={() => handleDelete(plan.id)}
                    >
                      Delete
                    </button>
                  </div>
                </article>
              ))
            : null}
        </div>

        <div className="study-results">
          {selectedPlan ? (
            <>
              <article className="resource-card">
                <h2>{selectedPlan.title}</h2>
                <p>Created {formatDate(selectedPlan.created_at)}</p>
              </article>
              <StudyPlanResults plan={selectedPlan.weekly_plan_json} />
            </>
          ) : (
            <EmptyState
              title="No plan selected"
              description="Open a saved study plan to view the full weekly schedule."
            />
          )}
        </div>
      </section>
    </>
  )
}
