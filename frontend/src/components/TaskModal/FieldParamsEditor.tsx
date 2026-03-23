import { useState, useEffect, useMemo } from 'react'
import { Search, ChevronDown, Clock } from 'lucide-react'
import type { AssertionFieldInfo, AssertionFieldGroup } from '../../types'
import { externalAssertionsApi } from '../../api/externalAssertions'
import { LoadingSpinner } from '../shared/LoadingSpinner'

// Time offset presets for time fields
const TIME_PRESETS = [
  { value: 'now', label: 'now (当前时间)' },
  { value: 'now-1m', label: 'now-1m (1分钟前)' },
  { value: 'now-3m', label: 'now-3m (3分钟前)' },
  { value: 'now-5m', label: 'now-5m (5分钟前)' },
  { value: 'now-10m', label: 'now-10m (10分钟前)' },
  { value: 'now+1m', label: 'now+1m (1分钟后)' },
  { value: 'now+5m', label: 'now+5m (5分钟后)' },
  { value: 'now-1h', label: 'now-1h (1小时前)' },
  { value: 'now-1d', label: 'now-1d (1天前)' },
]

interface FieldParamsEditorProps {
  selectedFields: Map<string, { name: string; value: string }>
  onChange: (updater: (prev: Map<string, { name: string; value: string }>) => Map<string, { name: string; value: string }>) => void
}

export function FieldParamsEditor({
  selectedFields,
  onChange
}: FieldParamsEditorProps) {
  const [groups, setGroups] = useState<AssertionFieldGroup[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [expandedPanels, setExpandedPanels] = useState<Set<string>>(new Set())

  // Fetch fields on mount
  useEffect(() => {
    const fetchFields = async () => {
      setLoading(true)
      setError(null)
      try {
        const response = await externalAssertionsApi.listFields()
        if (!response.available) {
          setError(response.error || 'External assertion fields not available')
        } else {
          setGroups(response.groups)
          // Expand first group by default
          if (response.groups.length > 0) {
            setExpandedPanels(new Set([response.groups[0].name]))
          }
        }
      } catch {
        setError('Failed to load fields')
      } finally {
        setLoading(false)
      }
    }
    fetchFields()
  }, [])

  // Filter groups based on search query
  const filteredGroups = useMemo(() => {
    if (!searchQuery.trim()) return groups

    const query = searchQuery.toLowerCase()
    return groups
      .map(group => ({
        ...group,
        fields: group.fields.filter(
          f => f.name.toLowerCase().includes(query) ||
               f.description.toLowerCase().includes(query)
        )
      }))
      .filter(group => group.fields.length > 0)
  }, [groups, searchQuery])

  // Toggle panel expansion
  const togglePanel = (groupName: string) => {
    setExpandedPanels(prev => {
      const next = new Set(prev)
      if (next.has(groupName)) {
        next.delete(groupName)
      } else {
        next.add(groupName)
      }
      return next
    })
  }

  // Check if a field is selected
  const isFieldSelected = (fieldName: string) => selectedFields.has(fieldName)

  // Toggle field selection
  const toggleField = (field: AssertionFieldInfo) => {
    onChange(prev => {
      const next = new Map(prev)
      if (next.has(field.name)) {
        next.delete(field.name)
      } else {
        next.set(field.name, { name: field.name, value: '' })
      }
      return next
    })
  }

  // Update field value
  const updateFieldValue = (fieldName: string, value: string) => {
    onChange(prev => {
      const next = new Map(prev)
      const existing = next.get(fieldName)
      if (existing) {
        next.set(fieldName, { ...existing, value })
      }
      return next
    })
  }

  return (
    <div className="space-y-3">
      {/* Search input */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input
          type="text"
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          placeholder="Search fields..."
          className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
        />
      </div>

      {/* Content */}
      {loading && (
        <div className="flex items-center justify-center py-8">
          <LoadingSpinner size="md" />
        </div>
      )}

      {error && !loading && (
        <div className="text-center py-4 text-red-500 text-sm">
          {error}
        </div>
      )}

      {!loading && !error && filteredGroups.length === 0 && (
        <div className="text-center py-4 text-gray-500 text-sm">
          {searchQuery.trim() ? 'No matching fields found' : 'No fields available'}
        </div>
      )}

      {/* Grouped field list */}
      {!loading && !error && filteredGroups.length > 0 && (
        <div className="space-y-2 max-h-[300px] overflow-y-auto">
          {filteredGroups.map(group => {
            const isExpanded = expandedPanels.has(group.name)
            return (
              <div key={group.name} className="border border-gray-200 rounded-lg overflow-hidden">
                <button
                  type="button"
                  onClick={() => togglePanel(group.name)}
                  className="w-full flex items-center justify-between px-3 py-2 bg-gray-50 hover:bg-gray-100 transition-colors"
                >
                  <span className="font-medium text-sm text-gray-700">{group.name}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-gray-400">
                      {group.fields.length}
                    </span>
                    <ChevronDown
                      className={`w-4 h-4 text-gray-400 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                    />
                  </div>
                </button>
                {isExpanded && (
                  <div className="p-2 space-y-1">
                    {group.fields.map(field => {
                      const isSelected = isFieldSelected(field.name)
                      const selectedField = selectedFields.get(field.name)
                      return (
                        <div key={field.name} className="p-2 rounded-lg hover:bg-gray-50">
                          <label className="flex items-center gap-2 cursor-pointer">
                            <input
                              type="checkbox"
                              checked={isSelected}
                              onChange={() => toggleField(field)}
                              className="w-4 h-4 rounded border-gray-300 text-blue-500 focus:ring-blue-500"
                            />
                            <span className="font-mono text-xs text-blue-600">{field.name}</span>
                            <span className="text-xs text-gray-500 flex-1">{field.description}</span>
                          </label>
                          {isSelected && (
                            <div className="mt-2 ml-6 space-y-2">
                              <div className="flex items-center gap-2">
                                <input
                                  type="text"
                                  value={selectedField?.value || ''}
                                  onChange={e => updateFieldValue(field.name, e.target.value)}
                                  placeholder="Expected value"
                                  className="flex-1 px-2 py-1 border border-gray-200 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                />
                              </div>
                              {field.is_time_field && (
                                <div className="flex items-center gap-2">
                                  <Clock className="w-3 h-3 text-gray-400" />
                                  <select
                                    value={TIME_PRESETS.some(p => p.value === selectedField?.value) ? selectedField?.value : ''}
                                    onChange={e => {
                                      if (e.target.value) {
                                        updateFieldValue(field.name, e.target.value)
                                      }
                                    }}
                                    className="text-xs px-2 py-1 border border-gray-200 rounded bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                                  >
                                    <option value="">选择时间预设...</option>
                                    {TIME_PRESETS.map(preset => (
                                      <option key={preset.value} value={preset.value}>
                                        {preset.label}
                                      </option>
                                    ))}
                                  </select>
                                  <span className="text-xs text-gray-400">或输入自定义值</span>
                                </div>
                              )}
                            </div>
                          )}
                        </div>
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
  )
}
