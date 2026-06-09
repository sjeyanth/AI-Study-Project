import axios from 'axios'

export function getLoginErrorMessage(error: unknown) {
  if (!axios.isAxiosError(error)) {
    return 'Server error. Please try again later'
  }

  if (!error.response) {
    return 'Unable to connect to server'
  }

  if (error.response.status === 401) {
    return 'Invalid username or password'
  }

  if (error.response.status >= 500) {
    return 'Server error. Please try again later'
  }

  return 'Server error. Please try again later'
}
