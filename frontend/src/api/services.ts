import { apiClient } from './client'
import { endpoints } from './endpoints'
import { demoClusters, demoNodes, demoSummary, localizeCluster, localizeNode, makeDemoGraph } from './mockData'
import { fill, getDict } from '../i18n/i18n'
import type { ClusterDetails, ClusterListResponse, GraphResponse, NodeDetails, NodeListResponse, Role, SummaryResponse } from '../types'

export const isMockMode = import.meta.env.VITE_USE_MOCK_API !== 'false'
const mockScenario = import.meta.env.VITE_MOCK_SCENARIO ?? 'success'
const mockDelay = () => new Promise((resolve) => setTimeout(resolve, 220))

async function mock<T>(value: T, emptyValue?: T): Promise<T> {
  await mockDelay()
  if (mockScenario === 'error') throw new Error(getDict().errors.mockApi)
  return structuredClone(mockScenario === 'empty' && emptyValue !== undefined ? emptyValue : value)
}

export async function getSummary(): Promise<SummaryResponse> {
  if (isMockMode) return mock({ ...demoSummary, topNodes: demoSummary.topNodes.map(localizeNode), topClusters: demoSummary.topClusters.map(localizeCluster) }, { totalNodes: 0, totalEdges: 0, totalTransactions: 0, totalSeeds: 0, totalClusters: 0, roles: { coordinator: 0, consolidator: 0, distributor: 0, transit: 0, terminal: 0, peripheral: 0 }, topNodes: [], topClusters: [] })
  return (await apiClient.get<SummaryResponse>(endpoints.SUMMARY)).data
}

export async function getGraph(type: 'gid' | 'cluster', id: number): Promise<GraphResponse> {
  if (isMockMode) {
    if (mockScenario === 'error') return mock(makeDemoGraph(type, id))
    if (mockScenario === 'empty') return mock({ focus: { type, id }, nodes: [], edges: [], truncatedAtDepth: null })
    await mockDelay(); return makeDemoGraph(type, id)
  }
  const path = type === 'gid' ? endpoints.nodeGraph(id) : endpoints.clusterGraph(id)
  return (await apiClient.get<GraphResponse>(path)).data
}

export async function getNodes(params: { page: number; pageSize: number; search?: string; role?: Role | '' }): Promise<NodeListResponse> {
  if (!isMockMode) return (await apiClient.get<NodeListResponse>(endpoints.NODES, { params })).data
  await mockDelay()
  if (mockScenario === 'error') throw new Error(getDict().errors.mockApi)
  if (mockScenario === 'empty') return { items: [], page: params.page, pageSize: params.pageSize, total: 0 }
  let items = demoNodes.filter((node) => !params.search || String(node.gid).includes(params.search))
  if (params.role) items = items.filter((node) => node.role === params.role)
  items = items.sort((a, b) => b.priorityScore - a.priorityScore || a.gid - b.gid)
  const start = (params.page - 1) * params.pageSize
  return { items: items.slice(start, start + params.pageSize).map(localizeNode), page: params.page, pageSize: params.pageSize, total: items.length }
}

export async function getNode(gid: number): Promise<NodeDetails> {
  if (!isMockMode) return (await apiClient.get<NodeDetails>(endpoints.node(gid))).data
  await mockDelay()
  if (mockScenario === 'error') throw new Error(getDict().errors.mockApi)
  if (mockScenario === 'empty') throw new Error(fill(getDict().errors.gidNotFoundEmpty, { id: gid }))
  const node = demoNodes.find((item) => item.gid === gid)
  if (!node) throw new Error(fill(getDict().errors.gidNotFound, { id: gid }))
  return localizeNode(node)
}

export async function getClusters(): Promise<ClusterListResponse> {
  if (isMockMode) return mock({ items: demoClusters.map(localizeCluster), total: demoClusters.length }, { items: [], total: 0 })
  return (await apiClient.get<ClusterListResponse>(endpoints.CLUSTERS)).data
}

export async function getCluster(clusterId: number): Promise<ClusterDetails> {
  if (!isMockMode) return (await apiClient.get<ClusterDetails>(endpoints.cluster(clusterId))).data
  await mockDelay()
  const cluster = demoClusters.find((item) => item.clusterId === clusterId)
  if (!cluster) throw new Error(fill(getDict().errors.clusterNotFound, { id: clusterId }))
  return localizeCluster(cluster)
}
