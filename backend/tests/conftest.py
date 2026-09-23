import pandas as pd
import pytest

from app.analytics.models import RawDataset


@pytest.fixture
def synthetic_dataset() -> RawDataset:
    return RawDataset(
        nodes=pd.DataFrame({
            "gid": [1, 2, 3],
            "depth": [0, 1, 2],
            "is_seed": [True, False, False],
        }),
        edges=pd.DataFrame({
            "src": [1, 2],
            "dst": [2, 3],
            "sum_kzt": [30.0, 20.0],
            "n_tx": [2, 1],
            "depth": [1, 2],
        }),
        transactions=pd.DataFrame({
            "src": [1, 1, 2],
            "dst": [2, 2, 3],
            "date": pd.to_datetime(["2026-07-01", "2026-07-02", "2026-07-03"]),
            "sum_kzt": [10.0, 20.0, 20.0],
        }),
    )
