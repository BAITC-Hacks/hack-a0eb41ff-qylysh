import './DataLimitationsPage.scss'

export default function DataLimitationsPage() {
  return (
    <div className="data-limitations-page page-shell">
      <div className="page-shell__heading">
        <span className="page-shell__eyebrow">REFERENCE / DATA LIMITATIONS</span>
        <h1>Data limitations</h1>
      </div>
      <div className="data-limitations-page__note">
        <ul>
          <li>Graph observation is limited to four hops.</li>
          <li>Seed incoming transactions are incomplete.</li>
          <li>Absence of outgoing transfers at the observation boundary does not imply that funds stopped there.</li>
        </ul>
      </div>
    </div>
  )
}
