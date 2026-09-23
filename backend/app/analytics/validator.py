from datetime import date, datetime
from math import isclose, isfinite

import pandas as pd
from pandas.api.types import is_bool_dtype, is_datetime64_any_dtype, is_integer_dtype, is_numeric_dtype

from app.analytics.exceptions import DatasetValidationError
from app.analytics.models import DatasetExpectations, RawDataset


NODES_REQUIRED_COLUMNS = frozenset({"gid", "depth", "is_seed"})
EDGES_REQUIRED_COLUMNS = frozenset({"src", "dst", "sum_kzt", "n_tx", "depth"})
TRANSACTIONS_REQUIRED_COLUMNS = frozenset({"src", "dst", "date", "sum_kzt"})


def _required_columns(frame: pd.DataFrame, table: str, required: frozenset[str], errors: list[str]) -> None:
    for column in sorted(required - set(frame.columns)):
        errors.append(f"{table}.{column} is missing")


def _finite_numeric(series: pd.Series) -> bool:
    return is_numeric_dtype(series.dtype) and not is_bool_dtype(series.dtype) and bool(
        series.dropna().map(lambda value: isfinite(value)).all()
    )


def _integer_like(series: pd.Series) -> bool:
    if not _finite_numeric(series):
        return False
    if is_integer_dtype(series.dtype):
        return True
    return bool(series.dropna().map(lambda value: value == int(value)).all())


def _check_numeric(
    frame: pd.DataFrame,
    table: str,
    column: str,
    errors: list[str],
    *,
    integer: bool = False,
    minimum: int | None = None,
    maximum: int | None = None,
) -> bool:
    if column not in frame:
        return False
    series = frame[column]
    label = f"{table}.{column}"
    valid = True
    if series.isna().any():
        errors.append(f"{label} contains null values")
        valid = False
    if not _finite_numeric(series):
        errors.append(f"{label} must be finite numeric values")
        return False
    if integer and not _integer_like(series):
        errors.append(f"{label} must contain integer-like values")
        valid = False
    values = series.dropna()
    if minimum is not None and bool((values < minimum).any()):
        errors.append(f"{label} contains values below {minimum}")
        valid = False
    if maximum is not None and bool((values > maximum).any()):
        errors.append(f"{label} contains values above {maximum}")
        valid = False
    return valid


def _check_boolean(frame: pd.DataFrame, table: str, column: str, errors: list[str]) -> bool:
    if column not in frame:
        return False
    series = frame[column]
    valid = True
    if series.isna().any():
        errors.append(f"{table}.{column} contains null values")
        valid = False
    if not (is_bool_dtype(series.dtype) or all(isinstance(value, bool) for value in series.dropna())):
        errors.append(f"{table}.{column} must contain boolean values")
        valid = False
    return valid


def _check_date(frame: pd.DataFrame, errors: list[str]) -> None:
    if "date" not in frame:
        return
    series = frame["date"]
    if series.isna().any():
        errors.append("transactions.date contains null values")
    # The supplied parquet returns Python date objects; datetime dtypes are also valid.
    if not (is_datetime64_any_dtype(series.dtype) or all(
        isinstance(value, (date, datetime)) for value in series.dropna()
    )):
        errors.append("transactions.date must contain date or datetime values")


def _check_references(
    frame: pd.DataFrame,
    table: str,
    column: str,
    gids: set[int],
    errors: list[str],
) -> None:
    if column not in frame or not _integer_like(frame[column]) or frame[column].isna().any():
        return
    unknown = set(frame[column]) - gids
    if unknown:
        examples = sorted(unknown)[:5]
        errors.append(f"{table}.{column} contains {len(unknown)} unknown gids: {examples}")


