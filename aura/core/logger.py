"""Centralized logging configuration for AURA."""

from __future__ import annotations

import logging
from pathlib import Path

_LOGGER_NAME = "aura"


def configure_logging(
    level: str = "INFO",
    log_directory: Path = Path("data/logs"),
) -> logging.Logger:
    """Configure and return the AURA logger."""
    logger = logging.getLogger(_LOGGER_NAME)

    if logger.handlers:
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        return logger

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    log_directory.mkdir(parents=True, exist_ok=True)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        log_directory / "aura.log",
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger