from pathlib import Path
from typing import Any, Dict, Optional, Union
import json
from utils import Network
from config import PROXIES, ENGINE_MAP, DEFAULT_PARAMS, DEFAULT_COOKIES


class BaseSearchModel:
    def __init__(self, proxies: Optional[str] = PROXIES, cookies: Optional[str] = None,
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
                return self._format_result(api, response)
        except Exception as e:
            return self._format_error(api, str(e))

    def _format_result(self, api: str, response: Any) -> str:
        formatters = {
            "anime_trace": self._format_anime_trace,
            "baidu": self._format_baidu,
            "bing": self._format_bing,
            "copyseeker": self._format_copyseeker,
            "ehentai": self._format_ehentai,
            "google_lens": self._format_google_lens,
            "saucenao": self._format_saucenao,
            "tineye": self._format_tineye,
        }
        formatter = formatters.get(api)
        if formatter:
            return formatter(response)
        else:
            return self._format_generic(api, response)

    def _format_anime_trace(self, resp) -> str:
        lines = ["-" * 50, f"是否为 AI 生成: {'是' if resp.ai else '否'}", "-" * 50]
        if resp.raw:
            if characters := resp.raw[0].characters:
                for character in characters:
                    lines.append(f"作品名: {character.work}")
                    lines.append(f"角色名: {character.name}")
                    lines.append("-" * 50)
        return "\n".join(lines)

    def _format_baidu(self, resp) -> str:
        lines = ["-" * 50, "相关结果:", f"  链接: {resp.raw[0].url}"]
        if resp.exact_matches:
            lines.extend(["-" * 50, "最佳结果:", f"  标题: {resp.exact_matches[0].title}",
                         f"  链接: {resp.exact_matches[0].url}"])
        lines.append("-" * 50)
        return "\n".join(lines)

    def _format_bing(self, resp) -> str:
        lines = ["-" * 50]
        combined = (resp.pages_including or []) + (resp.visual_search or [])
        if combined:
            for item in combined:
                lines.append(f"标题：{item.name}")
                lines.append(f"页面链接：{item.url}")
                lines.append(f"图片链接：{item.image_url}")
                lines.append("-" * 50)
        if resp.best_guess:
            lines.append(f"最佳结果：{resp.best_guess}")
            lines.append("-" * 50)
        return '\n'.join(lines)

    def _format_copyseeker(self, resp) -> str:
        lines = ["-" * 50, f"匹配图源：{resp.raw[0].url if resp.raw else '无'}", "相似图片："]
        lines.extend([f"  {url}" for url in resp.similar_image_urls])
        lines.append("-" * 50)
        return '\n'.join(lines)

    def _format_ehentai(self, resp, translations_file: str = "resource/ehviewer_translations.json") -> str:
        try:
            with open(translations_file, 'r', encoding='utf-8') as f:
                translations = json.load(f)
        except:
            translations = {}
        categorized_tags = {}
        for tag in resp.raw[0].tags:
            if ':' in tag:
                category, tag_name = tag.split(':', 1)
                category_cn = translations.get('rows', {}).get(category, category)
                tag_name_cn = tag_name
                if category in translations:
                    tag_name_cn = translations[category].get(tag_name, tag_name)
                if category_cn not in categorized_tags:
                    categorized_tags[category_cn] = []
                categorized_tags[category_cn].append(tag_name_cn)
        tag_lines = []
        for category, tags in categorized_tags.items():
            tag_line = f"{category}: {'; '.join(tags)}"
            tag_lines.append(tag_line)
        type_cn = translations.get('reclass', {}).get(resp.raw[0].type.lower(), resp.raw[0].type)
        lines = ["-" * 50, f"链接: {resp.raw[0].url}", f"上传时间: {resp.raw[0].date}",
                f"标题: {resp.raw[0].title}", f"类型: {type_cn}", f"页数: {resp.raw[0].pages}", "标签:"]
        lines.extend([f"  {tag_line}" for tag_line in tag_lines])
        lines.append("-" * 50)
        return "\n".join(lines)

    def _format_google_lens(self, resp) -> str:
        if hasattr(resp, 'raw') and resp.raw:
            lines = ["精确匹配的结果:", "-" * 50]
            for item in resp.raw:
                lines.append(f"标题: {item.title}")
                lines.append(f"链接: {item.url}")
                lines.append("-" * 50)
            return "\n".join(lines)
        return "未找到精确匹配结果"

    def _format_saucenao(self, resp) -> str:
        if resp.raw:
            result = ("-" * 50 + f"\n相似度: {resp.raw[0].similarity}%\n"
                     f"标题: {resp.raw[0].title}\n" f"作者: {resp.raw[0].author}\n"
                     f"作者链接: {resp.raw[0].author_url}\n" f"作者链接（备用）: {resp.raw[0].source}\n"
                     f"作品链接: {resp.raw[0].url}\n" f"更多相关链接: {resp.raw[0].ext_urls}\n" + "-" * 50)
            return result
        return "未找到匹配结果"

    def _format_tineye(self, resp) -> str:
        if not resp or not resp.raw:
            return "未找到匹配结果"
        lines = []
        for i, item in enumerate(resp.raw):
            lines.append("-" * 50)
            lines.append(f"原图链接: {item.image_url}")
            lines.append(f"来源网页: {item.url}")
        lines.append("-" * 50)
        return "\n".join(lines)

    def _format_generic(self, engine_name: str, resp) -> str:
        lines = [f"{engine_name} 搜索结果", "-" * 50]
        if hasattr(resp, 'raw') and resp.raw:
            lines.append("找到结果")
        else:
            lines.append("未找到结果")
        lines.append("-" * 50)
        return "\n".join(lines)

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
