import { useEffect, useMemo, useRef, useState, type FormEvent } from 'react'

type ChatRole = 'user' | 'assistant'

type ChatMessage = {
  id: number
  role: ChatRole
  content: string
}

function getAssistantReply(message: string) {
  const normalizedMessage = message.toLowerCase()

  if (normalizedMessage.includes('summarize') || normalizedMessage.includes('notes')) {
    return 'I can help summarize notes. Use the Note Summarizer tool below.'
  }

  if (normalizedMessage.includes('email')) {
    return 'I can help generate professional emails. Use the Email Generator tool below.'
  }

  if (normalizedMessage.includes('budget') || normalizedMessage.includes('spending')) {
    return 'I can help analyze spending. Use the Budget Insights tool below.'
  }

  if (normalizedMessage.includes('task') || normalizedMessage.includes('goal')) {
    return 'I can help break down work into steps. Use the Task Breakdown tool below.'
  }

  return 'I can help with note summaries, email drafts, task plans, and budget analysis. Pick a tool below to continue.'
}

export function AssistantChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const endOfMessagesRef = useRef<HTMLDivElement | null>(null)
  const nextMessageId = useRef(1)

  const hasMessages = messages.length > 0

  const quickPrompts = useMemo(
    () => ['Summarize my notes', 'Generate email', 'Analyze budget'],
    []
  )

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [messages, isLoading])

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const trimmedMessage = inputValue.trim()

    if (!trimmedMessage || isLoading) {
      return
    }

    const userMessage: ChatMessage = {
      id: nextMessageId.current++,
      role: 'user',
      content: trimmedMessage,
    }

    setMessages((current) => [...current, userMessage])
    setInputValue('')
    setIsLoading(true)

    await new Promise((resolve) => {
      window.setTimeout(resolve, 350)
    })

    const assistantMessage: ChatMessage = {
      id: nextMessageId.current++,
      role: 'assistant',
      content: getAssistantReply(trimmedMessage),
    }

    setMessages((current) => [...current, assistantMessage])
    setIsLoading(false)
  }

  function handleQuickPrompt(prompt: string) {
    setInputValue(prompt)
  }

  return (
    <article className="resource-card assistant-chat-card">
      <div className="assistant-chat-header">
        <div>
          <h2>Assistant Chat</h2>
          <p>Use chat for guidance, then run a tool below for the actual AI output.</p>
        </div>
      </div>

      <div className="assistant-chat-panel" aria-live="polite" aria-label="Assistant chat messages">
        {!hasMessages ? (
          <div className="assistant-empty-state">
            <strong>Start a conversation</strong>
            <p>Ask for help with summaries, emails, goals, or budget analysis.</p>
            <div className="assistant-quick-prompts">
              {quickPrompts.map((prompt) => (
                <button
                  key={prompt}
                  type="button"
                  className="assistant-quick-prompt"
                  onClick={() => handleQuickPrompt(prompt)}
                >
                  {prompt}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="assistant-message-list">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`assistant-message-row assistant-message-row-${message.role}`}
              >
                <div className={`assistant-message-bubble assistant-message-bubble-${message.role}`}>
                  {message.content}
                </div>
              </div>
            ))}
          </div>
        )}

        {isLoading ? <div className="assistant-loading">Thinking...</div> : null}
        <div ref={endOfMessagesRef} />
      </div>

      <form className="assistant-chat-form" onSubmit={handleSubmit}>
        <div className="field">
          <label htmlFor="assistant-chat-input">Message</label>
          <textarea
            id="assistant-chat-input"
            rows={3}
            value={inputValue}
            onChange={(event) => setInputValue(event.target.value)}
            placeholder="Ask for help with notes, email, goals, or budget..."
          />
        </div>

        <div className="form-actions">
          <button className="primary-button" type="submit" disabled={isLoading || !inputValue.trim()}>
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </form>
    </article>
  )
}