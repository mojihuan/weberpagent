import { useParams } from 'react-router-dom'

export function TaskDetail() {
  const { id } = useParams()

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">任务详情</h1>
      <p className="mt-2 text-gray-500">任务 ID: {id}</p>
    </div>
  )
}
