# Prompt: Chapter 5 — Explainable role engine

Continue the frozen Chapters 1–4 backend. Assign exactly one existing `NodeRole` to each feature row using deterministic, documented rules. Do not train ML, calculate role_score/evidence/priority, cluster, persist, or expose endpoints.

Create explicit rules for coordinator, consolidator, distributor, transit, terminal, and peripheral. Base thresholds on documented features and percentiles rather than hardcoded gid lists. Freeze precedence as coordinator → consolidator → distributor → transit → terminal → peripheral, and explain why overlaps resolve in that order.

Respect dataset limitations: `depth == 4` with zero observed outgoing edges must not automatically become terminal; seed pass-through is incomplete and must not by itself produce transit. Peripheral is the exhaustive fallback. Return a table keyed by unique `gid` with non-null `role` for all nodes and do not mutate the feature table.

Write unit tests that isolate every rule, precedence overlaps, threshold boundaries, truncated nodes, seed behavior, fallback, input validation, determinism, and non-mutation. Run against real data, verify all 2248 nodes receive one of six roles, print role distribution, and manually review at least three candidates for each materially populated role.

Document formal rules and thresholds in README so an AML analyst can reproduce each decision. Report rules, distribution, manual samples, tests, regressions, and a checklist. Do not claim criminality; roles are structural analytical hypotheses.
