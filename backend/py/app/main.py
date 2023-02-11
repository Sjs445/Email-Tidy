from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.config.config import settings

app = FastAPI(title="Email Tidy")

# Set all CORS enabled origins TODO
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
