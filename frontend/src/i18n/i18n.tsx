import { createContext, Fragment, useContext } from 'react'
import type { ReactNode } from 'react'
import { dictionaries } from './translations'
import type { Dictionary, Lang, PluralForms } from './translations'

const STORAGE_KEY = 'moneygraph.lang'
export const locales: Record<Lang, string> = { en: 'en-US', ru: 'ru-RU' }

function detectLang(): Lang {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved === 'en' || saved === 'ru') return saved
  } catch { /* storage unavailable */ }
  return typeof navigator !== 'undefined' && navigator.language.toLowerCase().startsWith('en') ? 'en' : 'ru'
}

// Module-level copy so non-React code (formatters, API services) follows the active language
let currentLang: Lang = detectLang()
export const getLang = () => currentLang
export const getDict = () => dictionaries[currentLang]

/** Replaces `{key}` placeholders with values. */
export function fill(template: string, vars: Record<string, string | number>) {
  return template.replace(/\{(\w+)\}/g, (match, key: string) => (key in vars ? String(vars[key]) : match))
}

/** Picks the plural form for `count` and fills `{n}` with `shown` (defaults to the raw count). */
export function plural(forms: PluralForms, count: number, shown: string | number = count) {
  const category = new Intl.PluralRules(locales[currentLang]).select(count) as keyof PluralForms
  return fill(forms[category] ?? forms.other, { n: shown })
}

/** Like `fill`, but placeholders can be React nodes (e.g. `<strong>`). */
export function rich(template: string, vars: Record<string, ReactNode>) {
  return template.split(/(\{\w+\})/g).map((part, index) => {
    const key = part.match(/^\{(\w+)\}$/)?.[1]
    return <Fragment key={index}>{key && key in vars ? vars[key] : part}</Fragment>
  })
}

type I18nValue = { lang: Lang; t: Dictionary; setLang: (lang: Lang) => void }
export const I18nContext = createContext<I18nValue | null>(null)

/** Switches the module-level language and remembers it; the provider mirrors it into React state. */
export function applyLang(next: Lang) {
  currentLang = next
  try { localStorage.setItem(STORAGE_KEY, next) } catch { /* storage unavailable */ }
}

export function useI18n() {
  const value = useContext(I18nContext)
  if (!value) throw new Error('useI18n must be used inside I18nProvider')
  return value
}
