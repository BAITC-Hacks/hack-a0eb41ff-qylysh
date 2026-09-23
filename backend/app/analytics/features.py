import networkx as nx
import pandas as pd

from app.analytics.exceptions import FeatureEngineeringError


FEATURE_COLUMNS = (
    "gid",
    "depth",
    "is_seed",
    "in_degree",
    "out_degree",
    "total_degree",
    "in_kzt",
    "out_kzt",
    "total_volume",
    "in_tx",
    "out_tx",
    "pagerank",
    "pass_through",
    "seed_reach_count",
    "truncated_by_depth",
    "in_degree_percentile",
    "out_degree_percentile",
    "volume_percentile",
    "pagerank_percentile",
    "seed_reach_percentile",
)


def _validate_graph_attributes(graph: nx.DiGraph) -> None:
    if not graph.is_directed():
        raise FeatureEngineeringError("Feature engineering requires a directed graph")
    for gid, attributes in graph.nodes(data=True):
        missing = {"depth", "is_seed"} - set(attributes)
        if missing:
            raise FeatureEngineeringError(
                f"Node {gid} is missing required attributes: {sorted(missing)}"
            )
    for source, target, attributes in graph.edges(data=True):
        missing = {"sum_kzt", "n_tx", "depth"} - set(attributes)
        if missing:
            raise FeatureEngineeringError(
                f"Edge ({source}, {target}) is missing required attributes: {sorted(missing)}"
            )


def _seed_reach_counts(graph: nx.DiGraph) -> dict[int, int]:
    counts = dict.fromkeys(graph.nodes, 0)
    seeds = [gid for gid, data in graph.nodes(data=True) if bool(data["is_seed"])]
    for seed in seeds:
        # A seed reaches itself through the zero-length path.
        for gid in nx.descendants(graph, seed) | {seed}:
            counts[gid] += 1
    return counts


def _percentile(series: pd.Series) -> pd.Series:
    # Average rank gives equal values the same deterministic percentile.
    return series.rank(method="average", pct=True).astype(float)


def calculate_features(graph: nx.DiGraph) -> pd.DataFrame:
    """Return one deterministic feature row per node without changing the graph."""
    _validate_graph_attributes(graph)
    gids = list(graph.nodes)
    in_degree = dict(graph.in_degree())
    out_degree = dict(graph.out_degree())
    in_kzt = dict(graph.in_degree(weight="sum_kzt"))
    out_kzt = dict(graph.out_degree(weight="sum_kzt"))
    in_tx = dict(graph.in_degree(weight="n_tx"))
    out_tx = dict(graph.out_degree(weight="n_tx"))
    pagerank = nx.pagerank(graph, weight="sum_kzt") if gids else {}
    seed_reach = _seed_reach_counts(graph)

    rows: list[dict[str, object]] = []
    for gid in gids:
        incoming = float(in_kzt[gid])
        outgoing = float(out_kzt[gid])
        depth = int(graph.nodes[gid]["depth"])
        row = {
            "gid": gid,
            "depth": depth,
            "is_seed": bool(graph.nodes[gid]["is_seed"]),
            "in_degree": int(in_degree[gid]),
            "out_degree": int(out_degree[gid]),
            "total_degree": int(in_degree[gid] + out_degree[gid]),
            "in_kzt": incoming,
            "out_kzt": outgoing,
            "total_volume": incoming + outgoing,
            "in_tx": int(in_tx[gid]),
            "out_tx": int(out_tx[gid]),
            "pagerank": float(pagerank[gid]),
            "pass_through": None if incoming == 0 else outgoing / incoming,
            "seed_reach_count": int(seed_reach[gid]),
            "truncated_by_depth": depth == 4 and out_degree[gid] == 0,
        }
        rows.append(row)

    features = pd.DataFrame(rows)
    if features.empty:
        return pd.DataFrame(columns=FEATURE_COLUMNS)
    features["pass_through"] = pd.Series(
        [row["pass_through"] for row in rows], dtype=object
    )
    features["in_degree_percentile"] = _percentile(features["in_degree"])
    features["out_degree_percentile"] = _percentile(features["out_degree"])
    features["volume_percentile"] = _percentile(features["total_volume"])
    features["pagerank_percentile"] = _percentile(features["pagerank"])
    features["seed_reach_percentile"] = _percentile(features["seed_reach_count"])
    return features.loc[:, FEATURE_COLUMNS]
