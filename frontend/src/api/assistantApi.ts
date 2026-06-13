import { apiClient } from './client'

import type {
  AssistantChatResponse,
} from '../types/assistant'

export const sendMessage = async (
  message: string
): Promise<AssistantChatResponse> => {
  const response = await apiClient.post(
    '/assistant/chat',
    {
      message,
    }
  )

  return response.data
}