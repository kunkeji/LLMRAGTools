"""
日志中间件
"""
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.utils.logger import Logger
from app.models.log import LogType, LogLevel

class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        logger: Logger
    ) -> None:
        super().__init__(app)
        self.logger = logger

    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        # 生成请求ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # 记录请求开始时间
        start_time = time.time()
        
        # 获取用户信息
        user_id = None
        username = None
        try:
            if hasattr(request.state, "user"):
                user = request.state.user
                user_id = user.id
                username = user.username
        except:
            pass
        
        # 记录请求日志
        self.logger.info(
            message=f"收到请求: {request.method} {request.url.path}",
            log_type=LogType.API,
            request_id=request_id,
            method=request.method,
            url=str(request.url),
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            user_id=user_id,
            username=username,
            module="api",
            details={
                "query_params": str(request.query_params),
                "path_params": str(request.path_params),
                "headers": dict(request.headers)
            }
        )
        
        try:
            # 处理请求
            response = await call_next(request)
            
            # 计算处理时间
            duration = int((time.time() - start_time) * 1000)
            
            # 记录响应日志
            self.logger.info(
                message=f"请求完成: {request.method} {request.url.path}",
                log_type=LogType.API,
                request_id=request_id,
                method=request.method,
                url=str(request.url),
                ip_address=request.client.host,
                user_id=user_id,
                username=username,
                module="api",
                duration=duration,
                details={
                    "status_code": response.status_code,
                    "headers": dict(response.headers)
                }
            )
            
            return response
            
        except Exception as e:
            # 计算处理时间
            duration = int((time.time() - start_time) * 1000)
            
            # 记录错误日志
            self.logger.error(
                message=f"请求异常: {str(e)}",
                log_type=LogType.API,
                request_id=request_id,
                method=request.method,
                url=str(request.url),
                ip_address=request.client.host,
                user_id=user_id,
                username=username,
                module="api",
                duration=duration,
                error_type=type(e).__name__,
                error_stack=str(e),
                details={
                    "exception": str(e)
                }
            )
            raise 