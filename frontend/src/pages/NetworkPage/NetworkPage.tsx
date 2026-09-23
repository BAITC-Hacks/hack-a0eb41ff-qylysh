import { GitBranch } from 'lucide-react'
import { useSearchParams } from 'react-router-dom'
import './NetworkPage.scss'

export default function NetworkPage() {
  const [searchParams] = useSearchParams()
  const gid = searchParams.get('gid')

  return (
    <div className="network-page page-shell">
      <div className="page-shell__heading">
        <span className="page-shell__eyebrow">WORKSPACE / NETWORK</span>
        <h1>Network Analysis</h1>
        <p>Explore client connections in the observed transaction network.</p>
      </div>

      {gid && <div className="network-page__selected">Selected GID: <strong>{gid}</strong></div>}

      <section className="network-page__workspace" aria-labelledby="network-workspace-title">
        <div className="network-page__workspace-top">
          <h2 id="network-workspace-title">Network Workspace</h2>
          <span>GRAPH VIEW</span>
        </div>
        <div className="network-page__workspace-empty">
          <span className="network-page__workspace-icon"><GitBranch size={26} strokeWidth={1.4} aria-hidden="true" /></span>
          <strong>Network workspace</strong>
          <p>Interactive network analysis will appear here.</p>
        </div>
        {/* Cytoscape.js will render the interactive graph in this workspace in a later chapter. */}
      </section>
    </div>
  )
}
