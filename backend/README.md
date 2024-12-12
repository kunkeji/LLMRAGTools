# Agent Tools Backend

基于 FastAPI + MySQL 的后端服务框架，提供用户认证、任务调度、LLM 调用等功能。

## 目录结构

```
backend/
├── app/                                # 应用主目录
│   ├── api/                           # API接口
│   │   └── v1/                        # V1版本API
│   │       ├── admin/                 # 管理员接口
│   │       │   ├── endpoints/
│   │       │   │   └── auth.py       # 管理员认证接口
│   │       │   └── router.py         # 管理员路由
|   │       ├── deps/
|   │       │   └── auth.py           # 依赖注入
|   │       └── user/                  # 用户接口
│   │           ├── endpoints/
│   │           │   ├── auth.py       # 用户认证接口
│   │           │   ├── password.py   # 密码管理接口
│   │           │   └── profile.py    # 个人资料接口
│   │           └── router.py         # 用户路由
│   ├── core/                          # 核心模块
│   │   ├── config.py                 # 配置管理
│   │   ├── docs.py                   # API文档配置
│   │   ├── exceptions.py             # 异常处理
│   │   ├── security/                 # 安全相关
│   │   │   ├── jwt.py               # JWT处理
│   │   │   └── password.py          # 密码处理
│   │   └── tasks/                    # 任务调度
│   │       ├── examples.py           # 示例任务
│   │       ├── registry.py           # 任务注册器
│   │       ├── scheduler.py          # 调度器
│   │       └── __init__.py
│   ├── crud/                          # 数据库操作
│   │   ├── admin.py                  # 管理员CRUD
│   │   ├── base.py                   # 基础CRUD
│   │   ├── user.py                   # 用户CRUD
│   │   └── verification_code.py      # 验证码CRUD
│   ├── db/                            # 数据库配置
│   │   ├── base.py                   # 数据库基础配置
│   │   ├── base_class.py            # 基础模型类
│   │   └── session.py               # 会话管理
│   ├── models/                        # 数据模型
│   │   ├── admin.py                  # 管理员模型
│   │   ├── base.py                   # 基础模型
│   │   ├── base_model.py            # 模型基类
│   │   ├── task.py                  # 任务模型
│   │   ├── user.py                  # 用户模型
│   │   └── verification_code.py     # 验证码模型
│   ├── schemas/                       # 数据验证
│   │   ├── admin.py                  # 管理员Schema
│   │   ├── avatar.py                # 头像Schema
│   │   ├── base.py                  # 基础Schema
│   │   ├── common.py                # 通用Schema
│   │   ├── file.py                  # 文件Schema
│   │   ├── filters.py               # 过滤Schema
│   │   ├── response.py              # 响应Schema
│   │   ├── sort.py                  # 排序Schema
│   │   ├── token.py                 # Token Schema
│   │   ├── user.py                  # 用户Schema
│   │   └── verification_code.py     # 验证码Schema
│   └── utils/                         # 工具函数
│       ├── email.py                  # 邮件工具
│       ├── email_templates/          # 邮件模板
│       │   ├── reset_password.html  # 重置密码模板
│       │   ├── test_email.html     # 测试邮件模板
│       │   └── verification_code.html # 验证码模板
│       ├── file.py                   # 文件处理
│       ├── llm/                      # LLM集成
│       │   ├── client.py            # LLM客户端
│       │   ├── mapping.py           # 模型映射
│       │   ├── providers/           # LLM提供者
│       │   │   └── zhipu_sdk.py    # 智谱AI实现
│       │   └── __init__.py
│       └── logging.py               # 日志工具
├── docker/                            # Docker配置
│   ├── docker-compose.yml           # 容器编排
│   └── mysql/                       # MySQL配置
│       └── conf.d/                  # MySQL自定义配置
├── static/                            # 静态文件
│   └── uploads/                     # 上传文件
│       └── avatars/                 # 头像文件
├── tests/                             # 测试用例
│   ├── test_llm.py                  # LLM测试
│   └── __init__.py
├── .env                              # 环境配置
├── .gitignore                        # Git忽略文件
├── README.md                         # 项目说明
├── requirements.txt                  # 依赖管理
├── run.bat                          # Windows启动脚本
└── scheduler_run.py                 # 调度器启动脚本
```

