import axios from 'axios'
import { getLang } from '../i18n/i18n'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
})

apiClient.interceptors.request.use((config) => {
  config.headers.set('Accept-Language', getLang())
  return config
})
