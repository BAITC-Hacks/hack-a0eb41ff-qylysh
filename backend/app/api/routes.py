import sqlite3

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.repositories.snapshot import cluster_to_api, connect, node_to_api
from app.schemas.api import ApiGraphResponse, ClusterListResponse, ClusterResponse, NodeDetailsResponse, PaginatedNodesResponse, SummaryResponse
from app.schemas.node import NodeRole


router = APIRouter()


def _error(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"code": code, "message": message})


@router.get("/summary", response_model=SummaryResponse)
def summary():
    try:
        with connect() as db:
            counts = {name: db.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0] for name in ("nodes", "edges", "transactions", "clusters")}
            seeds = db.execute("SELECT COUNT(*) FROM nodes WHERE is_seed = 1").fetchone()[0]
            roles = {role.value: 0 for role in NodeRole}
            roles.update(dict(db.execute("SELECT role, COUNT(*) FROM nodes GROUP BY role").fetchall()))
            top = db.execute("SELECT * FROM nodes ORDER BY priority_score DESC, gid LIMIT 10").fetchall()
            clusters = db.execute("SELECT * FROM clusters ORDER BY n_nodes DESC, cluster_id LIMIT 10").fetchall()
    except FileNotFoundError as exc:
        return _error(503, "SNAPSHOT_NOT_FOUND", str(exc))
    top_clusters = []
    for row in clusters:
        item = cluster_to_api(row)
        top_clusters.append(item)
    return {"total_nodes": counts["nodes"], "total_edges": counts["edges"], "total_transactions": counts["transactions"], "total_seeds": seeds, "total_clusters": counts["clusters"], "roles": roles, "top_nodes": [{"rank": index + 1, "gid": row["gid"], "role": row["role"], "priority_score": row["priority_score"], "cluster_id": row["cluster_id"], "evidence": row["evidence"]} for index, row in enumerate(top)], "top_clusters": top_clusters}


@router.get("/nodes", response_model=PaginatedNodesResponse)
def nodes(role: NodeRole | None = None, cluster: int | None = Query(None, ge=0), min_priority: float | None = Query(None, alias="minPriority", ge=0, le=1), is_seed: bool | None = Query(None, alias="isSeed"), search: str | None = Query(None, max_length=30), page: int = Query(1, ge=1), page_size: int | None = Query(None, alias="pageSize", ge=1, le=100), limit: int | None = Query(None, ge=1, le=100)):
    effective_limit = page_size or limit or 20
    clauses, values = [], []
    for condition, value in (("role = ?", role.value if role else None), ("cluster_id = ?", cluster), ("priority_score >= ?", min_priority), ("is_seed = ?", int(is_seed) if is_seed is not None else None), ("CAST(gid AS TEXT) LIKE ?", f"%{search}%" if search else None)):
        if value is not None: clauses.append(condition); values.append(value)
    where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
    try:
        with connect() as db:
            total = db.execute("SELECT COUNT(*) FROM nodes" + where, values).fetchone()[0]
            rows = db.execute("SELECT * FROM nodes" + where + " ORDER BY priority_score DESC, gid LIMIT ? OFFSET ?", [*values, effective_limit, (page - 1) * effective_limit]).fetchall()
    except FileNotFoundError as exc: return _error(503, "SNAPSHOT_NOT_FOUND", str(exc))
    return {"items": [node_to_api(row) for row in rows], "page": page, "page_size": effective_limit, "total": total}


@router.get("/nodes/{gid}", response_model=NodeDetailsResponse)
def node_details(gid: int):
    try:
        with connect() as db: row = db.execute("SELECT * FROM nodes WHERE gid = ?", (gid,)).fetchone()
    except FileNotFoundError as exc: return _error(503, "SNAPSHOT_NOT_FOUND", str(exc))
    return node_to_api(row, details=True) if row else _error(404, "NODE_NOT_FOUND", f"Node with gid={gid} was not found")


