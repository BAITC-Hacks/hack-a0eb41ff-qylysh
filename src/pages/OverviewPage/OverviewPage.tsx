import StatCard from '../../components/common/StatCard/StatCard'
import './OverviewPage.scss'

export default function OverviewPage() {
  return (
    <div className="overview-page page-shell">
      <div className="page-shell__heading">
        <span className="page-shell__eyebrow">WORKSPACE / OVERVIEW</span>
        <h1>Overview</h1>
        <p>Network monitoring overview and priority signals.</p>
      </div>

      <section className="overview-page__section" aria-labelledby="overview-snapshot-title">
        <div className="overview-page__section-heading">
          <div>
            <h2 id="overview-snapshot-title">Network snapshot</h2>
            <p>Current dataset at a glance</p>
          </div>
          <span>JULY 2026</span>
        </div>
        <div className="overview-page__stats">
          <StatCard label="Clients" value="2,248" description="In current dataset" />
          <StatCard label="Relations" value="3,119" description="Observed connections" />
          <StatCard label="Seed clients" value="81" description="Initial investigation set" />
          <StatCard label="Clusters" value="—" description="Pending analysis" />
        </div>
      </section>
    </div>
  )
}
