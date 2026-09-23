import EmptyState from '../../components/common/EmptyState/EmptyState'
import './PriorityPage.scss'

export default function PriorityPage() {
  return (
    <div className="priority-page page-shell">
      <div className="page-shell__heading">
        <span className="page-shell__eyebrow">WORKSPACE / PRIORITY</span>
        <h1>Priority Nodes</h1>
        <p>Clients ranked for further analyst review.</p>
      </div>
      <div className="priority-page__placeholder">
        <EmptyState title="Priority nodes are coming" description="Client ranking will appear here when analysis data is connected." />
      </div>
    </div>
  )
}
