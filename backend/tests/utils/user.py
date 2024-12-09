from typing import Dict
from sqlalchemy.orm import Session

from app.crud.user import crud_user
from app.models.user import User
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string

def create_random_user(db: Session, login_data: Dict[str, str] = None) -> User:
    """创建随机用户"""
    if login_data is None:
        email = random_email()
        password = random_lower_string()
    else:
        email = login_data["username"]
        password = login_data["password"]
        
    user_in = UserCreate(
        email=email,
        password=password,
        first_name=random_lower_string(),
        last_name=random_lower_string(),
    )
    user = crud_user.create(db=db, obj_in=user_in)
    return user 