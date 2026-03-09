import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { tasksApi } from '../api/tasks'
import type { Task, Run, CreateTaskDto } from '../types'
import {
  TaskHeader,
  TaskInfo,
  ConfigPanel,
  RunHistory,
  StatsChart,
} from '../components/TaskDetail'
import { TaskFormModal } from '../components/TaskModal'
import { ConfirmModal, LoadingSpinner } from '../components/shared'

export function TaskDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const [task, setTask] = useState<Task | null>(null)
  const [runs, setRuns] = useState<Run[]>([])
  const [stats, setStats] = useState<{ date: string; runs: number; successRate: number }[]>([])
  const [loading, setLoading] = useState(true)
  const [runsLoading, setRunsLoading] = useState(true)
  const [statsLoading, setStatsLoading] = useState(true)

  const [editModalOpen, setEditModalOpen] = useState(false)
  const [deleteConfirm, setDeleteConfirm] = useState(false)
  const [deleting, setDeleting] = useState(false)

  useEffect(() => {
    if (!id) return

    const loadTask = async () => {
      setLoading(true)
      try {
        const data = await tasksApi.get(id)
        setTask(data)
      } catch (error) {
        console.error('Failed to load task:', error)
      } finally {
        setLoading(false)
      }
    }

    loadTask()
  }, [id])

  useEffect(() => {
    if (!id) return

    const loadRuns = async () => {
      setRunsLoading(true)
      try {
        const data = await tasksApi.getRuns(id)
        setRuns(data)
      } catch (error) {
        console.error('Failed to load runs:', error)
      } finally {
        setRunsLoading(false)
      }
    }

    loadRuns()
  }, [id])

  useEffect(() => {
    if (!id) return

    const loadStats = async () => {
      setStatsLoading(true)
      try {
        const data = await tasksApi.getStats(id)
        setStats(data)
      } catch (error) {
        console.error('Failed to load stats:', error)
      } finally {
        setStatsLoading(false)
      }
    }

    loadStats()
  }, [id])

  const handleExecute = () => {
    console.log('Execute task:', id)
  }

  const handleUpdate = async (data: CreateTaskDto) => {
    if (!id) return
    const updated = await tasksApi.update(id, data)
    setTask(updated)
  }

  const handleDelete = async () => {
    if (!id) return
    setDeleting(true)
    try {
      await tasksApi.delete(id)
      navigate('/tasks')
    } finally {
      setDeleting(false)
      setDeleteConfirm(false)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (!task) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">任务不存在</p>
        <button
          onClick={() => navigate('/tasks')}
          className="mt-4 text-blue-500 hover:text-blue-600"
        >
          返回列表
        </button>
      </div>
    )
  }

  return (
    <div>
      <TaskHeader
        task={task}
        onEdit={() => setEditModalOpen(true)}
        onDelete={() => setDeleteConfirm(true)}
        onExecute={handleExecute}
      />

      <TaskInfo task={task} />
      <ConfigPanel task={task} />
      <StatsChart data={stats} loading={statsLoading} />
      <RunHistory runs={runs} loading={runsLoading} />

      <TaskFormModal
        open={editModalOpen}
        onClose={() => setEditModalOpen(false)}
        mode="edit"
        task={task}
        onSubmit={handleUpdate}
      />

      <ConfirmModal
        open={deleteConfirm}
        title="删除任务"
        message={`确定要删除任务「${task.name}」吗？此操作无法撤销。`}
        confirmText="删除"
        variant="danger"
        onConfirm={handleDelete}
        onCancel={() => setDeleteConfirm(false)}
        loading={deleting}
      />
    </div>
  )
}
