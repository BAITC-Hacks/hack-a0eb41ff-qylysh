# MoneyGraph backend

## Project purpose

Python backend for the MoneyGraph financial transfer graph analytics application.

## Stack

Python 3.11+, FastAPI, Uvicorn, Pydantic v2, pydantic-settings, pandas, pyarrow, pytest, and httpx.

## Current stage

Chapter 2 — dataset loading and validation.

The ingestion layer reads and validates the parquet files. Graph analytics, database, roles, clusters, and ranking are not implemented yet. `NodeRole` and the schemas define data contracts only; they do not calculate results. The starter code in `../docs/starter` is separate from this backend.

## Input files

The input directory must contain `nodes.parquet`, `edges.parquet`, and `transactions.parquet`. The supplied dataset is in `../docs/data` relative to `backend/`.

## Validate dataset

From `backend/`, run:

```bash
python -m app.analytics.check_data --data-dir ../docs/data
```

The CLI exits with code 0 on success and a nonzero code on loading or validation failure.

## Expected hackathon dataset

Nodes: 2248. Edges: 3119. Transactions: 4840. Seeds: 81. The CLI checks these counts; library validation can omit them for other datasets.

## Validation performed

Required columns, semantic dtypes, null and infinite values, nonnegative amounts and counts, node depth 0..4, edge depth 1..4, unique `gid`, unique edge `(src, dst)` pairs, references to existing nodes, and expected counts are checked. Since the dataset documentation defines edges as aggregated transactions, validation also checks the pair sets, transaction counts, and sums with floating point tolerance. Extra columns are allowed. No graph analytics is performed at this stage.

## Installation

Run these commands from `backend/`:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

Activate `.venv` using your shell's activation command before running the following commands. Copy `.env.example` to `.env` if you want to override settings. Environment variables use the `MONEYGRAPH_` prefix.

## Run

```bash
uvicorn app.main:app --reload
```

## Tests

```bash
pytest
```

## Endpoints

- `GET /health` — health status, outside the versioned API.
- `GET /docs` — interactive API documentation.
- `GET /openapi.json` — OpenAPI schema.

The API router uses `/api/v1`; domain routes have not been added.

## Naming conventions

Python fields and JSON use snake_case. Core names are `gid`, `role`, `role_score`, `priority_score`, `cluster_id`, and `evidence`. The full field set is defined in `app/schemas/`.
