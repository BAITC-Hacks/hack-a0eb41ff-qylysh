import { Inbox } from 'lucide-react'
import './EmptyState.scss'

type EmptyStateProps = {
  title: string
  description: string
}

export default function EmptyState({ title, description }: EmptyStateProps) {
  return (
    <div className="empty-state">
      <span className="empty-state__icon"><Inbox size={22} strokeWidth={1.5} aria-hidden="true" /></span>
      <h2>{title}</h2>
      <p>{description}</p>
    </div>
  )
}
