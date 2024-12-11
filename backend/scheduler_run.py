import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

# 设置项目根目录到 Python 路径
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

# 创建日志目录
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 配置日志
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # 文件处理器
    log_file = os.path.join(LOG_DIR, f'scheduler_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger

if __name__ == "__main__":
    # 设置日志
    logger = setup_logging()
    logger.info("正在启动任务调度器...")

    try:
        # 导入所有任务
        import app.core.tasks
        
        # 导入调度器
        from app.core.tasks.scheduler import scheduler
        from app.core.tasks.registry import task_registry
        
        # 打印已注册的任务
        tasks = task_registry.list_tasks()
        logger.info(f"已注册的任务: {list(tasks.keys())}")
        
        # 启动调度器
        scheduler.start()
        
        logger.info("任务调度器已启动，按 Ctrl+C 停止")
        
        # 保持程序运行
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("正在停止任务调度器...")
            scheduler.stop()
            logger.info("任务调度器已停止")
    
    except Exception as e:
        logger.exception("任务调度器运行出错")
        sys.exit(1) 