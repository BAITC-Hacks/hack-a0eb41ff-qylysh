# MoneyGraph frontend implementation report

This report records the original frontend handoff. The backend has since completed its API, and the current real-mode integration results are in [INTEGRATION_STATUS.md](INTEGRATION_STATUS.md).

## Scope

All six chapters in `FRONTEND_PLAN.md` are implemented on the frontend. Domain screens run through an explicitly labelled mock service by default. `/summary` follows the frozen camelCase contract. DTOs for graph, nodes and clusters are frontend candidates pending backend/OpenAPI agreement.

## Completed chapters

1. Foundation: shared layout, six routes, redirects, active navigation, numeric GID search, common states and responsive SCSS.
2. Overview: summary service/DTO, KPI, role distribution, top nodes/clusters, formatters and loading/empty/error/success states.
3. Network: URL-driven GID/cluster graph, Cytoscape directed edges, role colours, seed emphasis, node details and depth-four warning.
4. Priority: URL search/role/page state, 20-row pagination, stable mock ordering, node details and graph links.
5. Clusters/reference: cluster cards and links, six-role methodology, score interpretation and six explicit data limitations.
6. Finalisation: clean install/build, lazy route chunks, production route smoke check and 1366×768 visual checks.

## Data and endpoints

- `GET /summary` — frozen `SummaryResponse`, external camelCase.
- `GET /nodes`, `/nodes/{gid}`, `/nodes/{gid}/graph` — frontend candidate DTO.
- `GET /clusters`, `/clusters/{clusterId}`, `/clusters/{clusterId}/graph` — frontend candidate DTO.
- `VITE_USE_MOCK_API=true` — labelled demonstration data.
- `VITE_MOCK_SCENARIO=success|empty|error` — reproducible UI states.
- `VITE_USE_MOCK_API=false` — HTTP through `VITE_API_URL`.

## Verification

- `npm ci`: PASS, 112 packages installed, 0 vulnerabilities.
- `npm run build`: PASS, TypeScript and Vite production build completed.
- Lazy chunks: PASS; Cytoscape is isolated in the Network chunk and the initial JS is about 326 kB before gzip.
- Production HTTP smoke: PASS for `/dashboard`, known/unknown GID network URLs, cluster network URL, Priority pages 1/2, Clusters, Methodology and Data limitations.
- Headless visual check at 1366×768: PASS for Dashboard and known-GID Network graph.
- `git diff --check`: PASS; reported only Git line-ending notices.
- Browser keyboard interaction walkthrough: NOT VERIFIED; no interactive browser automation suite is configured.
- Real API mode and field-by-field OpenAPI comparison: NOT VERIFIED; the backend currently exposes health only and has no domain endpoints.

## Known integration work

Before enabling real mode, freeze graph/node/cluster DTOs in `INTEGRATION_PLAN.md`, implement matching backend schemas and handlers, then compare real JSON and OpenAPI for casing, nullability, pagination and 404/422 responses. Mock output must not be used as evidence of backend analytics.
