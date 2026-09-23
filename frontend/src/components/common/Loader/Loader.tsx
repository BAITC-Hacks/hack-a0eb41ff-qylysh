import { useI18n } from '../../../i18n/i18n'
import './Loader.scss'

export default function Loader() {
  const { t } = useI18n()
  return (
    <div className="loader" role="status" aria-live="polite">
      <span className="loader__spinner" aria-hidden="true" />
      <span>{t.common.loading}</span>
    </div>
  )
}
