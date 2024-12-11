"""
日志模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum as SQLEnum
from enum import Enum
from app.db.base_class import Base

class LogLevel(str, Enum):
    """日志级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogType(str, Enum):
    """日志类型"""
    OPERATION = "OPERATION"  # 操作日志
    SECURITY = "SECURITY"    # 安全日志
    SYSTEM = "SYSTEM"       # 系统日志
    API = "API"             # API请求日志

class Log(Base):
    """日志记录"""
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    level = Column(SQLEnum(LogLevel), nullable=False, index=True)
    type = Column(SQLEnum(LogType), nullable=False, index=True)
    
    # 请求相关
    request_id = Column(String(36), nullable=True, index=True)
    method = Column(String(10), nullable=True)
    url = Column(String(500), nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(200), nullable=True)
    
    # 用户相关
    user_id = Column(Integer, nullable=True, index=True)
    username = Column(String(50), nullable=True)
    
    # 日志内容
    module = Column(String(100), nullable=False)  # 模块名称
    function = Column(String(100), nullable=True)  # 函数名称
    message = Column(String(1000), nullable=False)  # 日志消息
    details = Column(JSON, nullable=True)  # 详细信息
    
    # 错误相关
    error_type = Column(String(100), nullable=True)
    error_stack = Column(String(2000), nullable=True)
    
    # 性能相关
    duration = Column(Integer, nullable=True)  # 执行时长(毫秒)
    
    def __repr__(self) -> str:
        return f"<Log {self.id}: [{self.level}] {self.message}>" 