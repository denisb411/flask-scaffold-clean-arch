import logging
from functools import wraps
from flask import request
from typing import Any, Callable, TypeVar, cast

# === ANSI color codes per log level ===
LEVEL_COLORS: dict[int, str] = {
    logging.DEBUG: "\033[94m",      # Light blue
    logging.INFO: "",               # Default (no color)
    logging.WARNING: "\033[33m",    # Yellow
    logging.ERROR: "\033[91m",      # Red
    logging.CRITICAL: "\033[31;1m"  # Bold dark red
}
RESET_COLOR = "\033[0m"

class ColorFormatter(logging.Formatter):
    """
    Formatter that applies ANSI color codes based on log level.
    """
    def format(self, record: logging.LogRecord) -> str:
        color = LEVEL_COLORS.get(record.levelno, "")
        message = super().format(record)
        return f"{color}{message}{RESET_COLOR}"

def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a named logger with colored console output.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = ColorFormatter('%(asctime)s %(levelname)s [%(name)s]: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

# Type variables for decorators
F = TypeVar("F", bound=Callable[..., Any])

def log_request(func: F) -> F:
    """
    Decorator that logs the HTTP method and path of each request.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger = get_logger(func.__module__)
        payload = request.get_json(silent=True)
        logger.info(f"{request.method} {request.path} - Payload: {payload}")
        return func(*args, **kwargs)

    return cast(F, wrapper)
