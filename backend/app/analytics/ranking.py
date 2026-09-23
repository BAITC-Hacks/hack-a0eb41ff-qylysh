import pandas as pd

from app.analytics.exceptions import AnalyticsError


PRIORITY_WEIGHTS = {
    "pagerank_percentile": 0.25,
    "seed_reach_percentile": 0.20,
    "role_score": 0.25,
    "volume_percentile": 0.20,
    "degree_percentile": 0.10,
}


def rank_nodes(features: pd.DataFrame, scored_roles: pd.DataFrame) -> pd.DataFrame:
    if set(features["gid"]) != set(scored_roles["gid"]):
        raise AnalyticsError("Ranking requires scored roles for every feature gid")
    data = features.merge(scored_roles, on="gid", validate="one_to_one")
    degree = (data["in_degree_percentile"] + data["out_degree_percentile"]) / 2
    data["priority_score"] = (
        PRIORITY_WEIGHTS["pagerank_percentile"] * data["pagerank_percentile"]
        + PRIORITY_WEIGHTS["seed_reach_percentile"] * data["seed_reach_percentile"]
        + PRIORITY_WEIGHTS["role_score"] * data["role_score"]
        + PRIORITY_WEIGHTS["volume_percentile"] * data["volume_percentile"]
        + PRIORITY_WEIGHTS["degree_percentile"] * degree
    ).clip(0, 1)
    data = data.sort_values(["priority_score", "gid"], ascending=[False, True], kind="stable").reset_index(drop=True)
    data.insert(0, "rank", data.index + 1)
    data["why"] = data["evidence"]
    return data[["rank", "gid", "role", "role_score", "priority_score", "why"]]
