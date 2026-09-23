# Prompt: Chapter 1 — Foundation and common data contracts

Continue the MoneyGraph backend and implement only the project foundation. Use Python 3.11+, FastAPI, Uvicorn, Pydantic v2, pydantic-settings, pytest, and httpx. Create the `app/api`, `app/core`, `app/schemas`, `app/analytics`, `app/repositories`, `app/services`, and `app/db` packages without business logic.

Create settings for `APP_NAME`, `APP_VERSION`, `API_V1_PREFIX`, `ENVIRONMENT`, and `DEBUG`, with defaults `MoneyGraph API`, `0.1.0`, `/api/v1`, `development`, and `true`. Build the FastAPI application and keep `/health` outside the versioned router. `/health` must return a typed response containing status, service, and version.

Freeze snake_case field names and create `NodeRole` with exactly: coordinator, consolidator, distributor, transit, terminal, peripheral. Create and constrain `HealthResponse`, `ApiError`, `NodeBase`, `NodeMetrics`, `NodeAnalytics`, `NodeRecord`, `EdgeRecord`, `ClusterRecord`, `GraphNode`, `GraphEdge`, and `GraphResponse`. Scores use 0..1, depth uses 0..4, identifiers and amounts are nonnegative, evidence is 1..200 characters.

Do not read parquet, implement analytics, connect a database, add authentication, CORS, Docker, ORM, or domain endpoints. Add `.env.example`, a minimal dependency file, README, health/schema tests, and `.gitignore`.

Definition of done: Uvicorn starts; `/health`, `/docs`, and `/openapi.json` return 200; `/api/v1` is fixed; all schemas validate and serialize in snake_case; all tests pass. Report files, schemas, endpoints, pytest output, and a PASS/FAIL checklist.
