import networkx as nx
import pandas as pd

from app.analytics.exceptions import AnalyticsError


def _undirected_projection(graph: nx.DiGraph) -> nx.Graph:
    projection = nx.Graph()
    projection.add_nodes_from(graph.nodes)
    for source, target, data in graph.edges(data=True):
        weight = float(data["sum_kzt"])
        if projection.has_edge(source, target):
            projection[source][target]["sum_kzt"] += weight
        else:
            projection.add_edge(source, target, sum_kzt=weight)
    return projection


def cluster_graph(graph: nx.DiGraph, features: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if set(graph.nodes) != set(features["gid"]):
        raise AnalyticsError("Clustering requires one feature row for every graph node")
    projection = _undirected_projection(graph)
    communities = nx.community.louvain_communities(projection, weight="sum_kzt", seed=42)
    ordered = sorted((set(c) for c in communities), key=lambda c: min(c))
    assignment = {gid: cluster_id for cluster_id, community in enumerate(ordered) for gid in community}
    node_clusters = pd.DataFrame({"gid": features["gid"].copy(), "cluster_id": features["gid"].map(assignment).astype(int)})
    feature_index = features.set_index("gid")
    summaries = []
    for cluster_id, members in enumerate(ordered):
        internal = sum(float(data["sum_kzt"]) for u, v, data in graph.edges(data=True) if u in members and v in members)
        ranked = sorted(members, key=lambda gid: (-float(feature_index.loc[gid, "pagerank"]), int(gid)))[:5]
        n_seed = sum(bool(graph.nodes[gid]["is_seed"]) for gid in members)
        if len(members) == 1:
            hypothesis = "Isolated or single-node fragment for analyst review."
        elif n_seed > 1:
            hypothesis = "Multi-seed connected community; review shared flow structure."
        elif n_seed == 1:
            hypothesis = "Community connected to one known seed; review downstream flow."
        else:
            hypothesis = "Connected non-seed community; review its links to the wider network."
        summaries.append({"cluster_id": cluster_id, "n_nodes": len(members), "n_seed": n_seed, "sum_kzt_internal": internal, "top_gids": ranked, "hypothesis": hypothesis})
    return node_clusters, pd.DataFrame(summaries)
