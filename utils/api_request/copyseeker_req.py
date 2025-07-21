from json import loads as json_loads
from pathlib import Path
from typing import Any, Optional, Union
from typing_extensions import override
from ..response_parser import CopyseekerResponse
from ..ext_tools import read_file
from .base_req import BaseSearchReq

COPYSEEKER_CONSTANTS = {
    "URL_SEARCH_TOKEN": "401c0a10f9d5aa3972a00e210283699640fbc08a21",
    "FILE_UPLOAD_TOKEN": "40e8441120d8ae3a0c72687eb64242d642081e8ddb",
    "SET_COOKIE_TOKEN": "0015445749632853586010cae7d4f7587b0a2eac4e",
    "GET_RESULTS_TOKEN": "40d33eda9b5e7a28d089feea4356d5925a1931b2f7"
}


class Copyseeker(BaseSearchReq[CopyseekerResponse]):
    def __init__(self, base_url: str = "https://copyseeker.net", **request_kwargs: Any):
        super().__init__(base_url, **request_kwargs)

    async def _get_discovery_id(
        self, url: Optional[str] = None, file: Union[str, bytes, Path, None] = None
    ) -> Optional[str]:
        headers = {"content-type": "text/plain;charset=UTF-8", "next-action": COPYSEEKER_CONSTANTS["SET_COOKIE_TOKEN"]}
        data = "[]"
        discovery_id = None
        await self._send_request(
            method="post",
            headers=headers,
            data=data,
        )
        if url:
            data = [{"discoveryType": "ReverseImageSearch", "imageUrl": url}]
            headers = {"next-action": COPYSEEKER_CONSTANTS["URL_SEARCH_TOKEN"]}
            resp = await self._send_request(
                method="post",
                headers=headers,
                json=data,
            )
        elif file:
            files = {
                "1_file": ("image.jpg", read_file(file), "image/jpeg"),
                "1_discoveryType": (None, "ReverseImageSearch"),
                "0": (None, '["$K1"]'),
            }
            headers = {"next-action": COPYSEEKER_CONSTANTS["FILE_UPLOAD_TOKEN"]}
            resp = await self._send_request(
                method="post",
                headers=headers,
                files=files,
            )
        if resp:
            for line in resp.text.splitlines():
                line = line.strip()
                if line.startswith("1:{"):
                    discovery_id = json_loads(line[2:]).get("discoveryId")
                    break
        return discovery_id

    @override
    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        **kwargs: Any,
    ) -> CopyseekerResponse:
        if not url and not file:
            raise ValueError("Either 'url' or 'file' must be provided")
        discovery_id = await self._get_discovery_id(url, file)
        if discovery_id is None:
            return CopyseekerResponse({}, "")
        data = [{"discoveryId": discovery_id, "hasBlocker": False}]
        headers = {"next-action": COPYSEEKER_CONSTANTS["GET_RESULTS_TOKEN"]}
        resp = await self._send_request(
            method="post",
            endpoint="discovery",
            headers=headers,
            json=data,
        )
        resp_json = {}
        for line in resp.text.splitlines():
            line = line.strip()
            if line.startswith("1:{"):
                resp_json = json_loads(line[2:])
                break
        return CopyseekerResponse(resp_json, resp.url)
