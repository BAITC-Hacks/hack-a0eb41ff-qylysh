# Prompt: Chapter 7 — Reproducible clustering

Continue the frozen Chapters 1–6 backend. Add reproducible community detection and cluster summaries only. Do not calculate priority, persist, or expose API endpoints.

Keep the canonical graph directed. Create a separate weighted undirected projection for Louvain, aggregating reciprocal directed amounts correctly. Run NetworkX Louvain with `weight="sum_kzt"` and fixed seed 42. Define deterministic cluster IDs independent of incidental community iteration order, for example by sorting communities by a stable key.

Assign every node, including isolates, a non-null `cluster_id`. Produce `clusters_df` with `cluster_id`, `n_nodes`, `n_seed`, `sum_kzt_internal`, `top_gids`, and `hypothesis`. Define internal volume without double-counting directed edges. Select top gids with a documented deterministic score and tie-break. Generate cautious, deterministic hypotheses based on aggregate structure.

Test projection weights, reciprocal edges, isolates, fixed-seed reproducibility, stable IDs, full assignment, summary counts, internal sums, top-gid membership, hypothesis length, non-mutation, and invalid inputs. Real-data checks require summed `n_nodes == 2248`, no missing cluster IDs, and identical repeated output.

Document that the undirected projection is used only for community detection. Report cluster distribution and summaries, reproducibility evidence, tests, regressions, and checklist.
