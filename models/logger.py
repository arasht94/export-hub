import logging
import sys


def get_logger(name: str = None, level: int = logging.INFO) -> logging.Logger:
    """
    Set up and return a logger using Python's logging library.

    Args:
        name: Name for the logger. If None, uses the root logger.
        level: Logging level (default: logging.INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid adding handlers multiple times if logger already exists
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # Create console handler with a format
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger
