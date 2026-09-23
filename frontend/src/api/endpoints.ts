import type { Gid } from '../types'

export const endpoints = {
  SUMMARY: '/summary',
  NODES: '/nodes',
  TOP_NODES: '/top-nodes',
  CLUSTERS: '/clusters',
  node: (gid: Gid) => `/nodes/${gid}`,
  nodeGraph: (gid: Gid) => `/nodes/${gid}/graph`,
  cluster: (clusterId: number) => `/clusters/${clusterId}`,
  clusterGraph: (clusterId: number) => `/clusters/${clusterId}/graph`,
} as const
