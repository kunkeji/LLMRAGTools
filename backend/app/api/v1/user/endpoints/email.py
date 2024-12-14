from typing import List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.api.v1.deps.auth import get_current_user, get_current_active_user, get_db
from app.models.user import User
from app.schemas.response import ResponseModel, response_success
from app.schemas.email_account import (
    EmailAccountResponse,
    EmailAccountCreate,
    EmailAccountUpdate,
    EmailAccountWithStats
)
from app.schemas.email_provider import EmailProvider
from app.crud.email_account import crud_email_account
from app.crud.email_provider import crud_email_provider
from app.db.session import get_db
from app.core.tasks.email_sync import create_sync_task
from app.schemas.email import Email, EmailUpdate
from app.crud.email import crud_email

router = APIRouter()

@router.get("/accounts", response_model=ResponseModel[List[EmailAccountResponse]])
def get_email_accounts(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    accounts = crud_email_account.get_multi_by_user(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    return ResponseModel(data=accounts)

@router.post("/accounts", response_model=ResponseModel[EmailAccountResponse])
def create_email_account(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    account_in: EmailAccountCreate
):
    # 检查邮箱地址是否已存在
    if crud_email_account.get_by_email(db, user_id=current_user.id, email=account_in.email_address):
        raise HTTPException(
            status_code=400,
            detail="Email address already exists"
        )
    
    # 如果是第一个账户，设置为默认账户
    if not crud_email_account.get_multi_by_user(db, user_id=current_user.id, limit=1):
        account_in.is_default = True
    elif account_in.is_default:
        # 如果设置为默认账户，需要将其他账户的默认状态取消
        crud_email_account.clear_default_status(db, user_id=current_user.id)
    
    account = crud_email_account.create_with_user(
        db,
        obj_in=account_in,
        user_id=current_user.id
    )
    return ResponseModel(data=account)

@router.put("/accounts/{account_id}", response_model=ResponseModel[EmailAccountResponse])
def update_email_account(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    account_id: int,
    account_in: EmailAccountUpdate
):
    """更新邮箱账户"""
    account = crud_email_account.get(db, id=account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Email account not found"
        )
    
    if account_in.is_default:
        # 如果设置为默认账户，需要将其他账户的默认状态取消
        crud_email_account.clear_default_status(db, user_id=current_user.id)
    
    account = crud_email_account.update(db, db_obj=account, obj_in=account_in)
    return ResponseModel(data=account)

@router.delete("/accounts/{account_id}", response_model=ResponseModel)
def delete_email_account(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    account_id: int
):
    """删除邮箱账户"""
    account = crud_email_account.get(db, id=account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Email account not found"
        )
    
    # 如果删除的是默认账户，需要设置其他账户为默认账户
    if account.is_default:
        next_account = crud_email_account.get_next_account(
            db,
            user_id=current_user.id,
            current_id=account_id
        )
        if next_account:
            crud_email_account.update(
                db,
                db_obj=next_account,
                obj_in={"is_default": True}
            )
    
    crud_email_account.remove(db, id=account_id)
    return ResponseModel()

@router.get("/accounts/{account_id}", response_model=ResponseModel[EmailAccountWithStats])
def get_email_account(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    account_id: int
):
    """获取邮箱账户详情"""
    account = crud_email_account.get(db, id=account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Email account not found"
        )
    return ResponseModel(data=account)

@router.get("/providers", response_model=ResponseModel[List[EmailProvider]])
def get_email_providers(
    *,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """获取可用的邮箱提供商列表"""
    providers = crud_email_provider.get_active_providers(
        db,
        skip=skip,
        limit=limit
    )
    return ResponseModel(data=providers)

@router.post("/accounts/{account_id}/test", response_model=ResponseModel)
async def test_email_account(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    account_id: int
):
    """测试邮箱账户连接"""
    account = crud_email_account.get(db, id=account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Email account not found"
        )
    
    # 执行连接测试
    success = await crud_email_account.test_connection(db, account)
    if not success:
        raise HTTPException(
            status_code=400,
            detail="Failed to connect to email server"
        )
    
    return ResponseModel(message="Connection test successful")

@router.post("/accounts/{account_id}/sync", summary="触发邮件同步")
def trigger_email_sync(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    account_id: int
) -> Any:
    # 检查账户是否存在且属于当前用户
    account = crud_email_account.get(db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=404,
            detail="邮件账户不存在"
        )
    if account.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="无权访问此邮件账户"
        )
    
    # 创建同步任务
    task = create_sync_task(account_id)
    
    return response_success(
        data={
            "task_id": task.id,
            "status": task.status,
            "scheduled_at": task.scheduled_at.isoformat()
        },
        message="同步任务已创建"
    )

@router.get("/accounts/{account_id}/emails", response_model=ResponseModel[dict])
def get_emails(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    account_id: int,
    folder: Optional[str] = None,
    is_read: Optional[bool] = None,
    is_flagged: Optional[bool] = None,
    skip: int = 0,
    limit: int = 50,  # 默认每页50条
    order_by: str = "date",
    order_desc: bool = True
):
    """获取邮件列表"""
    # 检查账户是否存在且属于当前用户
    account = crud_email_account.get(db, id=account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Email account not found"
        )
    
    emails, total = crud_email.get_multi_by_account(
        db,
        account_id=account_id,
        folder=folder,
        is_read=is_read,
        is_flagged=is_flagged,
        skip=skip,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc
    )
    
    # 将 SQLAlchemy 模型转换为 Pydantic 模型
    from app.schemas.email import Email as EmailSchema
    email_list = [EmailSchema.model_validate(email) for email in emails]
    
    return response_success(data={
        "items": email_list,
        "total": total,
        "page": skip // limit + 1,
        "size": limit,
        "pages": (total + limit - 1) // limit
    })

@router.get("/accounts/{account_id}/emails/{email_id}", response_model=ResponseModel[Email])
def get_email(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    account_id: int,
    email_id: int
):
    """获取邮件详情"""
    # 检查账户是否存在且属于当前用户
    account = crud_email_account.get(db, id=account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Email account not found"
        )
    
    email = crud_email.get(db, id=email_id)
    if not email or email.account_id != account_id:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )
    
    return response_success(data=email)

@router.put("/accounts/{account_id}/emails/{email_id}", response_model=ResponseModel[Email])
def update_email(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    account_id: int,
    email_id: int,
    email_in: EmailUpdate
):
    """更新邮件"""
    # 检查账户��否存在且属于当前用户
    account = crud_email_account.get(db, id=account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Email account not found"
        )
    
    email = crud_email.get(db, id=email_id)
    if not email or email.account_id != account_id:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )
    
    email = crud_email.update(db, db_obj=email, obj_in=email_in)
    return response_success(data=email)

