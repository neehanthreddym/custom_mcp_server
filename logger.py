# logging_config.py
import logging
import os
from pathlib import Path

def setup_logging(log_dir: str = "logs/app.log", log_level: str = "INFO") -> None:
    """Centralized logging setup for the entire project."""
    log_file = Path(log_dir)
    log_dir_path = log_file.parent
    log_dir_path.mkdir(parents=True, exist_ok=True)

    # Clear any existing handlers to avoid duplicates
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Common formatter
    fmt = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s:%(lineno)d %(message)s"
    )

    # File handler (INFO+ for cleaner output)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(fmt)
    root_logger.addHandler(file_handler)

    # Console handler (INFO+ for cleaner output)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(fmt)
    root_logger.addHandler(console_handler)