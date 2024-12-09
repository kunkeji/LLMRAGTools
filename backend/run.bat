@echo off
setlocal

:: 设置 Python 路径
set PYTHONPATH=%PYTHONPATH%;%CD%

:: 从环境变量获取运行模式和端口
if "%RUN_MODE%"=="prod" (
    uvicorn app.main:app --host 0.0.0.0 --port %PORT% --workers 4
) else (
    :: 开发模式使用单进程和延迟重载
    uvicorn app.main:app --reload --reload-dir app --host 0.0.0.0 --port %PORT% --reload-delay 2 --use-colors
)

endlocal