from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        获取单个记录（排除已删除的记录）
        """
        stmt = select(self.model).where(
            self.model.id == id,
            self.model.deleted_at.is_(None)
        )
        return db.execute(stmt).scalar_one_or_none()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        获取多个记录（排除已删除的记录）
        """
        stmt = select(self.model).where(
            self.model.deleted_at.is_(None)
        ).offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        创建记录
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        更新记录
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[ModelType]:
        """
        硬删除记录
        """
        obj = db.get(self.model, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def soft_delete(self, db: Session, *, id: int) -> Optional[ModelType]:
        """
        软删除记录
        """
        obj = db.get(self.model, id)
        if obj:
            obj.deleted_at = datetime.now()
            db.add(obj)
            db.commit()
            db.refresh(obj)
        return obj

    def restore(self, db: Session, *, id: int) -> Optional[ModelType]:
        """
        恢复已删除的记录
        """
        obj = db.get(self.model, id)
        if obj and obj.deleted_at:
            obj.deleted_at = None
            db.add(obj)
            db.commit()
            db.refresh(obj)
        return obj