def _check_edge_aggregation(dataset: RawDataset, errors: list[str]) -> None:
    edges = dataset.edges
    transactions = dataset.transactions
    if {"src", "dst"}.issubset(edges.columns) and all(
        _integer_like(edges[column]) and not edges[column].isna().any() for column in ("src", "dst")
    ) and edges.duplicated(subset=["src", "dst"]).any():
        examples = edges.loc[edges.duplicated(subset=["src", "dst"], keep=False), ["src", "dst"]]
        errors.append(f"edges contains duplicate (src, dst) pairs: {examples.drop_duplicates().head(5).values.tolist()}")
        return

    needed_edges = {"src", "dst", "sum_kzt", "n_tx"}
    needed_transactions = {"src", "dst", "sum_kzt"}
    if not needed_edges.issubset(edges.columns) or not needed_transactions.issubset(transactions.columns):
        return
    if any(edges[column].isna().any() for column in needed_edges):
        return
    if any(transactions[column].isna().any() for column in needed_transactions):
        return
    if not all(_finite_numeric(edges[column]) for column in needed_edges):
        return
    if not all(_finite_numeric(transactions[column]) for column in needed_transactions):
        return
    grouped = transactions.groupby(["src", "dst"], as_index=False).agg(
        sum_kzt=("sum_kzt", "sum"), n_tx=("sum_kzt", "size")
    )
    edge_pairs = set(zip(edges["src"], edges["dst"]))
    transaction_pairs = set(zip(grouped["src"], grouped["dst"]))
    if edge_pairs != transaction_pairs:
        missing = sorted(transaction_pairs - edge_pairs)[:5]
        extra = sorted(edge_pairs - transaction_pairs)[:5]
        errors.append(
            "edges and transactions contain different (src, dst) pairs: "
            f"{len(transaction_pairs - edge_pairs)} missing in edges (examples: {missing}), "
            f"{len(edge_pairs - transaction_pairs)} missing in transactions (examples: {extra})"
        )
    joined = edges.merge(grouped, on=["src", "dst"], how="inner", suffixes=("_edge", "_transactions"))
    wrong_counts = joined[joined["n_tx_edge"] != joined["n_tx_transactions"]]
    if not wrong_counts.empty:
        errors.append(f"edges.n_tx differs from transactions for {len(wrong_counts)} pairs")
    close = joined.apply(
        lambda row: isclose(row["sum_kzt_edge"], row["sum_kzt_transactions"], rel_tol=1e-9, abs_tol=1e-6),
        axis=1,
    )
    if not bool(close.all()):
        errors.append(f"edges.sum_kzt differs from transactions for {int((~close).sum())} pairs")


def validate_dataset(dataset: RawDataset, expectations: DatasetExpectations | None = None) -> None:
    errors: list[str] = []
    nodes, edges, transactions = dataset.nodes, dataset.edges, dataset.transactions
    _required_columns(nodes, "nodes", NODES_REQUIRED_COLUMNS, errors)
    _required_columns(edges, "edges", EDGES_REQUIRED_COLUMNS, errors)
    _required_columns(transactions, "transactions", TRANSACTIONS_REQUIRED_COLUMNS, errors)

    gid_valid = _check_numeric(nodes, "nodes", "gid", errors, integer=True, minimum=0)
    _check_numeric(nodes, "nodes", "depth", errors, integer=True, minimum=0, maximum=4)
    seed_valid = _check_boolean(nodes, "nodes", "is_seed", errors)
    if "gid" in nodes and nodes["gid"].dropna().duplicated().any():
        examples = nodes.loc[nodes["gid"].notna() & nodes["gid"].duplicated(keep=False), "gid"].drop_duplicates().head(5).tolist()
        errors.append(f"nodes.gid contains duplicate values: {examples}")

    for table, frame in (("edges", edges), ("transactions", transactions)):
        _check_numeric(frame, table, "src", errors, integer=True, minimum=0)
        _check_numeric(frame, table, "dst", errors, integer=True, minimum=0)
        _check_numeric(frame, table, "sum_kzt", errors, minimum=0)
    _check_numeric(edges, "edges", "n_tx", errors, integer=True, minimum=0)
    # Documentation defines edge depth as the discovery hop, from 1 through 4.
    _check_numeric(edges, "edges", "depth", errors, integer=True, minimum=1, maximum=4)
    _check_date(transactions, errors)

    if gid_valid:
        gids = set(nodes["gid"])
        for table, frame in (("edges", edges), ("transactions", transactions)):
            _check_references(frame, table, "src", gids, errors)
            _check_references(frame, table, "dst", gids, errors)

    _check_edge_aggregation(dataset, errors)

    if expectations is not None:
        for table, frame, expected in (
            ("nodes", nodes, expectations.node_count),
            ("edges", edges, expectations.edge_count),
            ("transactions", transactions, expectations.transaction_count),
        ):
            if expected is not None and len(frame) != expected:
                errors.append(f"{table} has {len(frame)} rows; expected {expected}")
        if expectations.seed_count is not None and seed_valid:
            actual_seeds = int(nodes["is_seed"].sum())
            if actual_seeds != expectations.seed_count:
                errors.append(f"nodes has {actual_seeds} seed nodes; expected {expectations.seed_count}")

    if errors:
        raise DatasetValidationError(errors)
