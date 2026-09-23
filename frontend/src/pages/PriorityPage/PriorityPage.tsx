import { Link, useSearchParams } from 'react-router-dom'
import ErrorState from '../../components/common/ErrorState/ErrorState'
import EmptyState from '../../components/common/EmptyState/EmptyState'
import Loader from '../../components/common/Loader/Loader'
import { getNode, getNodes, isMockMode } from '../../api/services'
import { useAsyncResource } from '../../hooks/useAsyncResource'
import { formatKzt, formatNumber, formatRole, formatScore } from '../../utils/formatters'
import type { Role } from '../../types'
import './PriorityPage.scss'

const roles: Role[] = ['coordinator', 'consolidator', 'distributor', 'transit', 'terminal', 'peripheral']
const pageSize = 20

export default function PriorityPage() {
  const [params, setParams] = useSearchParams()
  const page = Math.max(1, Number(params.get('page')) || 1)
  const search = params.get('search') ?? ''
  const role = (params.get('role') ?? '') as Role | ''
  const gid = params.get('gid') && /^\d+$/.test(params.get('gid')!) ? Number(params.get('gid')) : null
  const list = useAsyncResource(() => getNodes({ page, pageSize, search, role }), [page, search, role])
  const detail = useAsyncResource(() => gid === null ? Promise.resolve(null) : getNode(gid), [gid])

  function update(key: string, value: string) {
    const next = new URLSearchParams(params)
    if (value) next.set(key, value); else next.delete(key)
    if (key !== 'page') next.delete('page')
    setParams(next)
  }

  return <div className="priority-page page-shell">
    <div className="page-shell__heading"><span className="page-shell__eyebrow">WORKSPACE / PRIORITY</span><h1>Priority Nodes</h1><p>Clients ranked for analyst review. Scores describe queue priority, not criminal probability.</p></div>
    {isMockMode && <div className="priority-page__demo">DEMONSTRATION DATA · MOCK API</div>}
    <div className="priority-page__filters">
      <label>Search GID<input inputMode="numeric" value={search} onChange={(e) => update('search', e.target.value.replace(/\D/g, ''))} placeholder="e.g. 1001" /></label>
      <label>Role<select value={role} onChange={(e) => update('role', e.target.value)}><option value="">All roles</option>{roles.map((item) => <option value={item} key={item}>{formatRole(item)}</option>)}</select></label>
    </div>
    {list.loading && <Loader />}{list.error && <ErrorState title="Priority list unavailable" message={list.error} onRetry={list.refetch} />}
    {!list.loading && !list.error && list.data?.items.length === 0 && <EmptyState title="No matching nodes" description="Change the GID or role filter and try again." />}
    {!list.loading && !list.error && list.data && list.data.items.length > 0 && <>
      <div className="priority-page__table-wrap"><table><thead><tr><th>GID</th><th>Role</th><th>Priority</th><th>Role score</th><th>Cluster</th><th>Evidence</th><th /></tr></thead><tbody>{list.data.items.map((node) => <tr key={node.gid}><td><button type="button" onClick={() => update('gid', String(node.gid))}>{node.gid}</button></td><td><span className={`role role--${node.role}`}>{formatRole(node.role)}</span></td><td>{formatScore(node.priorityScore)}</td><td>{formatScore(node.roleScore)}</td><td>{node.clusterId}</td><td>{node.evidence}</td><td><Link to={`/network?gid=${node.gid}`}>Graph</Link></td></tr>)}</tbody></table></div>
      <div className="priority-page__pagination"><span>{formatNumber(list.data.total)} matching nodes</span><button type="button" disabled={page === 1} onClick={() => update('page', String(page - 1))}>Previous</button><strong>Page {page}</strong><button type="button" disabled={page * pageSize >= list.data.total} onClick={() => update('page', String(page + 1))}>Next</button></div>
    </>}
    {gid !== null && <aside className="priority-page__detail" aria-label={`Details for GID ${gid}`}><button type="button" aria-label="Close details" onClick={() => update('gid', '')}>×</button>{detail.loading && <Loader />}{detail.error && <ErrorState title="Node unavailable" message={detail.error} onRetry={detail.refetch} />}{detail.data && <><span>NODE DETAILS</span><h2>GID {detail.data.gid}</h2><p>{detail.data.evidence}</p><dl><div><dt>Role</dt><dd>{formatRole(detail.data.role)}</dd></div><div><dt>Priority score</dt><dd>{formatScore(detail.data.priorityScore)}</dd></div><div><dt>Incoming</dt><dd>{formatKzt(detail.data.inKzt)}</dd></div><div><dt>Outgoing</dt><dd>{formatKzt(detail.data.outKzt)}</dd></div><div><dt>Transactions</dt><dd>{detail.data.transactionCount}</dd></div></dl><Link to={`/network?gid=${detail.data.gid}`}>Explore network</Link></>}</aside>}
  </div>
}
