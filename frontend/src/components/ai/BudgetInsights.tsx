import { useState, type FormEvent } from 'react'

import { budgetInsights } from '../../api/aiApi'

export function BudgetInsights() {
  const [budgetSummary, setBudgetSummary] = useState('')
  const [insights, setInsights] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleAnalyze(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      const data = await budgetInsights(budgetSummary)
      setInsights(data.insights)
    } catch {
      setError('Unable to analyze this budget summary.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <article className="resource-card ai-tool-card">
      <div>
        <h2>Budget Insights</h2>
        <p>Review spending notes and surface useful observations.</p>
      </div>

      <form className="ai-tool-form" onSubmit={handleAnalyze}>
        <div className="field">
          <label htmlFor="budget-insights-summary">Budget summary</label>
          <textarea
            id="budget-insights-summary"
            rows={6}
            value={budgetSummary}
            onChange={(event) => setBudgetSummary(event.target.value)}
            placeholder="Budget summary..."
            required
          />
        </div>

        <div className="form-actions">
          <button className="primary-button" type="submit" disabled={isLoading}>
            {isLoading ? 'Analyzing...' : 'Analyze Budget'}
          </button>
        </div>
      </form>

      {error ? <div className="error-message">{error}</div> : null}

      <section className="ai-result-panel" aria-live="polite">
        <h3>Insights</h3>
        {insights ? <p>{insights}</p> : <p className="ai-empty-copy">Your insights will appear here.</p>}
      </section>
    </article>
  )
}