import logging
import os
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

def get_logger(name: str = "llm_structured_extract") -> logging.Logger:
    """
    获取配置好的日志对象。
    支持控制台输出和文件输出，自动创建根目录下的 logs 文件夹。
    """
    logger = logging.getLogger(name)
    
    # 如果已经配置过 handler，直接返回，避免重复日志
    if logger.handlers:
        return logger

    # 1. 确定项目根目录并创建 logs 目录
    # 假设 logger.py 在 llm_structured_extract/utils/ 下
    project_root = Path(__file__).resolve().parents[2]
    log_dir = project_root / "logs"
    try:
        log_dir.mkdir(exist_ok=True)
    except Exception:
        # 如果创建目录失败（如权限问题），降级为仅控制台输出
        pass

    # 2. 设置基础级别（从环境变量读取，默认 INFO）
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logger.setLevel(log_level)

    # 3. 定义统一的日志格式
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d) - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 4. 文件 Handler (如果目录可用)
    if log_dir.is_dir():
        log_file = log_dir / "app.log"
        # 使用滚动文件处理器，防止日志文件无限增大
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=10 * 1024 * 1024, # 10MB
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # 5. 控制台 Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
