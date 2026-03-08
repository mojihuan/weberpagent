import { NavLink } from 'react-router-dom'
import type { LucideIcon } from 'lucide-react'

interface NavItemProps {
  icon: LucideIcon
  label: string
  to: string
}

export function NavItem({ icon: Icon, label, to }: NavItemProps) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `flex items-center gap-3 h-10 px-3 rounded-lg text-sm font-medium transition-colors ${
          isActive
            ? 'bg-blue-500 text-white'
            : 'text-gray-600 hover:bg-gray-100'
        }`
      }
    >
      <Icon className="w-5 h-5" />
      <span>{label}</span>
    </NavLink>
  )
}
