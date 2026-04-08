import { useState, useRef, useCallback } from 'react'
import { Upload } from 'lucide-react'
import { importPreview } from '../../api/tasks'
import type { ImportPreviewResponse } from '../../api/tasks'
import { LoadingSpinner } from '../shared/LoadingSpinner'

interface UploadStepProps {
  onFileSelected: (file: File, data: ImportPreviewResponse) => void
  loading: boolean
}

export function UploadStep({ onFileSelected, loading }: UploadStepProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [uploading, setUploading] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  const validateFile = (file: File): string | null => {
    if (!file.name.endsWith('.xlsx')) {
      return '仅支持 .xlsx 格式文件，请重新选择'
    }
    if (file.size > 5 * 1024 * 1024) {
      return '文件大小不能超过 5MB，请重新选择'
    }
    return null
  }

  const handleFile = useCallback(async (file: File) => {
    const validationError = validateFile(file)
    if (validationError) {
      setError(validationError)
      return
    }

    setError(null)
    setUploading(true)
    try {
      const data = await importPreview(file)
      onFileSelected(file, data)
    } catch (err) {
      const message = err instanceof Error ? err.message : '上传失败'
      setError(message)
    } finally {
      setUploading(false)
    }
  }, [onFileSelected])

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback(() => {
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer.files[0]
    if (file) {
      handleFile(file)
    }
  }, [handleFile])

  const handleClick = useCallback(() => {
    inputRef.current?.click()
  }, [])

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      handleFile(file)
    }
    if (inputRef.current) {
      inputRef.current.value = ''
    }
  }, [handleFile])

  const isUploading = uploading || loading

  return (
    <div className="flex flex-col items-center justify-center py-8">
      <div
        role="button"
        tabIndex={0}
        onClick={handleClick}
        onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') handleClick() }}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`
          w-full max-w-md border-2 border-dashed rounded-xl p-12 text-center transition-colors cursor-pointer
          ${error ? 'border-red-300 bg-red-50' : ''}
          ${isDragging && !error ? 'border-blue-500 bg-blue-50' : ''}
          ${!error && !isDragging ? 'border-gray-300 hover:border-gray-400' : ''}
        `}
      >
        {isUploading ? (
          <div className="flex flex-col items-center">
            <LoadingSpinner size="lg" className="text-blue-500" />
            <p className="text-gray-500 mt-4">正在解析...</p>
          </div>
        ) : isDragging ? (
          <div className="flex flex-col items-center">
            <Upload className="w-12 h-12 text-blue-500" />
            <p className="text-blue-600 mt-4">释放文件以上传</p>
          </div>
        ) : (
          <div className="flex flex-col items-center">
            <Upload className="w-12 h-12 text-gray-400" />
            <p className="text-gray-500 mt-4">
              拖拽 .xlsx 文件到此处，或点击选择文件
            </p>
          </div>
        )}
      </div>

      <input
        ref={inputRef}
        type="file"
        accept=".xlsx"
        onChange={handleChange}
        className="hidden"
      />

      {error && (
        <p className="text-red-600 text-sm mt-3">{error}</p>
      )}
    </div>
  )
}
