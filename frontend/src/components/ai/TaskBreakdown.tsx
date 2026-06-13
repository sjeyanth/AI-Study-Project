import { useState, type FormEvent } from 'react'

import { taskBreakdown } from '../../api/aiApi'

export function TaskBreakdown() {
  const [goal, setGoal] = useState('')
  const [tasks, setTasks] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleBreakdown(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      const data = await taskBreakdown(goal)
      setTasks(data.tasks)
    } catch {
      setError('Unable to generate the task breakdown.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <article className="resource-card ai-tool-card">
      <div>
        <h2>Task Breakdown</h2>
        <p>Turn a goal into a practical step-by-step plan.</p>
      </div>

      <form className="ai-tool-form" onSubmit={handleBreakdown}>
        <div className="field">
          <label htmlFor="task-breakdown-goal">Goal</label>
          <input
            id="task-breakdown-goal"
            type="text"
            value={goal}
            onChange={(event) => setGoal(event.target.value)}
            placeholder="Enter goal"
            required
          />
        </div>

        <div className="form-actions">
          <button className="primary-button" type="submit" disabled={isLoading}>
            {isLoading ? 'Generating...' : 'Generate Tasks'}
          </button>
        </div>
      </form>

      {error ? <div className="error-message">{error}</div> : null}

      <section className="ai-result-panel" aria-live="polite">
        <h3>Tasks</h3>
        {tasks.length > 0 ? (
          <ul className="ai-list">
            {tasks.map((task, index) => (
              <li key={`${task}-${index}`}>{task}</li>
            ))}
          </ul>
        ) : (
          <p className="ai-empty-copy">Your generated steps will appear here.</p>
        )}
      </section>
    </article>
  )
}