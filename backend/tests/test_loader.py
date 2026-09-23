import pandas as pd
import pytest

from app.analytics.exceptions import DatasetLoadError
from app.analytics.loader import load_dataset
from app.analytics.models import RawDataset


def write_parquet_dataset(directory, dataset: RawDataset) -> None:
    directory.mkdir()
    dataset.nodes.to_parquet(directory / "nodes.parquet")
    dataset.edges.to_parquet(directory / "edges.parquet")
    dataset.transactions.to_parquet(directory / "transactions.parquet")


def test_loader_reads_all_files_without_changing_values(tmp_path, synthetic_dataset: RawDataset) -> None:
    directory = tmp_path / "data"
    write_parquet_dataset(directory, synthetic_dataset)

    loaded = load_dataset(str(directory))

    assert isinstance(loaded, RawDataset)
    pd.testing.assert_frame_equal(loaded.nodes, synthetic_dataset.nodes)
    pd.testing.assert_frame_equal(loaded.edges, synthetic_dataset.edges)
    pd.testing.assert_frame_equal(loaded.transactions, synthetic_dataset.transactions)


def test_missing_directory_raises_load_error(tmp_path) -> None:
    with pytest.raises(DatasetLoadError, match="directory does not exist"):
        load_dataset(tmp_path / "missing")


@pytest.mark.parametrize("filename", ["nodes.parquet", "edges.parquet", "transactions.parquet"])
def test_missing_file_raises_load_error(tmp_path, synthetic_dataset: RawDataset, filename: str) -> None:
    directory = tmp_path / "data"
    write_parquet_dataset(directory, synthetic_dataset)
    (directory / filename).unlink()

    with pytest.raises(DatasetLoadError, match=filename):
        load_dataset(directory)


def test_corrupt_parquet_raises_load_error(tmp_path, synthetic_dataset: RawDataset) -> None:
    directory = tmp_path / "data"
    write_parquet_dataset(directory, synthetic_dataset)
    (directory / "edges.parquet").write_bytes(b"not parquet")

    with pytest.raises(DatasetLoadError, match="edges.parquet"):
        load_dataset(directory)
