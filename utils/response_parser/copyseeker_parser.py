from typing import Any, Optional
from typing_extensions import override
from .base_parser import BaseResParser, BaseSearchResponse


class CopyseekerItem(BaseResParser):
    def __init__(self, data: dict[str, Any], **kwargs: Any):
        super().__init__(data, **kwargs)

    @override
    def _parse_data(self, data: dict[str, Any], **kwargs: Any) -> None:
        self.url: str = data["url"]
        self.title: str = data["title"]
        self.thumbnail: str = data.get("mainImage", "")
        self.thumbnail_list: list[str] = data.get("otherImages", [])
        self.website_rank: float = data.get("rank", 0.0)


class CopyseekerResponse(BaseSearchResponse[CopyseekerItem]):
    def __init__(self, resp_data: dict[str, Any], resp_url: str, **kwargs: Any) -> None:
        super().__init__(resp_data, resp_url, **kwargs)

    @override
    def _parse_response(self, resp_data: dict[str, Any], **kwargs: Any) -> None:
        self.id: str = resp_data["id"]
        self.image_url: str = resp_data["imageUrl"]
        self.best_guess_label: Optional[str] = resp_data.get("bestGuessLabel")
        self.entities: Optional[str] = resp_data.get("entities")
        self.total: int = resp_data["totalLinksFound"]
        self.exif: dict[str, Any] = resp_data.get("exif", {})
        self.raw: list[CopyseekerItem] = [CopyseekerItem(page) for page in resp_data.get("pages", [])]
        self.similar_image_urls: list[str] = resp_data.get("visuallySimilarImages", [])
        
    def show_result(self) -> str:
        lines = ["-" * 50]
        if self.raw:
            lines.append(f"匹配图源：{self.raw[0].url}")
        else:
            lines.append("匹配图源：无")
            
        lines.append("相似图片：")
        for i, url in enumerate(self.similar_image_urls, 1):
            lines.append(f"  #{i} {url}")
        lines.append("-" * 50)
        return '\n'.join(lines)
