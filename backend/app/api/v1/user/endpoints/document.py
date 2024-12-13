"""
文档管理API
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.deps.auth import get_current_active_user, get_db
from app.models.user import User
from app.crud.document import crud_document
from app.schemas.document import (
    Document, DocumentCreate, DocumentUpdate,
    DocumentMove, DocumentTree
)
from app.schemas.response import response_success

router = APIRouter()

@router.post("", summary="创建文档")
def create_document(
    *,
    db: Session = Depends(get_db),
    document_in: DocumentCreate,
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    创建新文档
    
    - 支持创建根文档或子文档
    - 自动生成文档路径
    - 记录创建者信息
    """
    # 如果指定了父文档，检查其是否存在
    if document_in.parent_id:
        parent = crud_document.get(db, id=document_in.parent_id)
        if not parent:
            raise HTTPException(
                status_code=404,
                detail="父文档不存在"
            )
    
    document = crud_document.create_with_path(
        db,
        obj_in=document_in,
        creator_id=current_user.id
    )
    return response_success(data=document)

@router.get("/tree", summary="获取文档树", response_model=dict)
def get_document_tree(
    *,
    db: Session = Depends(get_db),
    parent_id: Optional[int] = None,
    max_depth: Optional[int] = None,
    _: User = Depends(get_current_active_user)
) -> dict:
    """
    获取文档树结构
    
    - 支持指定父文档ID获取子树
    - 支持限制树的最大深度
    - 按照order字段排序
    """
    tree = crud_document.get_tree(
        db,
        parent_id=parent_id,
        max_depth=max_depth
    )
    return response_success(data=tree)

@router.get("/{document_id}", summary="获取文档详情")
def get_document(
    *,
    db: Session = Depends(get_db),
    document_id: int,
    _: User = Depends(get_current_active_user)
) -> dict:
    """
    获取文档详情
    
    - 包含文档内容
    - 包含完整的路径信息
    - 包含创建者和编辑者信息
    """
    result = crud_document.get_document_with_path(db, document_id=document_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="文档不存在"
        )
    return response_success(data=result)

@router.put("/{document_id}", summary="更新文档")
def update_document(
    *,
    db: Session = Depends(get_db),
    document_id: int,
    document_in: DocumentUpdate,
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    更新文档信息
    
    - 支持更新标题、内容、类型
    - 记录最后编辑者信息
    """
    document = crud_document.get(db, id=document_id)
    if not document:
        raise HTTPException(
            status_code=404,
            detail="文档不存在"
        )
    
    # 更新编辑者ID
    update_data = document_in.model_dump(exclude_unset=True)
    update_data["editor_id"] = current_user.id
    
    document = crud_document.update(
        db,
        db_obj=document,
        obj_in=update_data
    )
    return response_success(data=document)

@router.post("/{document_id}/move", summary="移动文档")
def move_document(
    *,
    db: Session = Depends(get_db),
    document_id: int,
    move_data: DocumentMove,
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    移动文档位置
    
    - 支持移动到不同父文档下
    - 支持调整顺序
    - 自动更新所有子文档的路径
    """
    # 检查目标父文档是否存在
    if move_data.target_parent_id:
        parent = crud_document.get(db, id=move_data.target_parent_id)
        if not parent:
            raise HTTPException(
                status_code=404,
                detail="目标父文档不存在"
            )
    
    document = crud_document.move_document(
        db,
        document_id=document_id,
        target_parent_id=move_data.target_parent_id,
        order=move_data.order,
        editor_id=current_user.id
    )
    if not document:
        raise HTTPException(
            status_code=404,
            detail="文档不存在"
        )
    return response_success(data=document)

@router.delete("/{document_id}", summary="删除文档")
def delete_document(
    *,
    db: Session = Depends(get_db),
    document_id: int,
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    删除文档
    
    - 支持软删除
    - 同时删除所有子文档
    """
    document = crud_document.get(db, id=document_id)
    if not document:
        raise HTTPException(
            status_code=404,
            detail="文档不存在"
        )
    
    document = crud_document.remove(db, id=document_id)
    return response_success(message="文档删除成功")

@router.get("", summary="搜索文档")
def search_documents(
    *,
    db: Session = Depends(get_db),
    keyword: Optional[str] = None,
    doc_type: Optional[str] = None,
    creator_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    搜索文档
    
    - 支持按关键词搜索（标题和内容）
    - 支持按文档类型筛选
    - 支持按创建者筛选
    - 支持分页
    """
    documents = crud_document.search_documents(
        db,
        keyword=keyword,
        doc_type=doc_type,
        creator_id=creator_id,
        skip=skip,
        limit=limit
    )
    return response_success(data=documents) 