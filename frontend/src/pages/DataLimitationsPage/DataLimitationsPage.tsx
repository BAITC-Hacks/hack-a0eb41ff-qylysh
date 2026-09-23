import './DataLimitationsPage.scss'

const limitations = [
  ['Observation period', 'The supplied transactions cover July 2026. Activity before or after that month is outside this view.'],
  ['Transfer threshold', 'Only transfers of at least 5,000 KZT are included. Smaller transfers are not represented.'],
  ['Seed direction', 'Expansion follows outgoing transfers from 81 seed clients. Incoming context around seeds may be incomplete.'],
  ['Four-hop boundary', 'The graph stops after four hops. A node at depth 4 is an observation boundary, not proof of a final recipient.'],
  ['No ground-truth labels', 'The dataset has no verified labels for illicit conduct. Roles and priority scores cannot be treated as accusations.'],
  ['Missing edge meaning', 'An absent edge means it was not observed under these collection rules. It does not prove that no real relationship exists.'],
]

export default function DataLimitationsPage() {
  return <div className="data-limitations-page page-shell">
    <div className="page-shell__heading"><span className="page-shell__eyebrow">REFERENCE / DATA LIMITATIONS</span><h1>Data limitations</h1><p>Read these constraints before interpreting a node, path, role, or cluster.</p></div>
    <div className="data-limitations-page__callout"><strong>Observed network ≠ complete financial reality</strong><p>Every result is conditional on the supplied period, threshold, seed set, direction and depth.</p></div>
    <div className="data-limitations-page__grid">{limitations.map(([title, text], index) => <article key={title}><span>{String(index + 1).padStart(2, '0')}</span><h2>{title}</h2><p>{text}</p></article>)}</div>
  </div>
}
