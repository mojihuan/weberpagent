import type { ReactNode } from 'react'

interface SummaryCardProps {
  icon: ReactNode
  label: string
  value: string | number
  valueColor?: string
}

export function SummaryCard({ icon, label, value, valueColor = 'text-gray-900' }: SummaryCardProps) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-4">
      <div className="flex items-center gap-3">
        <div className="p-2 bg-gray-100 rounded-lg text-gray-600">
          {icon}
        </div>
        <div>
          <p className="text-sm text-gray-500">{label}</p>
          <p className={`text-xl font-semibold ${valueColor}`}>{value}</p>
        </div>
      </div>
    </div>
  )
}
