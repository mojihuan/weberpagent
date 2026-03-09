import { useEffect } from 'react'
import { X, Download } from 'lucide-react'

interface ImageViewerProps {
  src: string
  isOpen: boolean
  onClose: () => void
  onDownload?: () => void
}

export function ImageViewer({ src, isOpen, onClose, onDownload }: ImageViewerProps) {
  // ESC 关闭
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose()
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isOpen, onClose])

  if (!isOpen) return null

  const handleDownload = () => {
    const link = document.createElement('a')
    link.href = src
    link.download = src.split('/').pop() || 'screenshot.png'
    link.click()
    onDownload?.()
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80"
      onClick={onClose}
    >
      {/* 关闭按钮 */}
      <button
        onClick={onClose}
        className="absolute top-4 right-4 p-2 rounded-full bg-white/10 hover:bg-white/20 text-white transition"
      >
        <X className="w-6 h-6" />
      </button>

      {/* 下载按钮 */}
      <button
        onClick={handleDownload}
        className="absolute top-4 right-14 p-2 rounded-full bg-white/10 hover:bg-white/20 text-white transition"
      >
        <Download className="w-6 h-6" />
      </button>

      {/* 图片 */}
      <img
        src={src}
        alt="Screenshot"
        className="max-w-[90vw] max-h-[90vh] object-contain"
        onClick={e => e.stopPropagation()}
      />
    </div>
  )
}
