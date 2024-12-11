from typing import Any, Callable, Dict, Optional
from functools import wraps
import asyncio
import logging

logger = logging.getLogger(__name__)

class TaskRegistry:
    """任务注册器"""
    
    def __init__(self):
        self._tasks: Dict[str, Callable] = {}
    
    def register(self, name: str = None, interval_minutes: Optional[int] = None):
        """
        注册任务装饰器
        :param name: 任务名称
        :param interval_minutes: 任务执行间隔（分钟）
        """
        def decorator(func: Callable) -> Callable:
            task_name = name or func.__name__
            
            # 检查是否为异步函数
            is_async = asyncio.iscoroutinefunction(func)
            logger.info(f"注册任务 {task_name}, 原始函数是否为异步: {is_async}")
            
            if is_async:
                @wraps(func)
                async def wrapper(*args, **kwargs):
                    return await func(*args, **kwargs)
            else:
                @wraps(func)
                def wrapper(*args, **kwargs):
                    return func(*args, **kwargs)
            
            # 存储任务元数据
            wrapper._task_meta = {
                'interval_minutes': interval_minutes,
                'is_async': is_async
            }
            
            self._tasks[task_name] = wrapper
            return wrapper
        return decorator
    
    def get_task_func(self, name: str) -> Callable:
        """获取任务函数"""
        return self._tasks.get(name)
    
    def list_tasks(self) -> Dict[str, Callable]:
        """列出所有已注册的任务"""
        return self._tasks
    
    def is_async_task(self, name: str) -> bool:
        """检查任务是否为异步"""
        func = self.get_task_func(name)
        if not func:
            return False
        return getattr(func, '_task_meta', {}).get('is_async', False)

# 全局任务注册器实例
task_registry = TaskRegistry()