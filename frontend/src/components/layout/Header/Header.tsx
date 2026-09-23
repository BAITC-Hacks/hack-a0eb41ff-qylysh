import { CalendarDays } from 'lucide-react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import SearchInput from '../../common/SearchInput/SearchInput'
import './Header.scss'

export default function Header() {
  const [gid, setGid] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  function handleSearch() {
    const value = gid.trim()
    if (!value) {
      setError('')
      return
    }
    if (!/^\d+$/.test(value)) {
      setError('Enter a numeric GID')
      return
    }
    setError('')
    navigate(`/network?gid=${encodeURIComponent(value)}`)
  }

  function handleChange(value: string) {
    setGid(value)
    if (error) setError('')
  }

  return (
    <header className="header">
      <div className="header__dataset">
        <span className="header__dataset-icon"><CalendarDays size={17} strokeWidth={1.8} aria-hidden="true" /></span>
        <span className="header__dataset-copy"><small>DATASET</small><strong>July 2026</strong></span>
      </div>
      <div className="header__metrics" aria-label="Dataset metrics">
        <span><strong>July 2026</strong> observation</span>
        <span className="header__separator" aria-hidden="true" />
        <span><strong>4-hop</strong> boundary</span>
      </div>
      <SearchInput
        value={gid}
        onChange={handleChange}
        onSubmit={handleSearch}
        placeholder="Search client GID..."
        error={error}
      />
    </header>
  )
}
