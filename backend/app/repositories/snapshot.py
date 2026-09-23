import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from app.core.config import settings


@contextmanager
def connect() -> Iterator[sqlite3.Connection]:
    path = Path(settings.DATABASE_PATH)
    if not path.is_file():
        raise FileNotFoundError(f"Analytical snapshot not found: {path}")
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()


def node_to_api(row: sqlite3.Row, *, details: bool = False) -> dict:
    source = dict(row)
    keys = {
        "gid", "role", "role_score", "priority_score", "cluster_id", "is_seed",
        "depth", "evidence", "in_degree", "out_degree", "in_kzt", "out_kzt",
    }
    if details:
        keys |= {"pagerank", "pass_through", "seed_reach_count", "truncated_by_depth"}
    item = {key: source[key] for key in keys}
    item["gid"] = str(item["gid"])
    item["is_seed"] = bool(item["is_seed"])
    if details:
        item["truncated_by_depth"] = bool(item["truncated_by_depth"])
    item["transaction_count"] = source["in_tx"] + source["out_tx"]
    return item


def cluster_to_api(row: sqlite3.Row, *, details: bool = False) -> dict:
    item = dict(row)
    top_gids = json.loads(item["top_gids"])
    result = {
        "cluster_id": item["cluster_id"], "node_count": item["n_nodes"],
        "seed_count": item["n_seed"], "internal_volume_kzt": item["sum_kzt_internal"],
        "top_gid": str(top_gids[0]) if top_gids else None,
        "hypothesis": item["hypothesis"], "description": item["hypothesis"],
    }
    if details:
        result["top_gids"] = [str(gid) for gid in top_gids]
    return result
