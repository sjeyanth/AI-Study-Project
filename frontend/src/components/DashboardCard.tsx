type DashboardCardProps = {
  label: string
  value: string | number
  helperText?: string
}

export function DashboardCard({ label, value, helperText }: DashboardCardProps) {
  return (
    <article className="dashboard-card">
      <span>{label}</span>
      <strong>{value}</strong>
      {helperText ? <small>{helperText}</small> : null}
    </article>
  )
}
