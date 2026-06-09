export type User = {
  id: number
  username: string
  email: string
}

export type LoginCredentials = {
  username: string
  password: string
}

export type RegisterPayload = LoginCredentials & {
  email: string
}

export type AuthTokenResponse = {
  access_token: string
  token_type: string
}
