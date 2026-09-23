import { useI18n } from '../../i18n/i18n'
import './DataLimitationsPage.scss'

export default function DataLimitationsPage() {
  const { t } = useI18n()
  const l = t.limitations
  return <div className="data-limitations-page page-shell">
    <div className="page-shell__heading"><span className="page-shell__eyebrow">{l.eyebrow}</span><h1>{l.title}</h1><p>{l.subtitle}</p></div>
    <div className="data-limitations-page__callout"><strong>{l.calloutTitle}</strong><p>{l.calloutText}</p></div>
    <div className="data-limitations-page__grid">{l.items.map(([title, text], index) => <article key={index}><span>{String(index + 1).padStart(2, '0')}</span><h2>{title}</h2><p>{text}</p></article>)}</div>
  </div>
}