## 功能模块

### 1. 用户认证系统

#### 1.1 用户注册
```python
POST /api/user/register
{
    "email": "user@example.com",
    "username": "username",
    "password": "password",
    "verification_code": "123456"
}
```

#### 1.2 用户登录
```python
POST /api/user/login
{
    "username": "username",
    "password": "password"
}
```

#### 1.3 密码重置
```python
POST /api/user/password/reset
{
    "email": "user@example.com",
    "code": "123456",
    "new_password": "newpassword"
}
```

### 2. 管理员系统

#### 2.1 管理员登录
```python
POST /api/admin/login
{
    "username": "admin",
    "password": "password"
}
```

#### 2.2 创建管理员
```python
POST /api/admin/create
{
    "username": "newadmin",
    "email": "admin@example.com",
    "password": "password",
    "role": "admin"
}
```

### 3. 文件处理

#### 3.1 头像上传
```python
POST /api/user/profile/me/avatar
Content-Type: multipart/form-data
{
    "file": <file>
}
```

### 4. 任务调度系统

```python
# 注册任务
@task_registry.register(name="task_name", interval_minutes=5)
async def your_task():
    pass

# 创建定时任务
task = Task(
    name="Task Name",
    func_name="task_name",
    scheduled_at=datetime.now() + timedelta(minutes=5)
)
```

### 5. LLM集成

#### 5.1 普通文本生成
```python
response = await LLMClient.generate(
    prompt="系统提示",
    message="用户消息",
    api_key="your-api-key",
    model="glm-4-flash"
)
```

#### 5.2 流式文本生成
```python
async for chunk in LLMClient.generate_stream(
    prompt="系统提示",
    message="用户消息",
    api_key="your-api-key",
    model="glm-4-flash"
):
    print(chunk, end="")
```

## 环境配置

1. 创建虚拟环境：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
复制 `.env.example` 到 `.env` 并修改相关配置。

4. 启动服务：
```bash
# 开发模式
python run.py

# 生产模式
RUN_MODE=prod python run.py
```

## 数据库表结构

### users 表
- 用户基本信息
- 认证相关字段
- 个人资料

### admins 表
- 管理员信息
- 角色权限

### verification_codes 表
- 验证码记录
- 用途标记
- 过期时间

### tasks 表
- 任务信息
- 执行状态
- 调度时间

## API 响应格式

所有API响应都遵循统一格式：
```json
{
    "code": "200",
    "message": "Success",
    "data": null
}
```

## 开发规范

1. 代码风格遵循 PEP 8
2. 所有函数和类必须有文档字符串
3. 使用 Type Hints 进行类型注解
4. 异常必须被妥善处理和记录
5. 新功能必须编写测试用例

## 部署说明

1. 使用 Docker Compose 启动服务：
```bash
docker-compose up -d
```

2. 数据库迁移：
```bash
# 创建迁移脚本
alembic revision --autogenerate -m "message"

# 执行迁移
alembic upgrade head
```

## 常见问题

1. 数据库连接失败
- 检查 MySQL 服务是否启动
- 验证数据库连接信息

2. 邮件发送失败
- 确认 SMTP 配置正确
- 检查网络连接

3. 文件上传失败
- 检查目录权限
- 确认文件大小限制 

待完善：
a. 安全相关：
⚠️ 请求速率限制（Rate Limiting）
⚠️ CORS 详细配置
⚠️ 安全中间件（XSS、CSRF防护）
⚠️ 敏感数据加密存储
b. 日志系统：
⚠️ 操作日志记录
⚠️ 审计日志
⚠️ 日志轮转和清理策略
c. 缓存系统：
⚠️ Redis 缓存集成
⚠️ 缓存策略实现
d. 监控和维护：
⚠️ 健康检查接口完善
⚠️ 性能监控
⚠️ 系统指标收集
e. 其他功能：
⚠️ WebSocket 支持（实时通知）
⚠️ 批量操作接口
⚠️ 导入/导出功能
⚠️ 更多 LLM 提供者的支持
f. 开发和部署相关：
⚠️ 单元测试覆盖
⚠️ CI/CD 配置
⚠️ 生产环境部署文档
⚠️ API 文档完善
⚠️ 开发环境配置文档