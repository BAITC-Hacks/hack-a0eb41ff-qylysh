import { Search } from 'lucide-react'
import type { FormEvent } from 'react'
import { useI18n } from '../../../i18n/i18n'
import './SearchInput.scss'

type SearchInputProps = {
  value: string
  onChange: (value: string) => void
  onSubmit: () => void
  placeholder?: string
  error?: string
}

export default function SearchInput({ value, onChange, onSubmit, placeholder, error }: SearchInputProps) {
  const { t } = useI18n()
  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    onSubmit()
  }

  return (
    <form className="search-input" role="search" onSubmit={handleSubmit}>
      <label className="search-input__label" htmlFor="global-gid-search">{t.header.searchLabel}</label>
      <div className={`search-input__field${error ? ' search-input__field--error' : ''}`}>
        <Search size={16} strokeWidth={2} aria-hidden="true" />
        <input
          id="global-gid-search"
          type="text"
          inputMode="numeric"
          autoComplete="off"
          value={value}
          onChange={(event) => onChange(event.target.value)}
          placeholder={placeholder}
          aria-invalid={Boolean(error)}
          aria-describedby={error ? 'global-gid-search-error' : undefined}
        />
        <button type="submit" aria-label={t.header.searchButton} title={t.header.searchButton}>
          <Search size={17} strokeWidth={2} aria-hidden="true" />
        </button>
      </div>
      {error && <span className="search-input__error" id="global-gid-search-error" role="alert">{error}</span>}
    </form>
  )
}
