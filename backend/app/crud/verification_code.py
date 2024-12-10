from typing import Optional
from datetime import datetime, timedelta
import random
import string
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.crud.base import CRUDBase
from app.models.verification_code import VerificationCode
from app.schemas.verification_code import VerificationCodeCreate

class CRUDVerificationCode(CRUDBase[VerificationCode, VerificationCodeCreate, VerificationCodeCreate]):
    def generate_code(self) -> str:
        """
        生成6位数字验证码
        """
        return ''.join(random.choices(string.digits, k=6))

    def create_verification_code(
        self, 
        db: Session, 
        *, 
        email: str,
        purpose: str = "register",
        expires_in_minutes: int = 10
    ) -> VerificationCode:
        """
        创建新的验证码
        """
        # 使之前的验证码失效
        self.invalidate_previous_codes(db, email=email, purpose=purpose)
        
        # 创建新验证码
        db_obj = VerificationCode(
            email=email,
            code=self.generate_code(),
            purpose=purpose,
            expires_at=datetime.utcnow() + timedelta(minutes=expires_in_minutes)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def verify_code(
        self, 
        db: Session, 
        *, 
        email: str,
        code: str,
        purpose: str = "register"
    ) -> bool:
        """
        验证验证码
        """
        verification_code = db.query(VerificationCode).filter(
            and_(
                VerificationCode.email == email,
                VerificationCode.code == code,
                VerificationCode.purpose == purpose,
                VerificationCode.is_used == False,
                VerificationCode.expires_at > datetime.utcnow()
            )
        ).first()

        if verification_code and verification_code.is_valid():
            verification_code.is_used = True
            db.add(verification_code)
            db.commit()
            return True
        return False

    def invalidate_previous_codes(
        self,
        db: Session,
        *,
        email: str,
        purpose: str
    ) -> None:
        """
        使之前的验证码失效
        """
        db.query(VerificationCode).filter(
            and_(
                VerificationCode.email == email,
                VerificationCode.purpose == purpose,
                VerificationCode.is_used == False
            )
        ).update({"is_used": True})
        db.commit()

    def get_latest_code(
        self,
        db: Session,
        *,
        email: str,
        purpose: str = "register"
    ) -> Optional[VerificationCode]:
        """
        获取最新的验证码
        """
        return db.query(VerificationCode).filter(
            and_(
                VerificationCode.email == email,
                VerificationCode.purpose == purpose,
                VerificationCode.is_used == False,
                VerificationCode.expires_at > datetime.utcnow()
            )
        ).order_by(VerificationCode.created_at.desc()).first()

crud_verification_code = CRUDVerificationCode(VerificationCode) 