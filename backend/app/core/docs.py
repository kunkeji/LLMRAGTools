from typing import List, Dict

tags_metadata: List[Dict] = [
    {
        "name": "用户认证",
        "description": """
        用户认证相关接口，包括：
        * 用户注册（需要邮箱验证）
        * 用户登录
        * 重置密码
        * 验证码发送
        """,
    },
    {
        "name": "用户管理",
        "description": """
        用户个人信息管理接口，包括：
        * 获取个人信息
        * 更新个人信息
        * 修改密码
        """,
    },
    {
        "name": "管理认证",
        "description": """
        管理员认证相关接口，包括：
        * 管理员登录
        * 创建管理员（需要超级管理员权限）
        * 管理员信息管理
        """,
    },
    {
        "name": "管理后台",
        "description": """
        系统管理接口，包括：
        * 用户管理（CRUD操作）
        * 系统配置管理
        * 日志查看
        """,
    },
    {
        "name": "system",
        "description": "系统相关接口，如健康���查、系统信息等",
    }
]

api_description: str = """
## Agent Tools API 接口文档

### 接口说明
* 所有接口返回格式统一为：
```json
{
    "code": 200,       // 状态码
    "data": null,      // 数据
    "message": "success" // 消息
}
```
* 除特殊说明外，所有接口都需要在请求头中携带 token：
```
Authorization: Bearer your_token_here
```

### 环境说明
* 开发环境：http://localhost:8111
* 测试环境：http://test-api.example.com
* 生产环境：https://api.example.com

### 错误码说明
* 200: 成功
* 400: 请求参数错误
* 401: 未认证
* 403: 无权限
* 404: 资源不存在
* 500: 服务器内部错误

### 注意事项
1. 所有时间相关字段均为 UTC 时间
2. 文件上传大小限制为 10MB
3. 接口调用频率限制为每分钟 60 次
"""

swagger_ui_parameters = {
    "defaultModelsExpandDepth": -1,  # 隐藏 Models
    "docExpansion": "none",          # 默认折叠所有接口
    "filter": True,                  # 开启搜索功能
    "persistAuthorization": True,    # 保持认证信息
    "syntaxHighlight.theme": "monokai",  # 代码高亮主题
    "tryItOutEnabled": True,         # 启用 Try it out 功能
} 