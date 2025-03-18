import logging
from os import getenv
import typing as t
from contextvars import ContextVar
from logging.handlers import RotatingFileHandler

current_username: ContextVar[t.Optional[str]] = ContextVar('current_username', default=None)


class CustomLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.username = current_username.get() or 'anonymous'
        return True


def setup_logging() -> None:
    log_level = getenv('LOG_LEVEL', 'INFO')
    log_max_bytes = int(getenv('LOG_MAX_BYTES', 10000000))
    log_backup_count = int(getenv('LOG_BACKUP_COUNT', 10))
    log_file_path = getenv('LOG_PATH', 'logs/test-task.log')

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(username)s - %(name)s:%(funcName)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            RotatingFileHandler(log_file_path, maxBytes=log_max_bytes, backupCount=log_backup_count),
            logging.StreamHandler()
        ]
    )
    for handler in logging.getLogger().handlers:
        handler.addFilter(CustomLogFilter())

    logging.getLogger("watchfiles").setLevel(logging.ERROR)
