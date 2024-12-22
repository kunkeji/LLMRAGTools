# 插件系统文档

## 概述

LLMRAGTools 的插件系统采用模块化设计，允许开发者轻松扩展和定制系统功能。通过插件机制，可以快速集成新的 LLM 模型、添加自定义功能、扩展现有功能等。系统提供了标准的插件接口和完整的生命周期管理。

## 核心特性

1. **模块化设计**
   - 松耦合架构
   - 标准化接口
   - 独立的配置管理

2. **生命周期管理**
   - 插件加载
   - 初始化过程
   - 优雅关闭

3. **扩展点系统**
   - 预定义扩展点
   - 自定义扩展点
   - 钩子机制

4. **配置管理**
   - 插件配置
   - 环境变量
   - 动态配置

## 插件开发

### 1. 基础插件结构

```python
from app.core.plugins import BasePlugin, plugin_registry

class MyPlugin(BasePlugin):
    name = "my_plugin"
    version = "1.0.0"
    description = "这是一个示例插件"
    
    async def initialize(self):
        # 初始化逻辑
        pass
        
    async def shutdown(self):
        # 清理逻辑
        pass
        
    def get_routes(self):
        # 返回插件的路由
        return []
        
    def register_hooks(self):
        # 注册钩子
        pass

# 注册插件
plugin_registry.register(MyPlugin)
```

### 2. 添加路由

```python
from fastapi import APIRouter, Depends
from app.schemas.response import Response

class MyPlugin(BasePlugin):
    def get_routes(self):
        router = APIRouter()
        
        @router.get("/my-plugin/status")
        async def get_status():
            return Response(code=200, data={"status": "ok"})
            
        @router.post("/my-plugin/action")
        async def do_action(data: ActionSchema):
            result = await self.process_action(data)
            return Response(code=200, data=result)
            
        return router
```

### 3. 注册钩子

```python
from app.core.plugins import Hook

class MyPlugin(BasePlugin):
    def register_hooks(self):
        @Hook("before_email_send")
        async def before_send(email):
            # 在发送邮件前的处理
            pass
            
        @Hook("after_email_send")
        async def after_send(email, result):
            # 在发送邮件后的处理
            pass
```

## 插件配置

### 1. 配置文件

```python
# config/plugins/my_plugin.py
config = {
    "enabled": True,
    "settings": {
        "option1": "value1",
        "option2": "value2"
    },
    "api": {
        "base_url": "http://api.example.com",
        "timeout": 30
    }
}
```

### 2. 环境变量

```bash
MY_PLUGIN_ENABLED=true
MY_PLUGIN_API_KEY=xxx
MY_PLUGIN_TIMEOUT=30
```

### 3. 动态配置

```python
class MyPlugin(BasePlugin):
    def __init__(self):
        self.config = self.load_config()
        
    def load_config(self):
        # 加载配置
        config = self.get_config("my_plugin")
        return config
        
    async def update_config(self, new_config):
        # 更新配置
        await self.save_config(new_config)
        self.config = new_config
```

## 扩展点系统

### 1. 预定义扩展点

```python
# 定义扩展点
from app.core.plugins import ExtensionPoint

class EmailProcessor(ExtensionPoint):
    name = "email_processor"
    
    async def process_email(self, email):
        # 处理邮件的默认逻辑
        pass

# 实现扩展点
class MyEmailProcessor(EmailProcessor):
    async def process_email(self, email):
        # 自定义邮件处理逻辑
        pass
```

### 2. 自定义扩展点

```python
class MyExtensionPoint(ExtensionPoint):
    name = "my_extension_point"
    
    def get_implementations(self):
        # 获取所有实现
        return self.get_extensions()
        
    async def execute(self, *args, **kwargs):
        # 执行扩展点逻辑
        implementations = self.get_implementations()
        results = []
        for impl in implementations:
            result = await impl.execute(*args, **kwargs)
            results.append(result)
        return results
```

## 示例插件

### 1. RAG 插件

```python
class RAGPlugin(BasePlugin):
    name = "rag_plugin"
    
    async def initialize(self):
        # 初始化向量数据库
        self.vector_db = await self.setup_vector_db()
        
    async def process_document(self, document):
        # 处理文档
        vectors = await self.vectorize_document(document)
        await self.vector_db.store(vectors)
        
    async def search_similar(self, query, limit=5):
        # 搜索相似文档
        results = await self.vector_db.search(query, limit)
        return results
```

### 2. 自定义 LLM 插件

```python
class CustomLLMPlugin(BasePlugin):
    name = "custom_llm"
    
    def register_provider(self):
        from app.utils.llm.registry import provider_registry
        
        class CustomProvider(BaseLLMProvider):
            async def generate(self, prompt, **kwargs):
                # 实现生成逻辑
                pass
                
        provider_registry.register("custom", CustomProvider)
```

### 3. 邮件处理插件

```python
class EmailProcessorPlugin(BasePlugin):
    name = "email_processor"
    
    def register_hooks(self):
        @Hook("on_email_received")
        async def process_email(email):
            # 处理收到的邮件
            await self.analyze_email(email)
            await self.update_tags(email)
            
    async def analyze_email(self, email):
        # 分析邮件内容
        pass
        
    async def update_tags(self, email):
        # 更新邮件标签
        pass
```

## 最佳实践

1. **插件设计**
   - 保持单一职责
   - 使用标准接口
   - 做好错误处理

2. **配置管理**
   - 使用类型提示
   - 验证配置值
   - 提供默认值

3. **性能考虑**
   - 异步操作
   - 资源管理
   - 缓存策略

4. **测试**
   - 单元测试
   - 集成测试
   - 性能测试

## 常见问题

1. **插件加载失败**
   - 检查依赖项
   - 验证配置
   - 查看错误日志

2. **性能问题**
   - 优化初始化过程
   - 控制资源使用
   - 实现缓存机制

3. **冲突处理**
   - 版本管理
   - 依赖解析
   - 优先级控制 