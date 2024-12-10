from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.v1 import api_router
import pytz
from datetime import datetime

# 设置时区
tz = pytz.timezone(settings.TIMEZONE)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Your API description",
    version=settings.VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    default_response_class=JSONResponse,
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "mode": settings.RUN_MODE,
        "timezone": settings.TIMEZONE,
        "current_time": datetime.now(tz).isoformat(),
        "language": settings.DEFAULT_LANGUAGE
    } 