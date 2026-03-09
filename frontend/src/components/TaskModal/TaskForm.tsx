import { useState, useEffect } from 'react'
import type { Task, CreateTaskDto } from '../../types'

interface TaskFormProps {
  initialData?: Task
  onSubmit: (data: CreateTaskDto) => void
  onCancel: () => void
  loading?: boolean
  mode: 'create' | 'edit'
}

interface FormData {
  name: string
  description: string
  target_url: string
  max_steps: number
}

interface FormErrors {
  name?: string
  target_url?: string
}

export function TaskForm({ initialData, onSubmit, onCancel, loading, mode }: TaskFormProps) {
  const [formData, setFormData] = useState<FormData>({
    name: initialData?.name || '',
    description: initialData?.description || '',
    target_url: initialData?.target_url || '',
    max_steps: initialData?.max_steps || 20,
  })
  const [errors, setErrors] = useState<FormErrors>({})

  useEffect(() => {
    if (initialData) {
      setFormData({
        name: initialData.name,
        description: initialData.description,
        target_url: initialData.target_url,
        max_steps: initialData.max_steps,
      })
    }
  }, [initialData])

  const validate = (): boolean => {
    const newErrors: FormErrors = {}

    if (!formData.name.trim()) {
      newErrors.name = '请输入任务名称'
    } else if (formData.name.length > 50) {
      newErrors.name = '任务名称不能超过 50 个字符'
    }

    if (!formData.target_url.trim()) {
      newErrors.target_url = '请输入目标 URL'
    } else {
      try {
        new URL(formData.target_url)
      } catch {
        newErrors.target_url = '请输入有效的 URL 格式'
      }
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (validate()) {
      onSubmit(formData)
    }
  }

  const handleStepsChange = (delta: number) => {
    const newSteps = Math.max(1, Math.min(50, formData.max_steps + delta))
    setFormData(prev => ({ ...prev, max_steps: newSteps }))
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          任务名称 <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          value={formData.name}
          onChange={e => setFormData(prev => ({ ...prev, name: e.target.value }))}
          placeholder="例如：用户登录测试"
          className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.name ? 'border-red-500' : 'border-gray-200'
          }`}
        />
        {errors.name && <p className="mt-1 text-sm text-red-500">{errors.name}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">任务描述</label>
        <textarea
          value={formData.description}
          onChange={e => setFormData(prev => ({ ...prev, description: e.target.value }))}
          placeholder="描述任务的目标和步骤..."
          rows={3}
          className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          目标 URL <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          value={formData.target_url}
          onChange={e => setFormData(prev => ({ ...prev, target_url: e.target.value }))}
          placeholder="https://example.com/login"
          className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.target_url ? 'border-red-500' : 'border-gray-200'
          }`}
        />
        {errors.target_url && <p className="mt-1 text-sm text-red-500">{errors.target_url}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          最大步数
        </label>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => handleStepsChange(-5)}
            className="w-8 h-8 flex items-center justify-center border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            -5
          </button>
          <button
            type="button"
            onClick={() => handleStepsChange(-1)}
            className="w-8 h-8 flex items-center justify-center border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            -1
          </button>
          <span className="w-16 text-center font-medium">{formData.max_steps}</span>
          <button
            type="button"
            onClick={() => handleStepsChange(1)}
            className="w-8 h-8 flex items-center justify-center border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            +1
          </button>
          <button
            type="button"
            onClick={() => handleStepsChange(5)}
            className="w-8 h-8 flex items-center justify-center border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            +5
          </button>
          <span className="text-sm text-gray-500 ml-2">范围 1-50</span>
        </div>
      </div>

      <div className="flex justify-end gap-3 pt-4 border-t border-gray-100">
        <button
          type="button"
          onClick={onCancel}
          disabled={loading}
          className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg disabled:opacity-50"
        >
          取消
        </button>
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 font-medium"
        >
          {loading ? '处理中...' : mode === 'create' ? '创建任务' : '保存修改'}
        </button>
      </div>
    </form>
  )
}
