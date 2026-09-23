import './StatCard.scss'

type StatCardProps = {
  label: string
  value: string | number
  description?: string
}

export default function StatCard({ label, value, description }: StatCardProps) {
  return (
    <div className="stat-card">
      <span className="stat-card__label">{label}</span>
      <strong className="stat-card__value">{value}</strong>
      {description && <span className="stat-card__description">{description}</span>}
    </div>
  )
}
