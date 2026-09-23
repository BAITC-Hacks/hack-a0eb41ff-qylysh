import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path

import pandas as pd

from app.analytics.pipeline import AnalysisSnapshot


NODE_EXPORT_COLUMNS = ["gid", "role", "role_score", "cluster_id", "priority_score", "evidence"]
TOP_EXPORT_COLUMNS = ["rank", "gid", "role", "priority_score", "why"]


def _sqlite_frames(snapshot: AnalysisSnapshot) -> dict[str, pd.DataFrame]:
    transactions = snapshot.dataset.transactions.copy(deep=True)
    transactions["date"] = transactions["date"].map(lambda value: value.isoformat())
    clusters = snapshot.clusters.copy(deep=True)
    clusters["top_gids"] = clusters["top_gids"].map(json.dumps)
    return {
        "nodes": snapshot.nodes.copy(deep=True),
        "edges": snapshot.dataset.edges.copy(deep=True),
        "transactions": transactions,
        "clusters": clusters,
    }


def write_snapshot(snapshot: AnalysisSnapshot, database_path: Path | str, output_dir: Path | str) -> None:
    database = Path(database_path)
    outputs = Path(output_dir)
    database.parent.mkdir(parents=True, exist_ok=True)
    outputs.mkdir(parents=True, exist_ok=True)
    temporary_database = database.with_name(f".{database.name}.tmp")
    if temporary_database.exists():
        temporary_database.unlink()
    try:
        with closing(sqlite3.connect(temporary_database)) as connection:
            with connection:
                for table, frame in _sqlite_frames(snapshot).items():
                    frame.to_sql(table, connection, if_exists="replace", index=False)
                connection.executescript("""
                    CREATE UNIQUE INDEX idx_nodes_gid ON nodes(gid);
                    CREATE INDEX idx_nodes_role ON nodes(role);
                    CREATE INDEX idx_nodes_cluster_id ON nodes(cluster_id);
                    CREATE INDEX idx_nodes_priority_score ON nodes(priority_score DESC);
                    CREATE INDEX idx_edges_src ON edges(src);
                    CREATE INDEX idx_edges_dst ON edges(dst);
                """)
        os.replace(temporary_database, database)
    except Exception:
        if temporary_database.exists():
            temporary_database.unlink()
        raise

    exports = {
        "nodes_roles.csv": snapshot.nodes[NODE_EXPORT_COLUMNS],
        "clusters.csv": _sqlite_frames(snapshot)["clusters"],
        "top_nodes.csv": snapshot.ranking[TOP_EXPORT_COLUMNS],
    }
    for filename, frame in exports.items():
        target = outputs / filename
        temporary = outputs / f".{filename}.tmp"
        frame.to_csv(temporary, index=False)
        os.replace(temporary, target)
