# 任务系统文档

## 概述

LLMRAGTools 的任务系统提供了一个强大的异步任务处理框架，支持定时任务、周期任务和一次性任务的管理和执行。系统基于装饰器模式实现，使用简单直观，同时提供了完善的监控和错误处理机制。

## 核心功能

1. **任务注册与管理**
   - 基于装饰器的任务注册
   - 支持多种任务类型
   - 灵活的任务配置

2. **调度功能**
   - 定时任务执行
   - 周期性任务
   - 动态任务调度

3. **执行控制**
   - 并发控制
   - 任务优先级
   - 超时处理

4. **监控和日志**
   - 任务执行状态
   - 性能监控
   - 错误追踪

## 使用方法

### 1. 基础任务注册

```python
from app.core.tasks import task_registry

# 注册普通任务
@task_registry.register(name="process_document")
async def process_document(doc_id: str):
    # 处理文档的逻辑
    pass

# 注册定时任务
@task_registry.register(
    name="daily_report",
    interval_minutes=1440,  # 每天执行一次
    max_instances=1  # 最大同时运行实例数
)
async def generate_daily_report():
    # 生成报告的逻辑
    pass

# 注册周期任务
@task_registry.register(
    name="sync_emails",
    interval_minutes=15,  # 每15分钟执行一次
    max_retries=3  # 最大重试次数
)
async def sync_emails():
    # 同步邮件的逻辑
    pass
```

### 2. 手动创建任务

```python
from app.models.task import Task
from datetime import datetime, timedelta

# 创建一次性任务
task = Task(
    name="one_time_task",
    func_name="process_document",
    params={"doc_id": "123"},
    scheduled_at=datetime.now() + timedelta(hours=1)
)
await task.save()

# 创建周期任务
task = Task(
    name="periodic_task",
    func_name="sync_emails",
    interval_minutes=30,
    next_run_at=datetime.now()
)
await task.save()
```

### 3. 任务控制

```python
# 暂停任务
await task.pause()

# 恢复任务
await task.resume()

# 取消任务
await task.cancel()

# 立即执行任务
await task.execute_now()
```

## 任务配置

### 1. 基础配置

```python
TASK_CONFIG = {
    "max_workers": 4,           # 最大工作线程数
    "default_timeout": 3600,    # 默认超时时间（秒）
    "max_retries": 3,          # 默认最大重试次数
    "retry_delay": 300         # 重试延迟（秒）
}
```

### 2. 任务特定配置

```python
@task_registry.register(
    name="custom_task",
    config={
        "timeout": 1800,        # 30分钟超时
        "max_retries": 5,       # 最多重试5次
        "retry_delay": 600,     # 重试间隔10分钟
        "priority": 1,          # 优先级（越小越高）
        "max_instances": 2      # 最大同时运行实例数
    }
)
async def custom_task():
    pass
```

## 错误处理

### 1. 重试机制

```python
from app.core.tasks.retry import retry_with_backoff

@retry_with_backoff(max_retries=3)
async def task_with_retry():
    # 可能失败的任务逻辑
    pass
```

### 2. 错误回调

```python
@task_registry.register(
    name="task_with_callback",
    on_failure=handle_failure
)
async def task_with_callback():
    pass

async def handle_failure(task, error):
    # 处理任务失败的逻辑
    pass
```

## 监控和日志

### 1. 任务状态监控

```python
from app.core.tasks.monitor import TaskMonitor

# 获取任务状态
status = await TaskMonitor.get_task_status(task_id)

# 获取任务统计
stats = await TaskMonitor.get_statistics()
```

### 2. 性能指标

```python
from app.core.tasks.metrics import track_task_performance

@track_task_performance
async def monitored_task():
    # 任务逻辑
    pass
```

## 最佳实��

1. **任务设计**
   - 保持任务原子性
   - 实现幂等性
   - 合理设置超时时间

2. **错误处理**
   - 实现合适的重试策略
   - 记录详细的错误信息
   - 设置错误通知机制

3. **性能优化**
   - 控制并发数量
   - 合理设置任务优先级
   - 避免长时间运行的任务

4. **监控和维护**
   - 定期检查任务状态
   - 清理过期任务
   - 分析性能指标

## 示例场景

### 1. 邮件同步任务

```python
@task_registry.register(
    name="sync_emails",
    interval_minutes=15,
    max_retries=3
)
async def sync_emails():
    try:
        accounts = await get_active_email_accounts()
        for account in accounts:
            await sync_account_emails(account)
    except Exception as e:
        logger.error(f"邮件同步失败: {str(e)}")
        raise
```

### 2. 文档处理任务

```python
@task_registry.register(
    name="process_document",
    config={
        "timeout": 1800,
        "max_retries": 3
    }
)
async def process_document(doc_id: str):
    try:
        doc = await get_document(doc_id)
        await process_content(doc)
        await update_document_status(doc_id, "processed")
    except DocumentNotFound:
        logger.error(f"文档不存在: {doc_id}")
    except ProcessingError as e:
        logger.error(f"处理失败: {str(e)}")
        raise
```

### 3. 定时报告生成

```python
@task_registry.register(
    name="generate_report",
    schedule="0 0 * * *",  # 每天零点执行
    max_instances=1
)
async def generate_daily_report():
    try:
        data = await collect_daily_data()
        report = await generate_report(data)
        await send_report_email(report)
    except Exception as e:
        logger.error(f"报告生成失败: {str(e)}")
        await notify_admin("报告生成失败", str(e))
        raise
```

## 常见问题

1. **任务卡死**
   - 设置合适的超时时间
   - 实现任务心跳机制
   - 使用监控工具检测

2. **重复执行**
   - 实现任务锁机制
   - 检查任务唯一性
   - 使用幂等设计

3. **资源占用**
   - 控制并发数量
   - 合理设置任务间隔
   - 监控系统资源 