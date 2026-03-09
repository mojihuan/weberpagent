import type { ReactNode } from 'react'
import { Outlet } from 'react-router-dom'
import { Sidebar } from './Sidebar'

interface LayoutProps {
  children?: ReactNode
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="flex h-screen bg-white">
      <Sidebar />
      <main className="flex-1 p-6 overflow-hidden flex flex-col">
        {children || <Outlet />}
      </main>
    </div>
  )
}
