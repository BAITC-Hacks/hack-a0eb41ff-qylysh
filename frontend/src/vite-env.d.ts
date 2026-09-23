/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL?: string
  readonly VITE_USE_MOCK_API?: string
  readonly VITE_MOCK_SCENARIO?: 'success' | 'empty' | 'error'
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
