import pandas as pd
import pytest

from app.analytics.exceptions import RoleAssignmentError
from app.analytics.roles import assign_roles
from app.schemas.node import NodeRole


def feature_row(**overrides) -> dict:
    row = {
        "gid": 1,
        "depth": 2,
        "is_seed": False,
        "in_degree": 1,
        "out_degree": 1,
        "pass_through": 0.5,
        "truncated_by_depth": False,
        "in_degree_percentile": 0.5,
        "out_degree_percentile": 0.5,
        "volume_percentile": 0.5,
        "pagerank_percentile": 0.5,
        "seed_reach_percentile": 0.5,
    }
    row.update(overrides)
    return row


@pytest.mark.parametrize(
    ("overrides", "expected"),
    [
        ({"seed_reach_percentile": 0.95, "pagerank_percentile": 0.85}, NodeRole.COORDINATOR),
        ({"in_degree": 4, "out_degree": 1, "in_degree_percentile": 0.9, "volume_percentile": 0.75}, NodeRole.CONSOLIDATOR),
        ({"in_degree": 1, "out_degree": 4, "out_degree_percentile": 0.9, "volume_percentile": 0.65}, NodeRole.DISTRIBUTOR),
        ({"pass_through": 1.0}, NodeRole.TRANSIT),
        ({"depth": 3, "in_degree": 1, "out_degree": 0, "pass_through": 0.0}, NodeRole.TERMINAL),
        ({"in_degree": 0, "out_degree": 0, "pass_through": None}, NodeRole.PERIPHERAL),
    ],
)
def test_each_role_rule(overrides: dict, expected: NodeRole) -> None:
    result = assign_roles(pd.DataFrame([feature_row(**overrides)]))
    assert result.loc[0, "role"] == expected


def test_precedence_prefers_coordinator_over_other_matching_rules() -> None:
    row = feature_row(
        in_degree=5,
        out_degree=3,
        seed_reach_percentile=1.0,
        pagerank_percentile=1.0,
        in_degree_percentile=1.0,
        volume_percentile=1.0,
        pass_through=1.0,
    )
    assert assign_roles(pd.DataFrame([row])).loc[0, "role"] == NodeRole.COORDINATOR


def test_truncated_depth_four_node_is_not_terminal() -> None:
    row = feature_row(depth=4, in_degree=1, out_degree=0, pass_through=0.0, truncated_by_depth=True)
    assert assign_roles(pd.DataFrame([row])).loc[0, "role"] == NodeRole.PERIPHERAL


def test_seed_is_not_transit_from_pass_through_alone() -> None:
    row = feature_row(is_seed=True, pass_through=1.0)
    assert assign_roles(pd.DataFrame([row])).loc[0, "role"] == NodeRole.PERIPHERAL


def test_assigns_every_gid_deterministically_without_mutation() -> None:
    features = pd.DataFrame([feature_row(gid=1), feature_row(gid=2, pass_through=1.0)])
    before = features.copy(deep=True)
    first = assign_roles(features)
    second = assign_roles(features)

    pd.testing.assert_frame_equal(first, second)
    pd.testing.assert_frame_equal(features, before)
    assert first["gid"].is_unique
    assert first["role"].notna().all()


def test_rejects_missing_columns_duplicate_gid_and_bad_percentiles() -> None:
    with pytest.raises(RoleAssignmentError, match="missing required"):
        assign_roles(pd.DataFrame({"gid": [1]}))

    duplicate = pd.DataFrame([feature_row(gid=1), feature_row(gid=1)])
    with pytest.raises(RoleAssignmentError, match="unique non-null"):
        assign_roles(duplicate)

    invalid = pd.DataFrame([feature_row(pagerank_percentile=1.1)])
    with pytest.raises(RoleAssignmentError, match="0..1"):
        assign_roles(invalid)
