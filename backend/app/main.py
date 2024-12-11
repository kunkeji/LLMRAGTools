from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

from app.core.config import settings
from app.core.exceptions import http_exception_handler, validation_exception_handler, python_exception_handler
from app.core.docs import tags_metadata, api_description, swagger_ui_parameters
from app.api.v1 import api_router
from app.schemas.response import response_success
import pytz
from datetime import datetime
from app.core.middleware.logging import LoggingMiddleware
from app.utils.logger import logger_instance


# 设置时区
tz = pytz.timezone(settings.TIMEZONE)

# 设置静态文件目录
ROOT_DIR = Path(__file__).parent.parent
STATIC_DIR = ROOT_DIR / "static"
UPLOAD_DIR = STATIC_DIR / "uploads"

# 确保目录存在
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
(UPLOAD_DIR / "avatars").mkdir(exist_ok=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=api_description,
    version=settings.VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    openapi_tags=tags_metadata,
    swagger_ui_parameters=swagger_ui_parameters,
    default_response_class=JSONResponse,
    redirect_slashes=True,
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    contact={
        "name": "技术支持",
        "url": "http://kunkeji.com",
        "email": "kunkeji@qq.com",
    },
    servers=[
        {"url": "http://localhost:8112", "description": "开发环境"},
        {"url": "http://test-api.example.com", "description": "测试环境"},
        {"url": "https://api.example.com", "description": "生产环境"},
    ] if settings.DEBUG else [
        {"url": "https://api.example.com", "description": "生产环境"},
    ]
)

# 注册异常处理器
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, python_exception_handler)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册日志中间件
app.add_middleware(LoggingMiddleware, logger=logger_instance)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount static files
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", tags=["system"])
async def root():
    """
    获取系统信息
    返回系统的基本信息，包括：
    * 系统名称
    * 版本号
    * 运行模式
    * 时区
    * 当前时间
    * 默认语言
    """
    return response_success(
        data={
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "mode": settings.RUN_MODE,
            "timezone": settings.TIMEZONE,
            "current_time": datetime.now(tz).isoformat(),
            "language": settings.DEFAULT_LANGUAGE
        }
    )

@app.get("/health", tags=["system"])
async def health_check():
    """
    健康检查接口
    用于监控系统是否正常运行
    """
    return response_success(
        data={
            "status": "healthy",
            "timestamp": datetime.now(tz).isoformat()
        }
    ) 