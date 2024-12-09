from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api.v1.deps.auth import get_current_active_user, get_db
from app.crud import crud_user
from app.schemas.user import User, UserUpdate

router = APIRouter()

@router.get("/me", response_model=User)
def read_user_me(
    current_user: User = Depends(get_current_active_user),
):
    """
    获取当前用户信息
    """
    return current_user

@router.put("/me", response_model=User)
def update_user_me(
    *,
    current_user: User = Depends(get_current_active_user),
    user_in: UserUpdate,
    db: Session = Depends(get_db),
):
    """
    更新当前用户信息
    """
    user = crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return user 