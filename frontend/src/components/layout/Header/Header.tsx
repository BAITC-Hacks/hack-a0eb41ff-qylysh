import { CalendarDays } from 'lucide-react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import SearchInput from '../../common/SearchInput/SearchInput'
import { useI18n } from '../../../i18n/i18n'
import type { Lang } from '../../../i18n/translations'
import './Header.scss'

const languages: { value: Lang; label: string; name: string }[] = [
  { value: 'ru', label: 'RU', name: 'Русский' },
  { value: 'en', label: 'EN', name: 'English' },
]

export default function Header() {
  const { t, lang, setLang } = useI18n()
  const [gid, setGid] = useState('')
  const [error, setError] = useState(false)
  const navigate = useNavigate()

  function handleSearch() {
    const value = gid.trim()
    if (!value) {
      setError(false)
      return
    }
    if (!/^\d+$/.test(value)) {
      setError(true)
      return
    }
    setError(false)
    navigate(`/network?gid=${encodeURIComponent(value)}`)
  }

  function handleChange(value: string) {
    setGid(value)
    if (error) setError(false)
  }

  return (
    <header className="header">
      <div className="header__dataset">
        <span className="header__dataset-icon"><CalendarDays size={17} strokeWidth={1.8} aria-hidden="true" /></span>
        <span className="header__dataset-copy"><small>{t.header.dataset}</small><strong>{t.header.datasetValue}</strong></span>
      </div>
      <div className="header__metrics" aria-label={t.header.metricsAria}>
        <span>{t.header.periodPrefix}<strong>{t.header.periodValue}</strong>{t.header.periodSuffix}</span>
        <span className="header__separator" aria-hidden="true" />
        <span>{t.header.depthPrefix}<strong>{t.header.depthValue}</strong>{t.header.depthSuffix}</span>
      </div>
      <SearchInput
        value={gid}
        onChange={handleChange}
        onSubmit={handleSearch}
        placeholder={t.header.searchPlaceholder}
        error={error ? t.header.numericError : ''}
      />
      <div className="header__lang" role="group" aria-label={t.header.language}>
        {languages.map((item) => (
          <button
            key={item.value}
            type="button"
            lang={item.value}
            className={lang === item.value ? 'is-active' : ''}
            aria-pressed={lang === item.value}
            title={item.name}
            onClick={() => setLang(item.value)}
          >
            {item.label}
          </button>
        ))}
      </div>
    </header>
  )
}
