import { CircleAlert } from 'lucide-react'
import './ErrorState.scss'

type ErrorStateProps = {
  title: string
  message: string
}

export default function ErrorState({ title, message }: ErrorStateProps) {
  return (
    <div className="error-state" role="alert">
      <CircleAlert size={20} strokeWidth={1.8} aria-hidden="true" />
      <div><h2>{title}</h2><p>{message}</p></div>
    </div>
  )
}
