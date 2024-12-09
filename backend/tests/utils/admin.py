from typing import Dict
from sqlalchemy.orm import Session

from app.crud.admin import crud_admin
from app.models.admin import Admin
from app.schemas.admin import AdminCreate
from app.tests.utils.utils import random_email, random_lower_string

def create_random_admin(db: Session, login_data: Dict[str, str] = None, is_super: bool = False) -> Admin:
    """创建随机管理员"""
    if login_data is None:
        username = random_lower_string()
        password = random_lower_string()
    else:
        username = login_data["username"]
        password = login_data["password"]
        
    admin_in = AdminCreate(
        username=username,
        email=random_email(),
        password=password,
        full_name=random_lower_string(),
        role="super_admin" if is_super else "admin"
    )
    admin = crud_admin.create(db=db, obj_in=admin_in)
    return admin 