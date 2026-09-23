# Prompt: Chapter 10 — Frozen API contract

Continue the frozen Chapters 1–9 backend. Define the complete Pydantic/OpenAPI response contract before implementing handlers. Do not add database queries or domain endpoint behavior in this chapter.

Create response and query-related schemas for summary, paginated nodes, node details, graph payloads, top nodes, cluster lists, and cluster details. At minimum include `SummaryResponse`, `NodeListItem`, `NodeDetailsResponse`, `GraphNode`, `GraphEdge`, `GraphResponse`, `ClusterListItem`, `ClusterResponse`, and `PaginatedNodesResponse`. Reuse existing Chapter 1 contracts where compatible rather than silently changing them.

Choose and document one JSON naming convention for the final frontend API after checking existing TypeScript expectations. Define nullability, numeric bounds, pagination metadata, graph semantics, and error bodies explicitly. Prevent leakage of SQLite-only columns. Provide representative JSON examples and export a committed OpenAPI contract or deterministic schema snapshot for review.

Tests must instantiate every schema, reject invalid scores/identifiers, validate nullability, serialization names, nested graph data, pagination, extra-field policy, examples, and deterministic OpenAPI output. Existing `/health` behavior and `/api/v1` prefix remain frozen.

Update contract documentation for frontend developers. Report every schema and field, naming decision, OpenAPI artifact, tests, regressions, and checklist. Treat the accepted output as frozen input to Chapter 11.
