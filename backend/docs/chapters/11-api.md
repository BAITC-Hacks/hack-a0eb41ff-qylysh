# Prompt: Chapter 11 — FastAPI domain endpoints

Continue the frozen Chapters 1–10 backend and implement read-only FastAPI endpoints backed by the Chapter 9 SQLite snapshot. Do not recalculate analytics inside requests and do not change the Chapter 10 response contract.

Implement `GET /api/v1/summary`, `/nodes`, `/nodes/{gid}`, `/nodes/{gid}/graph`, `/top-nodes`, `/clusters`, `/clusters/{cluster_id}`, and `/clusters/{cluster_id}/graph`. Add a small repository layer with parameterized SQLite queries and a service layer only where orchestration is needed.

Nodes filtering supports role, cluster, minimum priority, seed flag, gid search, page, and bounded limit. Define stable ordering. Graph endpoints return Cytoscape-friendly nodes and edges with explicit neighborhood/depth/size bounds to prevent unbounded payloads. Cluster endpoints return members/summaries consistently. Known empty collections return 200; unknown resources return the frozen `ApiError` body with 404; invalid queries return 422.

Manage database path through settings and connections safely per request. Add only required CORS if the frontend integration explicitly needs it and document allowed origins. Never expose internal SQL rows directly.

Test every happy path, filters, pagination, ordering, empty results, 404, 422, graph direction, payload bounds, response-model stripping, and OpenAPI compatibility using a temporary synthetic database. Smoke-test the real snapshot. Report endpoints, examples, tests, contract comparison, Chapter 1 regression, and checklist.