@router.delete("/accounts/{account_id}/emails/{email_id}", response_model=ResponseModel)
def delete_email(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    account_id: int,
    email_id: int,
    permanent: bool = False
):
    """删除邮件"""
    # 检查账户是否存在且属于当前用户
    account = crud_email_account.get(db, id=account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Email account not found"
        )
    
    # 获取邮件
    email = crud_email.get(db, id=email_id)
    if not email or email.account_id != account_id:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )
    
    if permanent:
        # 永久删除
        crud_email.remove(db, id=email_id)
    else:
        # 移动到已删除文件夹
        crud_email.update(
            db,
            db_obj=email,
            obj_in=EmailUpdate(
                folder="Trash",
                deleted_at=datetime.now()
            )
        )
    
    return ResponseModel(message="Email deleted successfully")

@router.post("/accounts/{account_id}/emails/{email_id}/mark-read", response_model=ResponseModel[Email])
def mark_email_read(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    account_id: int,
    email_id: int,
    is_read: bool = True
):
    """标记邮件已读/未读"""
    # 检查账户是否存在且属于当前用户
    account = crud_email_account.get(db, id=account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Email account not found"
        )
    
    # 获取邮件
    email = crud_email.get(db, id=email_id)
    if not email or email.account_id != account_id:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )
    
    # 标记已读/未读
    email = crud_email.mark_as_read(db, email_id=email_id, is_read=is_read)
    return ResponseModel(data=email)

@router.post("/accounts/{account_id}/emails/{email_id}/mark-flagged", response_model=ResponseModel[Email])
def mark_email_flagged(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    account_id: int,
    email_id: int,
    is_flagged: bool = True
):
    """标记邮件重要/取消重要"""
    # 检查账户是否存在且属于当前用户
    account = crud_email_account.get(db, id=account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Email account not found"
        )
    
    # 获取邮件
    email = crud_email.get(db, id=email_id)
    if not email or email.account_id != account_id:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )
    
    # 标记重要/取消重要
    email = crud_email.mark_as_flagged(db, email_id=email_id, is_flagged=is_flagged)
    return ResponseModel(data=email)

@router.post("/accounts/{account_id}/emails/{email_id}/move", response_model=ResponseModel[Email])
def move_email(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    account_id: int,
    email_id: int,
    folder: str
):
    """移动邮件到指定文件夹"""
    # 检查账户是否存在且属于当前用户
    account = crud_email_account.get(db, id=account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Email account not found"
        )
    
    # 获取邮件
    email = crud_email.get(db, id=email_id)
    if not email or email.account_id != account_id:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )
    
    # 移动到指定文件夹
    email = crud_email.move_to_folder(db, email_id=email_id, folder=folder)
    return ResponseModel(data=email) 