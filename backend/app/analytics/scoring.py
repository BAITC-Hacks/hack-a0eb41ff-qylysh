import pandas as pd

from app.analytics.exceptions import AnalyticsError
from app.schemas.node import NodeRole


def _money(value: float) -> str:
    if value >= 1_000_000:
        return f"KZT {value / 1_000_000:.1f}m"
    if value >= 1_000:
        return f"KZT {value / 1_000:.1f}k"
    return f"KZT {value:.0f}"


def score_roles(features: pd.DataFrame, roles: pd.DataFrame) -> pd.DataFrame:
    if roles["gid"].duplicated().any() or set(features["gid"]) != set(roles["gid"]):
        raise AnalyticsError("Role scoring requires exactly one role for every feature gid")
    data = features.merge(roles, on="gid", validate="one_to_one")
    rows = []
    for row in data.itertuples(index=False):
        role = NodeRole(row.role)
        if role == NodeRole.COORDINATOR:
            score = (row.seed_reach_percentile + row.pagerank_percentile + row.in_degree_percentile + row.out_degree_percentile) / 4
            evidence = f"Links {row.in_degree} in/{row.out_degree} out; reached by {row.seed_reach_count} seeds; PageRank p{row.pagerank_percentile:.2f}."
        elif role == NodeRole.CONSOLIDATOR:
            score = (row.in_degree_percentile + row.volume_percentile + row.pagerank_percentile) / 3
            evidence = f"Receives from {row.in_degree} nodes ({_money(row.in_kzt)}); sends to {row.out_degree}; incoming p{row.in_degree_percentile:.2f}."
        elif role == NodeRole.DISTRIBUTOR:
            score = (row.out_degree_percentile + row.volume_percentile + row.pagerank_percentile) / 3
            evidence = f"Sends to {row.out_degree} nodes ({_money(row.out_kzt)}); receives from {row.in_degree}; outgoing p{row.out_degree_percentile:.2f}."
        elif role == NodeRole.TRANSIT:
            closeness = max(0.0, 1.0 - abs(float(row.pass_through) - 1.0) / 0.2)
            score = (closeness + row.in_degree_percentile + row.out_degree_percentile) / 3
            evidence = f"Pass-through {float(row.pass_through):.2f}; {row.in_degree} incoming and {row.out_degree} outgoing links; depth {row.depth}."
        elif role == NodeRole.TERMINAL:
            score = (row.in_degree_percentile + row.volume_percentile + (1.0 - row.out_degree_percentile)) / 3
            evidence = f"Receives from {row.in_degree} nodes ({_money(row.in_kzt)}); no observed outgoing links; depth {row.depth}."
        else:
            prominence = max(row.in_degree_percentile, row.out_degree_percentile, row.volume_percentile, row.pagerank_percentile)
            score = 1.0 - prominence
            evidence = f"Limited observed structure: {row.in_degree} incoming, {row.out_degree} outgoing links; depth {row.depth}."
        rows.append({"gid": row.gid, "role": role.value, "role_score": min(1.0, max(0.0, float(score))), "evidence": evidence[:200]})
    return pd.DataFrame(rows, columns=["gid", "role", "role_score", "evidence"])
