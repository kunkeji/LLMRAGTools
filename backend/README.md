# LLMRAGTools Backend

LLMRAGTools 是一个专为大语言模型（LLM）落地设计的中间件框架。它提供了灵活的 LLM 映射机制、RAG 集成、插件化开发支持以及强大的异步任务处理能力，让开发者能够快速构建和部署基于 LLM 的应用。

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

### 环境要求
- Python 3.8+
- MySQL 5.7+
- Redis 6.0+

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/LLMRAGTools.git
cd LLMRAGTools/backend
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，配置必要的参数
```

4. 初始化数据库
```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE agent_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 执行数据库迁移
alembic upgrade head
```

5. 启动服务
```bash
# 开发模式
python run.py

# 生产模式
RUN_MODE=prod python run.py
```

## 项目结构

```
backend/
├── alembic/              # 数据库迁移
├── app/
│   ├── api/             # API 接口
│   │   └── v1/
│   │       ├── admin/  # 管理接口
│   │       └── user/   # 用户接口
│   ├── core/           # 核心功能
│   │   ├── config.py  # 配置管理
│   │   └── tasks/     # 任务系统
│   ├── crud/          # 数据库操作
│   ├── db/            # 数据库配置
│   ├── models/        # 数据库模型
│   ├── schemas/       # 数据验证
│   └── utils/         # 工具函数
├── logs/              # 日志文件
├── static/           # 静态文件
├── tests/            # 测试用例
├── uploads/          # 上传文件
└── docs/            # 文档
```

## 配置说明

主要配置项（在 .env 文件中设置）：

```bash
# 数据库配置
DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/agent_db

# JWT 配置
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# SMTP 配置
SMTP_HOST=smtp.example.com
SMTP_PORT=465
SMTP_USER=your-email
SMTP_PASSWORD=your-password

# 系统配置
RUN_MODE=dev
PORT=8111
LOG_LEVEL=INFO
TIMEZONE=Asia/Shanghai
```

## API 文档

启动服务后访问：
- Swagger UI: http://localhost:8111/docs
- ReDoc: http://localhost:8111/redoc

### 主要接口

1. 用户管理
   - POST /api/v1/user/register - 用户注册
   - POST /api/v1/user/login - 用户登录
   - GET /api/v1/user/me - 获取当前用户信息

2. 邮件管理
   - GET /api/v1/email/inbox - 收件箱列表
   - GET /api/v1/email/outbox - 发件箱列表
   - POST /api/v1/email/send - 发送邮件
   - GET /api/v1/email/{id} - 邮件详情

3. 任务管理
   - POST /api/v1/task/create - 创建任务
   - GET /api/v1/task/list - 任务列表
   - GET /api/v1/task/{id} - 任务详情

## 开发指南

### 1. 添加新的 API 接口

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
    result = await your_business_logic(data)
    return Response(code=200, data=result)
```

### 2. 创建新的任务

```python
from app.core.tasks import task_registry

@task_registry.register(
    name="custom_task",
    interval_minutes=60
)
async def custom_task():
    # 实现任务逻辑
    pass
```

### 3. 添加新的数据模型

```python
from app.db.base_class import Base
from sqlalchemy import Column, Integer, String

class YourModel(Base):
    __tablename__ = "your_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(200))
```

## 常见问题

1. 数据库连接问题
   - 检查数据库配置是否正确
   - 确保数据库服务正在运行
   - 验证用户权限

2. 邮件发送失败
   - 检查 SMTP 配置
   - 确认邮箱账号密码
   - 查看错误日志

3. 任务执行异常
   - 检查 Redis 连接
   - 确认任务注册状态
   - 查看任务日志

## 更新日志

### v1.0.0 (2023-12-22)
- 初始版本发布
- 基础功能实现
- 邮件系统集成
- 任务系统实现

## 待开发功能

- [ ] 更多 LLM 提供商支持
- [ ] 高级 RAG 策略
- [ ] 分布式任务支持
- [ ] 监控告警系统
- [ ] 更多向量数据库集成
- [ ] WebSocket 实时通信

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 发起 Pull Request

## 许可证

MIT License
