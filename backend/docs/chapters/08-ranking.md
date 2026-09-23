# Prompt: Chapter 8 — Priority ranking

Continue the frozen Chapters 1–7 backend. Calculate a deterministic analytical priority for all nodes and create a ranked view. Do not persist or add endpoints yet.

Define and document a 0..1 weighted formula using role_score, PageRank percentile, seed-reach percentile, volume percentile, and degree signals. Weights must sum to one and must not contain gid-specific exceptions. Explain the analytical rationale and limitations. Add `priority_score` for every gid, then rank descending with stable deterministic tie-breaks.

Produce a complete ranking for UI use and a top-nodes view containing at least 20 records. Include `rank`, `gid`, `role`, `priority_score`, and a short reason derived from actual node evidence/features. Scores must be finite, bounded, stable across repeated runs, and must not mutate upstream frames.

Tests must check formula arithmetic, boundaries, weight configuration, all-node coverage, sorting, ties, minimum top size, reasons, determinism, invalid inputs, and non-mutation. On real data require 2248 ranked nodes, unique consecutive ranks, and review the top 20 for explainable signals.

Update methodology docs. Report formula and weights, top candidates with reasons, test results, regressions, and checklist. Priority is a review order, never a guilt score.
