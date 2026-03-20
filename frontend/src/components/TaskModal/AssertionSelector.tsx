import { useState, useEffect, useMemo } from 'react'
import { X, Search, ChevronDown } from 'lucide-react'
import type { AssertionConfig, AssertionMethodsResponse, AssertionMethodInfo } from '../../types'
import { externalAssertionsApi } from '../../api/externalAssertions'
import { LoadingSpinner } from '../shared/LoadingSpinner'

interface AssertionSelectorProps {
  open: boolean
  onConfirm: (configs: AssertionConfig[]) => void
  onCancel: () => void
  initialConfigs?: AssertionConfig[]
}

export function AssertionSelector({
  open,
  onConfirm,
  onCancel,
  initialConfigs
}: AssertionSelectorProps) {
  const [methods, setMethods] = useState<AssertionMethodsResponse>({
    available: false,
    headers_options: [],
    classes: [],
    total: 0
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedKeys, setSelectedKeys] = useState<Set<string>>(new Set())
  const [expandedPanels, setExpandedPanels] = useState<Set<string>>(new Set())
  const [configs, setConfigs] = useState<Map<string, AssertionConfig>>(new Map())

  // Filter methods based on search query
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

  // Toggle panel expansion
  const togglePanel = (className: string) => {
    setExpandedPanels(prev => {
      const next = new Set(prev)
      if (next.has(className)) {
        next.delete(className)
      } else {
        next.add(className)
      }
      return next
    })
  }

  // Get method info by key
  const getMethodInfo = (className: string, methodName: string): AssertionMethodInfo | undefined => {
    const cls = methods.classes.find(c => c.name === className)
    return cls?.methods.find(m => m.name === methodName)
  }

  // Toggle method selection
  const toggleMethod = (className: string, methodName: string) => {
    const key = `${className}:${methodName}`
    setSelectedKeys(prev => {
      const next = new Set(prev)
      if (next.has(key)) {
        next.delete(key)
        // Remove config when deselected
        setConfigs(prevConfigs => {
          const nextConfigs = new Map(prevConfigs)
          nextConfigs.delete(key)
          return nextConfigs
        })
      } else {
        next.add(key)
        // Initialize config with defaults
        const method = getMethodInfo(className, methodName)
        setConfigs(prevConfigs => {
          const nextConfigs = new Map(prevConfigs)
          nextConfigs.set(key, {
            className,
            methodName,
            headers: methods.headers_options[0] || 'main',
            data: method?.data_options[0] || 'main',
            params: {}
          })
          return nextConfigs
        })
      }
      return next
    })
  }

  // Remove selected method
  const removeMethod = (key: string) => {
    setSelectedKeys(prev => {
      const next = new Set(prev)
      next.delete(key)
      return next
    })
    setConfigs(prev => {
      const next = new Map(prev)
      next.delete(key)
      return next
    })
  }

  // Update config for a method
  const updateConfig = (key: string, updates: Partial<AssertionConfig>) => {
    setConfigs(prev => {
      const next = new Map(prev)
      const existing = next.get(key)
      if (existing) {
        next.set(key, { ...existing, ...updates })
      }
      return next
    })
  }

  // Update parameter value
  const updateParam = (key: string, paramName: string, value: number | string) => {
    setConfigs(prev => {
      const next = new Map(prev)
      const existing = next.get(key)
      if (existing) {
        next.set(key, {
          ...existing,
          params: { ...existing.params, [paramName]: value }
        })
      }
      return next
    })
  }

  // Handle confirm
  const handleConfirm = () => {
    onConfirm(Array.from(configs.values()))
  }

  // Handle cancel
  const handleCancel = () => {
    onCancel()
  }

  // Fetch methods when modal opens
  useEffect(() => {
    if (!open) return

    const fetchMethods = async () => {
      setLoading(true)
      setError(null)
      try {
        const response = await externalAssertionsApi.list()
        if (!response.available) {
          setError(response.error || 'External assertion module not available')
        } else {
          setMethods(response)
          // Expand first class by default
          if (response.classes.length > 0) {
            setExpandedPanels(new Set([response.classes[0].name]))
          }
        }
      } catch {
        setError('External assertion module not available. Please check WEBSERP_PATH configuration.')
      } finally {
        setLoading(false)
      }
    }

    fetchMethods()

    // Initialize with initialConfigs if provided
    if (initialConfigs && initialConfigs.length > 0) {
      const newSelectedKeys = new Set<string>()
      const newConfigs = new Map<string, AssertionConfig>()
      initialConfigs.forEach(config => {
        const key = `${config.className}:${config.methodName}`
        newSelectedKeys.add(key)
        newConfigs.set(key, config)
      })
      setSelectedKeys(newSelectedKeys)
      setConfigs(newConfigs)
    } else {
      // Reset state when modal opens
      setSelectedKeys(new Set())
      setConfigs(new Map())
    }
    setSearchQuery('')
  }, [open, initialConfigs])

  // Handle Escape key to close modal
  useEffect(() => {
    if (!open) return

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        handleCancel()
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => {
      window.removeEventListener('keydown', handleKeyDown)
    }
  }, [open])

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black/50" onClick={handleCancel} />

      {/* Modal content */}
      <div className="relative bg-white rounded-xl shadow-xl w-full max-w-3xl mx-4 max-h-[80vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <h3 className="text-lg font-semibold text-gray-900">Select Assertion Methods</h3>
          <button
            type="button"
            onClick={handleCancel}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Search */}
        <div className="px-6 py-3 border-b border-gray-100">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="Search assertion methods..."
              className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
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

          {!loading && !error && !methods.available && (
            <div className="text-center py-8 text-gray-500">
              External assertion module is not available
            </div>
          )}

          {!loading && !error && methods.available && filteredClasses.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              No matching assertion methods found
            </div>
          )}

          {!loading && !error && methods.available && (
            <div className="space-y-2">
              {filteredClasses.map(cls => {
                const isExpanded = expandedPanels.has(cls.name)
                return (
                  <div key={cls.name} className="border border-gray-200 rounded-lg overflow-hidden">
                    <button
                      type="button"
                      onClick={() => togglePanel(cls.name)}
                      className="w-full flex items-center justify-between px-4 py-3 bg-gray-50 hover:bg-gray-100 transition-colors"
                    >
                      <span className="font-medium text-gray-700">{cls.name}</span>
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-gray-400">
                          {cls.methods.length} methods
                        </span>
                        <ChevronDown
                          className={`w-4 h-4 text-gray-400 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                        />
                      </div>
                    </button>
                    {isExpanded && (
                      <div className="space-y-1 p-2">
                        {cls.methods.map(m => {
                          const methodKey = `${cls.name}:${m.name}`
                          const isSelected = selectedKeys.has(methodKey)
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
                            </label>
                          )
                        })}
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          )}
        </div>

        {/* Selected items and configuration */}
        {selectedKeys.size > 0 && (
          <div className="px-6 py-4 border-t border-gray-100 bg-gray-50 max-h-[40vh] overflow-y-auto">
            <div className="text-sm text-gray-600 mb-3">Selected ({selectedKeys.size}):</div>

            {/* Tags display */}
            <div className="flex flex-wrap gap-2 mb-4">
              {Array.from(selectedKeys).map(key => {
                const [className, methodName] = key.split(':')
                return (
                  <span
                    key={key}
                    className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-700 rounded text-sm"
                  >
                    {className}.{methodName}
                    <button
                      type="button"
                      onClick={() => removeMethod(key)}
                      className="hover:text-blue-900"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                )
              })}
            </div>

            {/* Parameter configuration for each selected method */}
            <div className="space-y-4">
              {Array.from(selectedKeys).map(key => {
                const [className, methodName] = key.split(':')
                const config = configs.get(key)
                const method = getMethodInfo(className, methodName)

                if (!config || !method) return null

                return (
                  <div key={key} className="p-3 bg-white border border-gray-200 rounded-lg">
                    <h4 className="font-medium text-sm mb-3">
                      <span className="text-gray-500">{className}.</span>
                      {methodName}
                    </h4>

                    <div className="grid grid-cols-2 gap-3">
                      {/* Headers dropdown */}
                      <div>
                        <label className="block text-xs text-gray-500 mb-1">Headers</label>
                        <select
                          value={config.headers}
                          onChange={e => updateConfig(key, { headers: e.target.value })}
                          className="w-full px-2 py-1.5 border border-gray-200 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                          {methods.headers_options.map(opt => (
                            <option key={opt} value={opt}>{opt}</option>
                          ))}
                        </select>
                      </div>

                      {/* Data dropdown */}
                      <div>
                        <label className="block text-xs text-gray-500 mb-1">Data</label>
                        <select
                          value={config.data}
                          onChange={e => updateConfig(key, { data: e.target.value })}
                          className="w-full px-2 py-1.5 border border-gray-200 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                          {method.data_options.map(opt => (
                            <option key={opt} value={opt}>{opt}</option>
                          ))}
                        </select>
                      </div>
                    </div>

                    {/* i/j/k parameters */}
                    {method.parameters.length > 0 && (
                      <div className="mt-3 space-y-2">
                        <div className="text-xs text-gray-500">Filter Parameters</div>
                        <div className="grid grid-cols-3 gap-2">
                          {method.parameters.map(param => (
                            <div key={param.name}>
                              <label className="block text-xs text-gray-400 mb-0.5">
                                {param.name}
                                {param.description && (
                                  <span className="ml-1" title={param.description}>?</span>
                                )}
                              </label>
                              {param.options.length > 0 ? (
                                <select
                                  value={config.params[param.name] ?? ''}
                                  onChange={e => updateParam(key, param.name, e.target.value)}
                                  className="w-full px-2 py-1 border border-gray-200 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                >
                                  <option value="">Select...</option>
                                  {param.options.map(opt => (
                                    <option key={opt.value} value={opt.value}>
                                      {opt.label}
                                    </option>
                                  ))}
                                </select>
                              ) : (
                                <input
                                  type="number"
                                  value={config.params[param.name] ?? ''}
                                  onChange={e => updateParam(key, param.name, parseInt(e.target.value) || 0)}
                                  placeholder={param.name}
                                  className="w-full px-2 py-1 border border-gray-200 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                />
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="flex justify-end gap-3 px-6 py-4 border-t border-gray-100">
          <button
            type="button"
            onClick={handleCancel}
            className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={handleConfirm}
            disabled={selectedKeys.size === 0}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            Confirm ({selectedKeys.size})
          </button>
        </div>
      </div>
    </div>
  )
}
