# Prompt: Chapter 2 — Dataset loading and validation

Continue the frozen Chapter 1 backend. Implement only ingestion for `nodes.parquet`, `edges.parquet`, and `transactions.parquet`. Inspect the supplied `docs` README, starter, and real parquet schemas before coding. Add pandas and pyarrow without removing existing dependencies.

Create a `RawDataset` dataclass with `nodes`, `edges`, and `transactions` DataFrames. Implement `load_dataset(data_dir: Path | str)` using `pathlib`, with clear `DatasetLoadError` errors for a missing directory, missing files, or unreadable parquet. Never hardcode a machine path and never rename, cast, fill, drop, or repair source data.

Implement `validate_dataset()` that collects all errors in one `DatasetValidationError`. Centralize required columns and hackathon counts. Validate semantic dtypes, required nulls, finite numeric values, integer-like identifiers/counts, nonnegative amounts, node depth 0..4, edge depth 1..4, boolean `is_seed`, unique node gid, unique aggregated edge pairs, and all src/dst references. Since project documentation says edges aggregate transactions, compare pair sets, `n_tx`, and `sum_kzt` with float tolerance.

Keep fixed counts optional through `DatasetExpectations`; the real CLI uses 2248 nodes, 3119 edges, 4840 transactions, and 81 seeds. Provide `python -m app.analytics.check_data --data-dir PATH` with exit 0 on valid data and nonzero on failure. Library functions must not print or mutate DataFrames.

Test loading via temporary parquet files, every important validation failure, aggregation consistency, dtype variants, accumulated errors, expected counts, CLI exit codes, and deep non-mutation. Run the real dataset smoke check when available. Do not construct a graph or implement analytics. Report actual schemas, validation rules, real-data counts, tests, Chapter 1 regression, and a checklist.
