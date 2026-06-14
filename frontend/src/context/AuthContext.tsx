import {
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'

import {
  getCurrentUser,
  login as loginRequest,
  register as registerRequest,
} from '../api/authApi'
import type { LoginCredentials, RegisterPayload, User } from '../types/auth'
import {
  clearStoredToken,
  getStoredToken,
  storeToken,
} from '../utils/tokenStorage'
import { AuthContext } from './authContextValue'



export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(() => getStoredToken())
  const [isLoading, setIsLoading] = useState(true)

  const logout = useCallback(() => {
    clearStoredToken()
    setToken(null)
    setUser(null)
  }, [])

  useEffect(() => {
    let isMounted = true

    async function loadUser() {
      if (!token) {
        setIsLoading(false)
        return
      }

      try {
        const currentUser = await getCurrentUser()

        if (isMounted) {
          setUser(currentUser)
        }
      } catch {
        if (isMounted) {
          logout()
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    loadUser()

    return () => {
      isMounted = false
    }
  }, [logout, token])

  const login = useCallback(async (credentials: LoginCredentials) => {
    const authToken = await loginRequest(credentials)
    storeToken(authToken.access_token)
    setToken(authToken.access_token)
    const currentUser = await getCurrentUser()
    setUser(currentUser)
  }, [])

  const register = useCallback(async (payload: RegisterPayload) => {
    await registerRequest(payload)
    const authToken = await loginRequest({
      username: payload.username,
      password: payload.password,
    })
    storeToken(authToken.access_token)
    setToken(authToken.access_token)
    const currentUser = await getCurrentUser()
    setUser(currentUser)
  }, [])

  const value = useMemo(
    () => ({
      user,
      token,
      isAuthenticated: Boolean(token && user),
      isLoading,
      login,
      register,
      logout,
    }),
    [isLoading, login, logout, register, token, user],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}


