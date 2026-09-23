import { lazy, Suspense } from 'react'
import type { ReactNode } from 'react'
import { createBrowserRouter, Navigate } from 'react-router-dom'
import AppLayout from '../components/layout/AppLayout/AppLayout'
import Loader from '../components/common/Loader/Loader'

const OverviewPage = lazy(() => import('../pages/OverviewPage/OverviewPage'))
const NetworkPage = lazy(() => import('../pages/NetworkPage/NetworkPage'))
const PriorityPage = lazy(() => import('../pages/PriorityPage/PriorityPage'))
const ClustersPage = lazy(() => import('../pages/ClustersPage/ClustersPage'))
const MethodologyPage = lazy(() => import('../pages/MethodologyPage/MethodologyPage'))
const DataLimitationsPage = lazy(() => import('../pages/DataLimitationsPage/DataLimitationsPage'))

const page = (content: ReactNode) => <Suspense fallback={<Loader />}>{content}</Suspense>

export const router = createBrowserRouter([
  {
    element: <AppLayout />,
    children: [
      { path: '/', element: <Navigate to="/dashboard" replace /> },
      { path: '/dashboard', element: page(<OverviewPage />) },
      { path: '/network', element: page(<NetworkPage />) },
      { path: '/priority', element: page(<PriorityPage />) },
      { path: '/clusters', element: page(<ClustersPage />) },
      { path: '/methodology', element: page(<MethodologyPage />) },
      { path: '/data-limitations', element: page(<DataLimitationsPage />) },
      { path: '*', element: <Navigate to="/dashboard" replace /> },
    ],
  },
])
