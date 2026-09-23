import networkx as nx
import pandas as pd
import pytest

from app.analytics.exceptions import FeatureEngineeringError
from app.analytics.features import FEATURE_COLUMNS, calculate_features
from app.analytics.graph_builder import build_graph
from app.analytics.models import RawDataset


def _indexed(features: pd.DataFrame) -> pd.DataFrame:
    return features.set_index("gid")


def test_calculates_hand_checkable_metrics(synthetic_dataset: RawDataset) -> None:
    features = _indexed(calculate_features(build_graph(synthetic_dataset)))

    assert tuple(features.reset_index().columns) == FEATURE_COLUMNS
    assert features.loc[1, "out_degree"] == 1
    assert features.loc[2, "in_degree"] == 1
    assert features.loc[2, "out_degree"] == 1
    assert features.loc[2, "in_kzt"] == 30.0
    assert features.loc[2, "out_kzt"] == 20.0
    assert features.loc[2, "total_volume"] == 50.0
    assert features.loc[2, "in_tx"] == 2
    assert features.loc[2, "out_tx"] == 1
    assert features.loc[2, "pass_through"] == pytest.approx(2 / 3)
    assert features["pagerank"].sum() == pytest.approx(1.0)


def test_seed_reach_counts_distinct_reachable_seeds() -> None:
    graph = nx.DiGraph()
    graph.add_nodes_from([
        (1, {"depth": 0, "is_seed": True}),
        (2, {"depth": 0, "is_seed": True}),
        (3, {"depth": 1, "is_seed": False}),
    ])
    graph.add_edges_from([
        (1, 3, {"sum_kzt": 1.0, "n_tx": 1, "depth": 1}),
        (2, 3, {"sum_kzt": 1.0, "n_tx": 1, "depth": 1}),
    ])

    features = _indexed(calculate_features(graph))

    assert features.loc[1, "seed_reach_count"] == 1
    assert features.loc[2, "seed_reach_count"] == 1
    assert features.loc[3, "seed_reach_count"] == 2


def test_handles_isolates_zero_input_and_truncation() -> None:
    graph = nx.DiGraph()
    graph.add_node(1, depth=4, is_seed=False)

    features = _indexed(calculate_features(graph))

    assert features.loc[1, "total_degree"] == 0
    assert features.loc[1, "total_volume"] == 0
    assert features.loc[1, "pass_through"] is None
    assert bool(features.loc[1, "truncated_by_depth"])
    assert features.loc[1, "pagerank"] == pytest.approx(1.0)


def test_percentiles_are_bounded_and_ties_match(synthetic_dataset: RawDataset) -> None:
    features = calculate_features(build_graph(synthetic_dataset))
    percentile_columns = [column for column in features if column.endswith("_percentile")]

    for column in percentile_columns:
        assert features[column].between(0, 1).all()
    tied = features.loc[features["in_degree"] == 1, "in_degree_percentile"]
    assert tied.nunique() == 1


def test_output_is_complete_deterministic_and_does_not_mutate_graph(
    synthetic_dataset: RawDataset,
) -> None:
    graph = build_graph(synthetic_dataset)
    nodes_before = list(graph.nodes(data=True))
    edges_before = list(graph.edges(data=True))

    first = calculate_features(graph)
    second = calculate_features(graph)

    assert len(first) == graph.number_of_nodes()
    assert first["gid"].is_unique
    pd.testing.assert_frame_equal(first, second)
    assert list(graph.nodes(data=True)) == nodes_before
    assert list(graph.edges(data=True)) == edges_before


def test_requires_directed_graph_and_attributes() -> None:
    with pytest.raises(FeatureEngineeringError, match="directed graph"):
        calculate_features(nx.Graph())

    graph = nx.DiGraph()
    graph.add_node(1, depth=0)
    with pytest.raises(FeatureEngineeringError, match="missing required attributes"):
        calculate_features(graph)
