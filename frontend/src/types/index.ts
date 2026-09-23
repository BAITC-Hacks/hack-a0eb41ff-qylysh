export type Role =
  | 'coordinator'
  | 'consolidator'
  | 'distributor'
  | 'transit'
  | 'terminal'
  | 'peripheral'

// Source GIDs exceed Number.MAX_SAFE_INTEGER. Keep them exact through JSON and URLs.
export type Gid = string

export interface SummaryTopNode {
  rank: number
  gid: Gid
  role: Role
  priorityScore: number
  clusterId: number
  evidence: string
}

export interface SummaryCluster {
  clusterId: number
  nodeCount: number
  seedCount: number
  internalVolumeKzt: number
  topGid: Gid | null
  hypothesis: string
}

export interface SummaryResponse {
  totalNodes: number
  totalEdges: number
  totalTransactions: number
  totalSeeds: number
  totalClusters: number
  roles: Record<Role, number>
  topNodes: SummaryTopNode[]
  topClusters: SummaryCluster[]
}

export interface GraphNode {
  gid: Gid
  role: Role
  roleScore: number
  priorityScore: number
  clusterId: number
  isSeed: boolean
  depth: number
}

export interface GraphEdge {
  source: Gid
  target: Gid
  sumKzt: number
  transactionCount: number
}

export interface GraphResponse {
  focus: { type: 'gid'; id: Gid } | { type: 'cluster'; id: number }
  nodes: GraphNode[]
  edges: GraphEdge[]
  truncatedAtDepth: number | null
}

export interface NodeDetails extends GraphNode {
  evidence: string
  inDegree: number
  outDegree: number
  inKzt: number
  outKzt: number
  transactionCount: number
}

export interface NodeListResponse {
  items: NodeDetails[]
  page: number
  pageSize: number
  total: number
}

export interface ClusterDetails extends SummaryCluster {
  description: string
}

export interface ClusterListResponse {
  items: ClusterDetails[]
  total: number
}
