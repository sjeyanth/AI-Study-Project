import { apiClient } from './client'
import type {
  AuthTokenResponse,
  LoginCredentials,
  RegisterPayload,
  User,
} from '../types/auth'

export async function login(credentials: LoginCredentials) {
  const formData = new URLSearchParams()
  formData.set('username', credentials.username)
  formData.set('password', credentials.password)

  const response = await apiClient.post<AuthTokenResponse>('/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  })

  return response.data
}

export async function register(payload: RegisterPayload) {
  const response = await apiClient.post<User>('/register', payload)
  return response.data
}

export async function getCurrentUser() {
  const response = await apiClient.get<User>('/me')
  return response.data
}
