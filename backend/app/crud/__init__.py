from app.crud.base import CRUDBase
from app.crud.user import crud_user
from app.crud.admin import crud_admin

# 导出所有 CRUD 操作
__all__ = [
    "crud_user",
    "crud_admin",
]
