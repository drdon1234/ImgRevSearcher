import re
from pathlib import Path
from typing import Any, Optional, Union
from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery


def deep_get(dictionary: dict[str, Any], keys: str) -> Optional[Any]:
    for key in keys.split("."):
        match = re.search(r"(\S+)?\[(\d+)]", key)
        try:
            if match:
                if match[1]:
                    dictionary = dictionary[match[1]]
                dictionary = dictionary[int(match[2])]
            else:
                dictionary = dictionary[key]
        except (KeyError, IndexError, TypeError):
            return None
    return dictionary


def read_file(file: Union[str, bytes, Path]) -> bytes:
    if isinstance(file, bytes):
        return file
    try:
        return Path(file).read_bytes()
    except (FileNotFoundError, OSError) as e:
        error_type = "FileNotFoundError" if isinstance(e, FileNotFoundError) else "OSError"
        raise type(e)(f"{error_type}：读取文件 {file} 时出错: {e}") from e


def parse_html(html: str) -> PyQuery:
    utf8_parser = HTMLParser(encoding="utf-8")
    return PyQuery(fromstring(html, parser=utf8_parser))
