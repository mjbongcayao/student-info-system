"""Logging setup: rotating file handler + console warnings."""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def setup_logging(log_file: str, level: str = "INFO") -> logging.Logger:
    """Configure the root 'sis' logger and return it."""
    logger = logging.getLogger("sis")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    if logger.handlers:  # avoid duplicate handlers on repeated calls
        return logger

    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(_FORMAT))
    logger.addHandler(file_handler)

    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    console.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(console)
    return logger
