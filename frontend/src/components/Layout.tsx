import type { ReactNode } from 'react'
import { Outlet } from 'react-router-dom'
import { Sidebar } from './Sidebar'

interface LayoutProps {
  children?: ReactNode
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="flex min-h-screen bg-white">
      <Sidebar />
      <main className="flex-1 p-6 overflow-auto">
        {children || <Outlet />}
      </main>
    </div>
  )
}
