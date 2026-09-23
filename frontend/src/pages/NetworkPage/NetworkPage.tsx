import cytoscape from 'cytoscape'
import type { Core, EdgeSingular, NodeSingular } from 'cytoscape'
import {
  CreditCard, GitBranch, HandCoins, Landmark, Maximize2, Minus, Pause, Play,
  Plus, ShieldAlert, Sparkles, User, UserMinus, Wallet,
} from 'lucide-react'
import type { LucideIcon } from 'lucide-react'
import { createElement, useEffect, useMemo, useRef, useState } from 'react'
import { renderToStaticMarkup } from 'react-dom/server'
import { Link, useSearchParams } from 'react-router-dom'
import EmptyState from '../../components/common/EmptyState/EmptyState'
import ErrorState from '../../components/common/ErrorState/ErrorState'
import Loader from '../../components/common/Loader/Loader'
import { getGraph, isMockMode } from '../../api/services'
import { useAsyncResource } from '../../hooks/useAsyncResource'
import { plural, rich, useI18n } from '../../i18n/i18n'
import { formatKzt, formatRole, formatScore } from '../../utils/formatters'
import type { GraphEdge, GraphNode, GraphResponse, Role } from '../../types'
import './NetworkPage.scss'

type RoleMeta = { color: string; icon: LucideIcon }

const roleMeta: Record<Role, RoleMeta> = {
  coordinator: { color: '#a68ce6', icon: Landmark },
  consolidator: { color: '#e47c80', icon: Wallet },
  distributor: { color: '#e9a568', icon: HandCoins },
  transit: { color: '#70a9dd', icon: CreditCard },
  terminal: { color: '#74c5a0', icon: User },
  peripheral: { color: '#8c9ba7', icon: UserMinus },
}

const roleOrder = Object.keys(roleMeta) as Role[]
const HIGH_PRIORITY_THRESHOLD = .95

// Same lucide icon as the legend, rendered once per role into a data URI for cytoscape
const roleIcons = Object.fromEntries(roleOrder.map((role) => {
  const svg = renderToStaticMarkup(createElement(roleMeta[role].icon, { size: 24, color: '#071019', strokeWidth: 1.8 }))
  return [role, `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`]
})) as Record<Role, string>

