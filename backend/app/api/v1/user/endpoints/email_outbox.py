from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.v1.deps.auth import get_current_user
from app.models.user import User
from app.schemas.response import ResponseModel
from app.schemas.email_outbox import EmailOutbox, EmailOutboxCreate
from app.crud.email_outbox import email_outbox
from app.db.session import get_db
from app.schemas.common import PageResponse

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

@router.get("/list", response_model=ResponseModel[PageResponse[EmailOutbox]])
def get_email_list(
    *,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    reply_type: Optional[str] = None,
    account_id: Optional[int] = None,
    search: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user)
) -> ResponseModel[PageResponse[EmailOutbox]]:
    """
    获取发件箱邮件列表
    
    - 支持分页查询
    - 支持按状态、回复类型、账户ID筛选
    - 支持按主题和收件人搜索
    - 支持按日期范围筛选
    """
    filters = {
        "status": status,
        "reply_type": reply_type,
        "account_id": account_id,
        "search": search,
        "start_date": start_date,
        "end_date": end_date
    }
    # 移除空值
    filters = {k: v for k, v in filters.items() if v is not None}
    
    result = email_outbox.get_multi_by_user(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        filters=filters
    )
    
    total = email_outbox.get_total_count(
        db=db,
        user_id=current_user.id,
        filters=filters
    )
    
    # 使用 PageResponse 包装分页数据
    page_response = PageResponse.create(
        items=result,
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )
    
    return ResponseModel(data=page_response)

@router.get("/{email_id}", response_model=ResponseModel[EmailOutbox])
def get_email(
    *,
    db: Session = Depends(get_db),
    email_id: int,
    current_user: User = Depends(get_current_user)
) -> ResponseModel[EmailOutbox]:
    """
    获取发件箱邮件详情
    """
    result = email_outbox.get_by_id_and_user(
        db=db,
        email_id=email_id,
        user_id=current_user.id
    )
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )
    return ResponseModel(data=result)

@router.delete("/{email_id}", response_model=ResponseModel)
def delete_email(
    *,
    db: Session = Depends(get_db),
    email_id: int,
    current_user: User = Depends(get_current_user)
) -> ResponseModel:
    """
    删除发送邮件（硬删除）
    """
    result = email_outbox.delete(
        db=db,
        email_id=email_id,
        user_id=current_user.id
    )
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )
    return ResponseModel(data={"message": "Email deleted successfully"})

@router.post("/{email_id}/resend", response_model=ResponseModel[EmailOutbox])
async def resend_email(
    *,
    db: Session = Depends(get_db),
    email_id: int,
    current_user: User = Depends(get_current_user)
) -> ResponseModel[EmailOutbox]:
    """
    重新发送失败的邮件
    """
    try:
        result = await email_outbox.resend_email(
            db=db,
            id=email_id,
            user_id=current_user.id
        )
        if not result:
            raise HTTPException(
                status_code=404,
                detail="Email not found"
            )
        return ResponseModel(data=result)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) 

@router.put("/pre-reply/{email_id}", response_model=ResponseModel[EmailOutbox])
def update_pre_reply(
    *,
    db: Session = Depends(get_db),
    email_id: int,
    email_in: EmailOutboxCreate,
    current_user: User = Depends(get_current_user)
) -> ResponseModel[EmailOutbox]:
    """
    更新预回复邮件
    
    - 只能更新预回复状态的邮件
    - 不能更新已发送的邮件
    """
    # 获取邮件
    email = email_outbox.get_by_id_and_user(
        db=db,
        email_id=email_id,
        user_id=current_user.id
    )
    if not email:
        raise HTTPException(
            status_code=404,
            detail="邮件不存在"
        )
    
    # 检查是否是预回复邮件
    if email.reply_type != "pre_reply":
        raise HTTPException(
            status_code=400,
            detail="只能更新预回复邮件"
        )
    
    # 检查邮件状态
    if email.status == "sent":
        raise HTTPException(
            status_code=400,
            detail="不能更新已发送的邮件"
        )
    
    # 更新邮件
    update_data = email_in.model_dump(exclude_unset=True)
    # 保持原有的reply_type和reply_to_email_id
    update_data["reply_type"] = "pre_reply"
    update_data["reply_to_email_id"] = email.reply_to_email_id
    
    try:
        updated_email = email_outbox.update(
            db=db,
            db_obj=email,
            obj_in=update_data
        )
        return ResponseModel(data=updated_email)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )