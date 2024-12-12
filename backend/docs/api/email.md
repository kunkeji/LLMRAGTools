# 邮箱系统接口文档

## 管理员接口

### 1. 获取邮箱提供商列表

**请求**
- 方法：`GET`
- 路径：`/api/admin/email/providers`
- 参数：
  ```json
  {
    "keyword": "qq",           // 可选，搜索关键词
    "is_active": true,         // 可选，是否启用
    "skip": 0,                 // 可选，默认0
    "limit": 100              // 可选，默认100
  }
  ```

**响应**
```json
{
  "code": "200",
  "message": "Success",
  "data": [
    {
      "id": 1,
      "name": "QQ邮箱",
      "domain_suffix": "@qq.com",
      "smtp_host": "smtp.qq.com",
      "smtp_port": 465,
      "imap_host": "imap.qq.com",
      "imap_port": 993,
      "use_ssl": true,
      "use_tls": false,
      "is_active": true,
      "logo_url": "https://example.com/qq-logo.png",
      "description": "QQ邮箱服务",
      "help_url": "https://service.mail.qq.com/",
      "auth_help_url": "https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256",
      "sort_order": 10
    }
  ]
}
```

### 2. 创建邮箱提供商

**请求**
- 方法：`POST`
- 路径：`/api/admin/email/providers`
- 请求体：
  ```json
  {
    "name": "QQ邮箱",
    "domain_suffix": "@qq.com",
    "smtp_host": "smtp.qq.com",
    "smtp_port": 465,
    "imap_host": "imap.qq.com",
    "imap_port": 993,
    "use_ssl": true,
    "use_tls": false,
    "is_active": true,
    "logo_url": "https://example.com/qq-logo.png",
    "description": "QQ邮箱服务",
    "help_url": "https://service.mail.qq.com/",
    "auth_help_url": "https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256",
    "sort_order": 10
  }
  ```

**响应**
```json
{
  "code": "200",
  "message": "Success",
  "data": {
    "id": 1,
    "name": "QQ邮箱",
    "domain_suffix": "@qq.com",
    "smtp_host": "smtp.qq.com",
    "smtp_port": 465,
    "imap_host": "imap.qq.com",
    "imap_port": 993,
    "use_ssl": true,
    "use_tls": false,
    "is_active": true,
    "logo_url": "https://example.com/qq-logo.png",
    "description": "QQ邮箱服务",
    "help_url": "https://service.mail.qq.com/",
    "auth_help_url": "https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256",
    "sort_order": 10
  }
}
```

### 3. 更新邮箱提供商

**请求**
- 方法：`PUT`
- 路径：`/api/admin/email/providers/{provider_id}`
- 请求体：
  ```json
  {
    "name": "QQ邮箱",
    "is_active": true,
    "description": "QQ邮箱服务更新",
    "sort_order": 20
  }
  ```

**响应**
```json
{
  "code": "200",
  "message": "Success",
  "data": {
    "id": 1,
    "name": "QQ邮箱",
    "domain_suffix": "@qq.com",
    "smtp_host": "smtp.qq.com",
    "smtp_port": 465,
    "imap_host": "imap.qq.com",
    "imap_port": 993,
    "use_ssl": true,
    "use_tls": false,
    "is_active": true,
    "logo_url": "https://example.com/qq-logo.png",
    "description": "QQ邮箱服务更新",
    "help_url": "https://service.mail.qq.com/",
    "auth_help_url": "https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256",
    "sort_order": 20
  }
}
```

### 4. 删除邮箱提供商

**请求**
- 方法：`DELETE`
- 路径：`/api/admin/email/providers/{provider_id}`

**响应**
```json
{
  "code": "200",
  "message": "Success",
  "data": null
}
```

### 5. 获取邮箱提供商详情

**请求**
- 方法：`GET`
- 路径：`/api/admin/email/providers/{provider_id}`

**响应**
```json
{
  "code": "200",
  "message": "Success",
  "data": {
    "id": 1,
    "name": "QQ邮箱",
    "domain_suffix": "@qq.com",
    "smtp_host": "smtp.qq.com",
    "smtp_port": 465,
    "imap_host": "imap.qq.com",
    "imap_port": 993,
    "use_ssl": true,
    "use_tls": false,
    "is_active": true,
    "logo_url": "https://example.com/qq-logo.png",
    "description": "QQ邮箱服务",
    "help_url": "https://service.mail.qq.com/",
    "auth_help_url": "https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256",
    "sort_order": 10
  }
}
```

## 用户接口

### 1. 获取邮箱账户列表

**请求**
- 方法：`GET`
- 路径：`/api/user/email/accounts`
- 参数：
  ```json
  {
    "skip": 0,     // 可选，默认0
    "limit": 100   // 可选，默认100
  }
  ```

**响应**
```json
{
  "code": "200",
  "message": "Success",
  "data": [
    {
      "id": 1,
      "user_id": 1,
      "email_address": "example@qq.com",
      "display_name": "我的QQ邮箱",
      "is_default": true,
      "is_active": true,
      "smtp_host": "smtp.qq.com",
      "smtp_port": 465,
      "imap_host": "imap.qq.com",
      "imap_port": 993,
      "use_ssl": true,
      "use_tls": false,
      "sync_status": "success",
      "last_sync_time": "2024-01-20T08:30:00Z",
      "next_sync_time": "2024-01-20T09:00:00Z",
      "sync_error": null,
      "total_emails": 1000,
      "unread_emails": 5,
      "last_email_time": "2024-01-20T08:25:00Z",
      "sync_interval": 30,
      "keep_days": 30,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-20T08:30:00Z"
    }
  ]
}
```

