import { useState } from 'react'
import { ChevronRight, ChevronDown, Check } from 'lucide-react'

interface JsonTreeViewerProps {
  data: unknown
  onFieldClick?: (path: string, value: unknown) => void
  selectedPaths?: string[]
  maxDepth?: number
}

interface JsonNodeProps {
  value: unknown
  path: string
  depth: number
  maxDepth: number
  onFieldClick?: (path: string, value: unknown) => void
  selectedPaths: string[]
  expandedPaths: Set<string>
  toggleExpand: (path: string) => void
}

function JsonNode({
  value,
  path,
  depth,
  maxDepth,
  onFieldClick,
  selectedPaths,
  expandedPaths,
  toggleExpand,
}: JsonNodeProps): JSX.Element {
  if (depth > maxDepth) {
    return <span className="text-gray-400">...</span>
  }

  const isSelected = selectedPaths.includes(path)

  // Handle null
  if (value === null) {
    return (
      <span
        className={`text-gray-400 cursor-pointer hover:bg-gray-100 px-0.5 rounded ${isSelected ? 'bg-blue-50' : ''}`}
        onClick={() => onFieldClick?.(path, null)}
      >
        null {isSelected && <Check className="inline w-3 h-3 text-blue-500 ml-1" />}
      </span>
    )
  }

  // Handle boolean
  if (typeof value === 'boolean') {
    return (
      <span
        className={`text-orange-600 cursor-pointer hover:bg-gray-100 px-0.5 rounded ${isSelected ? 'bg-blue-50' : ''}`}
        onClick={() => onFieldClick?.(path, value)}
      >
        {value.toString()} {isSelected && <Check className="inline w-3 h-3 text-blue-500 ml-1" />}
      </span>
    )
  }

  // Handle number
  if (typeof value === 'number') {
    return (
      <span
        className={`text-blue-600 cursor-pointer hover:bg-gray-100 px-0.5 rounded ${isSelected ? 'bg-blue-50' : ''}`}
        onClick={() => onFieldClick?.(path, value)}
      >
        {value} {isSelected && <Check className="inline w-3 h-3 text-blue-500 ml-1" />}
      </span>
    )
  }

  // Handle string
  if (typeof value === 'string') {
    return (
      <span
        className={`text-green-600 cursor-pointer hover:bg-gray-100 px-0.5 rounded ${isSelected ? 'bg-blue-50' : ''}`}
        onClick={() => onFieldClick?.(path, value)}
      >
        &quot;{value}&quot; {isSelected && <Check className="inline w-3 h-3 text-blue-500 ml-1" />}
      </span>
    )
  }

  // Handle array
  if (Array.isArray(value)) {
    const isExpanded = expandedPaths.has(path)

    if (value.length === 0) {
      return <span className="text-gray-500">[]</span>
    }

    return (
      <span>
        <span
          className="cursor-pointer hover:bg-gray-100 px-0.5 rounded"
          onClick={() => toggleExpand(path)}
        >
          {isExpanded ? (
            <ChevronDown className="inline w-4 h-4 text-gray-400" />
          ) : (
            <ChevronRight className="inline w-4 h-4 text-gray-400" />
          )}
          <span className="text-gray-500">[</span>
          {!isExpanded && <span className="text-gray-400">{value.length} items...</span>}
        </span>
        {isExpanded && (
          <span>
            {value.map((item, index) => (
              <div key={index} className="ml-4">
                <span className="text-purple-600 select-none">[{index}]</span>
                <span className="text-gray-500">: </span>
                <JsonNode
                  value={item}
                  path={`${path}[${index}]`}
                  depth={depth + 1}
                  maxDepth={maxDepth}
                  onFieldClick={onFieldClick}
                  selectedPaths={selectedPaths}
                  expandedPaths={expandedPaths}
                  toggleExpand={toggleExpand}
                />
              </div>
            ))}
            <span className="text-gray-500 ml-4">]</span>
          </span>
        )}
        {!isExpanded && <span className="text-gray-500">]</span>}
      </span>
    )
  }

  // Handle object
  if (typeof value === 'object') {
    const isExpanded = expandedPaths.has(path)
    const entries = Object.entries(value as Record<string, unknown>)

    if (entries.length === 0) {
      return <span className="text-gray-500">{'{}'}</span>
    }

    return (
      <span>
        <span
          className="cursor-pointer hover:bg-gray-100 px-0.5 rounded"
          onClick={() => toggleExpand(path)}
        >
          {isExpanded ? (
            <ChevronDown className="inline w-4 h-4 text-gray-400" />
          ) : (
            <ChevronRight className="inline w-4 h-4 text-gray-400" />
          )}
          <span className="text-gray-500">{'{'}</span>
          {!isExpanded && <span className="text-gray-400">{entries.length} keys...</span>}
        </span>
        {isExpanded && (
          <span>
            {entries.map(([key, val]) => (
              <div key={key} className="ml-4">
                <span className="text-purple-600">{key}</span>
                <span className="text-gray-500">: </span>
                <JsonNode
                  value={val}
                  path={path ? `${path}.${key}` : key}
                  depth={depth + 1}
                  maxDepth={maxDepth}
                  onFieldClick={onFieldClick}
                  selectedPaths={selectedPaths}
                  expandedPaths={expandedPaths}
                  toggleExpand={toggleExpand}
                />
              </div>
            ))}
            <span className="text-gray-500 ml-4">{'}'}</span>
          </span>
        )}
        {!isExpanded && <span className="text-gray-500">{'}'}</span>}
      </span>
    )
  }

  // Fallback for unknown types
  return <span className="text-gray-400">{String(value)}</span>
}

export function JsonTreeViewer({
  data,
  onFieldClick,
  selectedPaths = [],
  maxDepth = 10,
}: JsonTreeViewerProps): JSX.Element {
  const [expandedPaths, setExpandedPaths] = useState<Set<string>>(new Set(['']))

  const toggleExpand = (path: string) => {
    setExpandedPaths(prev => {
      const next = new Set(prev)
      if (next.has(path)) {
        next.delete(path)
      } else {
        next.add(path)
      }
      return next
    })
  }

  return (
    <div className="font-mono text-sm overflow-auto max-h-96 bg-white">
      <JsonNode
        value={data}
        path=""
        depth={0}
        maxDepth={maxDepth}
        onFieldClick={onFieldClick}
        selectedPaths={selectedPaths}
        expandedPaths={expandedPaths}
        toggleExpand={toggleExpand}
      />
    </div>
  )
}
