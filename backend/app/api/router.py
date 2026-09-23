from fastapi import APIRouter

from app.core.config import settings
from app.api.routes import router as domain_router


api_router = APIRouter(prefix=settings.API_V1_PREFIX)
api_router.include_router(domain_router)
