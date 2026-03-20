import type { AssertionMethodsResponse } from '../types'
import { apiClient } from './client'

export const externalAssertionsApi = {
  /**
   * Fetch available assertion methods grouped by class.
   * Returns 503 if external module is not available.
   *
   * Response includes:
   * - available: boolean indicating if external module is loaded
   * - headers_options: fixed list of header identifiers for dropdown
   * - classes: array of assertion class groups (PcAssert, MgAssert, McAssert)
   * - total: total number of methods available
   */
  async list(): Promise<AssertionMethodsResponse> {
    return apiClient<AssertionMethodsResponse>('/external-assertions/methods')
  },
}
