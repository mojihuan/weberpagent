export interface ReasoningSegment {
  label: string
  content: string
}

export function parseReasoning(text: string): ReasoningSegment[] {
  if (!text || !text.trim()) {
    return []
  }

  const parts = text.split(' | ')
  const segments: ReasoningSegment[] = []

  for (const part of parts) {
    const match = part.match(/^(Eval|Memory|Goal)\s*:\s*(.*)/i)
    if (match) {
      const rawLabel = match[1]
      const label = rawLabel.charAt(0).toUpperCase() + rawLabel.slice(1).toLowerCase()
      const value = match[2]

      if (label === 'Eval') {
        const verdictMatch = value.match(/Verdict\s*:\s*(.*)/i)
        if (verdictMatch) {
          const evalContent = value.slice(0, value.indexOf(verdictMatch[0])).trim()
          if (evalContent) {
            segments.push({ label: 'Eval', content: evalContent })
          }
          segments.push({ label: 'Verdict', content: verdictMatch[1].trim() })
        } else {
          segments.push({ label: 'Eval', content: value.trim() })
        }
      } else {
        segments.push({ label, content: value.trim() })
      }
    } else {
      const trimmed = part.trim()
      if (trimmed) {
        segments.push({ label: '', content: trimmed })
      }
    }
  }

  return segments
}
