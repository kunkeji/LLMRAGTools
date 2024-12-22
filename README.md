

![logo](./icon128.png)
# LLMRAGTools



# LLMRAGTools Backend

AgentTools 是一个专为大语言模型（LLM）落地设计的中间件框架。它提供了灵活的 LLM 映射机制、RAG 集成、插件化开发支持以及强大的异步任务处理能力，让开发者能够快速构建和部署基于 LLM 的应用。

## 核心特性

### 1. LLM 映射与集成
- 支持多种 LLM 提供商（OpenAI、Anthropic、智谱等）
- 统一的调用接口，灵活的模型映射
- 支持流式输出和普通对话模式
- 内置 Token 计数和成本控制

### 2. RAG（检索增强生成）支持
- 文档向量化和存储
- 相似度检索
- 上下文组装和优化
- 支持多种向量数据库

### 3. 插件化架构
- 松耦合的模块设计
- 简单的插件开发流程
- 丰富的扩展点

### 4. 异步任务系统
- 基于装饰器的任务注册
- 支持定时任务和周期任务
- 多线程执行能力
- 任务状态监控

## 快速开始

### 安装
```bash
git clone https://github.com/kunkeji/LLMRAGTools.git

# 创建数据库、导入sql文件
# sql文件在backend/sql/agent_db.sql

cd LLMRAGTools/backend
# 创建虚拟环境
python -m venv venv
# 激活虚拟环境
source venv/bin/activate
# 安装依赖
pip install -r requirements.txt
# 安装uvicorn
pip install uvicorn
# 启动服务
uvicorn main:app --reload
# 启动任务管理器
python scheduler_run.py

# 启动前端
cd ../web
npm install 
npm run dev

# 测试用户账号密码
admin/123456
```

### 基础配置
```bash
cp .env.example .env
# 编辑 .env 文件，配置必要的参数
# SMTP configuration
SMTP_TLS=False
SMTP_SSL=True
SMTP_PORT=465
SMTP_HOST=smtp.qq.com
SMTP_USER=admin@qq.com
SMTP_PASSWORD=jgpxvkp****
EMAILS_FROM_EMAIL=admin@qq.com
EMAILS_FROM_NAME="LLMRAGTools"

# 运行时配置
RUN_MODE=dev
PORT=8111
```

### 启动服务
```bash
# 开发模式
python ./run.sh


# 生产模式
RUN_MODE=prod python run.sh
```

## 示例功能

### 邮箱管理系统
在已有的邮箱管理系统中，可以配置邮箱账号，设置邮件同步，同步过程中可以使用LLM进行邮件分类，并对分类的邮件进行相应的操作，例如回复、转发、删除、生成预回复内容等。


## 使用示例

### 1. LLM 映射调用
```python
from app.utils.llm import LLMClient
from app.utils.llm.mapping import ModelMapping

# 配置模型映射
mapping = {
    "gpt-4": {
        "provider": "openai",
        "model": "gpt-4-1106-preview",
        "temperature": 0.7
    },
    "claude": {
        "provider": "anthropic",
        "model": "claude-2.1",
        "temperature": 0.9
    }
}

# 普通对话
response = await LLMClient.generate(
    prompt="你是一个专业的助手",
    message="帮我总结这篇文章",
    model="gpt-4",  # 将自动映射到配置的模型
    api_key="your-api-key"
)

# 流式对话
async for chunk in LLMClient.generate_stream(
    prompt="你是一个专业的助手",
    message="帮我总结这篇文章",
    model="claude",
    api_key="your-api-key"
):
    print(chunk, end="")
```

### 2. 任务注册与执行
```python
from app.core.tasks import task_registry
from datetime import datetime, timedelta

# 注册定时任务
@task_registry.register(
    name="daily_report",
    interval_minutes=1440,  # 每天执行一次
    max_instances=1  # 最大同时运行实例数
)
async def generate_daily_report():
    # 任务逻辑
    pass

# 注册普通任务
@task_registry.register(name="process_document")
async def process_document(doc_id: str):
    # 处理文档的逻辑
    pass

# 手动创建任务
from app.models.task import Task

task = Task(
    name="Specific Report",
    func_name="daily_report",
    scheduled_at=datetime.now() + timedelta(hours=1)
)
await task.save()
```

### 3. 开发新的 API 接口
```python
from fastapi import APIRouter, Depends
from app.schemas.response import Response
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/custom-endpoint")
async def custom_endpoint(
    data: YourSchema,
    current_user = Depends(get_current_user)
):
    # 实现你的业务逻辑
    result = await your_business_logic(data)
    return Response(code=200, data=result)
```

## 项目结构

```
backend/
├── app/
│   ├── api/                    # API 接口
│   │   └── v1/
│   │       ├── admin/         # 管理接口
│   │       └── user/          # 用户接口
│   ├── core/                  # 核心功能
│   │   ├── config.py         # 配置管理
│   │   └── tasks/            # 任务系统
│   ├── plugins/              # 插件目录
│   │   ├── rag/             # RAG 插件
│   │   └── custom/          # 自定义插件
│   ├── utils/
│   │   ├── llm/             # LLM 工具
│   │   │   ├── client.py    # 统一客户端
│   │   │   ├── mapping.py   # 模型映射
│   │   │   └── providers/   # 提供商实现
│   │   └── vector_store/    # 向量存储
│   └── models/              # 数据模型
└── tests/                   # 测试用例
```

## 业务流程

1. **LLM 调用流程**
   - 接收用户请求
   - 根据映射配置选择模型
   - 调用相应提供商 API
   - 处理响应并返回

2. **RAG 处理流程**
   - 文档预处理
   - 向量化存储
   - 相似度检索
   - 上下文组装
   - LLM 调用

3. **任务执行流程**
   - 任务注册
   - 调度器扫描
   - 任务分发
   - 异步执行
   - 状态更新

## 二次开发指南

### 1. 添加新的 LLM 提供商
1. 在 `app/utils/llm/providers/` 下创建新的提供商实现
2. 实现标准接口方法
3. 在 `mapping.py` 中注册提供商

### 2. 开发新插件
1. 在 `app/plugins/` 下创建新的插件目录
2. 实现插件接口
3. 注册插件到系统

### 3. 自定义任务
1. 创建任务函数
2. 使用 `@task_registry.register` 装饰器注册
3. 配置执行参数

### 4. API 开发
1. 在 `app/api/v1/` 下创建新的路由模块
2. 定义请求和响应模型
3. 实现业务逻辑
4. 注册路由

## 配置说明

### 环境变量
```bash
# LLM 配置
OPENAI_API_KEY=your-api-key
ANTHROPIC_API_KEY=your-api-key
ZHIPU_API_KEY=your-api-key

# 数据库配置
DATABASE_URL=mysql+pymysql://user:pass@localhost/dbname

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# 任务配置
MAX_WORKERS=4
TASK_TIMEOUT=3600
```


## 常见问题

1. LLM 调用失败
   - 检查 API Key 配置
   - 确认网络连接
   - 查看错误日志

2. 任务执行异常
   - 检查任务注册状态
   - 确认调度器运行状态
   - 查看任务日志

3. 插件加载失败
   - 检查插件依赖
   - 确认接口实现
   - 查看注册日志

## 待开发功能

- [ ] 更多 LLM 提供商支持
- [ ] 高级 RAG 策略
- [ ] 分布式任务支持
- [ ] 监控告警系统
- [ ] 更多向量数据库集成
- [ ] WebSocket 实时通信
- [ ] 插件市场

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交变更
4. 发起 Pull Request

## 许可证

MIT License