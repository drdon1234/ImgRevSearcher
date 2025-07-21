from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


class DomainTag(str, Enum):
    STOCK = "stock"
    COLLECTION = "collection"


@dataclass
class DomainInfo:
    domain: str
    count: int
    tag: Optional[DomainTag] = None

    @classmethod
    def from_raw_data(cls, data: list[Any]) -> "DomainInfo":
        domain_name = str(data[0])
        count = int(data[1])
        tag = DomainTag(data[2][0]) if data[2] else None
        return cls(domain=domain_name, count=count, tag=tag)
