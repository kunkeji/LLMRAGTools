from typing import Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.api.v1.deps.auth import get_current_active_user, get_db
from app.crud import crud_user
from app.models.user import User
from app.schemas.user import UserUpdate
from app.schemas.response import response_success, ResponseModel
from app.utils.file import save_avatar, delete_avatar
from app.schemas.avatar import AvatarUploadResponse, DEFAULT_AVATAR_CONFIG

router = APIRouter()

@router.get("/me", summary="获取当前用户信息")
def get_user_profile(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    获取当前登录用户的详细信息
    """
    return response_success(data=current_user)

@router.put("/me", summary="更新当前用户信息")
def update_user_profile(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    user_in: UserUpdate,
) -> Any:
    """
    更新当前登录用户的信息
    
    可更新字段包括：
    * nickname: 昵称
    * phone_number: 手机号码
    * password: 密码（可选）
    """
    # 如果更新手机号，检查是否已被使用
    if user_in.phone_number and user_in.phone_number != current_user.phone_number:
        if crud_user.get_by_phone(db, phone=user_in.phone_number):
            raise HTTPException(
                status_code=400,
                detail="该手机号已被使用"
            )
    
    user = crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return response_success(data=user)

@router.post("/me/avatar", summary="更新用户头像", response_model=ResponseModel[AvatarUploadResponse])
async def update_user_avatar(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    file: UploadFile = File(...),
) -> Any:
    """
    更新用户头像
    
    - 支持的图片格式：jpg, jpeg, png
    - 最大文件大小：2MB
    - 最小尺寸：100x100
    - 最大尺寸：800x800
    - 图片质量：85%
    """
    # 保存头像文件
    avatar_response = await save_avatar(file, current_user.id)
    
    # 如果用户已有头像，删除旧头像
    if current_user.avatar:
        delete_avatar(current_user.avatar)
    
    # 更新用户头像URL
    crud_user.update(
        db,
        db_obj=current_user,
        obj_in={"avatar": avatar_response.url}
    )
    
    return response_success(
        data=avatar_response,
        message="头像更新成功"
    )



