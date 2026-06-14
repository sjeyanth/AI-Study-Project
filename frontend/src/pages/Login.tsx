import { useState, type FormEvent } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'

import { useAuth } from '../context/useAuth'

type LocationState = {
  from?: {
    pathname?: string
  }
}

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const auth = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const state = location.state as LocationState | null

  const fromPath =
    state?.from?.pathname ??
    '/dashboard'

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault()

    setError('')
    setLoading(true)

    try {
      await auth.login({
        username,
        password,
      })

      navigate(fromPath, {
        replace: true,
      })
    } catch {
      setError(
        'Invalid username or password. Please try again.'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="auth-page">
      <form
        className="auth-card"
        onSubmit={handleSubmit}
      >
        <h1>Login</h1>

        <label htmlFor="username">
          Username
        </label>

        <input
          id="username"
          type="text"
          value={username}
          onChange={(event) =>
            setUsername(
              event.target.value
            )
          }
          required
        />

        <label htmlFor="password">
          Password
        </label>

        <input
          id="password"
          type="password"
          value={password}
          onChange={(event) =>
            setPassword(
              event.target.value
            )
          }
          required
        />

        {error && (
          <p className="error-text">
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={loading}
        >
          {loading
            ? 'Signing in...'
            : 'Login'}
        </button>

        <p className="helper-text">
          New here?{' '}
          <Link to="/register">
            Create an account
          </Link>
        </p>
      </form>
    </section>
  )
}