"""
日志CRUD操作
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.crud.base import CRUDBase
from app.models.log import Log
from app.schemas.log import LogCreate, LogFilter

class CRUDLog(CRUDBase[Log, LogCreate, LogCreate]):
    def create_log(
        self,
        db: Session,
        *,
        obj_in: LogCreate
    ) -> Log:
        """创建日志记录"""
        return super().create(db, obj_in=obj_in)
    
    def get_logs(
        self,
        db: Session,
        *,
        filters: Optional[LogFilter] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Log]:
        """获取日志列表"""
        query = db.query(self.model)
        
        if filters:
            if filters.level:
                query = query.filter(self.model.level == filters.level)
            if filters.type:
                query = query.filter(self.model.type == filters.type)
            if filters.start_time:
                query = query.filter(self.model.timestamp >= filters.start_time)
            if filters.end_time:
                query = query.filter(self.model.timestamp <= filters.end_time)
            if filters.user_id:
                query = query.filter(self.model.user_id == filters.user_id)
            if filters.request_id:
                query = query.filter(self.model.request_id == filters.request_id)
            if filters.module:
                query = query.filter(self.model.module == filters.module)
            if filters.keyword:
                query = query.filter(
                    or_(
                        self.model.message.ilike(f"%{filters.keyword}%"),
                        self.model.error_type.ilike(f"%{filters.keyword}%"),
                        self.model.function.ilike(f"%{filters.keyword}%")
                    )
                )
        
        return query.order_by(self.model.timestamp.desc()).offset(skip).limit(limit).all()
    
    def get_logs_by_request_id(
        self,
        db: Session,
        *,
        request_id: str
    ) -> List[Log]:
        """获取指定请求ID的所有日志"""
        return db.query(self.model).filter(
            self.model.request_id == request_id
        ).order_by(self.model.timestamp.asc()).all()
    
    def get_error_logs(
        self,
        db: Session,
        *,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Log]:
        """获取错误日志"""
        query = db.query(self.model).filter(
            self.model.level.in_(["ERROR", "CRITICAL"])
        )
        
        if start_time:
            query = query.filter(self.model.timestamp >= start_time)
        if end_time:
            query = query.filter(self.model.timestamp <= end_time)
            
        return query.order_by(self.model.timestamp.desc()).all()
    
    def clean_old_logs(
        self,
        db: Session,
        *,
        days: int = 30
    ) -> int:
        """清理指定天数之前的日志"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        result = db.query(self.model).filter(
            self.model.timestamp < cutoff_date
        ).delete()
        db.commit()
        return result

crud_log = CRUDLog(Log) 