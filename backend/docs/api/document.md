# 文档管理 API

## 基础信息

- 基础路径: `/api/v1/user/documents`
- 需要认证: 是 (Bearer Token)

## 数据结构

### Document

文档基础信息：

```json
{
    "id": 1,
    "title": "文档标题",
    "content": "文档内容",
    "parent_id": null,
    "path": "/1/",
    "level": 1,
    "sort_order": 1,
    "doc_type": "markdown",
    "creator_id": 1,
    "editor_id": 1,
    "created_at": "2024-01-20T10:00:00Z",
    "updated_at": "2024-01-20T10:00:00Z"
}
```

### DocumentTree

文档树节点：

```json
{
    "id": 1,
    "title": "文档标题",
    "doc_type": "markdown",
    "level": 1,
    "sort_order": 1,
    "has_children": true,
    "children": [
        {
            "id": 2,
            "title": "子文档",
            "doc_type": "markdown",
            "level": 2,
            "sort_order": 1,
            "has_children": false,
            "children": []
        }
    ]
}
```

## API 接口

### 1. 创建文档

```http
POST /documents
```

请求参数：

```json
{
    "title": "文档标题",
    "content": "文档内容",
    "parent_id": null,
    "doc_type": "markdown",
    "sort_order": 1
}
```

参数说明：
- `title`: 文档标题（必填，1-200字符）
- `content`: 文档内容（可选）
- `parent_id`: 父文档ID（可选，为null时创建根文档）
- `doc_type`: 文档类型（可选，默认"markdown"）
- `sort_order`: 排序顺序（可选，默认1）

响应示例：

```json
{
    "code": "200",
    "message": "Success",
    "data": {
        "id": 1,
        "title": "文档标题",
        "content": "文档内容",
        "parent_id": null,
        "path": "/1/",
        "level": 1,
        "sort_order": 1,
        "doc_type": "markdown",
        "creator_id": 1,
        "editor_id": 1,
        "created_at": "2024-01-20T10:00:00Z",
        "updated_at": "2024-01-20T10:00:00Z"
    }
}
```

### 2. 获取文档树

```http
GET /documents/tree
```

查询参数：
- `parent_id`: 父文档ID（可选，默认null获取根文档）
- `max_depth`: 最大深度（可选，默认不限制）

响应示例：

```json
{
    "code": "200",
    "message": "Success",
    "data": [
        {
            "id": 1,
            "title": "文档1",
            "doc_type": "markdown",
            "level": 1,
            "sort_order": 1,
            "has_children": true,
            "children": [
                {
                    "id": 2,
                    "title": "文档1.1",
                    "doc_type": "markdown",
                    "level": 2,
                    "sort_order": 1,
                    "has_children": false,
                    "children": []
                }
            ]
        }
    ]
}
```

### 3. 获取文档详情

```http
GET /documents/{document_id}
```

路径参数：
- `document_id`: 文档ID

响应示例：

```json
{
    "code": "200",
    "message": "Success",
    "data": {
        "id": 1,
        "title": "文档标题",
        "content": "文档内容",
        "parent_id": null,
        "path": "/1/",
        "level": 1,
        "sort_order": 1,
        "doc_type": "markdown",
        "creator_id": 1,
        "editor_id": 1,
        "created_at": "2024-01-20T10:00:00Z",
        "updated_at": "2024-01-20T10:00:00Z"
    }
}
```

### 4. 更新文档

```http
PUT /documents/{document_id}
```

路径参数：
- `document_id`: 文档ID

请求参数：

```json
{
    "title": "新标题",
    "content": "新内容",
    "doc_type": "markdown",
    "sort_order": 2
}
```

参数说明：
- `title`: 文档标题（可选）
- `content`: 文档内容（可选）
- `doc_type`: 文档类型（可选）
- `sort_order`: 排序顺序（可选）

响应示例：

```json
{
    "code": "200",
    "message": "Success",
    "data": {
        "id": 1,
        "title": "新标题",
        "content": "新内容",
        "parent_id": null,
        "path": "/1/",
        "level": 1,
        "sort_order": 2,
        "doc_type": "markdown",
        "creator_id": 1,
        "editor_id": 1,
        "created_at": "2024-01-20T10:00:00Z",
        "updated_at": "2024-01-20T10:00:00Z"
    }
}
```

### 5. 删除文档

```http
DELETE /documents/{document_id}
```

路径参数：
- `document_id`: 文档ID

响应示例：

```json
{
    "code": "200",
    "message": "Success",
    "data": null
}
```

### 6. 搜索文档

```http
GET /documents/search
```

查询参数：
- `keyword`: 搜索关键词（可选，搜索标题和内容）
- `doc_type`: 文档类型（可选）
- `creator_id`: 创建者ID（可选）
- `parent_id`: 父文档ID（可选）
- `skip`: 跳过记录数（可选，默认0）
- `limit`: 返回记录数（可选，默认100）

响应示例：

```json
{
    "code": "200",
    "message": "Success",
    "data": [
        {
            "id": 1,
            "title": "文档标题",
            "content": "文档内容",
            "parent_id": null,
            "path": "/1/",
            "level": 1,
            "sort_order": 1,
            "doc_type": "markdown",
            "creator_id": 1,
            "editor_id": 1,
            "created_at": "2024-01-20T10:00:00Z",
            "updated_at": "2024-01-20T10:00:00Z"
        }
    ]
}
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限访问 |
| 404 | 文档不存在 |
| 500 | 服务器内部错误 |

## 注意事项

1. 所有接口都需要用户认证
2. 删除文档会同时删除其所有子文档
3. 文档路径格式为：/1/2/3/，其中的数字为文档ID
4. 文档类型目前支持：markdown、rich_text
5. 排序顺序越小越靠前