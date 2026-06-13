import { useState, type FormEvent } from 'react'

import { summarizeNote } from '../../api/aiApi'

export function NoteSummarizer() {
  const [content, setContent] = useState('')
  const [summary, setSummary] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSummarize(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      const data = await summarizeNote(content)
      setSummary(data.summary)
    } catch {
      setError('Unable to summarize this note.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <article className="resource-card ai-tool-card">
      <div>
        <h2>Note Summarizer</h2>
        <p>Condense long notes into concise summaries.</p>
      </div>

      <form className="ai-tool-form" onSubmit={handleSummarize}>
        <div className="field">
          <label htmlFor="note-summarizer-content">Note content</label>
          <textarea
            id="note-summarizer-content"
            rows={8}
            value={content}
            onChange={(event) => setContent(event.target.value)}
            placeholder="Paste your note..."
            required
          />
        </div>

        <div className="form-actions">
          <button className="primary-button" type="submit" disabled={isLoading}>
            {isLoading ? 'Summarizing...' : 'Summarize'}
          </button>
        </div>
      </form>

      {error ? <div className="error-message">{error}</div> : null}

      <section className="ai-result-panel" aria-live="polite">
        <h3>Summary</h3>
        {summary ? <p>{summary}</p> : <p className="ai-empty-copy">Your summary will appear here.</p>}
      </section>
    </article>
  )
}