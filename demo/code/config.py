from pathlib import Path

PROXIES = "http://127.0.0.1:7897"


def get_image_path(image_name: str) -> Path:
    return Path(__file__).parent.parent / "images" / image_name


__all__ = ["PROXIES", "get_image_path"]
