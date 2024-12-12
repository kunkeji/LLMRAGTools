from datetime import datetime,timedelta
import logging
from sqlalchemy import text
from app.core.tasks.registry import task_registry
from app.utils.logger import logger_instance
from app.models.log import LogType
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.email_account import EmailAccount
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)

def create_sync_task(account_id: int) -> Task:
    try:
        with SessionLocal() as db:
            account = db.query(EmailAccount).filter(
                EmailAccount.id == account_id,
                EmailAccount.deleted_at.is_(None)
            ).first()
            if not account:
                raise ValueError(f"邮件账户不存在: {account_id}")
            
            # 检查是否已存在正在执行的同步任务TaskStatus.PENDING, 
            existing_task = (
                db.query(Task)
                .filter(
                    Task.func_name == "sync_email_account",
                    Task.status.in_([TaskStatus.RUNNING, TaskStatus.PENDING]),
                    text(f"JSON_EXTRACT(args, '$.account_id') = {account_id}"),
                    Task.deleted_at.is_(None)
                )
                .first()
            )
            # 如果任务状态是队列中切下次同步时间大于当前时间则更改下次同步时间为当前时间
            if existing_task and existing_task.status == TaskStatus.PENDING and existing_task.scheduled_at > datetime.now():
                existing_task.scheduled_at = datetime.now()
                db.commit()
                db.refresh(existing_task)
                return existing_task
            
            if existing_task:
                logger_instance.warning(
                    message="已存在正在执行的同步任务",
                    module="tasks",
                    function="create_sync_task",
                    type=LogType.SYSTEM,
                    details={
                        "account_id": account_id,
                        "task_id": existing_task.id
                    }
                )
                return existing_task
            
            
            
            # 创建新任务
            task = Task(
                name=f"同步邮件账户 {account_id}",
                func_name="sync_email_account",
                args={"account_id": account_id},
                status=TaskStatus.PENDING,
                priority=TaskPriority.NORMAL.value,
                scheduled_at=datetime.now(),  # 立即执行
                max_retries=3,
                timeout=3600  # 1小时超时
            )
            
            db.add(task)
            
            # 更新账户同步状态
            account.last_sync_time = datetime.now()
            account.sync_status = "PENDING"  # 设置为等待中
            
            db.commit()
            db.refresh(task)
            
            logger_instance.info(
                message="邮件同步任务创建成功",
                module="tasks",
                function="create_sync_task",
                type=LogType.SYSTEM,
                details={
                    "account_id": account_id,
                    "task_id": task.id
                }
            )
            
            return task
            
    except Exception as e:
        logger_instance.error(
            message=f"创建邮件同步任务失败: {str(e)}",
            module="tasks",
            function="create_sync_task",
            type=LogType.SYSTEM,
            error_type=type(e).__name__,
            error_stack=str(e),
            details={"account_id": account_id}
        )
        raise

@task_registry.register(name="sync_email_account")
async def sync_email_account(account_id: int):
    """
    邮件同步任务的占位实现
    后续将实现完整的邮件同步功能
    
    Args:
        account_id: 邮件账户ID
    """
    try:
        logger_instance.info(
            message="开始执行邮件同步任务",
            module="tasks",
            function="sync_email_account",
            type=LogType.SYSTEM,
            details={"account_id": account_id}
        )
        
        with SessionLocal() as db:
            # 获取邮件账户信息
            account = db.query(EmailAccount).filter(
                EmailAccount.id == account_id,
                EmailAccount.deleted_at.is_(None)
            ).first()
            
            if not account:
                raise ValueError(f"邮件账户不存在: {account_id}")
            
            # 这里是占位的任务逻辑
            # 后续将实现实际的邮件同步功能
            
            # 更新账户同步状态
            account.last_sync_time = datetime.now()
            account.sync_status = "completed"  # 设置为同步完成
            
            # 如果开启了自动同步，创建下一次的同步任务
            next_sync_time = datetime.now() + timedelta(minutes=account.sync_interval)
            next_task = Task(
                name=f"同步邮件账户 {account_id}",
                func_name="sync_email_account",
                args={"account_id": account_id},
                status=TaskStatus.PENDING,
                priority=TaskPriority.NORMAL.value,
                scheduled_at=next_sync_time,
                max_retries=3,
                timeout=3600
            )
            db.add(next_task)
            
            db.commit()
            
            logger_instance.info(
                message="邮件同步任务执行完成",
                module="tasks",
                function="sync_email_account",
                type=LogType.SYSTEM,
                details={
                    "account_id": account_id,
                    "next_sync_time": next_sync_time.isoformat()
                }
            )
            
        return {
            "status": "success",
            "message": "邮件同步任务执行完成",
            "account_id": account_id,
            "sync_time": datetime.now().isoformat(),
            "next_sync_time": next_sync_time.isoformat() 
        }
        
    except Exception as e:
        # 更新账户同步状态为失败
        with SessionLocal() as db:
            account = db.query(EmailAccount).filter(
                EmailAccount.id == account_id,
                EmailAccount.deleted_at.is_(None)
            ).first()
            if account:
                account.sync_status = "failed"
                db.commit()
        
        logger_instance.error(
            message=f"邮件同步任务执行出错: {str(e)}",
            module="tasks",
            function="sync_email_account",
            type=LogType.SYSTEM,
            error_type=type(e).__name__,
            error_stack=str(e),
            details={"account_id": account_id}
        )
        raise