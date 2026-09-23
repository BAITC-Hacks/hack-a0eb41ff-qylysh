# Prompt: Chapter 3 — Directed graph construction

Continue the frozen Chapters 1–2 backend and implement only construction of the canonical transaction graph. Add a Python 3.11-compatible NetworkX version. Do not calculate metrics, roles, clusters, scores, evidence, ranking, persistence, or API endpoints.

Create a focused graph builder that accepts a validated `RawDataset` and returns `networkx.DiGraph`. Add every row from `dataset.nodes`, including nodes absent from all edges. Use `gid` as the NetworkX node key and preserve node attributes `depth` and `is_seed`. Add every `src -> dst` edge in the documented money-flow direction and preserve `sum_kzt`, `n_tx`, and `depth` without changing the DataFrames.

Reject unsafe direct use with a clear graph construction error when required columns are absent, node gids are duplicated, an edge references an unknown gid, or duplicate `(src, dst)` pairs would be silently overwritten by `DiGraph`. Keep validation and graph construction separate: no cleaning or coercion belongs in the builder.

Add tests for directedness, node and edge counts, direction, attributes, isolated nodes, self-loops if present, invalid references, duplicate pairs, missing columns, deterministic construction, and non-mutation. Smoke-test the real dataset: 2248 nodes and 3119 edges; verify all 81 seeds and isolated nodes remain present.

Update backend documentation with the current stage and a minimal usage example. Preserve Chapter 1 API behavior and all Chapter 2 checks. Definition of done: canonical directed graph is reproducible, complete, correctly oriented, attribute-preserving, and all tests pass. End with files changed, real graph statistics, pytest result, regressions, and a PASS/FAIL checklist.
