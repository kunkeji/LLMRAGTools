# Agent Tools 项目

## 项目结构
```
.
├── backend/                # 后端服务
│   ├── alembic/           # 数据库迁移
│   ├── app/               # 应用主目录
│   │   ├── api/          # API 路由
│   │   │   └── v1/      # API 版本
│   │   │       ├── admin/  # 管理端 API
│   │   │       └── user/   # 用户端 API
│   │   ├── core/         # 核心功能
│   │   ├── crud/         # 数据库操作
│   │   ├── db/           # 数据库配置
│   │   ├── models/       # 数据模型
│   │   ├── schemas/      # Pydantic 模型
│   │   └── utils/        # 工具函数
│   ├── tests/            # 测试文件
│   └── docs/             # 文档
├── frontend-admin/        # 管理端前端
└── frontend-user/         # 用户端前端
```

## 技术栈
- 后端：Python + FastAPI + SQLAlchemy + MySQL
- 前端：React + UmiJS
- 数据库：MySQL (Docker)
- 开发工具：VSCode/PyCharm

## 功能特性

### 用户系统
- 用户注册/登录
- 用户信息管理
- 用户状态管理（活跃/禁用）
- 头像上传

### 管理系统
- 管理员登录
- 角色管理（管理员/超级管理员）
- 用户管理
- 系统配置

### 安全特性
- JWT 认证
- 密码加密
- CORS 配置
- 请求速率限制

## 开发环境设置

### 后端
1. 创建虚拟环境：
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
复制 `.env.example` 到 `.env` 并修改配置

4. 初始化数据库：
```bash
cd docker
docker-compose up -d
cd ../backend
alembic upgrade head
```

5. 启动开发服务器：
```bash
# Windows
run.bat

# Linux/Mac
# 设置端口
export PORT=8111
./run.sh
```

### 前端
1. 安装依赖：
```bash
# 管理端
cd frontend-admin
yarn install

# 用户端
cd frontend-user
yarn install
```

2. 启动开发服务器：
```bash
yarn dev
```

## 测试
运行测试：
```bash
cd backend
pytest
```

## API 文档
- 开发环境：http://localhost:8111/docs
- 生产环境：https://your-domain.com/docs

## 部署
详见 [部署文档](./docs/deployment.md)

## 贡献指南
1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证
MIT