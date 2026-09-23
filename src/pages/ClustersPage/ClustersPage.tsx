import EmptyState from '../../components/common/EmptyState/EmptyState'
import './ClustersPage.scss'

export default function ClustersPage() {
  return (
    <div className="clusters-page page-shell">
      <div className="page-shell__heading">
        <span className="page-shell__eyebrow">WORKSPACE / CLUSTERS</span>
        <h1>Clusters</h1>
        <p>Detected communities and connected financial structures.</p>
      </div>
      <div className="clusters-page__placeholder">
        <EmptyState title="Cluster analysis is coming" description="Detected communities will appear here when analysis data is connected." />
      </div>
    </div>
  )
}
