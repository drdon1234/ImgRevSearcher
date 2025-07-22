from typing import Any, Optional
from typing_extensions import override
from .base_parser import BaseResParser, BaseSearchResponse


class SauceNAOItem(BaseResParser):
    def __init__(self, data: dict[str, Any], **kwargs: Any):
        super().__init__(data, **kwargs)

    @override
    def _parse_data(self, data: dict[str, Any], **kwargs: Any) -> None:
        header = data["header"]
        self.similarity: float = float(header["similarity"])
        self.thumbnail: str = header["thumbnail"]
        self.index_id: int = header["index_id"]
        self.index_name: str = header["index_name"]
        self.hidden: int = header.get("hidden", 0)
        self.title: str = self._get_title(data["data"])
        self.url: str = self._get_url(data["data"])
        self.ext_urls: list[str] = data["data"].get("ext_urls", [])
        self.author: str = self._get_author(data["data"])
        self.author_url: str = self._get_author_url(data["data"])
        self.source: str = data["data"].get("source", "")

    @staticmethod
    def _get_title(data: dict[str, Any]) -> str:
        return (
            next(
                (
                    data[i]
                    for i in [
                        "title",
                        "material",
                        "jp_name",
                        "eng_name",
                        "source",
                        "created_at",
                    ]
                    if i in data and data[i]
                ),
                "",
            )
            or ""
        )

    @staticmethod
    def _get_url(data: dict[str, Any]) -> str:
        if "pixiv_id" in data:
            return f"https://www.pixiv.net/artworks/{data['pixiv_id']}"
        elif "pawoo_id" in data:
            return f"https://pawoo.net/@{data['pawoo_user_acct']}/{data['pawoo_id']}"
        elif "getchu_id" in data:
            return f"https://www.getchu.com/soft.phtml?id={data['getchu_id']}"
        elif "ext_urls" in data:
            return data["ext_urls"][0]
        return ""

    @staticmethod
    def _get_author(data: dict[str, Any]) -> str:
        return (
            next(
                (
                    (", ".join(data[i]) if i == "creator" and isinstance(data[i], list) else data[i])
                    for i in [
                        "author",
                        "member_name",
                        "creator",
                        "twitter_user_handle",
                        "pawoo_user_display_name",
                        "author_name",
                        "user_name",
                        "artist",
                        "company",
                    ]
                    if i in data and data[i]
                ),
                "",
            )
            or ""
        )

    @staticmethod
    def _get_author_url(data: dict[str, Any]) -> str:
        if "pixiv_id" in data:
            return f"https://www.pixiv.net/users/{data['member_id']}"
        elif "seiga_id" in data:
            return f"https://seiga.nicovideo.jp/user/illust/{data['member_id']}"
        elif "nijie_id" in data:
            return f"https://nijie.info/members.php?id={data['member_id']}"
        elif "bcy_id" in data:
            return f"https://bcy.net/u/{data['member_id']}"
        elif "tweet_id" in data:
            return f"https://twitter.com/intent/user?user_id={data['twitter_user_id']}"
        elif "pawoo_user_acct" in data:
            return f"https://pawoo.net/@{data['pawoo_user_acct']}"
        return str(data.get("author_url", ""))


class SauceNAOResponse(BaseSearchResponse[SauceNAOItem]):
    def __init__(self, resp_data: dict[str, Any], resp_url: str, **kwargs: Any) -> None:
        super().__init__(resp_data, resp_url, **kwargs)

    @override
    def _parse_response(self, resp_data: dict[str, Any], **kwargs: Any) -> None:
        self.status_code: int = resp_data["status_code"]
        header = resp_data["header"]
        results = resp_data.get("results", [])
        self.raw: list[SauceNAOItem] = [SauceNAOItem(i) for i in results]
        self.short_remaining: Optional[int] = header.get("short_remaining")
        self.long_remaining: Optional[int] = header.get("long_remaining")
        self.user_id: Optional[int] = header.get("user_id")
        self.account_type: Optional[int] = header.get("account_type")
        self.short_limit: Optional[str] = header.get("short_limit")
        self.long_limit: Optional[str] = header.get("long_limit")
        self.status: Optional[int] = header.get("status")
        self.results_requested: Optional[int] = header.get("results_requested")
        self.search_depth: Optional[int] = header.get("search_depth")
        self.minimum_similarity: Optional[float] = header.get("minimum_similarity")
        self.results_returned: Optional[int] = header.get("results_returned")
        self.url: str = f"https://saucenao.com/search.php?url=https://saucenao.com{header.get('query_image_display')}"

    def show_result(self) -> str:
        if self.raw:
            result = ("-" * 50 + f"\n相似度: {self.raw[0].similarity}%\n"
                     f"标题: {self.raw[0].title}\n" f"作者: {self.raw[0].author}\n"
                     f"作者链接: {self.raw[0].author_url}\n" f"作者链接（备用）: {self.raw[0].source}\n"
                     f"作品链接: {self.raw[0].url}\n" f"更多相关链接: {self.raw[0].ext_urls}\n" + "-" * 50)
            return result
        return "未找到匹配结果"
