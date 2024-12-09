from typing import Any
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    基础模型类
    """
    @declared_attr
    def __tablename__(cls) -> str:
        """
        自动生成表名
        """
        return cls.__name__.lower() 