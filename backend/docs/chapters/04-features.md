# Prompt: Chapter 4 — Feature engineering

Continue the frozen Chapters 1–3 backend. Build one deterministic feature table with exactly one row per graph node. Do not assign roles, clusters, priority, evidence, write SQLite/CSV, or add API endpoints.

Calculate `in_degree`, `out_degree`, `in_kzt`, `out_kzt`, `in_tx`, `out_tx`, weighted PageRank, `pass_through`, `seed_reach_count`, and `truncated_by_depth`. Add `total_degree` and `total_volume`. Preserve `gid`, `depth`, and `is_seed`. Define pass-through behavior for zero incoming value explicitly; seed nodes must not be interpreted as balanced accounts because incoming history is incomplete. A node is truncated only when `depth == 4` and its observed out-degree is zero.

Define `seed_reach_count` precisely as the number of distinct seed nodes that can reach a node through directed paths, using a scalable traversal strategy for this dataset. Add deterministic percentile columns for in-degree, out-degree, total volume, PageRank, and seed reach, all constrained to 0..1. Document tie handling.

Tests must cover tiny hand-checkable graphs, weighted sums, transaction counts, isolated nodes, zero denominators, seed reach, PageRank presence, percentiles, truncation, row/gid completeness, deterministic output, and non-mutation. On real data require 2248 unique gids and manually cross-check at least five nodes against NetworkX neighborhoods.

Keep calculation code independent of FastAPI and persistence. Update README with metric definitions and known dataset limitations. Report metric schema, real-data summary, manual checks, full pytest, earlier-chapter regressions, and checklist.
