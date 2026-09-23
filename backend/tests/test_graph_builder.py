import networkx as nx
import pandas as pd
import pytest

from app.analytics.exceptions import GraphConstructionError
from app.analytics.graph_builder import build_graph
from app.analytics.models import RawDataset


def test_builds_directed_graph_with_all_attributes(synthetic_dataset: RawDataset) -> None:
    graph = build_graph(synthetic_dataset)

    assert isinstance(graph, nx.DiGraph)
    assert graph.is_directed()
    assert graph.number_of_nodes() == 3
    assert graph.number_of_edges() == 2
    assert graph.nodes[1] == {"depth": 0, "is_seed": True}
    assert graph[1][2] == {"sum_kzt": 30.0, "n_tx": 2, "depth": 1}
    assert graph.has_edge(1, 2)
    assert not graph.has_edge(2, 1)


def test_keeps_nodes_that_do_not_appear_in_edges(synthetic_dataset: RawDataset) -> None:
    synthetic_dataset.nodes.loc[len(synthetic_dataset.nodes)] = [4, 3, False]

    graph = build_graph(synthetic_dataset)

    assert 4 in graph
    assert graph.degree(4) == 0


def test_preserves_self_loops(synthetic_dataset: RawDataset) -> None:
    synthetic_dataset.edges.loc[len(synthetic_dataset.edges)] = [3, 3, 5.0, 1, 3]

    graph = build_graph(synthetic_dataset)

    assert graph.has_edge(3, 3)
    assert graph[3][3]["sum_kzt"] == 5.0


@pytest.mark.parametrize(
    ("table", "column"),
    [("nodes", "is_seed"), ("edges", "sum_kzt")],
)
def test_rejects_missing_required_columns(
    synthetic_dataset: RawDataset, table: str, column: str
) -> None:
    setattr(
        synthetic_dataset,
        table,
        getattr(synthetic_dataset, table).drop(columns=column),
    )

    with pytest.raises(GraphConstructionError, match=f"{table} is missing"):
        build_graph(synthetic_dataset)


def test_rejects_duplicate_gids(synthetic_dataset: RawDataset) -> None:
    synthetic_dataset.nodes.at[1, "gid"] = 1

    with pytest.raises(GraphConstructionError, match="duplicate values"):
        build_graph(synthetic_dataset)


def test_rejects_duplicate_edge_pairs(synthetic_dataset: RawDataset) -> None:
    duplicate = synthetic_dataset.edges.iloc[[0]].copy()
    synthetic_dataset.edges = pd.concat(
        [synthetic_dataset.edges, duplicate], ignore_index=True
    )

    with pytest.raises(GraphConstructionError, match="duplicate \\(src, dst\\) pairs"):
        build_graph(synthetic_dataset)


@pytest.mark.parametrize("column", ["src", "dst"])
def test_rejects_unknown_edge_nodes(
    synthetic_dataset: RawDataset, column: str
) -> None:
    synthetic_dataset.edges.at[0, column] = 99

    with pytest.raises(GraphConstructionError, match=f"edges.{column} contains 1 unknown"):
        build_graph(synthetic_dataset)


def test_is_deterministic_and_does_not_mutate_frames(
    synthetic_dataset: RawDataset,
) -> None:
    nodes_before = synthetic_dataset.nodes.copy(deep=True)
    edges_before = synthetic_dataset.edges.copy(deep=True)
    transactions_before = synthetic_dataset.transactions.copy(deep=True)

    first = build_graph(synthetic_dataset)
    second = build_graph(synthetic_dataset)

    assert list(first.nodes(data=True)) == list(second.nodes(data=True))
    assert list(first.edges(data=True)) == list(second.edges(data=True))
    pd.testing.assert_frame_equal(synthetic_dataset.nodes, nodes_before)
    pd.testing.assert_frame_equal(synthetic_dataset.edges, edges_before)
    pd.testing.assert_frame_equal(synthetic_dataset.transactions, transactions_before)
