import { useEffect, useMemo, useRef, useState, type FormEvent } from 'react'

import { sendMessage } from '../../api/assistantApi'

type ChatRole = 'user' | 'assistant'

type ChatMessage = {
  id: number
  role: ChatRole
  content: string
  timestamp: string
}

export function AssistantChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const endOfMessagesRef = useRef<HTMLDivElement | null>(null)
  const nextMessageId = useRef(1)

  const hasMessages = messages.length > 0

  const quickPrompts = useMemo(
    () => [
      'Summarize my notes',
      'Generate email',
      'Analyze budget',
      'Help me plan my goal',
    ],
    []
  )

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({
      behavior: 'smooth',
      block: 'end',
    })
  }, [messages, isLoading])

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault()

    const trimmedMessage =
      inputValue.trim()

    if (
      !trimmedMessage ||
      isLoading
    ) {
      return
    }

    const userMessage: ChatMessage = {
      id: nextMessageId.current++,
      role: 'user',
      content: trimmedMessage,
      timestamp: new Date().toISOString(),
    }

    setMessages((current) => [
      ...current,
      userMessage,
    ])

    setInputValue('')

    try {
      setIsLoading(true)

      const data =
        await sendMessage(
          trimmedMessage
        )

      const assistantMessage: ChatMessage =
        {
          id:
            nextMessageId.current++,
          role: 'assistant',
          content:
            data.response,
          timestamp: new Date().toISOString(),
        }

      setMessages((current) => [
        ...current,
        assistantMessage,
      ])
    } catch (error) {
      console.error(error)

      const errorMessage: ChatMessage =
        {
          id:
            nextMessageId.current++,
          role: 'assistant',
          content:
            'Unable to connect to assistant.',
          timestamp: new Date().toISOString(),
        }

      setMessages((current) => [
        ...current,
        errorMessage,
      ])
    } finally {
      setIsLoading(false)
    }
  }

  function handleQuickPrompt(
    prompt: string
  ) {
    setInputValue(prompt)
  }

  async function copyMessage(
  content: string
) {
  await navigator.clipboard.writeText(
    content
  )
}

  function clearConversation() {
  setMessages([])
}

  return (
    <article className="resource-card assistant-chat-card">
      <div className="assistant-chat-header">
        <div>
          <h2>
            Assistant Chat
          </h2>

          <p>
            Ask questions about
            notes, emails,
            tasks, goals, or
            budgets.
          </p>
        </div>
      </div>

      <div
        className="assistant-chat-panel"
        aria-live="polite"
        aria-label="Assistant chat messages"
      >
        {!hasMessages ? (
          <div className="assistant-empty-state">
            <strong>
              Start a conversation
            </strong>

            <p>
              Ask for help with
              summaries, emails,
              goals, or budget
              analysis.
            </p>

            <div className="assistant-quick-prompts">
              {quickPrompts.map(
                (prompt) => (
                  <button
                    key={prompt}
                    type="button"
                    className="assistant-quick-prompt"
                    onClick={() =>
                      handleQuickPrompt(
                        prompt
                      )
                    }
                  >
                    {prompt}
                  </button>
                )
              )}
            </div>
          </div>
        ) : (
          <div className="assistant-message-list">
            {messages.map(
              (message) => (
                <div
                  key={
                    message.id
                  }
                  className={`assistant-message-row assistant-message-row-${message.role}`}
                >
                  <div
                    className={`assistant-message-bubble assistant-message-bubble-${message.role}`}
                  >
                    {
                      message.content
                    }
                  </div>
                  {message.role === 'assistant' && (
                  <button
                    type="button"
                    onClick={() =>
                    copyMessage(message.content)
                    }
                    >
                      Copy
                  </button>
              )}
                  <small
                    style={{
                    display: 'block',
                    marginTop: '2px',
                    opacity: 0.7,
                  }}
                  >
                    {message.timestamp}
                  </small>
                </div>
              )
            )}
          </div>
        )}

        {isLoading ? (
          <div className="assistant-loading">
            Thinking...
          </div>
        ) : null}

        <div
          ref={
            endOfMessagesRef
          }
        />
      </div>

      <form
        className="assistant-chat-form"
        onSubmit={handleSubmit}
      >
        <div className="field">
          <label htmlFor="assistant-chat-input">
            Message
          </label>

          <textarea
            id="assistant-chat-input"
            rows={3}
            value={inputValue}
            onChange={(
              event
            ) =>
              setInputValue(
                event.target
                  .value
              )
            }
            placeholder="Ask for help with notes, email, goals, or budget..."
          />
        </div>

        <div className="form-actions">
          <button
            className="primary-button"
            type="submit"
            disabled={
              isLoading ||
              !inputValue.trim()
            }
          >
            {isLoading
              ? 'Sending...'
              : 'Send'}
          </button>
          <button
            type="button"
            onClick={clearConversation}
          >
            Clear Chat
          </button>
        </div>
      </form>
    </article>
  )
}