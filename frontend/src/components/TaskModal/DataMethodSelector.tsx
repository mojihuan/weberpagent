import { useState, useEffect, useMemo } from 'react'
import { X, Check, ChevronLeft, ChevronRight, Search, Play } from 'lucide-react'
import type { DataMethodConfig, DataMethodsResponse } from '../../types'
import { externalDataMethodsApi } from '../../api/externalDataMethods'
import { LoadingSpinner } from '../shared/LoadingSpinner'
import { JsonTreeViewer } from './JsonTreeViewer'

const STEPS = ['Select Method', 'Configure Parameters', 'Extraction Path', 'Variable Naming'] as const

interface DataMethodSelectorProps {
  open: boolean
  onConfirm: (configs: DataMethodConfig[]) => void
  onCancel: () => void
}

export function DataMethodSelector({ open, onConfirm, onCancel }: DataMethodSelectorProps) {
  const [currentStep, setCurrentStep] = useState(0)
  const [methods, setMethods] = useState<DataMethodsResponse>({ available: false, classes: [], total: 0 })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Step 1 state: search and multi-select
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedMethodKeys, setSelectedMethodKeys] = useState<Set<string>>(new Set())
  // Key format: "className:methodName"

  // Step 2 state: method configurations with parameters
  const [methodConfigs, setMethodConfigs] = useState<Map<string, DataMethodConfig>>(new Map())

  // Step 3 state: data preview
  const [previewData, setPreviewData] = useState<unknown>(null)
  const [previewLoading, setPreviewLoading] = useState(false)
  const [previewError, setPreviewError] = useState<string | null>(null)
  const [currentPreviewKey, setCurrentPreviewKey] = useState<string | null>(null)

  // Filter methods based on search query (following OperationCodeSelector pattern)
  const filteredClasses = useMemo(() => {
    if (!searchQuery.trim()) return methods.classes
    const query = searchQuery.toLowerCase()
    return methods.classes
      .map(cls => ({
        ...cls,
        methods: cls.methods.filter(
          m => m.name.toLowerCase().includes(query) ||
               m.description.toLowerCase().includes(query)
        )
      }))
      .filter(cls => cls.methods.length > 0)
  }, [methods.classes, searchQuery])

  // Toggle method selection
  const toggleMethod = (className: string, methodName: string) => {
    const key = `${className}:${methodName}`
    setSelectedMethodKeys(prev => {
      const next = new Set(prev)
      if (next.has(key)) {
        next.delete(key)
      } else {
        next.add(key)
      }
      return next
    })
  }

  // Remove a selected method
  const removeMethod = (key: string) => {
    setSelectedMethodKeys(prev => {
      const next = new Set(prev)
      next.delete(key)
      return next
    })
  }

  // Update a parameter value for a method config
  const updateParameter = (key: string, paramName: string, value: any) => {
    setMethodConfigs(prev => {
      const next = new Map(prev)
      const config = next.get(key)
      if (config) {
        next.set(key, {
          ...config,
          parameters: { ...config.parameters, [paramName]: value }
        })
      }
      return next
    })
  }

  // Check if all required parameters are filled for Step 2 validation
  const hasAllRequiredParams = (): boolean => {
    for (const key of selectedMethodKeys) {
      const [className, methodName] = key.split(':')
      const cls = methods.classes.find(c => c.name === className)
      const method = cls?.methods.find(m => m.name === methodName)
      const config = methodConfigs.get(key)

      if (!method || !config) return false

      for (const param of method.parameters) {
        if (param.required) {
          const value = config.parameters[param.name]
          if (value === undefined || value === null || value === '') {
            return false
          }
        }
      }
    }
    return true
  }

  // Step 3: Preview data function
  const previewMethodData = async (key: string) => {
    const config = methodConfigs.get(key)
    if (!config) return

    setCurrentPreviewKey(key)
    setPreviewLoading(true)
    setPreviewError(null)
    try {
      const response = await externalDataMethodsApi.execute(
        config.className,
        config.methodName,
        config.parameters
      )
      if (response.success) {
        setPreviewData(response.data)
      } else {
        setPreviewError(response.error || 'Execution failed')
      }
    } catch {
      setPreviewError('Failed to execute method')
    } finally {
      setPreviewLoading(false)
    }
  }

  // Step 3: Add field extraction
  const addExtraction = (key: string, path: string) => {
    setMethodConfigs(prev => {
      const next = new Map(prev)
      const config = next.get(key)
      if (config) {
        // Extract default variable name from path (last segment)
        const segments = path.split(/[.\[\]]/).filter(Boolean)
        const defaultName = segments[segments.length - 1] || 'value'
        // Check if path already exists
        if (!config.extractions.some(e => e.path === path)) {
          next.set(key, {
            ...config,
            extractions: [...config.extractions, { path, variableName: defaultName }]
          })
        }
      }
      return next
    })
  }

  // Step 3: Remove field extraction
  const removeExtraction = (key: string, index: number) => {
    setMethodConfigs(prev => {
      const next = new Map(prev)
      const config = next.get(key)
      if (config) {
        next.set(key, {
          ...config,
          extractions: config.extractions.filter((_, i) => i !== index)
        })
      }
      return next
    })
  }

  // Step 4: Update variable name for an extraction
  const updateVariableName = (key: string, extractionIndex: number, newName: string) => {
    setMethodConfigs(prev => {
      const next = new Map(prev)
      const config = next.get(key)
      if (config) {
        const newExtractions = [...config.extractions]
        newExtractions[extractionIndex] = {
          ...newExtractions[extractionIndex],
          variableName: newName
        }
        next.set(key, { ...config, extractions: newExtractions })
      }
      return next
    })
  }

  // Step 4: Detect duplicate variable names
  const getVariableConflicts = (): Set<string> => {
    const allNames: string[] = []
    const conflicts = new Set<string>()
    methodConfigs.forEach(config => {
      config.extractions.forEach(ex => {
        if (allNames.includes(ex.variableName)) {
          conflicts.add(ex.variableName)
        }
        allNames.push(ex.variableName)
      })
    })
    return conflicts
  }

  // Step 4: Generate Python code preview
  const generateCode = (): string => {
    const lines: string[] = []
    methodConfigs.forEach(config => {
      if (config.extractions.length === 0) return

      const params = Object.entries(config.parameters)
        .map(([k, v]) => `${k}=${typeof v === 'string' ? `'${v}'` : v}`)
        .join(', ')
      const methodCall = `context.get_data('${config.methodName}', ${params})`

      config.extractions.forEach(ex => {
        const pathAccess = ex.path
          .replace(/\[(\d+)\]/g, '[$1]')
          .replace(/\.([^.[]+)/g, "['$1']")
        lines.push(`${ex.variableName} = ${methodCall}${pathAccess}`)
      })
    })
    return lines.join('\n')
  }

  // Fetch methods when modal opens
  useEffect(() => {
    if (!open) return

    const fetchMethods = async () => {
      setLoading(true)
      setError(null)
      try {
        const response = await externalDataMethodsApi.list()
        if (!response.available) {
          setError(response.error || 'External module not available')
        } else {
          setMethods(response)
        }
      } catch {
        setError('External data methods module not available. Please check WEBSERP_PATH configuration.')
      } finally {
        setLoading(false)
      }
    }

    fetchMethods()
    // Reset state when modal opens
    setCurrentStep(0)
    setPreviewData(null)
    setPreviewError(null)
    setCurrentPreviewKey(null)
    setSelectedMethodKeys(new Set())
    setSearchQuery('')
    setMethodConfigs(new Map())
  }, [open])

  const handleCancel = () => {
    onCancel()
  }

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleNext = () => {
    if (currentStep < STEPS.length - 1) {
      // Initialize configs when moving from Step 1 to Step 2
      if (currentStep === 0) {
        const newConfigs = new Map(methodConfigs)
        selectedMethodKeys.forEach(key => {
          if (!newConfigs.has(key)) {
            const [className, methodName] = key.split(':')
            const cls = methods.classes.find(c => c.name === className)
            const method = cls?.methods.find(m => m.name === methodName)
            const params: Record<string, any> = {}
            method?.parameters.forEach(p => {
              if (p.default !== null) {
                params[p.name] = p.type === 'int' ? parseInt(p.default) : p.default
              }
            })
            newConfigs.set(key, {
              className,
              methodName,
              parameters: params,
              extractions: []
            })
          }
        })
        setMethodConfigs(newConfigs)
      }
      setCurrentStep(currentStep + 1)
    }
  }

  const handleConfirm = () => {
    const configs: DataMethodConfig[] = Array.from(methodConfigs.values())
    onConfirm(configs)
  }

  const goToStep = (step: number) => {
    if (step >= 0 && step < STEPS.length) {
      setCurrentStep(step)
    }
  }

  const renderStepContent = () => {
    switch (currentStep) {
      case 0:
        // Step 1: Method Selection with search and multi-select
        return (
          <>
            {/* Search input */}
            <div className="mb-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  placeholder="Search by method name or description..."
                  className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            {/* Empty state */}
            {!loading && !error && filteredClasses.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                No matching data methods found
              </div>
            )}

            {/* Grouped list of methods */}
            {!loading && !error && filteredClasses.map(cls => (
              <div key={cls.name} className="mb-4">
                <h4 className="text-sm font-medium text-gray-700 mb-2">{cls.name}</h4>
                <div className="space-y-1">
                  {cls.methods.map(m => {
                    const methodKey = `${cls.name}:${m.name}`
                    const isSelected = selectedMethodKeys.has(methodKey)
                    return (
                      <label
                        key={methodKey}
                        className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50 cursor-pointer"
                      >
                        <input
                          type="checkbox"
                          checked={isSelected}
                          onChange={() => toggleMethod(cls.name, m.name)}
                          className="w-4 h-4 rounded border-gray-300 text-blue-500 focus:ring-blue-500"
                        />
                        <span className="font-mono text-sm text-blue-600">{m.name}</span>
                        <span className="text-sm text-gray-600 flex-1">{m.description}</span>
                        <span className="text-xs text-gray-400 bg-gray-100 px-2 py-0.5 rounded">
                          {m.parameters.length} params
                        </span>
                      </label>
                    )
                  })}
                </div>
              </div>
            ))}

            {/* Selected count display */}
            {selectedMethodKeys.size > 0 && (
              <div className="mt-4 pt-4 border-t border-gray-100">
                <div className="text-sm text-gray-600 mb-2">Selected ({selectedMethodKeys.size}):</div>
                <div className="flex flex-wrap gap-2">
                  {Array.from(selectedMethodKeys).map(key => {
                    const [className, methodName] = key.split(':')
                    return (
                      <span
                        key={key}
                        className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-700 rounded text-sm"
                      >
                        {className}.{methodName}
                        <button
                          onClick={() => removeMethod(key)}
                          className="hover:text-blue-900"
                        >
                          <X className="w-3 h-3" />
                        </button>
                      </span>
                    )
                  })}
                </div>
              </div>
            )}
          </>
        )
      case 1:
        // Step 2: Parameter Configuration
        return (
          <div className="space-y-4">
            <p className="text-sm text-gray-600 mb-4">
              Configure parameters for each selected method. Required parameters are marked with *.
            </p>
            {Array.from(selectedMethodKeys).map(key => {
              const [className, methodName] = key.split(':')
              const cls = methods.classes.find(c => c.name === className)
              const method = cls?.methods.find(m => m.name === methodName)
              const config = methodConfigs.get(key)

              if (!method || !config) return null

              return (
                <div key={key} className="p-4 border border-gray-200 rounded-lg">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-medium">
                      <span className="text-gray-500 text-sm">{className}.</span>
                      {methodName}
                    </h4>
                    {method.description && (
                      <span className="text-xs text-gray-400">{method.description}</span>
                    )}
                  </div>
                  {method.parameters.length === 0 ? (
                    <p className="text-sm text-gray-500 italic">No parameters required</p>
                  ) : (
                    <div className="space-y-3">
                      {method.parameters.map(param => (
                        <div key={param.name} className="flex items-center gap-3">
                          <label className="w-32 text-sm text-gray-700 flex-shrink-0">
                            {param.name}
                            {param.required && <span className="text-red-500 ml-1">*</span>}
                          </label>
                          <input
                            type={param.type === 'int' ? 'number' : 'text'}
                            value={config.parameters[param.name] ?? ''}
                            onChange={e => updateParameter(
                              key,
                              param.name,
                              param.type === 'int' ? parseInt(e.target.value) || 0 : e.target.value
                            )}
                            placeholder={param.type}
                            className="flex-1 px-3 py-1.5 border border-gray-200 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                          />
                          {param.default !== null && (
                            <span className="text-xs text-gray-400">
                              default: {param.default}
                            </span>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        )
      case 2:
        // Step 3: Data Preview and Field Extraction
        return (
          <div className="space-y-4">
            <p className="text-sm text-gray-600 mb-4">
              Preview data by executing the method, then click on fields to select them for extraction.
            </p>
            {Array.from(selectedMethodKeys).map(key => {
              const config = methodConfigs.get(key)
              const isCurrentPreview = currentPreviewKey === key

              if (!config) return null

              return (
                <div key={key} className="p-4 border border-gray-200 rounded-lg">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-medium">
                      <span className="text-gray-500 text-sm">{config.className}.</span>
                      {config.methodName}
                    </h4>
                    <button
                      onClick={() => previewMethodData(key)}
                      disabled={previewLoading && isCurrentPreview}
                      className="flex items-center gap-1 px-3 py-1.5 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
                    >
                      <Play className="w-4 h-4" />
                      {previewLoading && isCurrentPreview ? 'Loading...' : 'Preview Data'}
                    </button>
                  </div>

                  {isCurrentPreview && previewError && (
                    <div className="text-red-500 text-sm mb-2 p-2 bg-red-50 rounded">
                      {previewError}
                    </div>
                  )}

                  {isCurrentPreview && previewData && (
                    <>
                      <div className="border border-gray-100 rounded p-2 mb-3 bg-gray-50 max-h-64 overflow-auto">
                        <JsonTreeViewer
                          data={previewData}
                          onFieldClick={(path) => addExtraction(key, path)}
                          selectedPaths={config.extractions.map(e => e.path)}
                        />
                      </div>
                      <div className="text-xs text-gray-500 mb-2">
                        Click on a field value to extract it
                      </div>
                    </>
                  )}

                  {config.extractions.length > 0 && (
                    <div className="space-y-2 mt-3">
                      <div className="text-sm font-medium text-gray-700">Selected fields:</div>
                      {config.extractions.map((extraction, idx) => (
                        <div key={idx} className="flex items-center gap-2 text-sm">
                          <code className="bg-gray-100 px-2 py-1 rounded">{extraction.path}</code>
                          <span className="text-gray-400">-&gt;</span>
                          <code className="text-blue-600">{extraction.variableName}</code>
                          <button
                            onClick={() => removeExtraction(key, idx)}
                            className="text-red-400 hover:text-red-600 ml-auto"
                          >
                            <X className="w-4 h-4" />
                          </button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        )
      case 3:
        // Step 4: Variable Naming and Code Preview
        const conflicts = getVariableConflicts()
        const hasExtractions = Array.from(methodConfigs.values()).some(c => c.extractions.length > 0)

        return (
          <div className="space-y-4">
            <p className="text-sm text-gray-600 mb-4">
              Review and edit variable names for extracted fields. Duplicate names are highlighted.
            </p>

            {!hasExtractions && (
              <div className="text-center py-8 text-gray-500">
                No fields selected for extraction. Go back to Step 3 to select fields.
              </div>
            )}

            {Array.from(methodConfigs.entries()).map(([key, config]) => {
              if (config.extractions.length === 0) return null

              return (
                <div key={key} className="p-4 border border-gray-200 rounded-lg">
                  <h4 className="font-medium mb-3">
                    <span className="text-gray-500 text-sm">{config.className}.</span>
                    {config.methodName}
                  </h4>
                  <div className="space-y-2">
                    {config.extractions.map((ex, idx) => {
                      const hasConflict = conflicts.has(ex.variableName)
                      return (
                        <div key={idx} className="flex items-center gap-3">
                          <code className="bg-gray-100 px-2 py-1 rounded text-sm flex-shrink-0 max-w-[200px] truncate" title={ex.path}>
                            {ex.path}
                          </code>
                          <span className="text-gray-400">=</span>
                          <input
                            type="text"
                            value={ex.variableName}
                            onChange={e => updateVariableName(key, idx, e.target.value)}
                            className={`flex-1 px-2 py-1 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                              hasConflict ? 'border-yellow-400 bg-yellow-50' : 'border-gray-200'
                            }`}
                          />
                          {hasConflict && (
                            <span className="text-xs text-yellow-600 flex-shrink-0">
                              Duplicate name
                            </span>
                          )}
                        </div>
                      )
                    })}
                  </div>
                </div>
              )
            })}

            {/* Code Preview */}
            {hasExtractions && (
              <div className="mt-4 p-4 bg-gray-900 rounded-lg">
                <div className="text-gray-400 text-sm mb-2">Generated Code:</div>
                <pre className="text-green-400 font-mono text-sm whitespace-pre-wrap overflow-auto">
                  {generateCode()}
                </pre>
              </div>
            )}
          </div>
        )
      default:
        return null
    }
  }

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black/50" onClick={handleCancel} />

      {/* Modal content */}
      <div className="relative bg-white rounded-xl shadow-xl w-full max-w-3xl mx-4 max-h-[85vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <h3 className="text-lg font-semibold text-gray-900">Select Data Method</h3>
          <button
            onClick={handleCancel}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Step bar */}
        <div className="flex items-center justify-center gap-2 px-4 py-3 border-b border-gray-100 bg-gray-50">
          {STEPS.map((step, index) => {
            const isCompleted = index < currentStep
            const isCurrent = index === currentStep

            return (
              <button
                key={step}
                onClick={() => goToStep(index)}
                className="flex items-center gap-2 px-3 py-1.5 rounded-full transition-colors"
              >
                <span
                  className={`flex items-center justify-center w-6 h-6 rounded-full text-sm font-medium ${
                    isCompleted
                      ? 'bg-green-500 text-white'
                      : isCurrent
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-200 text-gray-600'
                  }`}
                >
                  {isCompleted ? <Check className="w-4 h-4" /> : index + 1}
                </span>
                <span
                  className={`text-sm ${
                    isCurrent ? 'text-blue-600 font-medium' : 'text-gray-500'
                  }`}
                >
                  {step}
                </span>
                {index < STEPS.length - 1 && (
                  <ChevronRight className="w-4 h-4 text-gray-300" />
                )}
              </button>
            )
          })}
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto px-6 py-4">
          {loading && (
            <div className="flex items-center justify-center py-8">
              <LoadingSpinner size="lg" />
            </div>
          )}

          {error && !loading && (
            <div className="text-center py-8 text-red-500">
              {error}
            </div>
          )}

          {!loading && !error && renderStepContent()}
        </div>

        {/* Footer */}
        <div className="flex justify-between gap-3 px-6 py-4 border-t border-gray-100">
          <div className="flex gap-3">
            <button
              onClick={handleCancel}
              className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
            >
              Cancel
            </button>
          </div>
          <div className="flex gap-3">
            {currentStep > 0 && (
              <button
                onClick={handlePrevious}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg flex items-center gap-1"
              >
                <ChevronLeft className="w-4 h-4" />
                Previous
              </button>
            )}
            {currentStep < STEPS.length - 1 && (
              <button
                onClick={handleNext}
                disabled={
                  (currentStep === 0 && selectedMethodKeys.size === 0) ||
                  (currentStep === 1 && !hasAllRequiredParams())
                }
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1"
              >
                Next
                <ChevronRight className="w-4 h-4" />
              </button>
            )}
            {currentStep === STEPS.length - 1 && (
              <button
                onClick={handleConfirm}
                disabled={selectedMethodKeys.size === 0 || !Array.from(methodConfigs.values()).some(c => c.extractions.length > 0)}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
              >
                Confirm
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
