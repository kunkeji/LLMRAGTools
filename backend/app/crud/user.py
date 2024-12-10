# app/crud/user.py
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security.password import get_password_hash, verify_password
from app.utils.file import delete_avatar

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        通过邮箱获取用户
        """
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """
        通过用户名获取用户
        """
        return db.query(User).filter(User.username == username).first()

    def get_by_phone(self, db: Session, *, phone: str) -> Optional[User]:
        """
        通过手机号获取用户
        """
        return db.query(User).filter(User.phone_number == phone).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        创建新用户
        """
        create_data = {
            "email": obj_in.email,
            "username": obj_in.username,
            "hashed_password": get_password_hash(obj_in.password),
            "nickname": obj_in.nickname or obj_in.username,  # 如果没有昵称，使用用户名
            "avatar": obj_in.avatar,
            "phone_number": obj_in.phone_number,
            "status": "active",
            "is_active": True
        }
        
        db_obj = User(**create_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        """
        更新用户信息
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        # 如果更新密码
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        # 如果更新头像，删除旧头像文件
        if update_data.get("avatar") and db_obj.avatar:
            delete_avatar(db_obj.avatar)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
        """
        验证用户
        """
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def soft_delete(self, db: Session, *, user_id: int) -> User:
        """
        软删除用户
        """
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            # 删除头像文件
            if user.avatar:
                delete_avatar(user.avatar)
            
            user.deleted_at = datetime.utcnow()
            user.is_active = False
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

crud_user = CRUDUser(User)