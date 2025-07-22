from pathlib import Path
from typing import Any, Optional, Union
from utils import Network
from config import PROXIES, ENGINE_MAP, DEFAULT_PARAMS, DEFAULT_COOKIES


class BaseSearchModel:
    def __init__(self, proxies: Optional[str] = None, cookies: Optional[str] = None,
                 timeout: int = 60, **kwargs: Any):
        self.proxies = proxies
        self.cookies = cookies
        self.timeout = timeout
        self.config = kwargs

    async def search(self, api: str, file: Union[str, bytes, Path, None] = None,
                    url: Optional[str] = None, **kwargs: Any) -> str:
        if api not in ENGINE_MAP:
            available = ", ".join(ENGINE_MAP.keys())
            raise ValueError(f"不支持的引擎: {api}，支持的引擎: {available}")
        if not file and not url:
            raise ValueError("必须提供 file 或 url 参数")
        if file and url:
            raise ValueError("file 和 url 参数不能同时提供")
        try:
            engine_class = ENGINE_MAP[api]
            default_params = DEFAULT_PARAMS.get(api, {})
            search_params = {**default_params, **kwargs}
            network_kwargs = {}
            if self.proxies:
                network_kwargs["proxies"] = self.proxies
            effective_cookies = self.cookies or DEFAULT_COOKIES.get(api)
            if effective_cookies:
                network_kwargs["cookies"] = effective_cookies
            if self.timeout:
                network_kwargs["timeout"] = self.timeout
            async with Network(**network_kwargs) as client:
                if api == "ehentai":
                    is_ex = search_params.pop("is_ex", False)
                    engine_instance = engine_class(is_ex=is_ex, client=client)
                elif api == "saucenao":
                    api_key = search_params.pop("api_key")
                    hide = search_params.pop("hide", 3)
                    engine_instance = engine_class(api_key=api_key, hide=hide, client=client)
                elif api == "google_lens":
                    search_type = search_params.pop("search_type", "exact_matches")
                    hl = search_params.pop("hl", "en")
                    country = search_params.pop("country", "HK")
                    engine_instance = engine_class(client=client, search_type=search_type, hl=hl, country=country)
                else:
                    engine_instance = engine_class(client=client)
                response = await engine_instance.search(file=file, url=url, **search_params)
                return response.show_result()
        except Exception as e:
            return self._format_error(api, str(e))

    def _format_error(self, api: str, error_msg: str) -> str:
        if "list index out of range" in error_msg.lower():
            friendly_msg = "未搜索到相关信息"
        else:
            friendly_msg = error_msg

        return f"""{'=' * 50}
{api.upper()} 搜索失败
{'=' * 50}
错误信息: {friendly_msg}
{'=' * 50}"""

    @classmethod
    def get_supported_engines(cls) -> list[str]:
        return list(ENGINE_MAP.keys())
