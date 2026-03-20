import { useState, useEffect, useMemo } from 'react'
import { X, Search } from 'lucide-react'
import type { ModuleGroup } from '../../types'
import { externalOperationsApi } from '../../api/externalOperations'
import { LoadingSpinner } from '../shared/LoadingSpinner'

interface OperationCodeSelectorProps {
  open: boolean
  onConfirm: (selectedCodes: string[]) => void
  onCancel: () => void
}

export function OperationCodeSelector({ open, onConfirm, onCancel }: OperationCodeSelectorProps) {
  const [modules, setModules] = useState<ModuleGroup[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCodes, setSelectedCodes] = useState<Set<string>>(new Set())

  // Fetch operations when modal opens
  useEffect(() => {
    if (!open) return

    const fetchOperations = async () => {
      setLoading(true)
      setError(null)
      try {
        const response = await externalOperationsApi.list()
        if (!response.available) {
          setError(response.error || 'External module not available')
        } else {
          setModules(response.modules)
        }
      } catch {
        // 503 or other errors
        setError('External precondition module not available. Please check WEBSERP_PATH configuration.')
      } finally {
        setLoading(false)
      }
    }

    fetchOperations()
    // Reset selection when modal opens
    setSelectedCodes(new Set())
    setSearchQuery('')
  }, [open])

  // Handle Escape key to close modal
  useEffect(() => {
    if (!open) return

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onCancel()
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => {
      window.removeEventListener('keydown', handleKeyDown)
    }
  }, [open, onCancel])

  // Filter modules based on search query
  const filteredModules = useMemo(() => {
    if (!searchQuery.trim()) return modules

    const query = searchQuery.toLowerCase()
    return modules
      .map(module => ({
        ...module,
        operations: module.operations.filter(
          op => op.code.toLowerCase().includes(query) ||
                op.description.toLowerCase().includes(query)
        )
      }))
      .filter(module => module.operations.length > 0)
  }, [modules, searchQuery])

  const toggleCode = (code: string) => {
    setSelectedCodes(prev => {
      const next = new Set(prev)
      if (next.has(code)) {
        next.delete(code)
      } else {
        next.add(code)
      }
      return next
    })
  }

  const removeCode = (code: string) => {
    setSelectedCodes(prev => {
      const next = new Set(prev)
      next.delete(code)
      return next
    })
  }

  const handleConfirm = () => {
    onConfirm(Array.from(selectedCodes))
  }

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black/50" onClick={onCancel} />

      {/* Modal content */}
      <div className="relative bg-white rounded-xl shadow-xl w-full max-w-2xl mx-4 max-h-[80vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <h3 className="text-lg font-semibold text-gray-900">Select Operation Codes</h3>
          <button
            onClick={onCancel}
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
              placeholder="Search by code or description..."
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

          {!loading && !error && filteredModules.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              No matching operation codes found
            </div>
          )}

          {!loading && !error && filteredModules.map(module => (
            <div key={module.name} className="mb-4">
              <h4 className="text-sm font-medium text-gray-700 mb-2">{module.name}</h4>
              <div className="space-y-1">
                {module.operations.map(op => (
                  <label
                    key={op.code}
                    className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50 cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      checked={selectedCodes.has(op.code)}
                      onChange={() => toggleCode(op.code)}
                      className="w-4 h-4 rounded border-gray-300 text-blue-500 focus:ring-blue-500"
                    />
                    <span className="font-mono text-sm text-blue-600">{op.code}</span>
                    <span className="text-sm text-gray-600">{op.description}</span>
                  </label>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Selected items */}
        {selectedCodes.size > 0 && (
          <div className="px-6 py-3 border-t border-gray-100 bg-gray-50">
            <div className="text-sm text-gray-600 mb-2">Selected ({selectedCodes.size}):</div>
            <div className="flex flex-wrap gap-2">
              {Array.from(selectedCodes).map(code => (
                <span
                  key={code}
                  className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-700 rounded text-sm"
                >
                  {code}
                  <button
                    onClick={() => removeCode(code)}
                    className="hover:text-blue-900"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="flex justify-end gap-3 px-6 py-4 border-t border-gray-100">
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={handleConfirm}
            disabled={selectedCodes.size === 0}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            Confirm ({selectedCodes.size})
          </button>
        </div>
      </div>
    </div>
  )
}
