import { Activity, ChartNoAxesCombined, CircleHelp, GitBranch, Layers3, ShieldAlert } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'
import { NavLink } from 'react-router-dom'
import './Sidebar.scss'

type NavItem = {
  label: string
  to: string
  icon: LucideIcon
}

const primaryItems: NavItem[] = [
  { label: 'Overview', to: '/dashboard', icon: ChartNoAxesCombined },
  { label: 'Network', to: '/network', icon: GitBranch },
  { label: 'Priority', to: '/priority', icon: ShieldAlert },
  { label: 'Clusters', to: '/clusters', icon: Layers3 },
]

const secondaryItems: NavItem[] = [
  { label: 'Methodology', to: '/methodology', icon: CircleHelp },
  { label: 'Data limitations', to: '/data-limitations', icon: Activity },
]

function NavigationGroup({ items, label }: { items: NavItem[]; label: string }) {
  return (
    <nav className="sidebar__nav" aria-label={label}>
      {items.map(({ label: itemLabel, to, icon: Icon }) => (
        <NavLink
          key={to}
          to={to}
          className={({ isActive }) => `sidebar__link${isActive ? ' sidebar__link--active' : ''}`}
          title={itemLabel}
        >
          <Icon size={18} strokeWidth={1.8} aria-hidden="true" />
          <span>{itemLabel}</span>
        </NavLink>
      ))}
    </nav>
  )
}

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar__brand" aria-label="MoneyGraph, AML Network Analysis">
        <span className="sidebar__mark" aria-hidden="true"><GitBranch size={21} strokeWidth={2.2} /></span>
        <span className="sidebar__brand-copy">
          <strong>MoneyGraph</strong>
          <small>AML Network Analysis</small>
        </span>
      </div>

      <div className="sidebar__section">
        <p className="sidebar__caption">WORKSPACE</p>
        <NavigationGroup items={primaryItems} label="Main navigation" />
      </div>

      <div className="sidebar__section sidebar__section--secondary">
        <p className="sidebar__caption">REFERENCE</p>
        <NavigationGroup items={secondaryItems} label="Reference navigation" />
      </div>

      <div className="sidebar__footer">
        <span className="sidebar__status-dot" aria-hidden="true" />
        <span>Analysis workspace</span>
      </div>
    </aside>
  )
}
