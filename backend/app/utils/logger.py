"""
日志工具类
"""
import os
import sys
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path
from loguru import logger

from app.core.config import settings
from app.models.log import LogLevel, LogType
from app.crud.log import crud_log
from app.schemas.log import LogCreate
from app.db.session import SessionLocal

class Logger:
    """日志工具类"""
    
    def __init__(self):
        self._setup_logging()
    
    def _setup_logging(self):
        """配置日志"""
        # 移除默认处理器
        logger.remove()
        
        # 确保日志目录存在
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # 定义基本日志格式
        log_format = "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
        log_format += "<cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
        
        # 添加控制台处理器
        logger.add(
            sys.stdout,
            format=log_format,
            level=settings.LOG_LEVEL,
            enqueue=True
        )
        
        # 添加文件处理器
        logger.add(
            settings.LOG_PATH,
            format=log_format,
            level=settings.LOG_LEVEL,
            rotation=settings.LOG_ROTATION,
            retention=settings.LOG_RETENTION,
            enqueue=True
        )
    
    def _log(
        self,
        level: LogLevel,
        message: str,
        log_type: LogType = LogType.SYSTEM,
        **kwargs
    ):
        """
        记录日志
        
        Args:
            level: 日志级别
            message: 日志消息
            log_type: 日志类型
            **kwargs: 其他字段
        """
        # 记录到文件
        log_func = getattr(logger, level.lower())
        log_func(f"[{log_type}] {message}")
        
        try:
            # 记录到数据库
            with SessionLocal() as db:
                log_data = {
                    "level": level,
                    "type": log_type,
                    "message": message,
                    **kwargs
                }
                
                # 确保必填字段存在
                if "module" not in log_data:
                    log_data["module"] = "system"
                
                log_in = LogCreate(**log_data)
                crud_log.create_log(db, obj_in=log_in)
        except Exception as e:
            logger.error(f"记录日志到数据库失败: {str(e)}")
    
    def debug(
        self,
        message: str,
        log_type: LogType = LogType.SYSTEM,
        **kwargs
    ):
        """记录DEBUG级别日志"""
        self._log(LogLevel.DEBUG, message, log_type, **kwargs)
    
    def info(
        self,
        message: str,
        log_type: LogType = LogType.SYSTEM,
        **kwargs
    ):
        """记录INFO级别日志"""
        self._log(LogLevel.INFO, message, log_type, **kwargs)
    
    def warning(
        self,
        message: str,
        log_type: LogType = LogType.SYSTEM,
        **kwargs
    ):
        """记录WARNING级别日志"""
        self._log(LogLevel.WARNING, message, log_type, **kwargs)
    
    def error(
        self,
        message: str,
        log_type: LogType = LogType.SYSTEM,
        **kwargs
    ):
        """记录ERROR级别日志"""
        self._log(LogLevel.ERROR, message, log_type, **kwargs)
    
    def critical(
        self,
        message: str,
        log_type: LogType = LogType.SYSTEM,
        **kwargs
    ):
        """记录CRITICAL级别日志"""
        self._log(LogLevel.CRITICAL, message, log_type, **kwargs)

# 全局日志实例
logger_instance = Logger() 