import type { ClusterDetails, GraphResponse, NodeDetails, Role, SummaryResponse } from '../types'

const roles: Role[] = ['coordinator', 'consolidator', 'distributor', 'transit', 'terminal', 'peripheral']

export const demoNodes: NodeDetails[] = Array.from({ length: 46 }, (_, index) => {
  const gid = 1001 + index
  const role = roles[index % roles.length]
  return {
    gid,
    role,
    roleScore: Math.max(0.5, 0.96 - index * 0.009),
    priorityScore: Math.max(0.35, 0.98 - index * 0.012),
    clusterId: (index % 4) + 1,
    isSeed: index % 7 === 0,
    depth: index % 5,
    evidence: `${role} pattern from observed flow concentration and network position. Demonstration data.`,
    inDegree: 2 + (index % 9),
    outDegree: 1 + (index % 7),
    inKzt: 580000 + index * 97500,
    outKzt: 420000 + index * 81250,
    transactionCount: 8 + index * 2,
  }
})

export const demoClusters: ClusterDetails[] = [
  { clusterId: 1, nodeCount: 714, seedCount: 28, internalVolumeKzt: 184200000, topGid: 1001, hypothesis: 'Dense coordination around several high-flow nodes.', description: 'Observed community with repeated transfers among a compact core.' },
  { clusterId: 2, nodeCount: 603, seedCount: 21, internalVolumeKzt: 147850000, topGid: 1002, hypothesis: 'Layered distribution into terminal accounts.', description: 'Broad distribution pattern with multiple short outward paths.' },
  { clusterId: 3, nodeCount: 511, seedCount: 18, internalVolumeKzt: 121400000, topGid: 1003, hypothesis: 'Consolidation followed by several transit chains.', description: 'Incoming flows converge before continuing through observed intermediaries.' },
  { clusterId: 4, nodeCount: 420, seedCount: 14, internalVolumeKzt: 93300000, topGid: 1004, hypothesis: 'Sparse peripheral structure near the depth boundary.', description: 'Looser community containing many depth-four observations.' },
]

export const demoSummary: SummaryResponse = {
  totalNodes: 2248,
  totalEdges: 3119,
  totalTransactions: 4840,
  totalSeeds: 81,
  totalClusters: 4,
  roles: { coordinator: 87, consolidator: 196, distributor: 284, transit: 533, terminal: 642, peripheral: 506 },
  topNodes: demoNodes.slice(0, 5).map((node, index) => ({ rank: index + 1, gid: node.gid, role: node.role, priorityScore: node.priorityScore, clusterId: node.clusterId, evidence: node.evidence })),
  topClusters: demoClusters.slice(0, 3),
}

export function makeDemoGraph(type: 'gid' | 'cluster', id: number): GraphResponse {
  if ((type === 'gid' && !demoNodes.some((node) => node.gid === id)) || (type === 'cluster' && !demoClusters.some((cluster) => cluster.clusterId === id))) {
    throw new Error(`${type === 'gid' ? 'GID' : 'Cluster'} ${id} was not found in demonstration data.`)
  }
  const pool = type === 'gid'
    ? [demoNodes.find((node) => node.gid === id)!, ...demoNodes.filter((node) => node.gid !== id).slice(0, 8)]
    : demoNodes.filter((node) => node.clusterId === id).slice(0, 12)
  return {
    focus: { type, id },
    nodes: pool,
    edges: pool.slice(1).map((node, index) => ({ source: pool[Math.floor(index / 2)].gid, target: node.gid, sumKzt: 125000 + index * 84000, transactionCount: 2 + index })),
    truncatedAtDepth: pool.some((node) => node.depth === 4) ? 4 : null,
  }
}
