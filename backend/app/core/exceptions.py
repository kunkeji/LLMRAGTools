from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.schemas.response import ResponseCode, response_error
import logging

async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    HTTP异常处理器
    """
    return JSONResponse(
        status_code=200,
        content=response_error(
            code=str(exc.status_code),
            message=str(exc.detail)
        )
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    请求验证异常处理器
    """
    errors = []
    for error in exc.errors():
        error_msg = f"{' -> '.join(str(x) for x in error['loc'])}: {error['msg']}"
        errors.append(error_msg)
    
    return JSONResponse(
        status_code=200,
        content=response_error(
            code=ResponseCode.BAD_REQUEST,
            message="\n".join(errors)
        )
    )

async def python_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Python异常处理器
    """
    logging.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=200,
        content=response_error(
            code=ResponseCode.SERVER_ERROR,
            message=str(exc)
        )
    )

"""
自定义异常类
"""

class FeatureNotConfiguredError(Exception):
    """功能未配置错误"""
    pass 