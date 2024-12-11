from datetime import datetime, timedelta
import logging
import asyncio
from threading import current_thread
from app.core.tasks.registry import task_registry
from app.utils.email import email_client
from app.db.session import SessionLocal
from app.models.task import Task, TaskPriority, TaskStatus
from app.utils.logger import logger_instance
from app.models.log import LogType

logger = logging.getLogger(__name__)

# 调试语句
logger_instance.info(
    message="正在注册任务: send_test_email",
    module="tasks",
    function="register_task",
    type=LogType.SYSTEM
)

@task_registry.register(name="send_test_email", interval_minutes=1)
async def send_test_email():
    """发送测试邮件"""
    try:
        thread_id = current_thread().ident
        task_id = asyncio.current_task().get_name() if asyncio.current_task() else None
        logger_instance.info(
            message=f"开始执行发送测试邮件任务",
            module="tasks",
            function="send_test_email",
            type=LogType.SYSTEM,
            details={
                "thread_id": thread_id,
                "task_id": task_id
            }
        )
        
        # 检查当前事件循环
        try:
            loop = asyncio.get_running_loop()
            logger_instance.debug(
                message=f"当前事件循环状态",
                module="tasks",
                function="send_test_email",
                type=LogType.SYSTEM,
                details={
                    "loop": str(loop),
                    "is_running": loop.is_running()
                }
            )
        except RuntimeError:
            logger_instance.warning(
                message="没有正在运行的事件循环",
                module="tasks",
                function="send_test_email",
                type=LogType.SYSTEM
            )
        
        # 构建邮件内容
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subject = f"测试邮件 - {current_time}"
        template_data = {
            "time": current_time,
            "message": "这是一封测试邮件"
        }
        
        logger_instance.info(
            message=f"准备发送邮件",
            module="tasks",
            function="send_test_email",
            type=LogType.SYSTEM,
            details={
                "subject": subject,
                "template_data": template_data
            }
        )
        
        # 发送邮件
        await email_client.send_email(
            to_email="1346699791@qq.com",
            subject=subject,
            template_name="test_email.html",
            template_data=template_data
        )
        
        logger_instance.info(
            message="测试邮件发送成功",
            module="tasks",
            function="send_test_email",
            type=LogType.SYSTEM
        )
        return "邮件发送成功"
    except Exception as e:
        logger_instance.error(
            message=f"发送测试邮件时发生错误: {str(e)}",
            module="tasks",
            function="send_test_email",
            type=LogType.SYSTEM,
            error_type=type(e).__name__,
            error_stack=str(e)
        )
        raise

def create_periodic_email_task():
    """创建定期发送邮件的任务"""
    try:
        logger_instance.info(
            message="开始创建定期发送邮件任务",
            module="tasks",
            function="create_periodic_email_task",
            type=LogType.SYSTEM
        )
        
        with SessionLocal() as db:
            # 创建一个一分钟后执行的任务
            next_run = datetime.utcnow() + timedelta(minutes=1)
            logger_instance.debug(
                message=f"计划执行时间",
                module="tasks",
                function="create_periodic_email_task",
                type=LogType.SYSTEM,
                details={"next_run": next_run.isoformat()}
            )
            
            # 检查是否已存在相同的任务
            existing_task = (
                db.query(Task)
                .filter(
                    Task.func_name == "send_test_email",
                    Task.deleted_at.is_(None),
                    Task.status.in_([TaskStatus.PENDING, TaskStatus.RUNNING])
                )
                .first()
            )
            
            if existing_task:
                logger_instance.info(
                    message=f"定期发送邮件的任务已存在",
                    module="tasks",
                    function="create_periodic_email_task",
                    type=LogType.SYSTEM,
                    details={"task_id": existing_task.id}
                )
                return existing_task
            
            task = Task(
                name="定期发送测试邮件",
                func_name="send_test_email",
                args={},
                status=TaskStatus.PENDING,
                priority=TaskPriority.NORMAL.value,
                scheduled_at=next_run
            )
            
            db.add(task)
            db.commit()
            logger_instance.info(
                message=f"已创建定期发送邮件任务",
                module="tasks",
                function="create_periodic_email_task",
                type=LogType.SYSTEM,
                details={"task_id": task.id}
            )
            
            return task
    except Exception as e:
        logger_instance.error(
            message=f"创建定期发送邮件任务时发生错误: {str(e)}",
            module="tasks",
            function="create_periodic_email_task",
            type=LogType.SYSTEM,
            error_type=type(e).__name__,
            error_stack=str(e)
        )
        raise