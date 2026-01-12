export interface User {
  id: number
  username: string
  email: string
  created_at: string // ISO 8601 timestamp
  updated_at: string // ISO 8601 timestamp
  is_active: boolean
}

export interface Session {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: Error | null
}

export interface AuthCredentials {
  username: string
  password: string
}

export interface SignupData {
  username: string
  email: string
  password: string
}

export interface SigninData {
  username: string
  password: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user_id: number
  username: string
}