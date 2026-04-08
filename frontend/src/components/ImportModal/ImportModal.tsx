import { useState, useCallback, useRef } from 'react'
import { X } from 'lucide-react'
import { toast } from 'sonner'
import { importConfirm } from '../../api/tasks'
import type { ImportPreviewResponse } from '../../api/tasks'
import { UploadStep } from './UploadStep'
import { PreviewStep } from './PreviewStep'
import { ResultStep } from './ResultStep'

type ImportStep = 'upload' | 'preview' | 'result'

interface ImportModalProps {
  open: boolean
  onClose: () => void
  onImportComplete: () => void
}

const STEP_TITLES: Record<ImportStep, string> = {
  upload: '上传 Excel 文件',
  preview: '预览导入数据',
  result: '导入完成',
}

export function ImportModal({ open, onClose, onImportComplete }: ImportModalProps) {
  const [step, setStep] = useState<ImportStep>('upload')
  const [file, setFile] = useState<File | null>(null)
  const [previewData, setPreviewData] = useState<ImportPreviewResponse | null>(null)
  const [uploading, setUploading] = useState(false)
  const [confirming, setConfirming] = useState(false)
  const [createdCount, setCreatedCount] = useState(0)
  const autoCloseTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  const resetState = useCallback(() => {
    setStep('upload')
    setFile(null)
    setPreviewData(null)
    setUploading(false)
    setConfirming(false)
    setCreatedCount(0)
    if (autoCloseTimerRef.current !== null) {
      clearTimeout(autoCloseTimerRef.current)
      autoCloseTimerRef.current = null
    }
  }, [])

  const handleClose = useCallback(() => {
    resetState()
    onClose()
  }, [resetState, onClose])

  const handleFileSelected = useCallback((selectedFile: File, data: ImportPreviewResponse) => {
    setFile(selectedFile)
    setPreviewData(data)
    setStep('preview')
  }, [])

  const handleBack = useCallback(() => {
    setFile(null)
    setPreviewData(null)
    setStep('upload')
  }, [])

  const handleConfirm = useCallback(async () => {
    if (!file) return
    setConfirming(true)
    try {
      const result = await importConfirm(file)
      setCreatedCount(result.created_count)
      setStep('result')
      toast.success(`成功导入 ${result.created_count} 个任务`)
      autoCloseTimerRef.current = setTimeout(() => {
        handleClose()
        onImportComplete()
      }, 1500)
    } catch (error) {
      const message = error instanceof Error ? error.message : '导入失败'
      toast.error(message)
    } finally {
      setConfirming(false)
    }
  }, [file, handleClose, onImportComplete])

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="fixed inset-0 bg-black/50" onClick={handleClose} />
      <div className="relative bg-white rounded-xl shadow-xl w-full max-w-4xl mx-4 max-h-[85vh] flex flex-col">
        <div className="sticky top-0 bg-white px-6 py-4 border-b border-gray-100 flex items-center justify-between rounded-t-xl">
          <h2 className="text-lg font-semibold text-gray-900">
            {STEP_TITLES[step]}
          </h2>
          <button onClick={handleClose} className="text-gray-400 hover:text-gray-600" aria-label="关闭">
            <X className="w-5 h-5" />
          </button>
        </div>
        <div className="p-6 overflow-y-auto">
          {step === 'upload' && (
            <UploadStep onFileSelected={handleFileSelected} loading={uploading} />
          )}
          {step === 'preview' && previewData && file && (
            <PreviewStep
              data={previewData}
              file={file}
              onConfirm={handleConfirm}
              onBack={handleBack}
              confirming={confirming}
            />
          )}
          {step === 'result' && (
            <ResultStep count={createdCount} onComplete={handleClose} />
          )}
        </div>
      </div>
    </div>
  )
}
