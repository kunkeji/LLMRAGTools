"""
邮箱提供商管理接口
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.deps.auth import get_current_admin
from app.models.admin import Admin
from app.schemas.response import ResponseModel, response_success
from app.schemas.email_provider import EmailProvider, EmailProviderCreate, EmailProviderUpdate
from app.crud.email_provider import crud_email_provider
from app.db.session import get_db

router = APIRouter()

@router.get("/providers", response_model=ResponseModel[List[EmailProvider]])
def get_email_providers(
    *,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
    keyword: str = None,
    is_active: bool = None,
    skip: int = 0,
    limit: int = 100
):
    """获取邮箱提供商列表"""
    providers = crud_email_provider.search_providers(
        db,
        keyword=keyword,
        is_active=is_active,
        skip=skip,
        limit=limit
    )
    return response_success(data=providers)

@router.post("/providers", response_model=ResponseModel[EmailProvider])
def create_email_provider(
    *,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
    provider_in: EmailProviderCreate
):
    """创建邮箱提供商"""
    # 检查名称是否已存在
    if crud_email_provider.get_by_name(db, name=provider_in.name):
        raise HTTPException(
            status_code=400,
            detail="Provider name already exists"
        )
    # 检查域名后缀是否已存在
    if crud_email_provider.get_by_domain(db, domain=provider_in.domain_suffix):
        raise HTTPException(
            status_code=400,
            detail="Domain suffix already exists"
        )
    provider = crud_email_provider.create(db, obj_in=provider_in)
    return response_success(data=provider)

@router.put("/providers/{provider_id}", response_model=ResponseModel[EmailProvider])
def update_email_provider(
    *,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
    provider_id: int,
    provider_in: EmailProviderUpdate
):
    """更新邮箱提供商"""
    provider = crud_email_provider.get(db, id=provider_id)
    if not provider:
        raise HTTPException(
            status_code=404,
            detail="Email provider not found"
        )
    
    # 如果更新了名称，检查是否与其他提供商重复
    if provider_in.name and provider_in.name != provider.name:
        if crud_email_provider.get_by_name(db, name=provider_in.name):
            raise HTTPException(
                status_code=400,
                detail="Provider name already exists"
            )
    
    # 如果更新了域名后缀，检查是否与其他提供商重复
    if provider_in.domain_suffix and provider_in.domain_suffix != provider.domain_suffix:
        if crud_email_provider.get_by_domain(db, domain=provider_in.domain_suffix):
            raise HTTPException(
                status_code=400,
                detail="Domain suffix already exists"
            )
    
    provider = crud_email_provider.update(db, db_obj=provider, obj_in=provider_in)
    return response_success(data=provider)

@router.delete("/providers/{provider_id}", response_model=ResponseModel)
def delete_email_provider(
    *,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
    provider_id: int
):
    """删除邮箱提供商"""
    provider = crud_email_provider.get(db, id=provider_id)
    if not provider:
        raise HTTPException(
            status_code=404,
            detail="Email provider not found"
        )
    crud_email_provider.remove(db, id=provider_id)
    return response_success()

@router.get("/providers/{provider_id}", response_model=ResponseModel[EmailProvider])
def get_email_provider(
    *,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
    provider_id: int
):
    """获取邮箱提供商详情"""
    provider = crud_email_provider.get(db, id=provider_id)
    if not provider:
        raise HTTPException(
            status_code=404,
            detail="Email provider not found"
        )
    return response_success(data=provider) 