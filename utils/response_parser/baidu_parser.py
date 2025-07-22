from typing import Any
from typing_extensions import override
from ..ext_tools import deep_get
from .base_parser import BaseResParser, BaseSearchResponse


class BaiDuItem(BaseResParser):
    def __init__(self, data: dict[str, Any], **kwargs: Any) -> None:
        super().__init__(data, **kwargs)

    @override
    def _parse_data(self, data: dict[str, Any], **kwargs: Any) -> None:
        self.title: str = deep_get(data, "title[0]") or ""
        self.thumbnail: str = data.get("image_src") or data.get("thumbUrl") or ""
        self.url: str = data.get("url") or data.get("fromUrl") or ""


class BaiDuResponse(BaseSearchResponse[BaiDuItem]):
    def __init__(self, resp_data: dict[str, Any], resp_url: str, **kwargs: Any):
        super().__init__(resp_data, resp_url, **kwargs)

    @override
    def _parse_response(self, resp_data: dict[str, Any], **kwargs: Any) -> None:
        self.raw: list[BaiDuItem] = []
        self.exact_matches: list[BaiDuItem] = []
        if same_data := resp_data.get("same"):
            if "list" in same_data:
                self.exact_matches.extend(BaiDuItem(i) for i in same_data["list"] if "url" in i and "image_src" in i)
        if data_list := deep_get(resp_data, "data.list"):
            self.raw.extend([BaiDuItem(i) for i in data_list])
            
    def show_result(self) -> str:
        lines = ["-" * 50, "相关结果:"]
        if self.raw:
            for idx, item in enumerate(self.raw, 1):
                lines.append(f"结果 #{idx}")
                lines.append(f"链接: {item.url}")
        else:
            lines.append("  无")
            
        if self.exact_matches:
            lines.extend(["-" * 50, "最佳结果:"])
            for idx, item in enumerate(self.exact_matches, 1):
                lines.append(f"结果 #{idx}")
                lines.append(f"  标题: {item.title}")
                lines.append(f"  链接: {item.url}")
                lines.append("-" * 50)
        return "\n".join(lines)
