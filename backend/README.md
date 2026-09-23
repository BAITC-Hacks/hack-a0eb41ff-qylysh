# MoneyGraph backend

## Project purpose

Python backend for the MoneyGraph financial transfer graph analytics application.

## Stack

Python 3.11+, FastAPI, Uvicorn, Pydantic v2, pydantic-settings, pandas, pyarrow, NetworkX, pytest, and httpx.

## Current stage

Chapter 4 — deterministic graph feature engineering.

The ingestion layer validates the parquet files, the graph builder creates a directed `src -> dst` money-flow graph, and feature engineering calculates one metric row per client. Every node is retained, including clients absent from all edges. Roles, database, clusters, and ranking are not implemented yet. `NodeRole` and the schemas define data contracts only; they do not calculate results.

## Input files

The input directory must contain `nodes.parquet`, `edges.parquet`, and `transactions.parquet`. The supplied dataset is in `../docs/data` relative to `backend/`.

## Validate dataset

From `backend/`, run:

```bash
python -m app.analytics.check_data --data-dir ../docs/data
```

The CLI exits with code 0 on success and a nonzero code on loading or validation failure.

## Build and check the graph

From `backend/`, run:

```bash
python -m app.analytics.check_graph --data-dir ../docs/data
```

Library usage after validation:

```python
from app.analytics.graph_builder import build_graph

graph = build_graph(dataset)
```

Nodes use `gid` as their key and retain `depth` and `is_seed`. Directed edges retain `sum_kzt`, `n_tx`, and `depth`.

## Calculate and check features

```bash
python -m app.analytics.check_features --data-dir ../docs/data
```

The feature table contains directed degree, KZT and transaction totals, weighted PageRank, pass-through, seed reach, depth truncation, and percentile signals. `seed_reach_count` includes a seed's zero-length path to itself. Percentiles use average ranks for ties. `pass_through` is `None` when observed incoming value is zero; seed incoming history remains known to be incomplete.

## Implementation roadmap

Detailed prompts for all 12 backend stages are in [`docs/chapters`](docs/chapters/README.md).

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

Python fields and the current schema JSON use snake_case. Core names are `gid`, `role`, `role_score`, `priority_score`, `cluster_id`, and `evidence`. The full field set is defined in `app/schemas/`. The planned `GET /api/v1/summary` response is an explicit exception: its external JSON uses camelCase as specified in `../docs/INTEGRATION_PLAN.md`, while backend data keeps snake_case.
