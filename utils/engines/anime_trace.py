from json import loads as json_loads
from pathlib import Path
from typing import Any, Optional, Union
from typing_extensions import override
from ..model import AnimeTraceResponse
from ..utils import read_file
from .base import BaseSearchEngine


class AnimeTrace(BaseSearchEngine[AnimeTraceResponse]):
    def __init__(
        self,
        base_url: str = "https://api.animetrace.com",
        endpoint: str = "v1/search",
        is_multi: Optional[int] = None,
        ai_detect: Optional[int] = None,
        **request_kwargs: Any,
    ):
        base_url = f"{base_url}/{endpoint}"
        super().__init__(base_url, **request_kwargs)
        self.is_multi: Optional[int] = is_multi
        self.ai_detect: Optional[int] = ai_detect

    @override
    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        base64: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs: Any,
    ) -> AnimeTraceResponse:
        params: dict[str, Any] = {}
        if self.is_multi:
            params["is_multi"] = self.is_multi
        if self.ai_detect:
            params["ai_detect"] = self.ai_detect
        if model:
            params["model"] = model
        if url:
            data = {"url": url, **params}
            resp = await self._send_request(
                method="post",
                json=data,
            )
        elif file:
            files = {"file": read_file(file)}
            resp = await self._send_request(
                method="post",
                files=files,
                data=params or None,
            )
        elif base64:
            data = {"base64": base64, **params}
            resp = await self._send_request(
                method="post",
                json=data,
            )
        else:
            raise ValueError("One of 'url', 'file', or 'base64' must be provided")
        return AnimeTraceResponse(json_loads(resp.text), resp.url)
