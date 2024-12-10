from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime

# 验证码用途枚举
VerificationPurpose = Literal["register", "reset_password"]

class VerificationCodeBase(BaseModel):
    email: EmailStr
    purpose: VerificationPurpose = "register"

class VerificationCodeCreate(VerificationCodeBase):
    pass

class VerificationCodeVerify(VerificationCodeBase):
    code: str

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    code: str
    new_password: str

class VerificationCode(VerificationCodeBase):
    id: int
    code: str
    expires_at: datetime
    is_used: bool
    created_at: datetime

    class Config:
        from_attributes = True 