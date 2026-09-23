import { Outlet } from 'react-router-dom'
import Header from '../Header/Header'
import Sidebar from '../Sidebar/Sidebar'
import './AppLayout.scss'

export default function AppLayout() {
  return (
    <div className="app-layout">
      <Sidebar />
      <Header />
      <main className="app-layout__content" id="main-content">
        <Outlet />
      </main>
    </div>
  )
}
