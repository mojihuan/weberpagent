import { CheckCircle, XCircle } from 'lucide-react'

interface PreconditionResult {
  index: number
  code: string
  status: 'success' | 'failed'
  duration_ms?: number
  error?: string
  variables?: Record<string, unknown>
}

interface PreconditionSectionProps {
  results: PreconditionResult[]
}

function formatDuration(ms: number): string {
  if (ms < 1000) return `${ms}ms`
  return `${(ms / 1000).toFixed(1)}s`
}

export function PreconditionSection({ results }: PreconditionSectionProps) {
  if (results.length === 0) {
    return null
  }

  return (
    <div className="mb-6">
      <h2 className="text-lg font-medium text-gray-900 mb-3">
        Precondition Execution
      </h2>
      <div className="space-y-3">
        {results.map((result) => (
          <div
            key={result.index}
            className={`border rounded-lg p-4 ${
              result.status === 'success'
                ? 'border-green-200 bg-green-50'
                : 'border-red-200 bg-red-50'
            }`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                {result.status === 'success' ? (
                  <CheckCircle className="w-5 h-5 text-green-500" />
                ) : (
                  <XCircle className="w-5 h-5 text-red-500" />
                )}
                <span className="font-medium text-gray-900">
                  Precondition {result.index + 1}
                </span>
              </div>
              {result.duration_ms !== undefined && (
                <span className="text-sm text-gray-500">
                  {formatDuration(result.duration_ms)}
                </span>
              )}
            </div>

            {/* Variables section */}
            {result.status === 'success' && result.variables && Object.keys(result.variables).length > 0 && (
              <div className="mt-3 pt-3 border-t border-green-200">
                <div className="text-sm font-medium text-gray-700 mb-2">
                  Extracted Variables:
                </div>
                <div className="bg-gray-50 rounded p-2 font-mono text-sm">
                  {Object.entries(result.variables).map(([key, value]) => (
                    <div key={key} className="flex gap-2">
                      <span className="text-blue-600">{key}</span>
                      <span className="text-gray-400">=</span>
                      <span className="text-green-600">
                        {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Error message */}
            {result.status === 'failed' && result.error && (
              <div className="mt-3 pt-3 border-t border-red-200 text-red-600 text-sm">
                Error: {result.error}
              </div>
            )}

            {/* Expandable code */}
            <details className="mt-3">
              <summary className="text-sm text-blue-500 cursor-pointer hover:text-blue-700">
                View Code
              </summary>
              <pre className="mt-2 p-2 bg-gray-100 rounded text-xs overflow-auto whitespace-pre-wrap">
                {result.code}
              </pre>
            </details>
          </div>
        ))}
      </div>
    </div>
  )
}
