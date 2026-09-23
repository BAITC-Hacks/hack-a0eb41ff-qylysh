from dataclasses import dataclass

import pandas as pd

from app.analytics.exceptions import RoleAssignmentError
from app.schemas.node import NodeRole


ROLE_FEATURE_COLUMNS = frozenset({
    "gid",
    "depth",
    "is_seed",
    "in_degree",
    "out_degree",
    "pass_through",
    "truncated_by_depth",
    "in_degree_percentile",
    "out_degree_percentile",
    "volume_percentile",
    "pagerank_percentile",
    "seed_reach_percentile",
})


@dataclass(frozen=True)
class RoleThresholds:
    coordinator_seed_reach_percentile: float = 0.95
    coordinator_pagerank_percentile: float = 0.85
    consolidator_in_degree_percentile: float = 0.90
    consolidator_volume_percentile: float = 0.75
    distributor_out_degree_percentile: float = 0.90
    distributor_volume_percentile: float = 0.65
    transit_pass_through_min: float = 0.80
    transit_pass_through_max: float = 1.20


DEFAULT_ROLE_THRESHOLDS = RoleThresholds()


def _validate_features(features: pd.DataFrame) -> None:
    missing = sorted(ROLE_FEATURE_COLUMNS - set(features.columns))
    if missing:
        raise RoleAssignmentError(
            f"Role assignment is missing required feature columns: {missing}"
        )
    if features["gid"].isna().any() or features["gid"].duplicated().any():
        raise RoleAssignmentError("Role assignment requires unique non-null gid values")
    percentile_columns = [
        "in_degree_percentile",
        "out_degree_percentile",
        "volume_percentile",
        "pagerank_percentile",
        "seed_reach_percentile",
    ]
    for column in percentile_columns:
        if features[column].isna().any() or not features[column].between(0, 1).all():
            raise RoleAssignmentError(f"{column} must contain values in the 0..1 range")


def _assign_row(row: pd.Series, thresholds: RoleThresholds) -> NodeRole:
    # Precedence is part of the public analytical methodology.
    if (
        row["seed_reach_percentile"] >= thresholds.coordinator_seed_reach_percentile
        and row["pagerank_percentile"] >= thresholds.coordinator_pagerank_percentile
        and row["in_degree"] > 0
        and row["out_degree"] > 0
    ):
        return NodeRole.COORDINATOR
    if (
        row["in_degree_percentile"] >= thresholds.consolidator_in_degree_percentile
        and row["volume_percentile"] >= thresholds.consolidator_volume_percentile
        and row["in_degree"] > row["out_degree"]
    ):
        return NodeRole.CONSOLIDATOR
    if (
        row["out_degree_percentile"] >= thresholds.distributor_out_degree_percentile
        and row["volume_percentile"] >= thresholds.distributor_volume_percentile
        and row["out_degree"] > row["in_degree"]
    ):
        return NodeRole.DISTRIBUTOR
    if (
        not bool(row["is_seed"])
        and not bool(row["truncated_by_depth"])
        and row["in_degree"] > 0
        and row["out_degree"] > 0
        and pd.notna(row["pass_through"])
        and thresholds.transit_pass_through_min
        <= row["pass_through"]
        <= thresholds.transit_pass_through_max
    ):
        return NodeRole.TRANSIT
    if (
        row["depth"] < 4
        and row["in_degree"] > 0
        and row["out_degree"] == 0
    ):
        return NodeRole.TERMINAL
    return NodeRole.PERIPHERAL


def assign_roles(
    features: pd.DataFrame,
    thresholds: RoleThresholds = DEFAULT_ROLE_THRESHOLDS,
) -> pd.DataFrame:
    """Assign one structural role to every gid without mutating features."""
    _validate_features(features)
    roles = features.apply(lambda row: _assign_row(row, thresholds), axis=1)
    return pd.DataFrame({"gid": features["gid"].copy(), "role": roles})