def _graph_payload(db: sqlite3.Connection, gids: set[int], focus_type: str, focus_id: int) -> dict:
    ordered = sorted(gids)
    placeholders = ",".join("?" for _ in ordered)
    node_rows = db.execute(f"SELECT * FROM nodes WHERE gid IN ({placeholders})", ordered).fetchall()
    edge_rows = db.execute(f"SELECT * FROM edges WHERE src IN ({placeholders}) AND dst IN ({placeholders})", [*ordered, *ordered]).fetchall()
    nodes_payload = [{"gid": r["gid"], "role": r["role"], "role_score": r["role_score"], "priority_score": r["priority_score"], "cluster_id": r["cluster_id"], "is_seed": bool(r["is_seed"]), "depth": r["depth"]} for r in node_rows]
    edges_payload = [{"source": r["src"], "target": r["dst"], "sum_kzt": r["sum_kzt"], "transaction_count": r["n_tx"]} for r in edge_rows]
    truncated = 4 if any(n["depth"] == 4 for n in nodes_payload) else None
    return {"focus": {"type": focus_type, "id": focus_id}, "nodes": nodes_payload, "edges": edges_payload, "truncated_at_depth": truncated}


@router.get("/nodes/{gid}/graph", response_model=ApiGraphResponse)
def node_graph(gid: int):
    try:
        with connect() as db:
            if not db.execute("SELECT 1 FROM nodes WHERE gid = ?", (gid,)).fetchone(): return _error(404, "NODE_NOT_FOUND", f"Node with gid={gid} was not found")
            rows = db.execute("SELECT src, dst FROM edges WHERE src = ? OR dst = ?", (gid, gid)).fetchall()
            gids = {gid} | {r["src"] for r in rows} | {r["dst"] for r in rows}
            return _graph_payload(db, gids, "gid", gid)
    except FileNotFoundError as exc: return _error(503, "SNAPSHOT_NOT_FOUND", str(exc))


@router.get("/top-nodes", response_model=PaginatedNodesResponse)
def top_nodes(limit: int = Query(20, ge=20, le=100)):
    try:
        with connect() as db:
            total = db.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
            rows = db.execute(
                "SELECT * FROM nodes ORDER BY priority_score DESC, gid LIMIT ?", (limit,)
            ).fetchall()
    except FileNotFoundError as exc:
        return _error(503, "SNAPSHOT_NOT_FOUND", str(exc))
    return {"items": [node_to_api(row) for row in rows], "page": 1, "page_size": limit, "total": total}


@router.get("/clusters", response_model=ClusterListResponse)
def clusters():
    try:
        with connect() as db: rows = db.execute("SELECT * FROM clusters ORDER BY n_nodes DESC, cluster_id").fetchall()
    except FileNotFoundError as exc: return _error(503, "SNAPSHOT_NOT_FOUND", str(exc))
    return {"items": [cluster_to_api(row) for row in rows], "total": len(rows)}


@router.get("/clusters/{cluster_id}", response_model=ClusterResponse)
def cluster_details(cluster_id: int):
    try:
        with connect() as db: row = db.execute("SELECT * FROM clusters WHERE cluster_id = ?", (cluster_id,)).fetchone()
    except FileNotFoundError as exc: return _error(503, "SNAPSHOT_NOT_FOUND", str(exc))
    return cluster_to_api(row, details=True) if row else _error(404, "CLUSTER_NOT_FOUND", f"Cluster {cluster_id} was not found")


@router.get("/clusters/{cluster_id}/graph", response_model=ApiGraphResponse)
def cluster_graph(cluster_id: int):
    try:
        with connect() as db:
            rows = db.execute("SELECT gid FROM nodes WHERE cluster_id = ? ORDER BY priority_score DESC, gid LIMIT 1000", (cluster_id,)).fetchall()
            if not rows: return _error(404, "CLUSTER_NOT_FOUND", f"Cluster {cluster_id} was not found")
            return _graph_payload(db, {row["gid"] for row in rows}, "cluster", cluster_id)
    except FileNotFoundError as exc: return _error(503, "SNAPSHOT_NOT_FOUND", str(exc))
