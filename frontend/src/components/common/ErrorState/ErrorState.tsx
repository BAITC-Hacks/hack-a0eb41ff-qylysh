import { CircleAlert } from 'lucide-react'
import { useI18n } from '../../../i18n/i18n'
import './ErrorState.scss'

type ErrorStateProps = {
  title: string
  message: string
  onRetry?: () => void
}

export default function ErrorState({ title, message, onRetry }: ErrorStateProps) {
  const { t } = useI18n()
  return (
    <div className="error-state" role="alert">
      <CircleAlert size={20} strokeWidth={1.8} aria-hidden="true" />
      <div><h2>{title}</h2><p>{message}</p>{onRetry && <button type="button" onClick={onRetry}>{t.common.tryAgain}</button>}</div>
    </div>
  )
}
