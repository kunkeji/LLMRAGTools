#!/bin/bash

# 设置 Python 路径
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 设置 uvicorn 参数
# 默认使用.env中的PORT
PORT=${PORT:-8112}
if [ "$RUN_MODE" = "prod" ]; then
    uvicorn app.main:app --host 127.0.0.1 --port $PORT --workers 4
else
    # 开发模式下禁用默认的 watchfiles，使用 watchgod
    uvicorn app.main:app --reload --reload-dir app --host 127.0.0.1 --port $PORT --reload-delay 2 --use-colors
fi
