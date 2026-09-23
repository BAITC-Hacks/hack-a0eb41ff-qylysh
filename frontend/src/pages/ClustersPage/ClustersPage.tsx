import { Link } from 'react-router-dom'
import EmptyState from '../../components/common/EmptyState/EmptyState'
import ErrorState from '../../components/common/ErrorState/ErrorState'
import Loader from '../../components/common/Loader/Loader'
import { getClusters, isMockMode } from '../../api/services'
import { useAsyncResource } from '../../hooks/useAsyncResource'
import { fill, plural, useI18n } from '../../i18n/i18n'
import { formatKzt, formatNumber } from '../../utils/formatters'
import './ClustersPage.scss'

export default function ClustersPage() {
  const { t, lang } = useI18n()
  const c = t.clusters
  const { data, loading, error, refetch } = useAsyncResource(getClusters, [lang])
  return <div className="clusters-page page-shell">
    <div className="page-shell__heading"><span className="page-shell__eyebrow">{c.eyebrow}</span><h1>{c.title}</h1><p>{c.subtitle}</p></div>
    {isMockMode && <div className="clusters-page__demo">{t.common.demo}</div>}
    {loading && <Loader />}{error && <ErrorState title={c.unavailable} message={error} onRetry={refetch} />}{!loading && !error && data?.items.length === 0 && <EmptyState title={c.emptyTitle} description={c.emptyDesc} />}
    {data && data.items.length > 0 && <div className="clusters-page__grid">{data.items.map((cluster) => <article className="clusters-page__card" key={cluster.clusterId}><span>{fill(c.cluster, { id: cluster.clusterId })}</span><h2>{plural(c.nodes, cluster.nodeCount, formatNumber(cluster.nodeCount))}</h2><p>{cluster.description}</p><blockquote>{cluster.hypothesis}</blockquote><dl><div><dt>{c.seeds}</dt><dd>{cluster.seedCount}</dd></div><div><dt>{c.internalVolume}</dt><dd>{formatKzt(cluster.internalVolumeKzt)}</dd></div><div><dt>{c.topGid}</dt><dd>{cluster.topGid ?? '—'}</dd></div></dl><Link to={`/network?cluster=${cluster.clusterId}`}>{c.explore}</Link></article>)}</div>}
  </div>
}
