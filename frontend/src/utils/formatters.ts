import { getDict, getLang, locales } from '../i18n/i18n'
import type { Role } from '../types'

export const formatNumber = (value: number) => new Intl.NumberFormat(locales[getLang()]).format(value)

export const formatKzt = (value: number) =>
  new Intl.NumberFormat(locales[getLang()], { style: 'currency', currency: 'KZT', maximumFractionDigits: 0 }).format(value)

export const formatScore = (value: number) => value.toFixed(2)

export const formatRole = (value: Role) => getDict().roles[value] ?? value
