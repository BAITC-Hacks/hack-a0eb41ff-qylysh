from enum import Enum

from pydantic import BaseModel, Field


class NodeRole(str, Enum):
    COORDINATOR = "coordinator"
    CONSOLIDATOR = "consolidator"
    DISTRIBUTOR = "distributor"
    TRANSIT = "transit"
    TERMINAL = "terminal"
    PERIPHERAL = "peripheral"


class NodeBase(BaseModel):
    gid: int = Field(ge=0)
    depth: int = Field(ge=0, le=4)
    is_seed: bool


class NodeMetrics(BaseModel):
    in_degree: int = Field(ge=0)
    out_degree: int = Field(ge=0)
    in_kzt: float = Field(ge=0)
    out_kzt: float = Field(ge=0)
    in_tx: int = Field(ge=0)
    out_tx: int = Field(ge=0)
    pagerank: float = Field(ge=0)
    pass_through: float | None
    seed_reach_count: int = Field(ge=0)
    truncated_by_depth: bool


class NodeAnalytics(BaseModel):
    role: NodeRole
    role_score: float = Field(ge=0, le=1)
    priority_score: float = Field(ge=0, le=1)
    cluster_id: int = Field(ge=0)
    evidence: str = Field(min_length=1, max_length=200)


class NodeRecord(NodeBase, NodeMetrics, NodeAnalytics):
    pass
