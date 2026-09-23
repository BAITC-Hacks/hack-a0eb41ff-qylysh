from pathlib import Path

import pandas as pd

from app.analytics.exceptions import DatasetLoadError
from app.analytics.models import RawDataset


def load_dataset(data_dir: Path | str) -> RawDataset:
    directory = Path(data_dir)
    if not directory.is_dir():
        raise DatasetLoadError(f"Dataset directory does not exist: {directory}")

    frames: dict[str, pd.DataFrame] = {}
    for name in ("nodes", "edges", "transactions"):
        path = directory / f"{name}.parquet"
        if not path.is_file():
            raise DatasetLoadError(f"Required parquet file is missing: {path}")
        try:
            frames[name] = pd.read_parquet(path)
        except Exception as exc:
            raise DatasetLoadError(f"Could not read {path}: {exc}") from exc

    return RawDataset(
        nodes=frames["nodes"],
        edges=frames["edges"],
        transactions=frames["transactions"],
    )
