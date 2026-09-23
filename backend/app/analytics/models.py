from dataclasses import dataclass

import pandas as pd


@dataclass
class RawDataset:
    nodes: pd.DataFrame
    edges: pd.DataFrame
    transactions: pd.DataFrame


@dataclass(frozen=True)
class DatasetExpectations:
    node_count: int | None = None
    edge_count: int | None = None
    transaction_count: int | None = None
    seed_count: int | None = None


EXPECTED_NODE_COUNT = 2248
EXPECTED_EDGE_COUNT = 3119
EXPECTED_TRANSACTION_COUNT = 4840
EXPECTED_SEED_COUNT = 81

HACKATHON_EXPECTATIONS = DatasetExpectations(
    node_count=EXPECTED_NODE_COUNT,
    edge_count=EXPECTED_EDGE_COUNT,
    transaction_count=EXPECTED_TRANSACTION_COUNT,
    seed_count=EXPECTED_SEED_COUNT,
)
