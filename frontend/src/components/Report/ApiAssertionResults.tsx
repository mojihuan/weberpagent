import { CheckCircle, XCircle, Clock } from 'lucide-react'
import type { AssertionResult } from '../../types'

interface ApiAssertionResultsProps {
  results: AssertionResult[]
  passRate: string
}

export function ApiAssertionResults({ results, passRate }: ApiAssertionResultsProps) {
  if (!results || results.length === 0) {
    return null
  }

  const allPassed = results.every(r => r.status === 'pass')

  return (
    <div className="mt-4 mb-6">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-medium text-gray-900">接口断言结果</h3>
        <span className={`px-2 py-1 rounded-full text-sm font-medium ${
          allPassed ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        }`}>
          通过率: {passRate}
        </span>
      </div>

      <div className="space-y-2">
        {results.map((result, index) => (
          <div
            key={result.id || index}
            className={`p-4 rounded-lg border ${
              result.status === 'pass'
                ? 'bg-green-50 border-green-200'
                : 'bg-red-50 border-red-200'
            }`}
          >
            <div className="flex items-start gap-3">
              {result.status === 'pass' ? (
                <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
              ) : (
                <XCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
              )}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-sm text-gray-700">
                    {result.assertion_id}
                  </span>
                </div>
                {result.message && (
                  <p className="text-sm text-gray-600 mt-1">
                    {result.message}
                  </p>
                )}
                {result.actual_value && (
                  <p className="text-sm text-gray-500 mt-1">
                    : {result.actual_value}
                  </p>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
