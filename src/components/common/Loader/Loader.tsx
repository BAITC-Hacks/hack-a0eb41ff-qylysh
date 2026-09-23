import './Loader.scss'

export default function Loader() {
  return (
    <div className="loader" role="status" aria-live="polite">
      <span className="loader__spinner" aria-hidden="true" />
      <span>Loading data...</span>
    </div>
  )
}
