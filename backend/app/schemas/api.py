from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.node import NodeRole


def _camel(name: str) -> str:
    head, *tail = name.split("_")
    return head + "".join(part.capitalize() for part in tail)


# The source data uses 18-digit GIDs. JSON numbers lose their exact value in browsers.
Gid = Annotated[str, Field(pattern=r"^[0-9]+$")]


class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=_camel, populate_by_name=True, extra="forbid")


class NodeListItem(ApiModel):
    gid: Gid
    role: NodeRole
    role_score: float = Field(ge=0, le=1)
    priority_score: float = Field(ge=0, le=1)
    cluster_id: int = Field(ge=0)
    is_seed: bool
    depth: int = Field(ge=0, le=4)
    evidence: str = Field(min_length=1, max_length=200)
    in_degree: int = Field(ge=0)
    out_degree: int = Field(ge=0)
    in_kzt: float = Field(ge=0)
    out_kzt: float = Field(ge=0)
    transaction_count: int = Field(ge=0)


class NodeDetailsResponse(NodeListItem):
    pagerank: float = Field(ge=0)
    pass_through: float | None
    seed_reach_count: int = Field(ge=0)
    truncated_by_depth: bool


class PaginatedNodesResponse(ApiModel):
    items: list[NodeListItem]
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total: int = Field(ge=0)


class SummaryTopNode(ApiModel):
    rank: int = Field(ge=1)
    gid: Gid
    role: NodeRole
    priority_score: float = Field(ge=0, le=1)
    cluster_id: int = Field(ge=0)
    evidence: str


class ClusterListItem(ApiModel):
    cluster_id: int = Field(ge=0)
    node_count: int = Field(ge=0)
    seed_count: int = Field(ge=0)
    internal_volume_kzt: float = Field(ge=0)
    top_gid: Gid | None
    hypothesis: str
    description: str


class ClusterResponse(ClusterListItem):
    top_gids: list[Gid]


class ClusterListResponse(ApiModel):
    items: list[ClusterListItem]
    total: int = Field(ge=0)


class SummaryResponse(ApiModel):
    total_nodes: int
    total_edges: int
    total_transactions: int
    total_seeds: int
    total_clusters: int
    roles: dict[NodeRole, int]
    top_nodes: list[SummaryTopNode]
    top_clusters: list[ClusterListItem]


class ApiGraphNode(ApiModel):
    gid: Gid
    role: NodeRole
    role_score: float
    priority_score: float
    cluster_id: int
    is_seed: bool
    depth: int


class ApiGraphEdge(ApiModel):
    source: Gid
    target: Gid
    sum_kzt: float
    transaction_count: int


class GraphFocus(ApiModel):
    type: Literal["gid", "cluster"]
    id: Gid | int


class ApiGraphResponse(ApiModel):
    focus: GraphFocus
    nodes: list[ApiGraphNode]
    edges: list[ApiGraphEdge]
    truncated_at_depth: int | None
