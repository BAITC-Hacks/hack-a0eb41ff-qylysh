from pydantic import BaseModel, Field

from app.schemas.node import NodeRole


class GraphNode(BaseModel):
    gid: int = Field(ge=0)
    role: NodeRole
    role_score: float = Field(ge=0, le=1)
    priority_score: float = Field(ge=0, le=1)
    cluster_id: int = Field(ge=0)
    is_seed: bool


class GraphEdge(BaseModel):
    source: int = Field(ge=0)
    target: int = Field(ge=0)
    sum_kzt: float = Field(ge=0)
    n_tx: int = Field(ge=0)


class GraphResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]
