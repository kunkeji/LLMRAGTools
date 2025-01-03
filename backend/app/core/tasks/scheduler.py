import time
import logging
import asyncio
import inspect
from datetime import datetime, timedelta
from threading import Thread, current_thread
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.task import Task, TaskStatus, TaskPriority
from app.core.tasks.registry import task_registry
from app.core.config import settings

logger = logging.getLogger(__name__)

class TaskSchedulerConfig:
    """任务调度器配置"""
    
    def __init__(
        self,
        max_workers: int = settings.TASK_SCHEDULER_MAX_WORKERS,
        poll_interval: int = settings.TASK_SCHEDULER_POLL_INTERVAL,
        batch_size: int = settings.TASK_SCHEDULER_BATCH_SIZE,
        max_retries: int = settings.TASK_SCHEDULER_MAX_RETRIES,
        task_timeout: int = settings.TASK_SCHEDULER_TASK_TIMEOUT,
        retry_delay: int = settings.TASK_SCHEDULER_RETRY_DELAY
    ):
        self.max_workers = max_workers  # 最大工作线程数
        self.poll_interval = poll_interval  # 轮询间隔（秒）
        self.batch_size = batch_size  # 每批获取任务数
        self.max_retries = max_retries  # 最大重试次数
        self.task_timeout = task_timeout  # 任务超时时间（秒）
        self.retry_delay = retry_delay  # 重试延迟（秒）

class TaskSchedulerStats:
    """任务调度器统计信息"""
    
    def __init__(self):
        self.total_tasks = 0  # 总任务数
        self.completed_tasks = 0  # 已完成任务数
        self.failed_tasks = 0  # 失败任务数
        self.active_threads = 0  # 活动线程数
        self.queue_size = 0  # 队列大小
        self.avg_execution_time = 0  # 平均执行时间
        self.last_poll_time = None  # 最后轮询时间
        self.last_task_time = None  # 最后任务执行时间

