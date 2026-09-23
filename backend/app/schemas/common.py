from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class ApiError(BaseModel):
    code: str
    message: str
