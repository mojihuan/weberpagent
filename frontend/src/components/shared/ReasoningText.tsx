import { parseReasoning } from '../../utils/reasoningParser'

const BADGE_STYLES: Record<string, string> = {
  Eval: 'bg-purple-100 text-purple-700',
  Verdict: 'bg-green-100 text-green-700',
  Memory: 'bg-orange-100 text-orange-700',
  Goal: 'bg-blue-100 text-blue-700',
}

interface ReasoningTextProps {
  text: string
}

export function ReasoningText({ text }: ReasoningTextProps) {
  const segments = parseReasoning(text)

  if (segments.length === 0) {
    return <span className="text-sm text-gray-600">{text}</span>
  }

  return (
    <div className="space-y-1">
      {segments.map((segment, index) => (
        <div key={index} className="flex items-start gap-2">
          {segment.label ? (
            <>
              <span
                className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium shrink-0 ${BADGE_STYLES[segment.label] ?? 'bg-gray-100 text-gray-600'}`}
              >
                {segment.label}
              </span>
              <span className="text-sm text-gray-600">{segment.content}</span>
            </>
          ) : (
            <span className="text-sm text-gray-600">{segment.content}</span>
          )}
        </div>
      ))}
    </div>
  )
}