class TaskScheduler:
    """任务调度器"""
    
    def __init__(self, config: TaskSchedulerConfig = None):
        self.config = config or TaskSchedulerConfig()
        self.pool = ThreadPoolExecutor(max_workers=self.config.max_workers)
        self.running = False
        self._thread = None
        self.stats = TaskSchedulerStats()
        
        # 检查已注册的任务
        tasks = task_registry.list_tasks()
        if not tasks:
            logger.warning("没有找到已注册的任务！请确保在启动调度器前已导入所有任务模块。")
        else:
            for name, func in tasks.items():
                is_async = task_registry.is_async_task(name)
                logger.info(f"发现任务: {name}, 是否为异步: {is_async}")
    
    def start(self):
        """启动调度器"""
        if self._thread is not None:
            logger.warning("调度器已经在运行")
            return
        
        # 再次检查已注册的任务
        tasks = task_registry.list_tasks()
        if not tasks:
            logger.error("没有找到已注册的任务！调度器将不会启动。")
            return
            
        self.running = True
        self._thread = Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()
        logger.info(f"任务调度器已启动，已注册任务：{list(tasks.keys())}")
    
    def stop(self):
        """停止调度器"""
        self.running = False
        if self._thread is not None:
            self._thread.join()
            self._thread = None
        self.pool.shutdown(wait=True)
        logger.info("任务调度器已停止")
    
    def update_stats(self):
        """更新统计信息"""
        self.stats.active_threads = len(self.pool._threads)
        self.stats.queue_size = self.pool._work_queue.qsize()
        self.stats.last_poll_time = datetime.now()
    
    def _get_pending_tasks(self, db: Session) -> list[Task]:
        """获取待执行的任务"""
        return (
            db.query(Task)
            .filter(
                Task.status == TaskStatus.PENDING,
                Task.scheduled_at <= datetime.now(),
                Task.deleted_at.is_(None)
            )
            .order_by(Task.priority.desc(), Task.scheduled_at.asc())
            .limit(self.config.batch_size)
            .all()
        )
    
    def _reschedule_task(self, db: Session, task: Task):
        """重新调度任务"""
        try:
            # 获取任务的元数据
            method = task_registry.get_task_func(task.func_name)
            if not method:
                logger.error(f"重新调度任务时未找到方法: {task.func_name}")
                return
                
            task_meta = getattr(method, '_task_meta', {})
            interval_minutes = task_meta.get('interval_minutes')
            logger.debug(f"任务 {task.id} 的元数据: {task_meta}")
            
            if interval_minutes:
                # 如果任务有间隔时间，创建下一次执行的任务
                next_run = datetime.now() + timedelta(minutes=interval_minutes)
                new_task = Task(
                    name=task.name,
                    func_name=task.func_name,
                    args=task.args,
                    status=TaskStatus.PENDING,
                    priority=task.priority,
                    scheduled_at=next_run,
                    max_retries=self.config.max_retries,
                    timeout=self.config.task_timeout
                )
                db.add(new_task)
                db.commit()
                logger.info(f"任务 {task.id} 已重新调度，下次执行时间: {next_run}")
        except Exception as e:
            logger.exception(f"重新调度任务 {task.id} 时发生错误")
    
    async def _execute_task_async(self, task_id: int):
        """异步执行任务"""
        logger.info(f"开始异步执行任务 {task_id}, 线程ID: {current_thread().ident}")
        start_time = time.time()
        
        with SessionLocal() as db:
            task = db.query(Task).get(task_id)
            if not task:
                logger.error(f"任务不存在: {task_id}")
                return
            
            try:
                # 更新任务状态为执行中
                task.status = TaskStatus.RUNNING
                task.started_at = datetime.now()
                db.commit()
                
                # 获取任务方法
                method = task_registry.get_task_func(task.func_name)
                if not method:
                    raise ValueError(f"未找到任务方法: {task.func_name}，已注册的任务：{list(task_registry.list_tasks().keys())}")
                
                is_async = task_registry.is_async_task(task.func_name)
                logger.info(f"准备执行任务 {task_id}, 方法: {task.func_name}, "
                          f"是否为异步: {is_async}, "
                          f"是否为生成器: {inspect.isgeneratorfunction(method)}, "
                          f"方法类型: {type(method)}")
                
                # 执行任务
                try:
                    if is_async:
                        logger.info(f"开始执行异步任务 {task_id}")
                        result = await method(**(task.args or {}))
                        logger.info(f"异步任务 {task_id} 执行完成")
                    else:
                        logger.info(f"开始执行同步任务 {task_id}")
                        result = method(**(task.args or {}))
                        logger.info(f"同步任务 {task_id} 执行完成")
                except Exception as e:
                    logger.exception(f"执行任务 {task_id} 的方法时发生错误")
                    raise

                execution_time = time.time() - start_time
                
                # 更新任务状态为完成
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now()
                task.result = {
                    "result": result if isinstance(result, (dict, list)) else str(result),
                    "execution_time": execution_time
                }
                db.commit()
                
                # 更新统计信息
                self.stats.completed_tasks += 1
                self.stats.avg_execution_time = (
                    (self.stats.avg_execution_time * (self.stats.completed_tasks - 1) + execution_time)
                    / self.stats.completed_tasks
                )
                self.stats.last_task_time = datetime.now()
                
                # 重新调度任务（如果需要）
                self._reschedule_task(db, task)
                
                logger.info(f"任务 {task_id} 执行成功")
                
            except Exception as e:
                logger.exception(f"任务 {task_id} 执行失败")
                
                # 处理任务失败
                task.retry_count += 1
                if task.retry_count >= self.config.max_retries:
                    task.status = TaskStatus.FAILED
                    self.stats.failed_tasks += 1
                else:
                    task.status = TaskStatus.PENDING
                    # 添加重试延迟
                    task.scheduled_at = datetime.now() + timedelta(seconds=self.config.retry_delay)
                
                task.error = str(e)
                db.commit()
    
    def _execute_task(self, task_id: int):
        """执行任务的包装方法"""
        logger.info(f"开始执行任务 {task_id}, 线程ID: {current_thread().ident}")
        
        async def run_task():
            try:
                logger.info(f"进入异步任务包装器 run_task, 任务ID: {task_id}")
                await self._execute_task_async(task_id)
                logger.info(f"异步任务包装器 run_task 完成, 任务ID: {task_id}")
            except Exception as e:
                logger.exception(f"执行任务 {task_id} 时发生错误")
        
        # 创建新的事件循环
        try:
            logger.info(f"为任务 {task_id} 创建新的事件循环")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # 运行异步任务
            logger.info(f"开始运行任务 {task_id} 的事件循环")
            loop.run_until_complete(run_task())
            logger.info(f"任务 {task_id} 的事件循环运行完成")
        except Exception as e:
            logger.exception(f"任务 {task_id} 的事件循环执行出错")
        finally:
            logger.info(f"关闭任务 {task_id} 的事件循环")
            loop.close()
    
    def _run(self):
        """主循环"""
        logger.info(f"调度器主循环启动, 线程ID: {current_thread().ident}")
        
        while self.running:
            try:
                with SessionLocal() as db:
                    # 获取待执行的任务
                    tasks = self._get_pending_tasks(db)
                    if tasks:
                        logger.info(f"找到 {len(tasks)} 个待执行的任务")
                        # 分配任务到线程池
                        for task in tasks:
                            logger.info(f"提交任务到线程池: {task.id} - {task.name}")
                            self.pool.submit(self._execute_task, task.id)
                            self.stats.total_tasks += 1
                    
                    # 更新统计信息
                    self.update_stats()
                    
                    # 无任务时休眠
                    time.sleep(self.config.poll_interval)
            except Exception as e:
                logger.exception(f"调度器错误: {e}")
                time.sleep(self.config.poll_interval)

# 全局调度器实例
scheduler = TaskScheduler() 