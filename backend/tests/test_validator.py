from datetime import date
import sys

import pandas as pd
import pytest

from app.analytics import check_data
from app.analytics.exceptions import DatasetValidationError
from app.analytics.models import DatasetExpectations, RawDataset
from app.analytics.validator import validate_dataset


def test_valid_synthetic_dataset_passes(synthetic_dataset: RawDataset) -> None:
    validate_dataset(synthetic_dataset)


@pytest.mark.parametrize(
    ("table", "column"),
    [("nodes", "gid"), ("edges", "n_tx"), ("transactions", "date")],
)
def test_missing_required_column_fails(synthetic_dataset: RawDataset, table: str, column: str) -> None:
    frame = getattr(synthetic_dataset, table)
    frame.drop(columns=column, inplace=True)

    with pytest.raises(DatasetValidationError, match=f"{table}.{column} is missing"):
        validate_dataset(synthetic_dataset)


@pytest.mark.parametrize(
    ("table", "column", "value", "expected"),
    [
        ("nodes", "gid", 1, "duplicate values"),
        ("nodes", "gid", float("nan"), "nodes.gid contains null"),
        ("nodes", "depth", 5, "nodes.depth contains values above 4"),
        ("nodes", "depth", 1.5, "integer-like"),
        ("nodes", "is_seed", None, "nodes.is_seed contains null"),
        ("edges", "sum_kzt", -1.0, "edges.sum_kzt contains values below 0"),
        ("edges", "sum_kzt", float("nan"), "edges.sum_kzt contains null"),
        ("transactions", "sum_kzt", -1.0, "transactions.sum_kzt contains values below 0"),
        ("edges", "src", 99, "edges.src contains 1 unknown gids"),
        ("edges", "dst", 99, "edges.dst contains 1 unknown gids"),
        ("transactions", "src", 99, "transactions.src contains 1 unknown gids"),
        ("transactions", "dst", 99, "transactions.dst contains 1 unknown gids"),
        ("edges", "depth", 0, "edges.depth contains values below 1"),
        ("edges", "n_tx", float("inf"), "edges.n_tx must be finite"),
        ("transactions", "date", "not-a-date", "transactions.date must contain date"),
    ],
)
def test_bad_values_fail(synthetic_dataset: RawDataset, table: str, column: str, value, expected: str) -> None:
    frame = getattr(synthetic_dataset, table)
    if value is None or column == "date":
        frame[column] = frame[column].astype("object")
    elif isinstance(value, float) and column in {"depth", "n_tx"}:
        frame[column] = frame[column].astype("float64")
    frame.at[1 if (table, column, value) == ("nodes", "gid", 1) else 0, column] = value

    with pytest.raises(DatasetValidationError, match=expected):
        validate_dataset(synthetic_dataset)


@pytest.mark.parametrize(
    ("expectations", "expected"),
    [
        (DatasetExpectations(node_count=4), "nodes has 3 rows; expected 4"),
        (DatasetExpectations(edge_count=3), "edges has 2 rows; expected 3"),
        (DatasetExpectations(transaction_count=4), "transactions has 3 rows; expected 4"),
        (DatasetExpectations(seed_count=2), "nodes has 1 seed nodes; expected 2"),
    ],
)
def test_expected_counts_are_optional_and_independent(
    synthetic_dataset: RawDataset, expectations: DatasetExpectations, expected: str
) -> None:
    with pytest.raises(DatasetValidationError, match=expected):
        validate_dataset(synthetic_dataset, expectations)


def test_validator_does_not_mutate_any_frame(synthetic_dataset: RawDataset) -> None:
    before = RawDataset(
        nodes=synthetic_dataset.nodes.copy(deep=True),
        edges=synthetic_dataset.edges.copy(deep=True),
        transactions=synthetic_dataset.transactions.copy(deep=True),
    )

    validate_dataset(synthetic_dataset)

    pd.testing.assert_frame_equal(synthetic_dataset.nodes, before.nodes)
    pd.testing.assert_frame_equal(synthetic_dataset.edges, before.edges)
    pd.testing.assert_frame_equal(synthetic_dataset.transactions, before.transactions)


def test_valid_dtype_variants_and_extra_columns(synthetic_dataset: RawDataset) -> None:
    synthetic_dataset.nodes["gid"] = synthetic_dataset.nodes["gid"].astype("int64[pyarrow]")
    synthetic_dataset.nodes["depth"] = synthetic_dataset.nodes["depth"].astype("Int32")
    synthetic_dataset.nodes["is_seed"] = synthetic_dataset.nodes["is_seed"].astype("boolean")
    synthetic_dataset.edges["depth"] = synthetic_dataset.edges["depth"].astype("int8")
    synthetic_dataset.transactions["date"] = [date(2026, 7, 1), date(2026, 7, 2), date(2026, 7, 3)]
    synthetic_dataset.nodes["extra"] = ["a", "b", "c"]

    validate_dataset(synthetic_dataset)


def test_duplicate_edge_pair_fails(synthetic_dataset: RawDataset) -> None:
    synthetic_dataset.edges.loc[1, ["src", "dst"]] = [1, 2]

    with pytest.raises(DatasetValidationError, match="duplicate \\(src, dst\\) pairs"):
        validate_dataset(synthetic_dataset)


def test_edge_aggregation_mismatch_fails(synthetic_dataset: RawDataset) -> None:
    synthetic_dataset.edges.at[0, "n_tx"] = 3
    synthetic_dataset.edges.at[1, "sum_kzt"] = 21.0

    with pytest.raises(DatasetValidationError) as exc_info:
        validate_dataset(synthetic_dataset)

    assert "edges.n_tx differs" in str(exc_info.value)
    assert "edges.sum_kzt differs" in str(exc_info.value)


def test_multiple_errors_are_reported_together(synthetic_dataset: RawDataset) -> None:
    synthetic_dataset.nodes.at[1, "gid"] = 1
    synthetic_dataset.edges.at[0, "sum_kzt"] = -1

    with pytest.raises(DatasetValidationError) as exc_info:
        validate_dataset(synthetic_dataset)

    assert len(exc_info.value.errors) >= 2
    assert "duplicate values" in str(exc_info.value)
    assert "values below 0" in str(exc_info.value)


def test_cli_exit_codes(tmp_path, synthetic_dataset: RawDataset, monkeypatch, capsys) -> None:
    directory = tmp_path / "data"
    directory.mkdir()
    synthetic_dataset.nodes.to_parquet(directory / "nodes.parquet")
    synthetic_dataset.edges.to_parquet(directory / "edges.parquet")
    synthetic_dataset.transactions.to_parquet(directory / "transactions.parquet")
    monkeypatch.setattr(check_data, "HACKATHON_EXPECTATIONS", DatasetExpectations(3, 2, 3, 1))
    monkeypatch.setattr(sys, "argv", ["check_data", "--data-dir", str(directory)])

    assert check_data.main() == 0
    assert "Dataset validation: PASSED" in capsys.readouterr().out

    synthetic_dataset.nodes.at[1, "gid"] = 1
    synthetic_dataset.nodes.to_parquet(directory / "nodes.parquet")
    assert check_data.main() != 0
    assert "Dataset validation: FAILED" in capsys.readouterr().out
