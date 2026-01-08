export interface User {
  id: string
  email: string
  name: string
  createdAt: string // ISO 8601 timestamp
}

export interface Session {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: Error | null
}

export interface AuthCredentials {
  email: string
  password: string
}

export interface SignupData extends AuthCredentials {
  name: string
}