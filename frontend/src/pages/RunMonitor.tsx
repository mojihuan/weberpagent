import { useParams } from 'react-router-dom'

export function RunMonitor() {
  const { id } = useParams()

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">执行监控</h1>
      <p className="mt-2 text-gray-500">执行 ID: {id}</p>
    </div>
  )
}
