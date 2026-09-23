import { Link } from 'react-router-dom'
import EmptyState from '../../components/common/EmptyState/EmptyState'
import ErrorState from '../../components/common/ErrorState/ErrorState'
import Loader from '../../components/common/Loader/Loader'
import { getClusters, isMockMode } from '../../api/services'
import { useAsyncResource } from '../../hooks/useAsyncResource'
import { formatKzt, formatNumber } from '../../utils/formatters'
import './ClustersPage.scss'

export default function ClustersPage() {
  const { data, loading, error, refetch } = useAsyncResource(getClusters, [])
  return <div className="clusters-page page-shell">
    <div className="page-shell__heading"><span className="page-shell__eyebrow">WORKSPACE / CLUSTERS</span><h1>Clusters</h1><p>Detected communities in the observed financial network.</p></div>
    {isMockMode && <div className="clusters-page__demo">DEMONSTRATION DATA · MOCK API</div>}
    {loading && <Loader />}{error && <ErrorState title="Clusters unavailable" message={error} onRetry={refetch} />}{!loading && !error && data?.items.length === 0 && <EmptyState title="No clusters" description="No communities were returned for this dataset." />}
    {data && data.items.length > 0 && <div className="clusters-page__grid">{data.items.map((cluster) => <article className="clusters-page__card" key={cluster.clusterId}><span>CLUSTER {cluster.clusterId}</span><h2>{formatNumber(cluster.nodeCount)} nodes</h2><p>{cluster.description}</p><blockquote>{cluster.hypothesis}</blockquote><dl><div><dt>Seeds</dt><dd>{cluster.seedCount}</dd></div><div><dt>Internal volume</dt><dd>{formatKzt(cluster.internalVolumeKzt)}</dd></div><div><dt>Top GID</dt><dd>{cluster.topGid ?? '—'}</dd></div></dl><Link to={`/network?cluster=${cluster.clusterId}`}>Explore cluster network</Link></article>)}</div>}
  </div>
}
