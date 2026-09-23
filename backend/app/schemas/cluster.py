from pydantic import BaseModel, Field


class ClusterRecord(BaseModel):
    cluster_id: int = Field(ge=0)
    n_nodes: int = Field(ge=0)
    n_seed: int = Field(ge=0)
    sum_kzt_internal: float = Field(ge=0)
    top_gids: list[int]
    hypothesis: str = Field(max_length=300)
