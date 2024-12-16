"""
邮件同步任务模块
"""
from datetime import datetime, timedelta
import logging
from typing import Dict, Any

from sqlalchemy import text
from app.core.tasks.registry import task_registry
from app.utils.logger import logger_instance
from app.models.log import LogType
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.email_account import EmailAccount
from app.models.email import Email, EmailAttachment
from app.crud.email import crud_email, crud_email_sync_log
from app.schemas.email import EmailCreate, EmailSyncLogCreate, EmailSyncLogUpdate
from app.db.session import SessionLocal
from app.utils.email.imap_client import IMAPClient
from app.utils.email.parser import (
    parse_email_date,
    parse_email_address,
    get_email_body,
    get_attachment_info,
    parse_email_addresses,
    decode_mime_words
)
from app.core.tasks.email_tag import create_tag_task

logger = logging.getLogger(__name__)
def create_sync_task(account_id: int) -> Task:
    try:
        # 使用SessionLocal上下文管理器进行数据库会话管理
        with SessionLocal() as db:
            # 查询邮件账户
            account = db.query(EmailAccount).filter(
                EmailAccount.id == account_id,
                EmailAccount.deleted_at.is_(None)
            ).first()
            # 如果账户不存在，则抛出异常
            if not account:
                raise ValueError(f"邮件账户不存在: {account_id}")
            
            # 检查是否已存在正在执行的同步任务
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
            
            # 如果任务状态是队列中且下次同步时间大于当前时间则更改下次同步时间为当前时间
            if existing_task and existing_task.status == TaskStatus.PENDING and existing_task.scheduled_at > datetime.now():
                existing_task.scheduled_at = datetime.now()
                db.commit()
                db.refresh(existing_task)
                return existing_task
            
            # 如果已存在任务，则记录警告日志并返回现有任务
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
                scheduled_at=datetime.now(),
                max_retries=3,
                timeout=3600
            )
            
            # 将新任务添加到数据库
            db.add(task)
            # 更新账户同步状态为"PENDING"
            account.sync_status = "PENDING"
            
            # 提交数据库会话
            db.commit()
            # 刷新任务对象以反映数据库中的最新状态
            db.refresh(task)
            
            # 记录信息日志
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
            
            # 返回新创建的任务
            return task
            
    except Exception as e:
        # 记录错误日志
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
async def sync_email_account(account_id: int) -> Dict[str, Any]:
    """执行邮件同步任务"""
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
                
            # 创建同步日志
            sync_log = crud_email_sync_log.create(
                db,
                obj_in=EmailSyncLogCreate(
                    account_id=account_id,
                    start_time=datetime.now(),
                    status="RUNNING",
                    sync_type="INCREMENT" if account.last_sync_time else "FULL"
                )
            )
            
            try:
                # 使用IMAP客户端
                with IMAPClient(account.imap_host, account.imap_port, account.use_ssl) as imap:
                    imap.connect(account.email_address, account.auth_token)
                    imap.select_folder("INBOX")
                    
                    # 获取邮件列表
                    emails = imap.get_emails_since(account.last_sync_time)
                    
                    total_emails = len(emails)
                    new_emails = 0
                    updated_emails = 0
                    
                    # 更新同步日志
                    crud_email_sync_log.update(
                        db,
                        db_obj=sync_log,
                        obj_in=EmailSyncLogUpdate(
                            total_emails=total_emails
                        )
                    )
                    
                    # 处理每封邮件
                    for email_body, msg in emails:
                        try:
                            # 解析邮件基本信息
                            message_id = msg.get('Message-ID', '')
                            subject = decode_mime_words(msg.get('Subject', ''))
                            from_name, from_address = parse_email_address(msg.get('From', ''))
                            
                            # 解析日期
                            date_str = msg.get('Date')
                            date = parse_email_date(date_str) if date_str else datetime.now()
                            
                            # 解析收件人信息
                            to_list = parse_email_addresses(msg.get_all('To', []))
                            cc_list = parse_email_addresses(msg.get_all('Cc', []) or [])
                            bcc_list = parse_email_addresses(msg.get_all('Bcc', []) or [])
                            # 获取邮件内容
                            content, content_type = get_email_body(msg)
                            # 检查是否已存在该邮件
                            existing_email = crud_email.get_by_message_id(db, account_id=account_id, message_id=message_id)
                            
                            if existing_email:
                                # 更新现有邮件
                                crud_email.update(
                                    db,
                                    db_obj=existing_email,
                                    obj_in={
                                        "subject": decode_mime_words(subject),
                                        "content": content,
                                        "content_type": content_type
                                    }
                                )
                                updated_emails += 1
                                # 创建标签同步任务
                                create_tag_task(message_id);
                            else:
                                # 创建新邮件
                                email_obj = crud_email.create(
                                    db,
                                    obj_in=EmailCreate(
                                        account_id=account_id,
                                        message_id=message_id,
                                        subject=decode_mime_words(subject),
                                        from_address=from_address,
                                        from_name=from_name,
                                        to_address=to_list,
                                        cc_address=cc_list,
                                        bcc_address=bcc_list,
                                        date=date,
                                        content_type=content_type,
                                        content=content,
                                        raw_content=email_body.decode(),
                                        has_attachments=False,
                                        size=len(email_body)
                                    )
                                )
                                
                                # 处理附件
                                if msg.is_multipart():
                                    for part in msg.walk():
                                        if part.get_content_maintype() == 'multipart':
                                            continue
                                        if part.get_content_maintype() != 'text':
                                            attachment = get_attachment_info(part, email_obj.id)
                                            if attachment:
                                                email_obj.has_attachments = True
                                                db.add(EmailAttachment(**attachment.dict()))
                                
                                new_emails += 1
                                # 创建标签同步任务
                                create_tag_task(message_id);
                            
                            # 定期提交事务和更新同步状态
                            if (new_emails + updated_emails) % 10 == 0:
                                db.commit()
                                crud_email_sync_log.update_sync_stats(
                                    db,
                                    sync_id=sync_log.id,
                                    new_emails=new_emails,
                                    updated_emails=updated_emails
                                )
                            
                            
                        except Exception as e:
                            logger.error(f"处理邮件失败: {str(e)}")
                            continue
                    
                    # 更新同步完成状态
                    crud_email_sync_log.update(
                        db,
                        db_obj=sync_log,
                        obj_in=EmailSyncLogUpdate(
                            status="COMPLETED",
                            end_time=datetime.now(),
                            new_emails=new_emails,
                            updated_emails=updated_emails
                        )
                    )
                    # 更新账户同步状态
                    account.last_sync_time = datetime.now()
                    account.sync_status = "COMPLETED"
                    account.total_emails = db.query(Email).filter(Email.account_id == account_id).count()
                    account.unread_emails = db.query(Email).filter(
                        Email.account_id == account_id,
                        Email.is_read == False
                    ).count()
                    
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
                            "total_emails": total_emails,
                            "new_emails": new_emails,
                            "updated_emails": updated_emails,
                            "next_sync_time": next_sync_time.isoformat()
                        }
                    )
                    
                    return {
                        "status": "success",
                        "message": "邮件同步任务执行完成",
                        "account_id": account_id,
                        "total_emails": total_emails,
                        "new_emails": new_emails,
                        "updated_emails": updated_emails,
                        "sync_time": datetime.now().isoformat(),
                        "next_sync_time": next_sync_time.isoformat()
                    }
                    
            except Exception as e:
                # 更新同步失败状态
                crud_email_sync_log.update(
                    db,
                    db_obj=sync_log,
                    obj_in=EmailSyncLogUpdate(
                        status="FAILED",
                        end_time=datetime.now(),
                        error_message=str(e)
                    )
                )
                raise
                
    except Exception as e:
        # 更新账户同步状态为失败
        with SessionLocal() as db:
            account = db.query(EmailAccount).filter(
                EmailAccount.id == account_id,
                EmailAccount.deleted_at.is_(None)
            ).first()
            if account:
                account.sync_status = "FAILED"
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