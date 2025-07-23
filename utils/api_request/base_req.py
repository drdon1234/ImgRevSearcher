from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar
from ..response_parser.base_parser import BaseSearchResponse
from ..network import RESP, HandOver
from ..types import FileContent

ResponseT = TypeVar("ResponseT")
T = TypeVar("T", bound=BaseSearchResponse[Any])


class BaseSearchReq(HandOver, ABC, Generic[T]):
    base_url: str

    def __init__(self, base_url: str, **request_kwargs: Any):
        super().__init__(**request_kwargs)
        self.base_url = base_url

    @abstractmethod
    async def search(
        self,
        url: Optional[str] = None,
        file: FileContent = None,
        **kwargs: Any,
    ) -> T:
        raise NotImplementedError

    async def _send_request(self, method: str, endpoint: str = "", url: str = "", **kwargs: Any) -> RESP:
        request_url = url or (f"{self.base_url}/{endpoint}" if endpoint else self.base_url)
        method = method.lower()
        if method == "get":
            kwargs.pop("files", None)
            return await self.get(request_url, **kwargs)
        elif method == "post":
            return await self.post(request_url, **kwargs)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
