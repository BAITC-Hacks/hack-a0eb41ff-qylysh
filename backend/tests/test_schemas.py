import pytest
from pydantic import ValidationError

from app.schemas.cluster import ClusterRecord
from app.schemas.common import ApiError, HealthResponse
from app.schemas.edge import EdgeRecord
from app.schemas.graph import GraphEdge, GraphNode, GraphResponse
from app.schemas.node import NodeAnalytics, NodeBase, NodeMetrics, NodeRecord, NodeRole


def valid_node_data() -> dict:
    return {
        "gid": 123,
        "depth": 4,
        "is_seed": False,
        "in_degree": 1,
        "out_degree": 0,
        "in_kzt": 500.0,
        "out_kzt": 0.0,
        "in_tx": 2,
        "out_tx": 0,
        "pagerank": 0.1,
        "pass_through": None,
        "seed_reach_count": 1,
        "truncated_by_depth": True,
        "role": NodeRole.TERMINAL,
        "role_score": 1.0,
        "priority_score": 0.0,
        "cluster_id": 0,
        "evidence": "2 incoming transfers",
    }


def test_node_record_and_flat_snake_case_json() -> None:
    node = NodeRecord(**valid_node_data())

    assert node.pass_through is None
    assert node.model_dump()["gid"] == 123
    assert node.model_dump(mode="json")["role"] == "terminal"
    assert "priority_score" in node.model_dump_json()
    assert set(NodeRecord.model_fields) == (
        set(NodeBase.model_fields)
        | set(NodeMetrics.model_fields)
        | set(NodeAnalytics.model_fields)
    )


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("role_score", 1.01),
        ("priority_score", -0.01),
        ("depth", 5),
        ("role", "unknown"),
        ("evidence", "x" * 201),
        ("evidence", ""),
        ("in_kzt", -1),
        ("gid", -1),
    ],
)
def test_node_record_rejects_invalid_values(field: str, invalid_value: object) -> None:
    data = valid_node_data()
    data[field] = invalid_value

    with pytest.raises(ValidationError):
        NodeRecord(**data)


def test_role_enum_has_exactly_six_roles() -> None:
    assert {role.value for role in NodeRole} == {
        "coordinator",
        "consolidator",
        "distributor",
        "transit",
        "terminal",
        "peripheral",
    }


def test_graph_response_serializes() -> None:
    graph = GraphResponse(
        nodes=[GraphNode(
            gid=123,
            role=NodeRole.TERMINAL,
            role_score=0.8,
            priority_score=0.9,
            cluster_id=3,
            is_seed=False,
        )],
        edges=[GraphEdge(source=1, target=123, sum_kzt=500.0, n_tx=2)],
    )

    assert graph.model_dump(mode="json") == {
        "nodes": [{
            "gid": 123,
            "role": "terminal",
            "role_score": 0.8,
            "priority_score": 0.9,
            "cluster_id": 3,
            "is_seed": False,
        }],
        "edges": [{"source": 1, "target": 123, "sum_kzt": 500.0, "n_tx": 2}],
    }


def test_other_contracts_exist_and_validate() -> None:
    assert HealthResponse(status="ok", service="MoneyGraph API", version="0.1.0")
    assert ApiError(code="NODE_NOT_FOUND", message="Missing node")
    assert ClusterRecord(
        cluster_id=0,
        n_nodes=1,
        n_seed=0,
        sum_kzt_internal=0,
        top_gids=[123],
        hypothesis="Unknown",
    )
    with pytest.raises(ValidationError):
        EdgeRecord(source=1, target=2, sum_kzt=-1, n_tx=1, depth=0)
