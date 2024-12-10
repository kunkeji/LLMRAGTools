from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.v1.deps.auth import get_current_user, get_db
from app.core.config import settings
from app.core.security import jwt
from app.crud import crud_user
from app.crud.verification_code import crud_verification_code
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate
from app.schemas.verification_code import VerificationCodeCreate
from app.utils.email import send_verification_email
from app.schemas.response import response_success, ResponseModel

router = APIRouter()

@router.post("/send-verification-code")
async def send_verification_code(
    *,
    db: Session = Depends(get_db),
    email_in: VerificationCodeCreate,
    background_tasks: BackgroundTasks,
) -> dict:
    """
    发送验证码
    """
    # 检查邮箱是否已注册
    user = crud_user.get_by_email(db, email=email_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="该邮箱已被注册"
        )
    
    # 获取最新的验证码
    latest_code = crud_verification_code.get_latest_code(
        db, email=email_in.email, purpose=email_in.purpose
    )
    
    # 如果存在未过期的验证码且发送时间小于1分钟，则不允许重新发送
    if latest_code and (datetime.utcnow() - latest_code.created_at).total_seconds() < 60:
        raise HTTPException(
            status_code=400,
            detail="请求过于频繁，请稍后再试"
        )
    
    # 创建新的验证码
    verification_code = crud_verification_code.create_verification_code(
        db, email=email_in.email, purpose=email_in.purpose
    )
    
    # 在后台发送邮件
    background_tasks.add_task(
        send_verification_email,
        email_to=email_in.email,
        code=verification_code.code
    )
    
    return response_success(message="验证码已发送，请查收邮件")

@router.post("/register")
def register(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> dict:
    """
    用户注册
    """
    # 验证验证码
    if not crud_verification_code.verify_code(
        db,
        email=user_in.email,
        code=user_in.verification_code,
        purpose="register"
    ):
        raise HTTPException(
            status_code=400,
            detail="验证码无效或已过期"
        )
    
    # 检查邮箱是否已注册
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="该邮箱已被注册"
        )
    
    # 检查用户名是否已被使用
    user = crud_user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="该用户名已被使用"
        )
    
    # 创建用户
    user = crud_user.create(db, obj_in=user_in)
    return response_success(data=user)

@router.post("/login")
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    """
    用户登录获取token
    """
    user = crud_user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="用户未激活")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = {
        "access_token": jwt.create_access_token(
            subject=str(user.id),
            token_type="user",
            expires_delta=access_token_expires,
            extra_data={"status": user.status}
        ),
        "token_type": "bearer",
    }
    return response_success(data=token)

@router.get("/me")
def read_user_me(
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    获取当前用户信息
    """
    return response_success(data=current_user) 