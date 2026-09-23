import StatCard from '../../components/common/StatCard/StatCard'
import Loader from '../../components/common/Loader/Loader'
import ErrorState from '../../components/common/ErrorState/ErrorState'
import EmptyState from '../../components/common/EmptyState/EmptyState'
import { Link } from 'react-router-dom'
import { getSummary, isMockMode } from '../../api/services'
import { useAsyncResource } from '../../hooks/useAsyncResource'
import { formatKzt, formatNumber, formatRole, formatScore } from '../../utils/formatters'
import type { Role } from '../../types'
import './OverviewPage.scss'

const roleOrder: Role[] = ['coordinator', 'consolidator', 'distributor', 'transit', 'terminal', 'peripheral']

export default function OverviewPage() {
  const { data, loading, error, refetch } = useAsyncResource(getSummary, [])

  return (
    <div className="overview-page page-shell">
      <div className="page-shell__heading">
        <span className="page-shell__eyebrow">WORKSPACE / OVERVIEW</span>
        <h1>Overview</h1>
        <p>Network monitoring overview and priority signals.</p>
      </div>

      {isMockMode && <div className="overview-page__demo">DEMONSTRATION DATA · MOCK API</div>}
      {loading && <Loader />}
      {error && <ErrorState title="Summary unavailable" message={error} onRetry={refetch} />}
      {!loading && !error && data?.totalNodes === 0 && <EmptyState title="No network data" description="The summary returned an empty dataset." />}
      {!loading && !error && data && data.totalNodes > 0 && <>
      <section className="overview-page__section" aria-labelledby="overview-snapshot-title">
        <div className="overview-page__section-heading">
          <div>
            <h2 id="overview-snapshot-title">Network snapshot</h2>
            <p>Current dataset at a glance</p>
          </div>
          <span>JULY 2026</span>
        </div>
        <div className="overview-page__stats">
          <StatCard label="Clients" value={formatNumber(data.totalNodes)} description="In current dataset" />
          <StatCard label="Relations" value={formatNumber(data.totalEdges)} description={`${formatNumber(data.totalTransactions)} transactions`} />
          <StatCard label="Seed clients" value={formatNumber(data.totalSeeds)} description="Initial investigation set" />
          <StatCard label="Clusters" value={formatNumber(data.totalClusters)} description="Detected communities" />
        </div>
      </section>
      <div className="overview-page__grid">
        <section className="overview-page__panel" aria-labelledby="role-distribution-title">
          <h2 id="role-distribution-title">Role distribution</h2>
          <div className="overview-page__roles">
            {roleOrder.map((role) => <div className={`overview-page__role overview-page__role--${role}`} key={role}>
              <div><span>{formatRole(role)}</span><strong>{formatNumber(data.roles[role])}</strong></div>
              <div className="overview-page__bar"><span style={{ width: `${data.roles[role] / data.totalNodes * 100}%` }} /></div>
            </div>)}
          </div>
        </section>
        <section className="overview-page__panel" aria-labelledby="top-nodes-title">
          <div className="overview-page__panel-title"><h2 id="top-nodes-title">Priority nodes</h2><Link to="/priority">View all</Link></div>
          <div className="overview-page__list">
            {data.topNodes.slice(0, 5).map((node) => <Link to={`/network?gid=${node.gid}`} key={node.gid} className="overview-page__row">
              <span>#{node.rank}</span><strong>GID {node.gid}</strong><em className={`role role--${node.role}`}>{formatRole(node.role)}</em><b>{formatScore(node.priorityScore)}</b>
            </Link>)}
          </div>
        </section>
      </div>
      <section className="overview-page__section" aria-labelledby="top-clusters-title">
        <div className="overview-page__section-heading"><div><h2 id="top-clusters-title">Leading clusters</h2><p>Communities ordered for analyst review</p></div><Link to="/clusters">All clusters</Link></div>
        <div className="overview-page__clusters">
          {data.topClusters.slice(0, 3).map((cluster) => <Link to={`/network?cluster=${cluster.clusterId}`} className="overview-page__cluster" key={cluster.clusterId}>
            <span>CLUSTER {cluster.clusterId}</span><strong>{formatNumber(cluster.nodeCount)} nodes</strong><p>{cluster.hypothesis}</p><small>{formatKzt(cluster.internalVolumeKzt)} observed internal volume</small>
          </Link>)}
        </div>
      </section>
      </>}
    </div>
  )
}
