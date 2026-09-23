import './MethodologyPage.scss'

const roles = [
  ['Coordinator', 'Connects important parts of the observed network and participates in several flow paths.'],
  ['Consolidator', 'Receives transfers from multiple observed sources into a smaller set of accounts.'],
  ['Distributor', 'Sends observed value onward to multiple destinations.'],
  ['Transit', 'Shows both incoming and outgoing flow consistent with an intermediate position.'],
  ['Terminal', 'Has observed incoming value with little or no outgoing value inside this dataset.'],
  ['Peripheral', 'Has limited connectivity or flow relative to the observed network.'],
]

export default function MethodologyPage() {
  return <div className="methodology-page page-shell">
    <div className="page-shell__heading"><span className="page-shell__eyebrow">REFERENCE / METHODOLOGY</span><h1>Methodology</h1><p>How MoneyGraph describes observed structure and creates an analyst review queue.</p></div>
    <section className="methodology-page__note"><h2>Interpretation first</h2><p>Roles and scores summarize computed patterns in the supplied transaction network. They support investigation and do not establish identity, intent, wrongdoing, or legal responsibility.</p></section>
    <section className="methodology-page__section"><h2>Six structural roles</h2><div className="methodology-page__roles">{roles.map(([name, text], index) => <article key={name} className={`methodology-page__role methodology-page__role--${index}`}><span>{String(index + 1).padStart(2, '0')}</span><div><h3>{name}</h3><p>{text}</p></div></article>)}</div></section>
    <section className="methodology-page__section methodology-page__scores"><h2>Scores</h2><article><h3>Role score · 0 to 1</h3><p>Strength of fit between a node's observed metrics and its assigned structural role.</p></article><article><h3>Priority score · 0 to 1</h3><p>Relative position in the analyst review queue, based on computed graph and flow signals. It is not a probability of crime.</p></article></section>
    <section className="methodology-page__section"><h2>Analyst workflow</h2><ol><li>Review the summary and role distribution.</li><li>Open a ranked node or cluster and inspect its local directed graph.</li><li>Read the evidence statement and measured metrics together.</li><li>Account for the observation boundary before forming a hypothesis.</li><li>Validate any hypothesis using authorised source systems and human review.</li></ol></section>
  </div>
}
