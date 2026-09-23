from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.schemas.common import HealthResponse


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API foundation for the MoneyGraph analytics application.",
    debug=settings.DEBUG,
)

app.include_router(api_router)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=settings.APP_NAME,
        version=settings.APP_VERSION,
    )
