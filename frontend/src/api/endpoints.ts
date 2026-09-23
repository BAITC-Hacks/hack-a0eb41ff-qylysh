export const endpoints = {
  SUMMARY: '/summary',
  NODES: '/nodes',
  TOP_NODES: '/top-nodes',
  CLUSTERS: '/clusters',
  node: (gid: number) => `/nodes/${gid}`,
  nodeGraph: (gid: number) => `/nodes/${gid}/graph`,
  cluster: (clusterId: number) => `/clusters/${clusterId}`,
  clusterGraph: (clusterId: number) => `/clusters/${clusterId}/graph`,
} as const
