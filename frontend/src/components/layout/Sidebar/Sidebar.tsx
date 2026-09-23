import { Activity, ChartNoAxesCombined, CircleHelp, GitBranch, Layers3, ShieldAlert } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'
import { NavLink } from 'react-router-dom'
import { useI18n } from '../../../i18n/i18n'
import type { Dictionary } from '../../../i18n/translations'
import './Sidebar.scss'

type NavItem = {
  label: keyof Dictionary['sidebar']
  to: string
  icon: LucideIcon
}

const primaryItems: NavItem[] = [
  { label: 'overview', to: '/dashboard', icon: ChartNoAxesCombined },
  { label: 'network', to: '/network', icon: GitBranch },
  { label: 'priority', to: '/priority', icon: ShieldAlert },
  { label: 'clusters', to: '/clusters', icon: Layers3 },
]

const secondaryItems: NavItem[] = [
  { label: 'methodology', to: '/methodology', icon: CircleHelp },
  { label: 'dataLimitations', to: '/data-limitations', icon: Activity },
]

function NavigationGroup({ items, label }: { items: NavItem[]; label: string }) {
  const { t } = useI18n()
  return (
    <nav className="sidebar__nav" aria-label={label}>
      {items.map(({ label: key, to, icon: Icon }) => { const itemLabel = t.sidebar[key]; return (
        <NavLink
          key={to}
          to={to}
          className={({ isActive }) => `sidebar__link${isActive ? ' sidebar__link--active' : ''}`}
          title={itemLabel}
        >
          <Icon size={18} strokeWidth={1.8} aria-hidden="true" />
          <span>{itemLabel}</span>
        </NavLink>
      ) })}
    </nav>
  )
}

export default function Sidebar() {
  const { t } = useI18n()
  return (
    <aside className="sidebar">
      <div className="sidebar__brand" aria-label={t.sidebar.brandAria}>
        <span className="sidebar__mark" aria-hidden="true"><GitBranch size={21} strokeWidth={2.2} /></span>
        <span className="sidebar__brand-copy">
          <strong>MoneyGraph</strong>
          <small>{t.sidebar.brandSubtitle}</small>
        </span>
      </div>

      <div className="sidebar__section">
        <p className="sidebar__caption">{t.sidebar.workspace}</p>
        <NavigationGroup items={primaryItems} label={t.sidebar.mainNav} />
      </div>

      <div className="sidebar__section sidebar__section--secondary">
        <p className="sidebar__caption">{t.sidebar.reference}</p>
        <NavigationGroup items={secondaryItems} label={t.sidebar.referenceNav} />
      </div>

      <div className="sidebar__footer">
        <span className="sidebar__status-dot" aria-hidden="true" />
        <span>{t.sidebar.footer}</span>
      </div>
    </aside>
  )
}
