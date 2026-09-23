import cytoscape from 'cytoscape'
import type { NodeSingular } from 'cytoscape'
import { GitBranch } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import EmptyState from '../../components/common/EmptyState/EmptyState'
import ErrorState from '../../components/common/ErrorState/ErrorState'
import Loader from '../../components/common/Loader/Loader'
import { getGraph, isMockMode } from '../../api/services'
import { useAsyncResource } from '../../hooks/useAsyncResource'
import { formatKzt, formatRole, formatScore } from '../../utils/formatters'
import type { GraphNode, GraphResponse } from '../../types'
import './NetworkPage.scss'

const roleColors: Record<string, string> = { coordinator: '#a68ce6', consolidator: '#e47c80', distributor: '#e9a568', transit: '#70a9dd', terminal: '#74c5a0', peripheral: '#8c9ba7' }

export default function NetworkPage() {
  const [searchParams] = useSearchParams()
  const gidParam = searchParams.get('gid')
  const clusterParam = searchParams.get('cluster')
  const type = gidParam ? 'gid' : clusterParam ? 'cluster' : null
  const rawId = gidParam ?? clusterParam
  const focus: GraphResponse['focus'] | null = gidParam && /^\d+$/.test(gidParam)
    ? { type: 'gid', id: gidParam }
    : clusterParam && /^\d+$/.test(clusterParam) && Number.isSafeInteger(Number(clusterParam))
      ? { type: 'cluster', id: Number(clusterParam) }
      : null
  const graphRef = useRef<HTMLDivElement>(null)
  const [selected, setSelected] = useState<GraphNode | null>(null)
  const { data, loading, error, refetch } = useAsyncResource(
    () => focus ? getGraph(focus) : Promise.resolve(null), [focus?.type, focus?.id],
  )

  useEffect(() => {
    if (!graphRef.current || !data || data.nodes.length === 0) return
    const instance = cytoscape({
      container: graphRef.current,
      elements: [
        ...data.nodes.map((node) => ({ data: { id: String(node.gid), label: String(node.gid), ...node } })),
        ...data.edges.map((edge, index) => ({ data: { id: `e${index}`, source: String(edge.source), target: String(edge.target), label: formatKzt(edge.sumKzt) } })),
      ],
      style: [
        { selector: 'node', style: { 'background-color': (element: NodeSingular) => roleColors[String(element.data('role'))], label: 'data(label)', color: '#eef3f7', 'font-size': 9, 'text-valign': 'bottom', 'text-margin-y': 7, width: (element: NodeSingular) => element.data('isSeed') ? 34 : 25, height: (element: NodeSingular) => element.data('isSeed') ? 34 : 25, 'border-width': (element: NodeSingular) => element.data('isSeed') ? 3 : 1, 'border-color': '#eef3f7' } },
        { selector: 'edge', style: { width: 1.4, 'line-color': '#526474', 'target-arrow-color': '#62c5bb', 'target-arrow-shape': 'triangle', 'curve-style': 'bezier', opacity: .75 } },
        { selector: ':selected', style: { 'overlay-color': '#62c5bb', 'overlay-opacity': .18, 'border-color': '#62c5bb', 'border-width': 3 } },
      ],
      layout: { name: 'cose', animate: false, padding: 35 },
    })
    instance.on('tap', 'node', (event) => setSelected(event.target.data() as GraphNode))
    return () => instance.destroy()
  }, [data])

  const invalid = rawId !== null && focus === null
  return <div className="network-page page-shell">
    <div className="page-shell__heading"><span className="page-shell__eyebrow">WORKSPACE / NETWORK</span><h1>Network Analysis</h1><p>Explore directed connections in the observed transaction network.</p></div>
    {isMockMode && <div className="network-page__demo">DEMONSTRATION DATA · MOCK API</div>}
    {!type && <div className="network-page__prompt"><GitBranch aria-hidden="true" /><div><strong>Choose a network focus</strong><p>Search for a numeric GID or open a cluster from the Clusters page.</p></div></div>}
    {invalid && <ErrorState title="Invalid network identifier" message="GID and cluster identifiers must be numeric." />}
    {focus && loading && <Loader />}
    {focus && error && <ErrorState title="Network unavailable" message={error} onRetry={refetch} />}
    {data && !loading && !error && data.nodes.length === 0 && <EmptyState title="Empty graph" description="No observed connections were returned for this focus." />}
    {data && !loading && !error && data.nodes.length > 0 && <>
      <div className="network-page__selected">Viewing {data.focus.type}: <strong>{data.focus.id}</strong><span>{data.nodes.length} nodes · {data.edges.length} directed relations</span></div>
      {data.truncatedAtDepth === 4 && <div className="network-page__boundary">Observation stops at depth 4. Boundary nodes do not prove that funds stopped there.</div>}
      <section className="network-page__workspace" aria-labelledby="network-workspace-title">
        <div className="network-page__workspace-top"><h2 id="network-workspace-title">Directed local graph</h2><span>SELECT A NODE FOR DETAILS</span></div>
        <div className="network-page__canvas" ref={graphRef} aria-label="Interactive transaction network graph" />
        {selected && <aside className="network-page__details"><button type="button" onClick={() => setSelected(null)} aria-label="Close node details">×</button><span>SELECTED NODE</span><h3>GID {selected.gid}</h3><dl><div><dt>Role</dt><dd>{formatRole(selected.role)}</dd></div><div><dt>Role score</dt><dd>{formatScore(selected.roleScore)}</dd></div><div><dt>Priority</dt><dd>{formatScore(selected.priorityScore)}</dd></div><div><dt>Cluster</dt><dd>{selected.clusterId}</dd></div><div><dt>Depth</dt><dd>{selected.depth}</dd></div></dl><Link to={`/priority?gid=${selected.gid}`}>Open details</Link></aside>}
      </section>
    </>}
  </div>
}
