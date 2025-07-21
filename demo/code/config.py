import sys
from pathlib import Path

from loguru import logger

USE_SIMPLE_LOGGER = True
PROXIES = "http://127.0.0.1:7897"

if USE_SIMPLE_LOGGER:
    logger.remove()
    logger.add(sys.stderr, format="<level>{level: <8}</level> <green>{message}</green>")  # pyright: ignore[reportUnusedCallResult]


def get_image_path(image_name: str) -> Path:
    return Path(__file__).parent.parent / "images" / image_name


__all__ = ["PROXIES", "get_image_path", "logger"]
