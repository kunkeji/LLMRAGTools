from typing import Dict, Any
from datetime import datetime

from app.core.tasks.registry import task_registry
from app.models.task import Task, TaskStatus, TaskPriority
from app.db.session import SessionLocal
from app.models.email import Email
from app.models.email_tag import EmailTag, EmailTagRelation
from app.utils.email.tag_actions import TagAction

# 创建标签对应操作的任务
def create_tag_operation_task(email_id: int) -> Task:
    """创建标签对应操作的任务"""
    # 获取邮件
    with SessionLocal() as db:
        email = db.query(Email).filter(Email.id == email_id).first()
        if not email:
            raise ValueError(f"邮件不存在: {email_id}")
        # 获取邮件关联的唯一标签
        email_tag_id = db.query(EmailTagRelation).filter(EmailTagRelation.email_id == email_id).first()
        if not email_tag_id:
            raise ValueError(f"邮件标签不存在: {email_id}")
        # 根据标签id获取标签
        tag = db.query(EmailTag).filter(EmailTag.id == email_tag_id.tag_id).first()
        if not tag:
            raise ValueError(f"标签不存在: {email_id}")
        # 获取标签对应的操作
        tag_operation = tag.action_name
        # 创建标签动作任务
        task = Task(
            name=f"标签操作 {email_id}",
            func_name="tag_operation",
            args={"email_id": email_id, "tag_operation": tag_operation},
            status=TaskStatus.PENDING,
            priority=TaskPriority.NORMAL.value,
            scheduled_at=datetime.now(),
        )
        db.add(task)
        db.commit()

@task_registry.register(name="tag_operation")
async def tag_operation(email_id: int, tag_operation: str) -> Dict[str, Any]:
    """标签操作"""
    with SessionLocal() as db:
        email = db.query(Email).filter(Email.id == email_id).first()
        if not email:
            raise ValueError(f"邮件不存在: {email_id}")
        # 根据操作名称获取操作的函数
        if tag_operation == TagAction.NO_OPERATION:     # 无操作
            return {"status": "success"}    
        elif tag_operation == TagAction.MARK_READ:      # 标记已读
            return {"status": "success"}
        elif tag_operation == TagAction.MARK_UNREAD:    # 标记未读
            return {"status": "success"}
        elif tag_operation == TagAction.MARK_IMPORTANT:  # 标记重要
            return {"status": "success"}
        elif tag_operation == TagAction.PRE_REPLY:      # 预回复
            return {"status": "success"}
        elif tag_operation == TagAction.AUTO_REPLY:      # 自动回复
            return {"status": "success"}
        elif tag_operation == TagAction.REMIND:        # 通过微信提醒
            return {"status": "success"}
        elif tag_operation == TagAction.MOVE_TO_TRASH:  # 移动到垃圾箱
            return {"status": "success"}
        elif tag_operation == TagAction.DELETE:        # 删除
            return {"status": "success"}
        


        print(f"标签操作: {email_id}, {tag_operation}")
    return {"status": "success"}