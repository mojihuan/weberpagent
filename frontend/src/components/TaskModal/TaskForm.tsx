import { useState, useEffect } from 'react'
import { Code, AlertCircle, Database } from 'lucide-react'
import type { Task, CreateTaskDto, OperationsResponse, DataMethodConfig } from '../../types'
import { OperationCodeSelector } from './OperationCodeSelector'
import { DataMethodSelector } from './DataMethodSelector'
import { externalOperationsApi } from '../../api/externalOperations'
import { externalDataMethodsApi } from '../../api/externalDataMethods'

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
  preconditions: string[]
  api_assertions: string[]
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
    preconditions: initialData?.preconditions || [''],
    api_assertions: initialData?.api_assertions || [''],
  })
  const [errors, setErrors] = useState<FormErrors>({})

  // Operation code selector state
  const [selectorOpen, setSelectorOpen] = useState(false)
  const [selectorIndex, setSelectorIndex] = useState<number | null>(null)
  const [operationsLoading, setOperationsLoading] = useState(false)
  const [operationsAvailable, setOperationsAvailable] = useState(true)
  const [operationsError, setOperationsError] = useState<string | null>(null)

  // Data method selector state
  const [dataSelectorOpen, setDataSelectorOpen] = useState(false)
  const [dataSelectorIndex, setDataSelectorIndex] = useState<number | null>(null)
  const [dataMethodsLoading, setDataMethodsLoading] = useState(false)
  const [dataMethodsAvailable, setDataMethodsAvailable] = useState(true)
  const [dataMethodsError, setDataMethodsError] = useState<string | null>(null)

  useEffect(() => {
    if (initialData) {
      setFormData({
        name: initialData.name,
        description: initialData.description,
        target_url: initialData.target_url,
        max_steps: initialData.max_steps,
        preconditions: initialData.preconditions || [''],
        api_assertions: initialData.api_assertions || [''],
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
      onSubmit({
        ...formData,
        preconditions: formData.preconditions.filter(p => p.trim()),
        api_assertions: formData.api_assertions.filter(a => a.trim()),
      })
    }
  }

  const handleStepsChange = (delta: number) => {
    const newSteps = Math.max(1, Math.min(50, formData.max_steps + delta))
    setFormData(prev => ({ ...prev, max_steps: newSteps }))
  }

  const handleAddPrecondition = () => {
    setFormData(prev => ({ ...prev, preconditions: [...prev.preconditions, ''] }))
  }

  const handleRemovePrecondition = (index: number) => {
    setFormData(prev => ({
      ...prev,
      preconditions: prev.preconditions.filter((_, i) => i !== index)
    }))
  }

  const handlePreconditionChange = (index: number, value: string) => {
    setFormData(prev => ({
      ...prev,
      preconditions: prev.preconditions.map((p, i) => i === index ? value : p)
    }))
  }

  const handleAddApiAssertion = () => {
    setFormData(prev => ({ ...prev, api_assertions: [...prev.api_assertions, ''] }))
  }

  const handleRemoveApiAssertion = (index: number) => {
    setFormData(prev => ({
      ...prev,
      api_assertions: prev.api_assertions.filter((_, i) => i !== index),
    }))
  }

  const handleApiAssertionChange = (index: number, value: string) => {
    setFormData(prev => ({
      ...prev,
      api_assertions: prev.api_assertions.map((a, i) => i === index ? value : a),
    }))
  }

  const handleOpenSelector = async (index: number) => {
    setSelectorIndex(index)
    setOperationsLoading(true)
    setOperationsError(null)

    try {
      const response: OperationsResponse = await externalOperationsApi.list()
      setOperationsAvailable(response.available)
      if (!response.available) {
        setOperationsError(response.error || 'External module not available')
      }
      setSelectorOpen(true)
    } catch {
      setOperationsAvailable(false)
      setOperationsError('External precondition module not available. Please check WEBSERP_PATH configuration.')
    } finally {
      setOperationsLoading(false)
    }
  }

  const handleSelectorConfirm = async (selectedCodes: string[]) => {
    if (selectorIndex === null || selectedCodes.length === 0) return

    try {
      const response = await externalOperationsApi.generate(selectedCodes)
      const currentPrecondition = formData.preconditions[selectorIndex] || ''
      const newCode = response.code

      // Append code: if empty, insert directly; otherwise add newline first
      const updatedPrecondition = currentPrecondition.trim()
        ? currentPrecondition + '\n' + newCode
        : newCode

      handlePreconditionChange(selectorIndex, updatedPrecondition)
    } catch {
      // Error already shown by apiClient toast
    }

    setSelectorOpen(false)
    setSelectorIndex(null)
  }

  const handleSelectorCancel = () => {
    setSelectorOpen(false)
    setSelectorIndex(null)
  }

  const handleOpenDataSelector = async (index: number) => {
    setDataSelectorIndex(index)
    setDataMethodsLoading(true)
    setDataMethodsError(null)
    try {
      const response = await externalDataMethodsApi.list()
      setDataMethodsAvailable(response.available)
      if (!response.available) {
        setDataMethodsError(response.error || 'External data methods not available')
      }
      setDataSelectorOpen(true)
    } catch {
      setDataMethodsAvailable(false)
      setDataMethodsError('External data methods module not available. Please check WEBSERP_PATH configuration.')
    } finally {
      setDataMethodsLoading(false)
    }
  }

  const handleDataSelectorConfirm = (configs: DataMethodConfig[]) => {
    if (dataSelectorIndex === null || configs.length === 0) return

    // Generate code from configs
    const lines: string[] = []
    configs.forEach(config => {
      const params = Object.entries(config.parameters)
        .map(([k, v]) => `${k}=${typeof v === 'string' ? `'${v}'` : v}`)
        .join(', ')
      const methodCall = `context.get_data('${config.className}', '${config.methodName}', ${params})`

      config.extractions.forEach(ex => {
        // Convert path like "[0].imei" to Python accessor
        const pathAccess = ex.path
          .replace(/\[(\d+)\]/g, '[$1]')
          .replace(/\.([^.[]+)/g, "['$1']")
        lines.push(`${ex.variableName} = ${methodCall}${pathAccess}`)
      })
    })

    const newCode = lines.join('\n')
    const currentPrecondition = formData.preconditions[dataSelectorIndex] || ''
    const updatedPrecondition = currentPrecondition.trim()
      ? currentPrecondition + '\n' + newCode
      : newCode

    handlePreconditionChange(dataSelectorIndex, updatedPrecondition)
    setDataSelectorOpen(false)
    setDataSelectorIndex(null)
  }

  const handleDataSelectorCancel = () => {
    setDataSelectorOpen(false)
    setDataSelectorIndex(null)
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

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          前置条件 <span className="text-gray-400 text-xs">(可选)</span>
        </label>
        <p className="text-xs text-gray-500 mb-2">
          输入 Python 代码，在前置条件中通过 context['变量名'] 存储结果
        </p>
        <div className="space-y-2">
          {formData.preconditions.map((precondition, index) => (
            <div key={index} className="space-y-2">
              <div className="flex items-center gap-2 flex-wrap">
                <button
                  type="button"
                  onClick={() => handleOpenSelector(index)}
                  disabled={operationsLoading || !operationsAvailable}
                  className={`inline-flex items-center gap-1 px-3 py-1.5 text-sm rounded-lg border ${
                    operationsAvailable
                      ? 'border-blue-200 text-blue-600 hover:bg-blue-50 disabled:opacity-50'
                      : 'border-gray-200 text-gray-400 cursor-not-allowed'
                  }`}
                  title={operationsError || ''}
                >
                  {operationsLoading ? (
                    <span className="animate-spin w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full" />
                  ) : (
                    <Code className="w-4 h-4" />
                  )}
                  选择操作码
                </button>
                {!operationsAvailable && operationsError && (
                  <span className="flex items-center gap-1 text-xs text-gray-400">
                    <AlertCircle className="w-3 h-3" />
                    {operationsError}
                  </span>
                )}
                <button
                  type="button"
                  onClick={() => handleOpenDataSelector(index)}
                  disabled={dataMethodsLoading || !dataMethodsAvailable}
                  className={`inline-flex items-center gap-1 px-3 py-1.5 text-sm rounded-lg border ${
                    dataMethodsAvailable
                      ? 'border-green-200 text-green-600 hover:bg-green-50 disabled:opacity-50'
                      : 'border-gray-200 text-gray-400 cursor-not-allowed'
                  }`}
                  title={dataMethodsError || ''}
                >
                  {dataMethodsLoading ? (
                    <span className="animate-spin w-4 h-4 border-2 border-green-500 border-t-transparent rounded-full" />
                  ) : (
                    <Database className="w-4 h-4" />
                  )}
                  获取数据
                </button>
                {!dataMethodsAvailable && dataMethodsError && (
                  <span className="flex items-center gap-1 text-xs text-gray-400">
                    <AlertCircle className="w-3 h-3" />
                    {dataMethodsError}
                  </span>
                )}
              </div>
              <div className="flex gap-2">
                <textarea
                  value={precondition}
                  onChange={e => handlePreconditionChange(index, e.target.value)}
                  placeholder="例如：context['token'] = login_and_get_token()"
                  rows={4}
                  className="flex-1 px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none font-mono text-sm"
                />
                {formData.preconditions.length > 1 && (
                  <button
                    type="button"
                    onClick={() => handleRemovePrecondition(index)}
                    className="px-3 py-2 text-red-500 hover:bg-red-50 rounded-lg"
                  >
                    删除
                  </button>
                )}
              </div>
            </div>
          ))}
          <button
            type="button"
            onClick={handleAddPrecondition}
            className="text-sm text-blue-500 hover:text-blue-600"
          >
            + 添加前置条件
          </button>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          接口断言 <span className="text-gray-400 text-xs">(可选)</span>
        </label>
        <p className="text-xs text-gray-500 mb-2">
          输入 Python 代码进行 API 断言，支持时间断言、数据匹配等
        </p>
        <div className="space-y-2">
          {formData.api_assertions.map((assertion, index) => (
            <div key={index} className="flex gap-2">
              <textarea
                value={assertion}
                onChange={e => handleApiAssertionChange(index, e.target.value)}
                placeholder="例如：result = api.get_order({{order_id}}); assert result['status'] == 'success'"
                rows={4}
                className="flex-1 px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none font-mono text-sm"
              />
              {formData.api_assertions.length > 1 && (
                <button
                  type="button"
                  onClick={() => handleRemoveApiAssertion(index)}
                  className="px-3 py-2 text-red-500 hover:bg-red-50 rounded-lg"
                >
                  删除
                </button>
              )}
            </div>
          ))}
          <button
            type="button"
            onClick={handleAddApiAssertion}
            className="text-sm text-blue-500 hover:text-blue-600"
          >
            + 添加接口断言
          </button>
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

      {/* Operation Code Selector Modal */}
      <OperationCodeSelector
        open={selectorOpen}
        onConfirm={handleSelectorConfirm}
        onCancel={handleSelectorCancel}
      />

      {/* Data Method Selector Modal */}
      <DataMethodSelector
        open={dataSelectorOpen}
        onConfirm={handleDataSelectorConfirm}
        onCancel={handleDataSelectorCancel}
      />
    </form>
  )
}
