from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate
from app.core.security.password import get_password_hash, verify_password

class CRUDAdmin(CRUDBase[Admin, AdminCreate, AdminUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Admin]:
        """
        通过邮箱获取管理员
        """
        return db.query(Admin).filter(Admin.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[Admin]:
        """
        通过用户名获取管理员
        """
        return db.query(Admin).filter(Admin.username == username).first()

    def create(self, db: Session, *, obj_in: AdminCreate) -> Admin:
        """
        创建新管理员
        """
        db_obj = Admin(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            role=obj_in.role,
            phone_number=obj_in.phone_number,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Admin, obj_in: AdminUpdate) -> Admin:
        """
        更新管理员信息
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[Admin]:
        """
        验证管理员
        """
        admin = self.get_by_username(db, username=username)
        if not admin:
            return None
        if not verify_password(password, admin.hashed_password):
            return None
        # 更新最后登录时间
        admin.last_login = datetime.now()
        db.add(admin)
        db.commit()
        db.refresh(admin)
        return admin

    def get_super_admins(self, db: Session) -> List[Admin]:
        """
        获取所有超���管理员
        """
        return db.query(Admin).filter(Admin.role == "super_admin").all()

crud_admin = CRUDAdmin(Admin) 