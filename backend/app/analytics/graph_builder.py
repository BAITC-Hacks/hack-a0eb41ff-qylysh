import networkx as nx

from app.analytics.exceptions import GraphConstructionError
from app.analytics.models import RawDataset


NODE_GRAPH_COLUMNS = frozenset({"gid", "depth", "is_seed"})
EDGE_GRAPH_COLUMNS = frozenset({"src", "dst", "sum_kzt", "n_tx", "depth"})


def _require_columns(actual: set[str], required: frozenset[str], table: str) -> None:
    missing = sorted(required - actual)
    if missing:
        raise GraphConstructionError(
            f"Cannot build graph: {table} is missing required columns: {missing}"
        )


def build_graph(dataset: RawDataset) -> nx.DiGraph:
    """Build the canonical directed money-flow graph without changing source frames.

    The caller is expected to run ``validate_dataset`` first. These defensive
    checks prevent NetworkX from silently merging duplicate nodes or edge pairs.
    """
    nodes = dataset.nodes
    edges = dataset.edges
    _require_columns(set(nodes.columns), NODE_GRAPH_COLUMNS, "nodes")
    _require_columns(set(edges.columns), EDGE_GRAPH_COLUMNS, "edges")

    duplicate_gids = nodes.loc[
        nodes["gid"].duplicated(keep=False), "gid"
    ].drop_duplicates()
    if not duplicate_gids.empty:
        raise GraphConstructionError(
            "Cannot build graph: nodes.gid contains duplicate values: "
            f"{duplicate_gids.head(5).tolist()}"
        )

    duplicate_edges = edges.loc[
        edges.duplicated(subset=["src", "dst"], keep=False), ["src", "dst"]
    ].drop_duplicates()
    if not duplicate_edges.empty:
        raise GraphConstructionError(
            "Cannot build graph: edges contains duplicate (src, dst) pairs: "
            f"{duplicate_edges.head(5).values.tolist()}"
        )

    gids = set(nodes["gid"])
    for column in ("src", "dst"):
        unknown = set(edges[column]) - gids
        if unknown:
            raise GraphConstructionError(
                f"Cannot build graph: edges.{column} contains {len(unknown)} "
                f"unknown gids: {sorted(unknown)[:5]}"
            )

    graph = nx.DiGraph()
    graph.add_nodes_from(
        (row.gid, {"depth": row.depth, "is_seed": row.is_seed})
        for row in nodes[["gid", "depth", "is_seed"]].itertuples(index=False)
    )
    graph.add_edges_from(
        (
            row.src,
            row.dst,
            {"sum_kzt": row.sum_kzt, "n_tx": row.n_tx, "depth": row.depth},
        )
        for row in edges[["src", "dst", "sum_kzt", "n_tx", "depth"]].itertuples(
            index=False
        )
    )
    return graph
