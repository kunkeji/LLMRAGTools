from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Shared properties
class AdminBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    role: Optional[str] = "admin"
    full_name: Optional[str] = None
    phone_number: Optional[str] = None

# Properties to receive via API on creation
class AdminCreate(AdminBase):
    username: str
    email: EmailStr
    password: str
    full_name: str
    role: str = "admin"

# Properties to receive via API on update
class AdminUpdate(AdminBase):
    password: Optional[str] = None

# Properties shared by models stored in DB
class AdminInDBBase(AdminBase):
    id: Optional[int] = None
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class Admin(AdminInDBBase):
    pass

# Additional properties stored in DB
class AdminInDB(AdminInDBBase):
    hashed_password: str 