from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.schemas.response import ResponseCode, response_error

async def http_exception_handler(request, exc):
    """
    处理 HTTP 异常
    """
    return JSONResponse(
        status_code=200,  # 始终返回200，通过code区分状态
        content=response_error(
            code=str(exc.status_code),
            message=exc.detail
        )
    )

async def validation_exception_handler(request, exc):
    """
    处理请求参数验证异常
    """
    errors = []
    for error in exc.errors():
        errors.append({
            'field': error['loc'][-1],
            'message': error['msg']
        })
    return JSONResponse(
        status_code=200,
        content=response_error(
            code=ResponseCode.BAD_REQUEST,
            message=f"参数验证错误: {errors}"
        )
    )

async def python_exception_handler(request, exc):
    """
    处理其他 Python 异常
    """
    return JSONResponse(
        status_code=200,
        content=response_error(
            code=ResponseCode.SERVER_ERROR,
            message=str(exc)
        )
    ) 