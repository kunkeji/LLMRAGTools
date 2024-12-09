from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User
from app.models.admin import Admin
from app.schemas.token import TokenPayload

# 用户认证
oauth2_user_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/user/login"
)

# 管理员认证
oauth2_admin_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/admin/login"
)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_user_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if token_data.type != "user":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无效的用户令牌",
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无法验证凭证",
        )
    user = db.query(User).filter(User.id == int(token_data.sub)).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="用户未激活")
    return user

def get_current_admin(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_admin_scheme)
) -> Admin:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if token_data.type != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无效的管理员令牌",
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无法验证凭证",
        )
    admin = db.query(Admin).filter(Admin.id == int(token_data.sub)).first()
    if not admin:
        raise HTTPException(status_code=404, detail="管理员不存在")
    if not admin.is_active:
        raise HTTPException(status_code=400, detail="管理员账号未激活")
    return admin

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="用户未激活")
    return current_user

def get_current_super_admin(
    current_admin: Admin = Depends(get_current_admin),
) -> Admin:
    if current_admin.role != "super_admin":
        raise HTTPException(
            status_code=403,
            detail="需要超级管理员权限",
        )
    return current_admin 