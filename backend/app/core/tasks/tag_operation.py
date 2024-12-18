from typing import Dict, Any
from datetime import datetime

from app.core.tasks.registry import task_registry
from app.models.task import Task, TaskStatus, TaskPriority
from app.db.session import SessionLocal
from app.models.email import Email
from app.crud.email import crud_email
from app.models.email_tag import EmailTag, EmailTagRelation
from app.utils.email.tag_actions import TagAction
from app.models.llm_feature_mapping import LLMFeatureMapping
from app.utils.llm.client import LLMClient
from app.crud.email_outbox import email_outbox
from app.schemas.email_outbox import EmailOutbox, EmailOutboxCreate

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
            crud_email.mark_as_read(db=db, email_id=email_id, is_read=True)
            return {"status": "success"}
        elif tag_operation == TagAction.MARK_UNREAD:    # 标记未读
            crud_email.mark_as_read(db=db, email_id=email_id, is_read=False)
            return {"status": "success"}
        elif tag_operation == TagAction.MARK_IMPORTANT:  # 标记重要
            crud_email.mark_as_flagged(db=db, email_id=email_id, is_flagged=True)
            return {"status": "success"}
        elif tag_operation == TagAction.PRE_REPLY:      # 预回复
            await pre_reply(email_id=email_id)
            return {"status": "success"}
        elif tag_operation == TagAction.AUTO_REPLY:      # 自动回复
            await pre_reply(email_id=email_id,auto_reply=True)
            return {"status": "success"}
        elif tag_operation == TagAction.REMIND:        # 通过微提醒

            return {"status": "success"}
        elif tag_operation == TagAction.MOVE_TO_TRASH:  # 移动到垃圾箱

            return {"status": "success"}
        elif tag_operation == TagAction.DELETE:        # 删除
            crud_email.remove(db=db, id=email_id)
            return {"status": "success"}
        print(f"标签操作: {email_id}, {tag_operation}")
    return {"status": "success"}



# 邮件预回复方法
async def pre_reply(email_id: int,auto_reply: bool = False) -> Dict[str, Any]:
    """邮件预回复"""
    with SessionLocal() as db:
        email = db.query(Email).filter(Email.id == email_id).first()
        if not email:
            raise ValueError(f"邮件不存在: {email_id}")
            
        # 获取账户和用户信息
        account = email.account
        user = account.user
        
        # 获取 EMAIL_REPLY 功能的映射信息
        feature_mapping = db.query(LLMFeatureMapping).filter(
            LLMFeatureMapping.user_id == user.id,
            LLMFeatureMapping.feature_type == "EMAIL_REPLY"
        ).first()
        
        if feature_mapping:
            # 获取关联的渠道信息
            channel = feature_mapping.channel
            model_type = channel.model_type
            model = channel.model
            api_key = channel.api_key
            prompt = feature_mapping.prompt_template
            # 调用llm，生成预回复邮件
            llm_response = LLMClient.generate(
                prompt=prompt,
                message="邮件内容："+email.content,
                api_key=api_key,
                provider=model_type,
                model=model
            )
            print(f"预回复邮件: {llm_response}")
            # 创建预回复邮件的输入数据
            email_in = EmailOutboxCreate(
                subject=f"RE: {email.subject}",
                content=llm_response,
                recipients=email.from_address,
                content_type="html",
                account_id=email.account_id,
                reply_type="pre_reply",
                reply_to_email_id=email_id
            )
            # 如果是自动回复则直接发送
            if auto_reply:
                email_in.reply_type = "auto_reply"
            else:
                email_in.reply_type = "pre_reply"

            email = email_outbox.create_email(
                db=db,
                obj_in=email_in,
                user_id=user.id
            )
            # 如果是自动回复则直接发送
            if auto_reply:
                result = await email_outbox.send_email(
                    db=db,
                    email_id=email.id,
                    user_id=user.id
                )
                
            
            if result:
                return {"status": "success"}
            else:
                return {"status": "error", "message": "预回复邮件创建失败"}
        else:
            print("\n警告: 未配置 邮件回复 功能的 LLM 映射！")

