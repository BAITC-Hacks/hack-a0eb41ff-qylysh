import { useI18n } from '../../i18n/i18n'
import type { Role } from '../../types'
import './MethodologyPage.scss'

const roleOrder: Role[] = ['coordinator', 'consolidator', 'distributor', 'transit', 'terminal', 'peripheral']

export default function MethodologyPage() {
  const { t } = useI18n()
  const m = t.methodology
  return <div className="methodology-page page-shell">
    <div className="page-shell__heading"><span className="page-shell__eyebrow">{m.eyebrow}</span><h1>{m.title}</h1><p>{m.subtitle}</p></div>
    <section className="methodology-page__note"><h2>{m.noteTitle}</h2><p>{m.noteText}</p></section>
    <section className="methodology-page__section"><h2>{m.rolesTitle}</h2><div className="methodology-page__roles">{roleOrder.map((role, index) => <article key={role} className={`methodology-page__role methodology-page__role--${index}`}><span>{String(index + 1).padStart(2, '0')}</span><div><h3>{t.roles[role]}</h3><p>{t.roleLong[role]}</p></div></article>)}</div></section>
    <section className="methodology-page__section methodology-page__scores"><h2>{m.scoresTitle}</h2><article><h3>{m.roleScoreTitle}</h3><p>{m.roleScoreText}</p></article><article><h3>{m.priorityTitle}</h3><p>{m.priorityText}</p></article></section>
    <section className="methodology-page__section"><h2>{m.workflowTitle}</h2><ol>{m.workflow.map((step) => <li key={step}>{step}</li>)}</ol></section>
  </div>
}
