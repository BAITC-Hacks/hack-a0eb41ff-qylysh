import { Link, useSearchParams } from 'react-router-dom'
import ErrorState from '../../components/common/ErrorState/ErrorState'
import EmptyState from '../../components/common/EmptyState/EmptyState'
import Loader from '../../components/common/Loader/Loader'
import { getNode, getNodes, isMockMode } from '../../api/services'
import { useAsyncResource } from '../../hooks/useAsyncResource'
import { fill, plural, useI18n } from '../../i18n/i18n'
import { formatKzt, formatNumber, formatRole, formatScore } from '../../utils/formatters'
import type { Role } from '../../types'
import './PriorityPage.scss'

const roles: Role[] = ['coordinator', 'consolidator', 'distributor', 'transit', 'terminal', 'peripheral']
const pageSize = 20

export default function PriorityPage() {
  const { t, lang } = useI18n()
  const p = t.priority
  const [params, setParams] = useSearchParams()
  const page = Math.max(1, Number(params.get('page')) || 1)
  const search = params.get('search') ?? ''
  const role = (params.get('role') ?? '') as Role | ''
  const gid = params.get('gid') && /^\d+$/.test(params.get('gid')!) ? params.get('gid') : null
  const list = useAsyncResource(() => getNodes({ page, pageSize, search, role }), [page, search, role, lang])
  const detail = useAsyncResource(() => gid === null ? Promise.resolve(null) : getNode(gid), [gid, lang])

  function update(key: string, value: string) {
    const next = new URLSearchParams(params)
    if (value) next.set(key, value); else next.delete(key)
    if (key !== 'page') next.delete('page')
    setParams(next)
  }

  return <div className="priority-page page-shell">
    <div className="page-shell__heading"><span className="page-shell__eyebrow">{p.eyebrow}</span><h1>{p.title}</h1><p>{p.subtitle}</p></div>
    {isMockMode && <div className="priority-page__demo">{t.common.demo}</div>}
    <div className="priority-page__filters">
      <label>{p.searchGid}<input inputMode="numeric" value={search} onChange={(e) => update('search', e.target.value.replace(/\D/g, ''))} placeholder={p.searchPlaceholder} /></label>
      <label>{p.role}<select value={role} onChange={(e) => update('role', e.target.value)}><option value="">{p.allRoles}</option>{roles.map((item) => <option value={item} key={item}>{formatRole(item)}</option>)}</select></label>
    </div>
    {list.loading && <Loader />}{list.error && <ErrorState title={p.unavailable} message={list.error} onRetry={list.refetch} />}
    {!list.loading && !list.error && list.data?.items.length === 0 && <EmptyState title={p.emptyTitle} description={p.emptyDesc} />}
    {!list.loading && !list.error && list.data && list.data.items.length > 0 && <>
      <div className="priority-page__table-wrap"><table><thead><tr><th>{p.colGid}</th><th>{p.colRole}</th><th>{p.colPriority}</th><th>{p.colRoleScore}</th><th>{p.colCluster}</th><th>{p.colEvidence}</th><th /></tr></thead><tbody>{list.data.items.map((node) => <tr key={node.gid}><td><button type="button" onClick={() => update('gid', String(node.gid))}>{node.gid}</button></td><td><span className={`role role--${node.role}`}>{formatRole(node.role)}</span></td><td>{formatScore(node.priorityScore)}</td><td>{formatScore(node.roleScore)}</td><td>{node.clusterId}</td><td>{node.evidence}</td><td><Link to={`/network?gid=${node.gid}`}>{p.graph}</Link></td></tr>)}</tbody></table></div>
      <div className="priority-page__pagination"><span>{plural(p.matching, list.data.total, formatNumber(list.data.total))}</span><button type="button" disabled={page === 1} onClick={() => update('page', String(page - 1))}>{p.previous}</button><strong>{fill(p.page, { n: page })}</strong><button type="button" disabled={page * pageSize >= list.data.total} onClick={() => update('page', String(page + 1))}>{p.next}</button></div>
    </>}
    {gid !== null && <aside className="priority-page__detail" aria-label={fill(p.detailsAria, { gid })}><button type="button" aria-label={p.closeDetails} onClick={() => update('gid', '')}>×</button>{detail.loading && <Loader />}{detail.error && <ErrorState title={p.nodeUnavailable} message={detail.error} onRetry={detail.refetch} />}{detail.data && <><span>{p.nodeDetails}</span><h2>GID {detail.data.gid}</h2><p>{detail.data.evidence}</p><dl><div><dt>{p.colRole}</dt><dd>{formatRole(detail.data.role)}</dd></div><div><dt>{p.priorityScore}</dt><dd>{formatScore(detail.data.priorityScore)}</dd></div><div><dt>{p.incoming}</dt><dd>{formatKzt(detail.data.inKzt)}</dd></div><div><dt>{p.outgoing}</dt><dd>{formatKzt(detail.data.outKzt)}</dd></div><div><dt>{p.transactions}</dt><dd>{detail.data.transactionCount}</dd></div></dl><Link to={`/network?gid=${detail.data.gid}`}>{p.exploreNetwork}</Link></>}</aside>}
  </div>
}
