import { useState } from 'react'
import { useTasks } from '../hooks/useTasks'
import {
  TaskListHeader,
  TaskFilters,
  TaskTable,
  BatchActions,
} from '../components/TaskList'
import { TaskFormModal } from '../components/TaskModal'
import { ImportModal } from '../components/ImportModal'
import { Pagination, EmptyState, LoadingSpinner, ConfirmModal } from '../components/shared'
import { tasksApi } from '../api/tasks'
import type { Task, CreateTaskDto } from '../types'

export function Tasks() {
  const {
    tasks,
    total,
    loading,
    filters,
    selectedIds,
    page,
    pageSize,
    setPage,
    updateFilter,
    toggleSelectAll,
    toggleSelect,
    fetchTasks,
    batchDelete,
    batchUpdateStatus,
  } = useTasks()

  const [modalOpen, setModalOpen] = useState(false)
  const [importModalOpen, setImportModalOpen] = useState(false)
  const [modalMode, setModalMode] = useState<'create' | 'edit'>('create')
  const [editingTask, setEditingTask] = useState<Task | undefined>()

  const [deleteConfirm, setDeleteConfirm] = useState<Task | null>(null)
  const [batchDeleteConfirm, setBatchDeleteConfirm] = useState(false)
  const [deleting, setDeleting] = useState(false)

  const handleCreate = () => {
    setModalMode('create')
    setEditingTask(undefined)
    setModalOpen(true)
  }

  const handleEdit = (task: Task) => {
    setModalMode('edit')
    setEditingTask(task)
    setModalOpen(true)
  }

  const handleSubmit = async (data: CreateTaskDto) => {
    if (modalMode === 'create') {
      await tasksApi.create(data)
    } else if (editingTask) {
      await tasksApi.update(editingTask.id, data)
    }
    await fetchTasks()
  }

  const handleDelete = async () => {
    if (!deleteConfirm) return
    setDeleting(true)
    try {
      await tasksApi.delete(deleteConfirm.id)
      await fetchTasks()
    } finally {
      setDeleting(false)
      setDeleteConfirm(null)
    }
  }

  const handleBatchDelete = async () => {
    setDeleting(true)
    try {
      await batchDelete()
    } finally {
      setDeleting(false)
      setBatchDeleteConfirm(false)
    }
  }

  const handleBatchSetReady = async () => {
    await batchUpdateStatus('ready')
  }

  if (loading && tasks.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  return (
    <div>
      <TaskListHeader onCreateClick={handleCreate} onImportClick={() => setImportModalOpen(true)} />

      <TaskFilters filters={filters} onFilterChange={updateFilter} />

      <BatchActions
        selectedCount={selectedIds.length}
        onBatchDelete={() => setBatchDeleteConfirm(true)}
        onBatchSetReady={handleBatchSetReady}
      />

      {tasks.length === 0 ? (
        <div className="bg-white rounded-xl border border-gray-200 p-8">
          <EmptyState
            message={filters.search || filters.status !== 'all' ? '没有找到匹配的任务' : '暂无任务'}
            action={
              !filters.search && filters.status === 'all' && (
                <button onClick={handleCreate} className="text-blue-500 hover:text-blue-600">
                  创建第一个任务
                </button>
              )
            }
          />
        </div>
      ) : (
        <TaskTable
          tasks={tasks}
          selectedIds={selectedIds}
          onSelectAll={toggleSelectAll}
          onToggleSelect={toggleSelect}
          onEdit={handleEdit}
          onDelete={task => setDeleteConfirm(task)}
        />
      )}

      <Pagination total={total} page={page} pageSize={pageSize} onChange={setPage} />

      <TaskFormModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        mode={modalMode}
        task={editingTask}
        onSubmit={handleSubmit}
      />

      <ConfirmModal
        open={!!deleteConfirm}
        title="删除任务"
        message={`确定要删除任务「${deleteConfirm?.name}」吗？此操作无法撤销。`}
        confirmText="删除"
        variant="danger"
        onConfirm={handleDelete}
        onCancel={() => setDeleteConfirm(null)}
        loading={deleting}
      />

      <ConfirmModal
        open={batchDeleteConfirm}
        title="批量删除"
        message={`确定要删除选中的 ${selectedIds.length} 个任务吗？此操作无法撤销。`}
        confirmText="删除"
        variant="danger"
        onConfirm={handleBatchDelete}
        onCancel={() => setBatchDeleteConfirm(false)}
        loading={deleting}
      />

      <ImportModal
        open={importModalOpen}
        onClose={() => setImportModalOpen(false)}
        onImportComplete={fetchTasks}
      />
    </div>
  )
}
