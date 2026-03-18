import type {
  DataMethodsResponse,
  ExecuteDataMethodRequest,
  ExecuteDataMethodResponse
} from '../types'
import { apiClient } from './client'

export const externalDataMethodsApi = {
  /**
   * Fetch available data methods grouped by class.
   * Returns 503 if external module is not available.
   */
  async list(): Promise<DataMethodsResponse> {
    return apiClient<DataMethodsResponse>('/external-data-methods')
  },

  /**
   * Execute a data method and return results.
   * @param className - Class name like "BaseParams"
   * @param methodName - Method name like "inventory_list_data"
   * @param params - Method parameters like { i: 2, j: 13 }
   */
  async execute(
    className: string,
    methodName: string,
    params: Record<string, any> = {}
  ): Promise<ExecuteDataMethodResponse> {
    const body: ExecuteDataMethodRequest = {
      class_name: className,
      method_name: methodName,
      params
    }
    return apiClient<ExecuteDataMethodResponse>('/external-data-methods/execute', {
      method: 'POST',
      body: JSON.stringify(body),
    })
  },
}
