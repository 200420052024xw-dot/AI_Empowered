import logging
from logging.handlers import TimedRotatingFileHandler
import os
from colorama import init, Fore, Style  # ← 新增

init(autoreset=True)  # ← 自动重置颜色，避免后续输出被污染

def get_logger(name="file_collate", when="midnight", interval=1, backup_count=3):

    # 确定日志文件地址
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(base_dir, "../runtime_log")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "program_running.log")

    # 创建logger实例并且设置最低等级为debug
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 避免重复创建handlers
    if logger.handlers:
        return logger

    # 文件 handler：按时间切分，每天一个文件，保留3个历史文件
    try:
        file_handler = TimedRotatingFileHandler(
            filename=log_file,
            when=when,            # "midnight" 表示每天轮转
            interval=interval,
            backupCount=backup_count,
            encoding="utf-8",
            utc=False
        )
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"无法创建文件日志 handler: {e}")

    # 控制台 handler（添加蓝色输出）
    console_handler = logging.StreamHandler()
    class BlueFormatter(logging.Formatter):
        def format(self, record):
            message = super().format(record)
            return Fore.BLUE + message + Style.RESET_ALL  # ← 蓝色输出

    console_formatter = BlueFormatter(" %(message)s")
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    return logger
