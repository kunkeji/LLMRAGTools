from datetime import datetime
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.api.v1.deps.auth import get_db
from app.crud import crud_user
from app.crud.verification_code import crud_verification_code
from app.schemas.verification_code import VerificationCodeCreate, ResetPasswordRequest
from app.utils.email import send_reset_password_email

router = APIRouter()

@router.post("/forgot-password")
async def forgot_password(
    *,
    db: Session = Depends(get_db),
    email_in: VerificationCodeCreate,
    background_tasks: BackgroundTasks,
) -> Any:
    """
    发送重置密码验证码
    """
    # 检查邮箱是否存在
    user = crud_user.get_by_email(db, email=email_in.email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="该邮箱未注册"
        )
    
    # 获取最新的验证码
    latest_code = crud_verification_code.get_latest_code(
        db, email=email_in.email, purpose="reset_password"
    )
    
    # 如果存在未过期的验证码且发送时间小于1分钟，则不允许重新发送
    if latest_code and (datetime.utcnow() - latest_code.created_at).total_seconds() < 60:
        raise HTTPException(
            status_code=400,
            detail="请求过于频繁，请稍后再试"
        )
    
    # 创建新的验证码
    verification_code = crud_verification_code.create_verification_code(
        db, 
        email=email_in.email, 
        purpose="reset_password"
    )
    
    # 在后台发送邮件
    background_tasks.add_task(
        send_reset_password_email,
        email_to=email_in.email,
        code=verification_code.code,
        username=user.username
    )
    
    return {"message": "重置密码验证码已发送，请查收邮件"}

@router.post("/reset-password")
def reset_password(
    *,
    db: Session = Depends(get_db),
    reset_data: ResetPasswordRequest,
) -> Any:
    """
    重置密码
    """
    # 验证验证码
    if not crud_verification_code.verify_code(
        db,
        email=reset_data.email,
        code=reset_data.code,
        purpose="reset_password"
    ):
        raise HTTPException(
            status_code=400,
            detail="验证码无效或已过期"
        )
    
    # 获取用户
    user = crud_user.get_by_email(db, email=reset_data.email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )
    
    # 更新密码
    user = crud_user.update(
        db,
        db_obj=user,
        obj_in={"password": reset_data.new_password}
    )
    
    return {"message": "密码重置成功"} 