export default function NetworkPage() {
  const { t, lang } = useI18n()
  const n = t.network
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
  const cyRef = useRef<Core | null>(null)
  const [selected, setSelected] = useState<GraphNode | null>(null)
  const [selectedEdge, setSelectedEdge] = useState<GraphEdge | null>(null)
  const [animationEnabled, setAnimationEnabled] = useState(
    () => typeof window !== 'undefined' && !window.matchMedia('(prefers-reduced-motion: reduce)').matches,
  )
  const { data, loading, error, refetch } = useAsyncResource(
    () => focus ? getGraph(focus) : Promise.resolve(null), [focus?.type, focus?.id],
  )

  const counts = useMemo(() => ({
    priority: data?.nodes.filter((node) => node.priorityScore >= HIGH_PRIORITY_THRESHOLD).length ?? 0,
    seeds: data?.nodes.filter((node) => node.isSeed).length ?? 0,
  }), [data])

  useEffect(() => {
    if (!graphRef.current || !data || data.nodes.length === 0) return
    const instance = cytoscape({
      container: graphRef.current,
      elements: [
        ...data.nodes.map((node) => ({
          data: { id: String(node.gid), label: `GID ${node.gid}\n${formatRole(node.role)}`, ...node },
        })),
        ...data.edges.map((edge, index) => ({ data: { id: `e${index}`, ...edge, source: String(edge.source), target: String(edge.target), label: formatKzt(edge.sumKzt) } })),
      ],
      style: [
        { selector: 'node', style: {
          'background-color': (element: NodeSingular) => roleMeta[element.data('role') as Role].color,
          'background-image': (element: NodeSingular) => roleIcons[element.data('role') as Role],
          'background-width': '58%', 'background-height': '58%', 'background-fit': 'contain',
          label: 'data(label)', color: '#e6ecf8', 'font-size': 8, 'font-weight': 600,
          'text-wrap': 'wrap', 'text-max-width': '90px', 'text-halign': 'center',
          'text-valign': 'bottom', 'text-margin-y': 8,
          width: (element: NodeSingular) => element.data('isSeed') ? 48 : 39,
          height: (element: NodeSingular) => element.data('isSeed') ? 48 : 39,
          'border-width': 0,
          'text-background-color': '#07101c', 'text-background-opacity': .82,
          'text-background-padding': '3px', 'text-background-shape': 'roundrectangle',
          'transition-property': 'width, height, opacity', 'transition-duration': 220, 'transition-timing-function': 'ease-out-cubic',
        } },
        { selector: 'node.hovered', style: { width: 52, height: 52, 'z-index': 20 } },
        { selector: 'edge', style: {
          width: 'mapData(sumKzt, 100000, 1000000, 1.5, 4)',
          'line-color': '#60a5fa', 'target-arrow-color': '#60a5fa', 'target-arrow-shape': 'triangle',
          'arrow-scale': 1.05, 'curve-style': 'bezier', opacity: .82,
          'line-style': 'dashed', 'line-dash-pattern': [9, 7],
          'transition-property': 'opacity', 'transition-duration': 220, 'transition-timing-function': 'ease-out-cubic',
        } },
        { selector: 'edge[sumKzt >= 500000]', style: { 'line-color': '#edb568', 'target-arrow-color': '#edb568' } },
        { selector: '.focused', style: { opacity: 1, 'z-index': 10 } },
        { selector: '.dimmed', style: { opacity: .16 } },
        { selector: ':selected', style: { 'overlay-color': '#62c5bb', 'overlay-opacity': .16 } },
      ],
      layout: { name: 'cose', animate: false, padding: 58, nodeRepulsion: () => 12000, idealEdgeLength: () => 145, nodeOverlap: 32, componentSpacing: 80 },
      minZoom: .35,
      maxZoom: 2.4,
    })

    let pinnedFocus = false
    const resetFocus = () => instance.elements().removeClass('dimmed focused hovered')
    instance.on('mouseover', 'node', (event) => {
      const node = event.target as NodeSingular
      node.addClass('hovered')
      if (!pinnedFocus) {
        instance.elements().not(node.closedNeighborhood()).addClass('dimmed')
        node.closedNeighborhood().addClass('focused')
      }
    })
    instance.on('mouseout', 'node', (event) => {
      ;(event.target as NodeSingular).removeClass('hovered')
      if (!pinnedFocus) resetFocus()
    })
    instance.on('tap', 'node', (event) => {
      const node = event.target as NodeSingular
      resetFocus()
      pinnedFocus = true
      instance.elements().not(node.closedNeighborhood()).addClass('dimmed')
      node.closedNeighborhood().addClass('focused')
      setSelected(node.data() as GraphNode)
      setSelectedEdge(null)
    })
    instance.on('tap', 'edge', (event) => {
      const edge = event.target as EdgeSingular
      resetFocus()
      pinnedFocus = true
      instance.elements().not(edge.connectedNodes().union(edge)).addClass('dimmed')
      edge.connectedNodes().union(edge).addClass('focused')
      setSelectedEdge(edge.data() as GraphEdge)
      setSelected(null)
    })
    instance.on('tap', (event) => {
      if (event.target === instance) { pinnedFocus = false; resetFocus(); setSelected(null); setSelectedEdge(null) }
    })
    cyRef.current = instance
    return () => { cyRef.current = null; instance.destroy() }
  }, [data])

  // Relabel in place on language change so the layout is kept
  useEffect(() => {
    const instance = cyRef.current
    if (!instance) return
    instance.batch(() => {
      instance.nodes().forEach((node) => { node.data('label', `GID ${node.data('gid')}
${formatRole(node.data('role') as Role)}`) })
      instance.edges().forEach((edge) => { edge.data('label', formatKzt(Number(edge.data('sumKzt')))) })
    })
  }, [lang, data])

  useEffect(() => {
    const instance = cyRef.current
    if (!instance) return
    if (!animationEnabled) {
      instance.edges().style('line-dash-offset', 0)
      return
    }
    let frame = 0
    const animate = (time: number) => {
      // 16px dash cycle every 1.2s
      instance.edges(':visible').style('line-dash-offset', -((time / 75) % 16))
      frame = requestAnimationFrame(animate)
    }
    frame = requestAnimationFrame(animate)
    return () => cancelAnimationFrame(frame)
  }, [animationEnabled, data])

  const zoom = (factor: number) => {
    const instance = cyRef.current
    if (!instance) return
    instance.zoom({ level: Math.min(2.4, Math.max(.35, instance.zoom() * factor)), renderedPosition: { x: instance.width() / 2, y: instance.height() / 2 } })
  }

  const invalid = rawId !== null && focus === null
  const count = (template: string, value: number) => rich(template, { n: <strong>{value}</strong> })
  return <div className="network-page page-shell">
    <div className="page-shell__heading"><span className="page-shell__eyebrow">{n.eyebrow}</span><h1>{n.title}</h1><p>{n.subtitle}</p></div>
    {isMockMode && <div className="network-page__demo">{t.common.demo}</div>}
    {!type && <div className="network-page__prompt"><GitBranch aria-hidden="true" /><div><strong>{n.chooseTitle}</strong><p>{n.chooseText}</p></div></div>}
    {invalid && <ErrorState title={n.invalidTitle} message={n.invalidText} />}
    {focus && loading && <Loader />}
    {focus && error && <ErrorState title={n.unavailable} message={error} onRetry={refetch} />}
    {data && !loading && !error && data.nodes.length === 0 && <EmptyState title={n.emptyTitle} description={n.emptyDesc} />}
    {data && !loading && !error && data.nodes.length > 0 && <>
      <div className="network-page__summary" aria-label={n.summaryAria}>
        <span>{count(plural(n.participants, data.nodes.length, '{n}'), data.nodes.length)}</span>
        <span>{count(plural(n.relations, data.edges.length, '{n}'), data.edges.length)}</span>
        <span className="network-page__summary--risk"><ShieldAlert size={13} /> {count(n.highPriority, counts.priority)}</span>
        <span className="network-page__summary--seed"><Sparkles size={13} /> {count(plural(n.seedNodes, counts.seeds, '{n}'), counts.seeds)}</span>
        <div className="network-page__summary-focus">{data.focus.type === 'gid' ? n.viewingGid : n.viewingCluster} <strong>{data.focus.id}</strong></div>
      </div>
      {data.truncatedAtDepth === 4 && <div className="network-page__boundary">{n.boundary}</div>}
      <div className="network-page__graph-layout">
        <section className="network-page__workspace" aria-labelledby="network-workspace-title">
          <div className="network-page__workspace-top">
            <div><h2 id="network-workspace-title">{n.graphTitle}</h2><span>{n.graphHint}</span></div>
            <span className="network-page__workspace-status">{n.graphStatus}</span>
          </div>
          <div className="network-page__canvas" ref={graphRef} role="application" tabIndex={0} aria-label={n.canvasAria} />
          <button type="button" className={`network-page__animation${animationEnabled ? ' is-active' : ''}`} aria-pressed={animationEnabled} onClick={() => setAnimationEnabled((value) => !value)}>{animationEnabled ? <Pause size={14} /> : <Play size={14} />} {n.animation} <i aria-hidden="true" /></button>
          <div className="network-page__controls" aria-label={n.zoomAria}>
            <button type="button" onClick={() => zoom(1.2)} aria-label={n.zoomIn} title={n.zoomIn}><Plus size={18} /></button>
            <button type="button" onClick={() => zoom(.8)} aria-label={n.zoomOut} title={n.zoomOut}><Minus size={18} /></button>
            <button type="button" onClick={() => cyRef.current?.fit(cyRef.current.elements(':visible'), 60)} aria-label={n.fit} title={n.fit}><Maximize2 size={17} /></button>
          </div>
          <span className="network-page__watermark" aria-hidden="true">MoneyGraph</span>
          {selected && <aside className="network-page__details"><button type="button" onClick={() => setSelected(null)} aria-label={n.closeNode}>×</button><span>{n.selectedNode}</span><h3>GID {selected.gid}</h3><div className="network-page__detail-role" style={{ color: roleMeta[selected.role].color }}>{formatRole(selected.role)}</div><p>{t.roleShort[selected.role]}</p><dl><div><dt>{n.roleScore}</dt><dd>{formatScore(selected.roleScore)}</dd></div><div><dt>{n.priority}</dt><dd>{formatScore(selected.priorityScore)}</dd></div><div><dt>{n.cluster}</dt><dd>{selected.clusterId}</dd></div><div><dt>{n.depth}</dt><dd>{selected.depth}</dd></div><div><dt>{n.seed}</dt><dd>{selected.isSeed ? t.common.yes : t.common.no}</dd></div></dl><Link to={`/priority?gid=${selected.gid}`}>{n.openDetails}</Link></aside>}
          {selectedEdge && <aside className="network-page__details"><button type="button" onClick={() => setSelectedEdge(null)} aria-label={n.closeRelation}>×</button><span>{n.selectedRelation}</span><h3>{selectedEdge.source} → {selectedEdge.target}</h3><dl><div><dt>{n.observedVolume}</dt><dd>{formatKzt(selectedEdge.sumKzt)}</dd></div><div><dt>{n.transactions}</dt><dd>{selectedEdge.transactionCount}</dd></div><div><dt>{n.direction}</dt><dd>{n.sourceTarget}</dd></div></dl></aside>}
        </section>
        <aside className="network-page__legend" aria-label={n.legendAria}>
          <h2>{n.nodeLegend}</h2>
          <div className="network-page__legend-list">{roleOrder.map((role) => { const Icon = roleMeta[role].icon; return <div key={role}><span style={{ color: roleMeta[role].color }}><Icon size={16} /></span><p><strong>{formatRole(role)}</strong><small>{t.roleShort[role]}</small></p></div> })}</div>
          <h2>{n.relationLegend}</h2>
          <div className="network-page__edge-key"><i /><span>{n.edgeDirection}</span></div>
          <div className="network-page__edge-key network-page__edge-key--volume"><i /><span>{n.edgeVolume}</span></div>
          <p className="network-page__legend-note">{n.legendNote}</p>
        </aside>
      </div>
    </>}
  </div>
}

