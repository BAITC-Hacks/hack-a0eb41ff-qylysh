import StatCard from '../../components/common/StatCard/StatCard'
import Loader from '../../components/common/Loader/Loader'
import ErrorState from '../../components/common/ErrorState/ErrorState'
import EmptyState from '../../components/common/EmptyState/EmptyState'
import { Link } from 'react-router-dom'
import { getSummary, isMockMode } from '../../api/services'
import { useAsyncResource } from '../../hooks/useAsyncResource'
import { fill, plural, useI18n } from '../../i18n/i18n'
import { formatKzt, formatNumber, formatRole, formatScore } from '../../utils/formatters'
import type { Role } from '../../types'
import './OverviewPage.scss'

const roleOrder: Role[] = ['coordinator', 'consolidator', 'distributor', 'transit', 'terminal', 'peripheral']

export default function OverviewPage() {
  const { t, lang } = useI18n()
  const o = t.overview
  const { data, loading, error, refetch } = useAsyncResource(getSummary, [lang])

  return (
    <div className="overview-page page-shell">
      <div className="page-shell__heading">
        <span className="page-shell__eyebrow">{o.eyebrow}</span>
        <h1>{o.title}</h1>
        <p>{o.subtitle}</p>
      </div>

      {isMockMode && <div className="overview-page__demo">{t.common.demo}</div>}
      {loading && <Loader />}
      {error && <ErrorState title={o.unavailable} message={error} onRetry={refetch} />}
      {!loading && !error && data?.totalNodes === 0 && <EmptyState title={o.emptyTitle} description={o.emptyDesc} />}
      {!loading && !error && data && data.totalNodes > 0 && <>
      <section className="overview-page__section" aria-labelledby="overview-snapshot-title">
        <div className="overview-page__section-heading">
          <div>
            <h2 id="overview-snapshot-title">{o.snapshot}</h2>
            <p>{o.snapshotSub}</p>
          </div>
          <span>{o.period}</span>
        </div>
        <div className="overview-page__stats">
          <StatCard label={o.clients} value={formatNumber(data.totalNodes)} description={o.clientsDesc} />
          <StatCard label={o.relations} value={formatNumber(data.totalEdges)} description={plural(o.transactions, data.totalTransactions, formatNumber(data.totalTransactions))} />
          <StatCard label={o.seedClients} value={formatNumber(data.totalSeeds)} description={o.seedDesc} />
          <StatCard label={o.clusters} value={formatNumber(data.totalClusters)} description={o.clustersDesc} />
        </div>
      </section>
      <div className="overview-page__grid">
        <section className="overview-page__panel" aria-labelledby="role-distribution-title">
          <h2 id="role-distribution-title">{o.roleDistribution}</h2>
          <div className="overview-page__roles">
            {roleOrder.map((role) => <div className={`overview-page__role overview-page__role--${role}`} key={role}>
              <div><span>{formatRole(role)}</span><strong>{formatNumber(data.roles[role])}</strong></div>
              <div className="overview-page__bar"><span style={{ width: `${data.roles[role] / data.totalNodes * 100}%` }} /></div>
            </div>)}
          </div>
        </section>
        <section className="overview-page__panel" aria-labelledby="top-nodes-title">
          <div className="overview-page__panel-title"><h2 id="top-nodes-title">{o.priorityNodes}</h2><Link to="/priority">{o.viewAll}</Link></div>
          <div className="overview-page__list">
            {data.topNodes.slice(0, 5).map((node) => <Link to={`/network?gid=${node.gid}`} key={node.gid} className="overview-page__row">
              <span>#{node.rank}</span><strong>GID {node.gid}</strong><em className={`role role--${node.role}`}>{formatRole(node.role)}</em><b>{formatScore(node.priorityScore)}</b>
            </Link>)}
          </div>
        </section>
      </div>
      <section className="overview-page__section" aria-labelledby="top-clusters-title">
        <div className="overview-page__section-heading"><div><h2 id="top-clusters-title">{o.leadingClusters}</h2><p>{o.leadingClustersSub}</p></div><Link to="/clusters">{o.allClusters}</Link></div>
        <div className="overview-page__clusters">
          {data.topClusters.slice(0, 3).map((cluster) => <Link to={`/network?cluster=${cluster.clusterId}`} className="overview-page__cluster" key={cluster.clusterId}>
            <span>{fill(o.cluster, { id: cluster.clusterId })}</span><strong>{plural(o.nodes, cluster.nodeCount, formatNumber(cluster.nodeCount))}</strong><p>{cluster.hypothesis}</p><small>{fill(o.internalVolume, { sum: formatKzt(cluster.internalVolumeKzt) })}</small>
          </Link>)}
        </div>
      </section>
      </>}
    </div>
  )
}
