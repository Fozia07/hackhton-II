import { getJWTToken } from './auth'

interface ApiOptions extends RequestInit {
  requireAuth?: boolean
}

class ApiClient {
  private async getJWTToken(): Promise<string> {
    // In a real implementation, this would call the backend to get a JWT token
    // For now, we'll simulate this behavior
    return getJWTToken()
  }

  async request<T>(endpoint: string, options: ApiOptions = {}): Promise<T> {
    const { requireAuth = true, headers, ...fetchOptions } = options

    let authHeaders = {}
    if (requireAuth) {
      const token = await this.getJWTToken()
      authHeaders = {
        'Authorization': `Bearer ${token}`,
      }
    }

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}${endpoint}`,
      {
        headers: {
          'Content-Type': 'application/json',
          ...authHeaders,
          ...headers,
        },
        ...fetchOptions,
      }
    )

    if (!response.ok) {
      if (response.status === 401) {
        // Redirect to login
        window.location.href = '/login'
        throw new Error('Unauthorized')
      }
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.message || 'API request failed')
    }

    return response.json()
  }

  async get<T>(endpoint: string, options?: ApiOptions): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'GET' })
  }

  async post<T>(endpoint: string, data?: unknown, options?: ApiOptions): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async put<T>(endpoint: string, data?: unknown, options?: ApiOptions): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async patch<T>(endpoint: string, data?: unknown, options?: ApiOptions): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PATCH',
      body: JSON.stringify(data),
    })
  }

  async delete<T>(endpoint: string, options?: ApiOptions): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' })
  }
}

export const api = new ApiClient()