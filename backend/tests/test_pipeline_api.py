import json
import sqlite3

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from app.analytics.clustering import cluster_graph
from app.analytics.features import calculate_features
from app.analytics.graph_builder import build_graph
from app.analytics.models import DatasetExpectations, RawDataset
from app.analytics.pipeline import run_analysis
from app.analytics.ranking import PRIORITY_WEIGHTS, rank_nodes
from app.analytics.roles import assign_roles
from app.analytics.scoring import score_roles
from app.core.config import settings
from app.db.snapshot import write_snapshot
from app.main import app


def _write_dataset(path, dataset: RawDataset) -> None:
    path.mkdir()
    dataset.nodes.to_parquet(path / "nodes.parquet")
    dataset.edges.to_parquet(path / "edges.parquet")
    dataset.transactions.to_parquet(path / "transactions.parquet")


def test_scores_clusters_and_ranking_are_complete_and_deterministic(synthetic_dataset: RawDataset) -> None:
    graph = build_graph(synthetic_dataset)
    features = calculate_features(graph)
    scored = score_roles(features, assign_roles(features))
    assignments, clusters = cluster_graph(graph, features)
    ranking = rank_nodes(features, scored)

    assert scored["role_score"].between(0, 1).all()
    assert scored["evidence"].str.len().between(1, 200).all()
    assert len(assignments) == len(features)
    assert assignments["cluster_id"].notna().all()
    assert clusters["n_nodes"].sum() == len(features)
    assert ranking["priority_score"].between(0, 1).all()
    assert ranking["priority_score"].is_monotonic_decreasing
    assert ranking["rank"].tolist() == list(range(1, len(ranking) + 1))
    assert sum(PRIORITY_WEIGHTS.values()) == pytest.approx(1.0)
    pd.testing.assert_frame_equal(scored, score_roles(features, assign_roles(features)))


def test_pipeline_persistence_and_api(tmp_path, synthetic_dataset: RawDataset, monkeypatch) -> None:
    data_dir = tmp_path / "data"
    database = tmp_path / "analysis.db"
    output = tmp_path / "out"
    _write_dataset(data_dir, synthetic_dataset)
    expectations = DatasetExpectations(3, 2, 3, 1)
    snapshot = run_analysis(data_dir, expectations)
    write_snapshot(snapshot, database, output)
    write_snapshot(snapshot, database, output)

    with sqlite3.connect(database) as db:
        assert db.execute("SELECT COUNT(*) FROM nodes").fetchone()[0] == 3
        assert db.execute("SELECT COUNT(*) FROM edges").fetchone()[0] == 2
        indexes = {row[1] for row in db.execute("PRAGMA index_list(nodes)")}
        assert "idx_nodes_gid" in indexes
    assert len(pd.read_csv(output / "nodes_roles.csv")) == 3
    assert len(pd.read_csv(output / "top_nodes.csv")) == 3
    assert json.loads(pd.read_csv(output / "clusters.csv").iloc[0]["top_gids"])

    monkeypatch.setattr(settings, "DATABASE_PATH", str(database))
    client = TestClient(app)
    summary = client.get("/api/v1/summary")
    assert summary.status_code == 200
    assert isinstance(summary.json()["topNodes"][0]["gid"], str)
    listing = client.get("/api/v1/nodes", params={"page": 1, "pageSize": 2})
    assert listing.status_code == 200
    assert listing.json()["pageSize"] == 2
    assert isinstance(listing.json()["items"][0]["gid"], str)
    details = client.get("/api/v1/nodes/1")
    assert details.status_code == 200
    assert details.json()["gid"] == "1"
    assert client.get("/api/v1/nodes/999").status_code == 404
    graph = client.get("/api/v1/nodes/1/graph")
    assert graph.status_code == 200
    assert set(graph.json()) == {"focus", "nodes", "edges", "truncatedAtDepth"}
    assert graph.json()["focus"] == {"type": "gid", "id": "1"}
    assert all(isinstance(node["gid"], str) for node in graph.json()["nodes"])
    assert all(isinstance(edge["source"], str) and isinstance(edge["target"], str) for edge in graph.json()["edges"])
    clusters = client.get("/api/v1/clusters")
    assert clusters.status_code == 200
    assert isinstance(clusters.json()["items"][0]["topGid"], str)
    cluster_id = clusters.json()["items"][0]["clusterId"]
    assert client.get(f"/api/v1/clusters/{cluster_id}").status_code == 200
    assert client.get(f"/api/v1/clusters/{cluster_id}/graph").json()["focus"]["id"] == cluster_id
    assert client.get("/api/v1/nodes", params={"minPriority": 2}).status_code == 422

    preflight = client.options(
        "/api/v1/summary",
        headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "GET"},
    )
    assert preflight.status_code == 200
    assert preflight.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_api_openapi_contains_frozen_domain_routes() -> None:
    paths = TestClient(app).get("/openapi.json").json()["paths"]
    for path in (
        "/api/v1/summary", "/api/v1/nodes", "/api/v1/nodes/{gid}",
        "/api/v1/nodes/{gid}/graph", "/api/v1/top-nodes", "/api/v1/clusters",
        "/api/v1/clusters/{cluster_id}", "/api/v1/clusters/{cluster_id}/graph",
    ):
        assert path in paths
