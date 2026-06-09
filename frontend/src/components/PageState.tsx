type PageStateProps = {
  message: string
  tone?: 'neutral' | 'error'
}

export function PageState({ message, tone = 'neutral' }: PageStateProps) {
  return (
    <section
      className={tone === 'error' ? 'resource-state resource-state-error' : 'resource-state'}
      role={tone === 'error' ? 'alert' : undefined}
    >
      {message}
    </section>
  )
}
