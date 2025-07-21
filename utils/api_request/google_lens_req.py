from pathlib import Path
from typing import Any, Literal, Optional, Union
from pyquery import PyQuery
from typing_extensions import override
from ..response_parser import GoogleLensExactMatchesResponse, GoogleLensResponse
from ..network import RESP
from ..ext_tools import read_file
from .base_req import BaseSearchReq


class GoogleLens(BaseSearchReq[Union[GoogleLensResponse, GoogleLensExactMatchesResponse]]):
    def __init__(
        self,
        base_url: str = "https://lens.google.com",
        search_url: str = "https://www.google.com",
        search_type: Literal["all", "products", "visual_matches", "exact_matches"] = "all",
        q: Optional[str] = None,
        hl: str = "en",
        country: str = "US",
        **request_kwargs: Any,
    ):
        super().__init__(base_url, **request_kwargs)
        valid_search_types = ["all", "products", "visual_matches", "exact_matches"]
        if search_type not in valid_search_types:
            raise ValueError(f"Invalid search_type: {search_type}. Must be one of {valid_search_types}")
        if search_type == "exact_matches" and q:
            raise ValueError("Query parameter 'q' is not applicable for 'exact_matches' search_type.")
        self.search_url: str = search_url
        self.hl_param: str = f"{hl}-{country.upper()}"
        self.search_type: str = search_type
        self.q: Optional[str] = q

    async def _perform_image_search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        q: Optional[str] = None,
    ) -> RESP:
        params = {"hl": self.hl_param}
        if q and self.search_type != "exact_matches":
            params["q"] = q
        if file:
            endpoint = "v3/upload"
            filename = "image.jpg" if isinstance(file, bytes) else Path(file).name
            files = {"encoded_image": (filename, read_file(file), "image/jpeg")}
            resp = await self._send_request(
                method="post",
                endpoint=endpoint,
                params=params,
                files=files,
            )
        elif url:
            endpoint = "uploadbyurl"
            params["url"] = url
            resp = await self._send_request(
                method="post" if file else "get",
                endpoint=endpoint,
                params=params,
            )
        else:
            raise ValueError("Either 'url' or 'file' must be provided")
        dom = PyQuery(resp.text)
        exact_link = ""
        if self.search_type != "all":
            if udm_value := {
                "products": "37",
                "visual_matches": "44",
                "exact_matches": "48",
            }.get(self.search_type):
                exact_link = dom(f'a[href*="udm={udm_value}"]').attr("href") or ""
        if exact_link:
            return await self._send_request(method="get", url=f"{self.search_url}{exact_link}")
        return resp

    @override
    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        q: Optional[str] = None,
        **kwargs: Any,
    ) -> Union[GoogleLensResponse, GoogleLensExactMatchesResponse]:
        if q is not None and self.search_type == "exact_matches":
            q = None
        resp = await self._perform_image_search(url, file, q)
        if self.search_type == "exact_matches":
            return GoogleLensExactMatchesResponse(resp.text, resp.url)
        else:
            return GoogleLensResponse(resp.text, resp.url)
