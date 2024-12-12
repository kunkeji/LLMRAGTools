"""
用户邮箱账户管理接口
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.deps.auth import get_current_user
from app.models.user import User
from app.schemas.response import ResponseModel
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

router = APIRouter()

@router.get("/accounts", response_model=ResponseModel[List[EmailAccountResponse]])
def get_email_accounts(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """获取用户的邮箱账户列表"""
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
    """创建邮箱账户"""
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

@router.post("/accounts/{account_id}/sync", response_model=ResponseModel)
def sync_email_account(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    account_id: int
):
    """手动同步邮箱账户"""
    account = crud_email_account.get(db, id=account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Email account not found"
        )
    
    # TODO: 实现邮箱同步逻辑
    success = crud_email_account.sync_emails(db, account)
    if not success:
        raise HTTPException(
            status_code=400,
            detail="Failed to sync emails"
        )
    
    return ResponseModel() 