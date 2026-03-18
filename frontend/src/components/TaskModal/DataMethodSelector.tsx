import { useState, useEffect } from 'react'
import { X, Check, ChevronLeft, ChevronRight } from 'lucide-react'
import type { DataMethodConfig, DataMethodsResponse, DataMethodInfo } from '../../types'
import { externalDataMethodsApi } from '../../api/externalDataMethods'
import { LoadingSpinner } from '../shared/LoadingSpinner'

const STEPS = ['Select Method', 'Configure Parameters', 'Extraction Path', 'Variable Naming'] as const

interface SelectedMethod {
  className: string
  method: DataMethodInfo
  parameters: Record<string, any>
  extractions: { path: string; variableName: string }[]
}

interface DataMethodSelectorProps {
  open: boolean
  onConfirm: (configs: DataMethodConfig[]) => void
  onCancel: () => void
}

export function DataMethodSelector({ open, onConfirm, onCancel }: DataMethodSelectorProps) {
  const [currentStep, setCurrentStep] = useState(0)
  const [_methods, setMethods] = useState<DataMethodsResponse | null>(null)
  const [selectedMethods, setSelectedMethods] = useState<SelectedMethod[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [_previewData, setPreviewData] = useState<unknown>(null)
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [_previewLoading, _setPreviewLoading] = useState(false)

  // Fetch methods when modal opens
  useEffect(() => {
    if (!open) return

    const fetchMethods = async () => {
      setLoading(true)
      setError(null)
      try {
        const response = await externalDataMethodsApi.list()
        if (!response.available) {
          setError(response.error || 'External module not available')
        } else {
          setMethods(response)
        }
      } catch {
        setError('External data methods module not available. Please check WEBSERP_PATH configuration.')
      } finally {
        setLoading(false)
      }
    }

    fetchMethods()
    // Reset state when modal opens
    setCurrentStep(0)
    setSelectedMethods([])
    setPreviewData(null)
  }, [open])

  const handleCancel = () => {
    onCancel()
  }

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleNext = () => {
    if (currentStep < STEPS.length - 1) {
      setCurrentStep(currentStep + 1)
    }
  }

  const handleConfirm = () => {
    const configs: DataMethodConfig[] = selectedMethods.map(sm => ({
      className: sm.className,
      methodName: sm.method.name,
      parameters: sm.parameters,
      extractions: sm.extractions,
    }))
    onConfirm(configs)
  }

  const goToStep = (step: number) => {
    if (step >= 0 && step < STEPS.length) {
      setCurrentStep(step)
    }
  }

  const renderStepContent = () => {
    switch (currentStep) {
      case 0:
        return (
          <div className="text-center py-8 text-gray-500">
            Step 1: Method selection content will be implemented in next plan
          </div>
        )
      case 1:
        return (
          <div className="text-center py-8 text-gray-500">
            Step 2: Parameter configuration content will be implemented in next plan
          </div>
        )
      case 2:
        return (
          <div className="text-center py-8 text-gray-500">
            Step 3: Extraction path content will be implemented in next plan
          </div>
        )
      case 3:
        return (
          <div className="text-center py-8 text-gray-500">
            Step 4: Variable naming content will be implemented in next plan
          </div>
        )
      default:
        return null
    }
  }

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black/50" onClick={handleCancel} />

      {/* Modal content */}
      <div className="relative bg-white rounded-xl shadow-xl w-full max-w-3xl mx-4 max-h-[85vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <h3 className="text-lg font-semibold text-gray-900">Select Data Method</h3>
          <button
            onClick={handleCancel}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Step bar */}
        <div className="flex items-center justify-center gap-2 px-4 py-3 border-b border-gray-100 bg-gray-50">
          {STEPS.map((step, index) => {
            const isCompleted = index < currentStep
            const isCurrent = index === currentStep

            return (
              <button
                key={step}
                onClick={() => goToStep(index)}
                className="flex items-center gap-2 px-3 py-1.5 rounded-full transition-colors"
              >
                <span
                  className={`flex items-center justify-center w-6 h-6 rounded-full text-sm font-medium ${
                    isCompleted
                      ? 'bg-green-500 text-white'
                      : isCurrent
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-200 text-gray-600'
                  }`}
                >
                  {isCompleted ? <Check className="w-4 h-4" /> : index + 1}
                </span>
                <span
                  className={`text-sm ${
                    isCurrent ? 'text-blue-600 font-medium' : 'text-gray-500'
                  }`}
                >
                  {step}
                </span>
                {index < STEPS.length - 1 && (
                  <ChevronRight className="w-4 h-4 text-gray-300" />
                )}
              </button>
            )
          })}
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto px-6 py-4">
          {loading && (
            <div className="flex items-center justify-center py-8">
              <LoadingSpinner size="lg" />
            </div>
          )}

          {error && !loading && (
            <div className="text-center py-8 text-red-500">
              {error}
            </div>
          )}

          {!loading && !error && renderStepContent()}
        </div>

        {/* Footer */}
        <div className="flex justify-between gap-3 px-6 py-4 border-t border-gray-100">
          <div className="flex gap-3">
            <button
              onClick={handleCancel}
              className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
            >
              Cancel
            </button>
          </div>
          <div className="flex gap-3">
            {currentStep > 0 && (
              <button
                onClick={handlePrevious}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg flex items-center gap-1"
              >
                <ChevronLeft className="w-4 h-4" />
                Previous
              </button>
            )}
            {currentStep < STEPS.length - 1 && (
              <button
                onClick={handleNext}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 flex items-center gap-1"
              >
                Next
                <ChevronRight className="w-4 h-4" />
              </button>
            )}
            {currentStep === STEPS.length - 1 && (
              <button
                onClick={handleConfirm}
                disabled={selectedMethods.length === 0}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
              >
                Confirm
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
