# Prompt: Chapter 12 — End-to-end integration and regression

Continue the completed Chapters 1–11. Add final automated proof that a clean checkout can rebuild and serve the MoneyGraph MVP. Do not redesign algorithms or contracts unless a failing invariant proves a defect.

Build an end-to-end test and documented command that start with the three parquet files, validate them, build the directed graph, compute features, roles, scores/evidence, clusters, ranking, CSVs and SQLite, then start or exercise FastAPI. Outputs must be reproducible after deleting the generated database and CSV directory.

Assert 2248 unique nodes, 3119 edges, 4840 transactions, 81 seeds, six-role validity, non-null role/cluster/evidence, scores within 0..1, evidence length, at least 20 ranked nodes, required CSV schemas, SQLite consistency, and idempotent reruns. API regression covers known and unknown gid, summary, filters, node graph, clusters, cluster graph, and sorted top nodes.

Compare each backend JSON response field-for-field with the frozen OpenAPI contract and the checked-in TypeScript interfaces without editing frontend application behavior. Add a lightweight compatibility check rather than duplicating interfaces manually where possible. Verify `/health`, `/docs`, and `/openapi.json`.

Document a clean-machine setup, one-command pipeline, server startup, limitations, performance, and how the approach changes near one million nodes. Measure the full real-data run against the five-minute requirement.

Report created outputs, elapsed time, final counts, API matrix, contract compatibility, full pytest results, remaining warnings/limitations, and a PASS/FAIL checklist for every chapter. Finish only when all mandatory checks pass.
