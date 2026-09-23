from dataclasses import dataclass
from pathlib import Path

import networkx as nx
import pandas as pd

from app.analytics.clustering import cluster_graph
from app.analytics.features import calculate_features
from app.analytics.graph_builder import build_graph
from app.analytics.loader import load_dataset
from app.analytics.models import DatasetExpectations, HACKATHON_EXPECTATIONS, RawDataset
from app.analytics.ranking import rank_nodes
from app.analytics.roles import assign_roles
from app.analytics.scoring import score_roles
from app.analytics.validator import validate_dataset


@dataclass
class AnalysisSnapshot:
    dataset: RawDataset
    graph: nx.DiGraph
    nodes: pd.DataFrame
    clusters: pd.DataFrame
    ranking: pd.DataFrame


def run_analysis(
    data_dir: Path | str,
    expectations: DatasetExpectations | None = HACKATHON_EXPECTATIONS,
) -> AnalysisSnapshot:
    dataset = load_dataset(data_dir)
    validate_dataset(dataset, expectations)
    graph = build_graph(dataset)
    features = calculate_features(graph)
    scored = score_roles(features, assign_roles(features))
    node_clusters, clusters = cluster_graph(graph, features)
    ranking = rank_nodes(features, scored)
    nodes = (
        features.merge(scored, on="gid", validate="one_to_one")
        .merge(node_clusters, on="gid", validate="one_to_one")
        .merge(ranking[["gid", "priority_score"]], on="gid", validate="one_to_one")
    )
    return AnalysisSnapshot(dataset, graph, nodes, clusters, ranking)
