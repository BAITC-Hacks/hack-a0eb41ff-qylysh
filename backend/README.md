# MoneyGraph backend

## Project purpose

Python backend for the MoneyGraph financial transfer graph analytics application.

## Stack

Python 3.11+, FastAPI, Uvicorn, Pydantic v2, pydantic-settings, pandas, pyarrow, NetworkX, pytest, and httpx.

## Current stage

Chapter 12 — integrated analytical pipeline, snapshot, and read API.

The complete local pipeline validates parquet files, builds the directed money-flow graph, calculates features and explainable roles, clusters the network, ranks nodes, and writes a SQLite read model plus CSV exports. FastAPI serves the frozen frontend contract from that snapshot.

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

## Assign structural roles

```bash
python -m app.analytics.check_roles --data-dir ../docs/data
```

Rules are evaluated in this order: coordinator, consolidator, distributor, transit, terminal, peripheral. Coordinators combine top seed reach and PageRank; consolidators combine high incoming degree and volume; distributors combine high outgoing degree and volume; transit requires observed incoming and outgoing flow with pass-through 0.8–1.2. Seed nodes are excluded from the transit rule. Terminal requires observed incoming flow, zero outgoing degree, and `depth < 4`; depth-four truncation therefore never creates a terminal automatically. Peripheral is the exhaustive fallback. `role_score` measures rule-match strength, while `priority_score` combines role strength, PageRank, seed reach, volume, and degree percentiles. Neither score is a probability of guilt.

## Build the analytical snapshot

```bash
python -m app.analytics.run_pipeline --data-dir ../docs/data --database analysis.db --out-dir out
```

The command replaces `analysis.db` atomically and writes `out/nodes_roles.csv`, `out/clusters.csv`, and `out/top_nodes.csv`. Repeated runs replace prior results and do not duplicate rows.

## Implementation roadmap

Detailed prompts for all 12 backend stages are in [`docs/chapters`](docs/chapters/README.md).

## Expected hackathon dataset

Nodes: 2248. Edges: 3119. Transactions: 4840. Seeds: 81. The CLI checks these counts; library validation can omit them for other datasets.

## Validation performed

Required columns, semantic dtypes, null and infinite values, nonnegative amounts and counts, node depth 0..4, edge depth 1..4, unique `gid`, unique edge `(src, dst)` pairs, references to existing nodes, and expected counts are checked. Since the dataset documentation defines edges as aggregated transactions, validation also checks pair sets, transaction counts, and sums with floating point tolerance. Extra columns are allowed.

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
- `GET /api/v1/summary`
- `GET /api/v1/nodes`
- `GET /api/v1/nodes/{gid}`
- `GET /api/v1/nodes/{gid}/graph`
- `GET /api/v1/top-nodes`
- `GET /api/v1/clusters`
- `GET /api/v1/clusters/{cluster_id}`
- `GET /api/v1/clusters/{cluster_id}/graph`

Run the snapshot command before starting the API. Node list filters are `role`, `cluster`, `minPriority`, `isSeed`, `search`, `page`, and frontend-compatible `pageSize`; `limit` remains an accepted alias.

## Naming conventions

Python, DataFrame, SQLite, and CSV fields use snake_case. Core names are `gid`, `role`, `role_score`, `priority_score`, `cluster_id`, and `evidence`. Final `/api/v1` response models serialize JSON in camelCase to match the checked-in TypeScript contract; `/health` retains its frozen Chapter 1 response.

External API GIDs (`gid`, `topGid`, graph `source`/`target`, and GID graph focus) are decimal strings. Internal Parquet and SQLite GIDs remain int64. This preserves exact 18-digit identifiers in JavaScript. Local browser requests from `http://localhost:5173` and `http://127.0.0.1:5173` are allowed by CORS; override `MONEYGRAPH_CORS_ORIGINS` with a comma-separated list for other origins.

## Scaling beyond the hackathon dataset

At roughly one million nodes, replace in-memory pandas/NetworkX stages with chunked parquet reads, a graph engine or sparse distributed implementation, and batch-written database tables. Compute reachability and centrality approximately or incrementally, keep API graph payloads bounded, and move snapshot construction to an offline job. The API can continue serving the same contract from indexed read tables.
