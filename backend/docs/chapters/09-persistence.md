# Prompt: Chapter 9 — SQLite analytical snapshot and CSV exports

Continue the frozen Chapters 1–8 backend. Materialize the completed analytical snapshot using Python's SQLite support and export the three required CSVs. Keep FastAPI domain endpoints out of scope.

Create a pipeline command that starts from the parquet directory, runs all frozen stages, and atomically replaces a snapshot. Store `nodes`, `edges`, `transactions`, and `clusters`. The nodes table contains base fields, roles, scores, cluster, metrics, truncation, and evidence. Create indexes for node gid, role, cluster_id, priority_score and edge src/dst. Use parameterized SQL and explicit transactions; do not introduce ORM unless a demonstrated need exists.

Export `nodes_roles.csv`, `clusters.csv`, and `top_nodes.csv` with the documented fixed columns and ordering. Ensure reruns replace data instead of duplicating rows. Create parent directories portably and avoid machine-specific paths. Failure must not leave a partially updated database or misleading exports.

Tests must build from synthetic input into temporary paths, inspect schema/indexes/counts, verify types/nullability, rerun idempotently, test rollback behavior, and compare random/sample rows across in-memory frames, SQLite, and CSV. Smoke-test real counts: 2248 nodes, 3119 edges, 4840 transactions, clusters present, top list at least 20.

Document one-command build and output files. Report DB schema/indexes, exports, real counts, cross-checks, tests, regressions, and checklist.
