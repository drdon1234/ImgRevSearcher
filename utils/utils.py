import re
from pathlib import Path
from typing import Any, Optional, Union
from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery


def deep_get(dictionary: dict[str, Any], keys: str) -> Optional[Any]:
    for key in keys.split("."):
        if list_search := re.search(r"(\S+)?\[(\d+)]", key):
            try:
                if list_search[1]:
                    dictionary = dictionary[list_search[1]]
                dictionary = dictionary[int(list_search[2])]
            except (KeyError, IndexError):
                return None
        else:
            try:
                dictionary = dictionary[key]
            except (KeyError, TypeError):
                return None
    return dictionary


def read_file(file: Union[str, bytes, Path]) -> bytes:
    if isinstance(file, bytes):
        return file
    if not Path(file).exists():
        raise FileNotFoundError(f"The file {file} does not exist.")
    try:
        with open(file, "rb") as f:
            return f.read()
    except OSError as e:
        raise OSError(f"An I/O error occurred while reading the file {file}: {e}") from e


def parse_html(html: str) -> PyQuery:
    utf8_parser = HTMLParser(encoding="utf-8")
    return PyQuery(fromstring(html, parser=utf8_parser))
