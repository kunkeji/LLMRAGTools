from typing import Dict, Any
from datetime import datetime, timedelta
import logging

from app.core.tasks.registry import task_registry
from app.models.llm_channel import LLMChannel
from app.crud.email_tag import crud_email_tag
from app.models.llm_feature import FeatureType
from app.crud.llm_feature_mapping import crud_feature_mapping
from app.models.task import Task, TaskStatus, TaskPriority
from app.db.session import SessionLocal
from app.models.email import Email

from app.utils.llm.client import LLMClient
from app.core.tasks.tag_operation import create_tag_operation_task

def create_tag_task(email_id: int) -> Task:
    """创建标签同步任务"""
    # pass
    # 查询email的message_id是否存在
    with SessionLocal() as db:
        email = db.query(Email).filter(Email.id == email_id).first()
        if not email:
            raise ValueError(f"邮件不存在: {email_id}")
        # 创建标签同步任务
        task = Task(
            name=f"同步邮件标签 {email.id}",
            func_name="sync_email_tag",
            args={"email_id": email.id},
            status=TaskStatus.PENDING,
            priority=TaskPriority.NORMAL.value,
            scheduled_at=datetime.now(),
        )
        db.add(task)
        db.commit()

@task_registry.register(name="sync_email_tag")
async def sync_email_tag(email_id: int) -> Dict[str, Any]:
    # 根据邮件id获取邮件
    with SessionLocal() as db:
        email = db.query(Email).filter(Email.id == email_id).first()
        if not email:
            raise ValueError(f"邮件不存在: {email_id}")
        # 获取用户标签列表和默认标签EmailTag.user_id == email.account.user_id,或者EmailTag.user_id == ""
        tags = crud_email_tag.get_all_available_tags(
            db=db,
            user_id=email.account.user_id
        )
        # 获取用户配置的LABEL_CLASSIFICATION映射的模型
        feature_mapping = crud_feature_mapping.get_by_feature_type(
            db=db,
            user_id=email.account.user_id,
            feature_type=FeatureType.LABEL_CLASSIFICATION
        )
        # 获取映射模型的具体模型
        llm_model = db.query(LLMChannel).filter(LLMChannel.id == feature_mapping.channel_id).first()
        if not llm_model:
            raise ValueError(f"模型不存在: {feature_mapping.channel_id}")
        tag_str = "\n".join([f"{tag.id}:{tag.name}({tag.description})\n" for tag in tags])

        prompt = feature_mapping.prompt_template.replace("{{tag_list}}", tag_str)
        # 调用llm模型
        tag_id = LLMClient.generate(
            prompt=prompt,
            message="邮件内容："+email.content,
            api_key=llm_model.api_key,
            provider=llm_model.model_type,
            model=llm_model.model
        )
        # 先将tag_id转换成int
        tag_id = int(tag_id)
        # 判断 tag_id是否为空
        if not tag_id:
            raise ValueError(f"标签同步失败: {tag_id}")
        
        # 添加标签
        email_tag = crud_email_tag.add_email_tag(db=db, email_id=email_id, tag_id=tag_id)
        # 更新|添加标签 
        # 判断任务是否完成
        if email_tag:
            # 创建邮件标签任务
            create_tag_operation_task(email_id=email_id)
            return {"status": "success", "message": "标签同步成功"}
        else:
            return {"status": "error", "message": "标签同步失败"}