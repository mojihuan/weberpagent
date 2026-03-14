import { CheckCircle, XCircle } from 'lucide-react'
import type { AssertionResult } from '../../types'

interface AssertionResultsProps {
  results: AssertionResult[]
}

export function AssertionResults({ results }: AssertionResultsProps) {
  if (results.length === 0) {
    return null
  }

  const passCount = results.filter(r => r.status === 'pass').length
  const passRate = results.length > 0 ? Math.round((passCount / results.length) * 100) : 0

  return (
    <div className="mb-6">
      {/* Pass rate summary */}
      <div className="flex items-center gap-4 mb-4">
        <h2 className="text-lg font-medium text-gray-900">断言结果</h2>
        <span className={passRate === 100 ? 'text-green-600' : 'text-red-600'}>
          通过率: {passRate}% ({passCount}/{results.length})
        </span>
      </div>

      {/* Results list */}
      <div className="space-y-2">
        {results.map(result => (
          <div
            key={result.id}
            className={`p-3 rounded-lg border ${
              result.status === 'pass'
                ? 'bg-green-50 border-green-200'
                : 'bg-red-50 border-red-200'
            }`}
          >
            <div className="flex items-center gap-2">
              {result.status === 'pass' ? (
                <CheckCircle className="w-5 h-5 text-green-500" />
              ) : (
                <XCircle className="w-5 h-5 text-red-500" />
              )}
              <span className="font-medium text-gray-900">
                {result.assertion_name || `断言 ${result.assertion_id.slice(0, 8)}`}
              </span>
            </div>
            {result.status === 'fail' && result.message && (
              <p className="text-sm text-red-600 mt-2">{result.message}</p>
            )}
            {result.actual_value && (
              <p className="text-sm text-gray-500 mt-1">
                实际值: {result.actual_value}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
