from pydantic import BaseModel, Field


class EdgeRecord(BaseModel):
    source: int = Field(ge=0)
    target: int = Field(ge=0)
    sum_kzt: float = Field(ge=0)
    n_tx: int = Field(ge=0)
    depth: int = Field(ge=0, le=4)
