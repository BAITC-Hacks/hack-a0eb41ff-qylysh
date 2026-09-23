import { createBrowserRouter, Navigate } from 'react-router-dom'
import AppLayout from '../components/layout/AppLayout/AppLayout'
import OverviewPage from '../pages/OverviewPage/OverviewPage'
import NetworkPage from '../pages/NetworkPage/NetworkPage'
import PriorityPage from '../pages/PriorityPage/PriorityPage'
import ClustersPage from '../pages/ClustersPage/ClustersPage'
import MethodologyPage from '../pages/MethodologyPage/MethodologyPage'
import DataLimitationsPage from '../pages/DataLimitationsPage/DataLimitationsPage'

export const router = createBrowserRouter([
  {
    element: <AppLayout />,
    children: [
      { path: '/', element: <Navigate to="/dashboard" replace /> },
      { path: '/dashboard', element: <OverviewPage /> },
      { path: '/network', element: <NetworkPage /> },
      { path: '/priority', element: <PriorityPage /> },
      { path: '/clusters', element: <ClustersPage /> },
      { path: '/methodology', element: <MethodologyPage /> },
      { path: '/data-limitations', element: <DataLimitationsPage /> },
      { path: '*', element: <Navigate to="/dashboard" replace /> },
    ],
  },
])