### 2. 创建邮箱账户

**请求**
- 方法：`POST`
- 路径：`/api/user/email/accounts`
- 请求体：
  ```json
  {
    "email_address": "example@qq.com",
    "auth_token": "abcdefghijklmn",
    "display_name": "我的QQ邮箱",
    "is_default": true,
    "smtp_host": "smtp.qq.com",
    "smtp_port": 465,
    "imap_host": "imap.qq.com",
    "imap_port": 993,
    "use_ssl": true,
    "use_tls": false,
    "sync_interval": 30,
    "keep_days": 30
  }
  ```

**响应**
```json
{
  "code": "200",
  "message": "Success",
  "data": {
    "id": 1,
    "user_id": 1,
    "email_address": "example@qq.com",
    "display_name": "我的QQ邮箱",
    "is_default": true,
    "is_active": true,
    "smtp_host": "smtp.qq.com",
    "smtp_port": 465,
    "imap_host": "imap.qq.com",
    "imap_port": 993,
    "use_ssl": true,
    "use_tls": false,
    "sync_status": "never",
    "sync_interval": 30,
    "keep_days": 30,
    "created_at": "2024-01-20T08:30:00Z",
    "updated_at": "2024-01-20T08:30:00Z"
  }
}
```

### 3. 更新邮箱账户

**请求**
- 方法：`PUT`
- 路径：`/api/user/email/accounts/{account_id}`
- 请求体：
  ```json
  {
    "display_name": "我的QQ邮箱(更新)",
    "is_default": true,
    "auth_token": "newtoken123",
    "sync_interval": 60
  }
  ```

**响应**
```json
{
  "code": "200",
  "message": "Success",
  "data": {
    "id": 1,
    "user_id": 1,
    "email_address": "example@qq.com",
    "display_name": "我的QQ邮箱(更新)",
    "is_default": true,
    "is_active": true,
    "smtp_host": "smtp.qq.com",
    "smtp_port": 465,
    "imap_host": "imap.qq.com",
    "imap_port": 993,
    "use_ssl": true,
    "use_tls": false,
    "sync_status": "success",
    "sync_interval": 60,
    "keep_days": 30,
    "created_at": "2024-01-20T08:30:00Z",
    "updated_at": "2024-01-20T09:30:00Z"
  }
}
```

### 4. 删除邮箱账户

**请求**
- 方法：`DELETE`
- 路径：`/api/user/email/accounts/{account_id}`

**响应**
```json
{
  "code": "200",
  "message": "Success",
  "data": null
}
```

### 5. 获取邮箱账户详情

**请求**
- 方法：`GET`
- 路径：`/api/user/email/accounts/{account_id}`

**响应**
```json
{
  "code": "200",
  "message": "Success",
  "data": {
    "id": 1,
    "user_id": 1,
    "email_address": "example@qq.com",
    "display_name": "我的QQ邮箱",
    "is_default": true,
    "is_active": true,
    "smtp_host": "smtp.qq.com",
    "smtp_port": 465,
    "imap_host": "imap.qq.com",
    "imap_port": 993,
    "use_ssl": true,
    "use_tls": false,
    "sync_status": "success",
    "last_sync_time": "2024-01-20T08:30:00Z",
    "next_sync_time": "2024-01-20T09:00:00Z",
    "sync_error": null,
    "total_emails": 1000,
    "unread_emails": 5,
    "last_email_time": "2024-01-20T08:25:00Z",
    "sync_interval": 30,
    "keep_days": 30,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-20T08:30:00Z"
  }
}
```

### 6. 获取可用的邮箱提供商列表

**请求**
- 方法：`GET`
- 路径：`/api/user/email/providers`
- 参数：
  ```json
  {
    "skip": 0,     // 可选，默认0
    "limit": 100   // 可选，默认100
  }
  ```

**响应**
```json
{
  "code": "200",
  "message": "Success",
  "data": [
    {
      "id": 1,
      "name": "QQ邮箱",
      "domain_suffix": "@qq.com",
      "smtp_host": "smtp.qq.com",
      "smtp_port": 465,
      "imap_host": "imap.qq.com",
      "imap_port": 993,
      "use_ssl": true,
      "use_tls": false,
      "logo_url": "https://example.com/qq-logo.png",
      "description": "QQ邮箱服务",
      "help_url": "https://service.mail.qq.com/",
      "auth_help_url": "https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256"
    }
  ]
}
```

### 7. 测试邮箱账户连接

**请求**
- 方法：`POST`
- 路径：`/api/user/email/accounts/{account_id}/test`

**响应**
```json
{
  "code": "200",
  "message": "Success",
  "data": null
}
```

### 8. 手动同步邮箱账户

**请求**
- 方法：`POST`
- 路径：`/api/user/email/accounts/{account_id}/sync`

**响应**
```json
{
  "code": "200",
  "message": "Success",
  "data": null
}
```

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | 未认证或认证失败 |
| 403 | 无权限访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 特定错误说明

1. 创建邮箱提供商时：
   - `Provider name already exists`: 提供商名称已存在
   - `Domain suffix already exists`: 域名后缀已存在

2. 创建邮箱账户时：
   - `Email address already exists`: 邮箱地址已存在
   - `Invalid email provider`: 无效的邮箱提供商

3. 邮箱连接测试时：
   - `Failed to connect to email server`: 连接邮箱服务器失败
   - `Invalid credentials`: 无效的认证信息

4. 邮箱同步时：
   - `Sync in progress`: 同步正在进行中
   - `Failed to sync emails`: 同步邮件失败