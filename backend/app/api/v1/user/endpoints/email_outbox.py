from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.deps.auth import get_current_user
from app.models.user import User
from app.schemas.response import ResponseModel
from app.schemas.email_outbox import EmailOutbox, EmailOutboxCreate
from app.crud.email_outbox import email_outbox
from app.db.session import get_db

router = APIRouter()

@router.post("/send", response_model=ResponseModel[EmailOutbox])
def create_email(
    *,
    db: Session = Depends(get_db),
    email_in: EmailOutboxCreate,
    current_user: User = Depends(get_current_user)
) -> ResponseModel[EmailOutbox]:
    """
    创建待发送邮件
    - 如果指定account_id则使用指定账户发送
    - 如果指定reply_to_email_id则作为回复邮件,使用原邮件的账户
    - 否则使用用户默认邮箱账户
    """
    try:
        result = email_outbox.create_email(
            db=db,
            obj_in=email_in,
            user_id=current_user.id
        )
        return ResponseModel(data=result)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post("/{email_id}/send", response_model=ResponseModel[EmailOutbox])
async def send_email(
    *,
    db: Session = Depends(get_db),
    email_id: int,
    current_user: User = Depends(get_current_user)
) -> ResponseModel[EmailOutbox]:
    """
    发送指定ID的邮件
    """
    try:
        result = await email_outbox.send_email(
            db=db,
            email_id=email_id,
            user_id=current_user.id
        )
        return ResponseModel(data=result)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post("/send-direct", response_model=ResponseModel[EmailOutbox])
async def create_and_send_email(
    *,
    db: Session = Depends(get_db),
    email_in: EmailOutboxCreate,
    current_user: User = Depends(get_current_user)
) -> ResponseModel[EmailOutbox]:
    """
    创建并立即发送邮件(组合接口)
    """
    try:
        # 先创建邮件
        email = email_outbox.create_email(
            db=db,
            obj_in=email_in,
            user_id=current_user.id
        )
        # 立即发送
        result = await email_outbox.send_email(
            db=db,
            email_id=email.id,
            user_id=current_user.id
        )
        return ResponseModel(data=result)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("/list", response_model=ResponseModel[List[EmailOutbox]])
def get_email_list(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> ResponseModel[List[EmailOutbox]]:
    """
    获取用户的发送邮件列表
    """
    result = email_outbox.get_multi_by_user(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    return ResponseModel(data=result)

@router.get("/{email_id}", response_model=ResponseModel[EmailOutbox])
def get_email(
    *,
    db: Session = Depends(get_db),
    email_id: int,
    current_user: User = Depends(get_current_user)
) -> ResponseModel[EmailOutbox]:
    """
    获取单个发送邮件详情
    """
    result = email_outbox.get(db=db, id=email_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )
    # 验证权限
    if result.account.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    return ResponseModel(data=result) 