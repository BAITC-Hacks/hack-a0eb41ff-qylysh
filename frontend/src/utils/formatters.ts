export const formatNumber = (value: number) => new Intl.NumberFormat('en-US').format(value)

export const formatKzt = (value: number) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'KZT', maximumFractionDigits: 0 }).format(value)

export const formatScore = (value: number) => value.toFixed(2)

export const formatRole = (value: string) => value.charAt(0).toUpperCase() + value.slice(1)
