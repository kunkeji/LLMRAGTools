# API 文档

## 简介

本文档包含了Agent Tools系统的所有API接口说明。所有API均采用RESTful风格设计，使用JSON格式进行数据交换。

## 文档结构

```
docs/
├── README.md              # 本文档
├── sql/                  # SQL文件目录
│   └── documents.sql     # 文档表SQL
└── api/                  # API文档目录
    ├── auth.md           # 认证相关接口
    ├── user.md           # 用户管理接口
    ├── profile.md        # 个人信息接口
    ├── channel.md        # LLM渠道管理接口
    ├── llm.md            # LLM服务接口
    ├── email.md          # 邮箱管理接口
    └── document.md       # 文档管理接口
```

## 通用说明

### 基础URL

- 开发环境：`http://localhost:8112/api`
- 生产环境：`https://api.example.com/api`

### 版本控制

API版本通过URL路径进行控制，当前版本为v1，如：`/api/v1/user/login`

### 认证方式

大部分API需要通过Bearer Token进行认证：

```
Authorization: Bearer {token}
```

token可以通过登录接口获取。

### 响应格式

所有API响应均使用统一的JSON格式：

```json
{
    "code": "200",        // 状态码
    "message": "Success", // 响应消息
    "data": {            // 响应数据
        // 具体数据字段
    }
}
```

### 通用错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未认证或认证失败 |
| 403 | 无权限访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

### 分页参数

支持分页的接口一般接受以下查询参数：

- `skip`: 跳过记录数（可选，默认0）
- `limit`: 返回记录数（可选，默认100）

### 时间格式

所有时间字段均使用ISO 8601格式的UTC时间，如：

```
"2024-01-20T08:30:00.000Z"
```

## 接口清单

1. 认证接口
   - 用户注册
   - 用户登录
   - 发送验证码
   - 重置密码

2. 用户管理
   - 获取用户信息
   - 更新用户信息
   - 上传头像

3. LLM渠道管理
   - 创建渠道
   - 获取渠道列表
   - 更新渠道
   - 删除渠道

4. LLM服务
   - 获取可用模型
   - 发送对话请求
   - 流式对话

5. 邮箱管理
   - 添加邮箱账号
   - 同步邮件
   - 管理邮箱设置

6. 文档管理
   - 创建文档
   - 获取文档树
   - 更新文档
   - 移动文档
   - 删除文档
   - 搜索文档

## 数据库表

系统包含以下主要数据表：

1. users - 用户表
2. admins - 管理员表
3. verification_codes - 验证码表
4. llm_models - LLM模型表
5. llm_channels - LLM渠道表
6. email_providers - 邮箱提供商表
7. email_accounts - 邮箱账号表
8. documents - 文档表
9. tasks - 任务表

详细的表结构请参考 `sql/` 目录下的SQL文件。

## 开发指南

### 环境要求

- Python 3.8+
- PostgreSQL 12+
- Redis 6+

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置文件

复制 `.env.example` 到 `.env` 并修改相关配置：

```bash
cp .env.example .env
```

### 运行服务

```bash
# 开发环境
python run.py

# 生产环境
python run.py --prod
```