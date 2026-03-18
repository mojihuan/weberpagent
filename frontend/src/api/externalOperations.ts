import type { OperationsResponse, GenerateRequest, GenerateResponse } from '../types'
import { apiClient } from './client'

export const externalOperationsApi = {
  /**
   * Fetch available operation codes grouped by module.
   * Returns 503 if external module is not available.
   */
  async list(): Promise<OperationsResponse> {
    return apiClient<OperationsResponse>('/external-operations')
  },

  /**
   * Generate precondition code for selected operation codes.
   * @param operationCodes - Array of operation codes like ['FA1', 'HC1']
   */
  async generate(operationCodes: string[]): Promise<GenerateResponse> {
    const body: GenerateRequest = { operation_codes: operationCodes }
    return apiClient<GenerateResponse>('/external-operations/generate', {
      method: 'POST',
      body: JSON.stringify(body),
    })
  },
}
