import { useState, type FormEvent } from 'react'

import { generateEmail } from '../../api/aiApi'

export function EmailGenerator() {
  const [purpose, setPurpose] = useState('')
  const [email, setEmail] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleGenerate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      const data = await generateEmail(purpose)
      setEmail(data.email)
    } catch {
      setError('Unable to generate this email.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <article className="resource-card ai-tool-card">
      <div>
        <h2>Email Generator</h2>
        <p>Draft professional emails from a short prompt.</p>
      </div>

      <form className="ai-tool-form" onSubmit={handleGenerate}>
        <div className="field">
          <label htmlFor="email-generator-purpose">Email purpose</label>
          <input
            id="email-generator-purpose"
            type="text"
            value={purpose}
            onChange={(event) => setPurpose(event.target.value)}
            placeholder="Email purpose"
            required
          />
        </div>

        <div className="form-actions">
          <button className="primary-button" type="submit" disabled={isLoading}>
            {isLoading ? 'Generating...' : 'Generate Email'}
          </button>
        </div>
      </form>

      {error ? <div className="error-message">{error}</div> : null}

      <section className="ai-result-panel" aria-live="polite">
        <h3>Email</h3>
        {email ? (
          <pre className="ai-preformatted">{email}</pre>
        ) : (
          <p className="ai-empty-copy">Your generated email will appear here.</p>
        )}
      </section>
    </article>
  )
}