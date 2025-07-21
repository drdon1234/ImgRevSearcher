from typing import Any
from pyquery import PyQuery
from typing_extensions import override
from ..ext_tools import parse_html
from .base_parser import BaseResParser, BaseSearchResponse


class EHentaiItem(BaseResParser):
    def __init__(self, data: PyQuery, **kwargs: Any):
        super().__init__(data, **kwargs)

    @override
    def _parse_data(self, data: PyQuery, **kwargs: Any) -> None:
        self._arrange(data)

    def _arrange(self, data: PyQuery) -> None:
        glink = data.find(".glink")
        self.title: str = glink.text()
        if glink.parent("div"):
            self.url: str = glink.parent("div").parent("a").attr("href")
        else:
            self.url = glink.parent("a").attr("href")
        thumbnail = data.find(".glthumb img") or data.find(".gl1e img") or data.find(".gl3t img")
        self.thumbnail: str = thumbnail.attr("data-src") or thumbnail.attr("src")
        _type = data.find(".cs") or data.find(".cn")
        self.type: str = _type.eq(0).text() or ""
        self.date: str = data.find("[id^='posted']").eq(0).text() or ""
        self.pages: str = "解析失败"
        if glink and len(glink) > 0:
            try:
                tr_element = glink.parent().parent().parent()
                if len(tr_element) > 0:
                    pages_div = tr_element.find(".gl4c div").filter(
                        lambda i, e: "pages" in PyQuery(e).text()
                    )
                    if len(pages_div) > 0:
                        pages_text = pages_div.eq(0).text().strip()
                        self.pages = pages_text.split()[0] if pages_text else "解析失败"
            except Exception:
                pass
        self.tags: list[str] = []
        for i in data.find("div[class=gt],div[class=gtl]").items():
            if tag := i.attr("title"):
                self.tags.append(tag)


class EHentaiResponse(BaseSearchResponse[EHentaiItem]):
    def __init__(self, resp_data: str, resp_url: str, **kwargs: Any):
        super().__init__(resp_data, resp_url, **kwargs)

    @override
    def _parse_response(self, resp_data: str, **kwargs: Any) -> None:
        data = parse_html(resp_data)
        self.origin: PyQuery = data
        if "No unfiltered results" in resp_data:
            self.raw: list[EHentaiItem] = []
        elif tr_items := data.find(".itg").children("tr").items():
            self.raw = [EHentaiItem(i) for i in tr_items if i.children("td")]
        else:
            gl1t_items = data.find(".itg").children(".gl1t").items()
            self.raw = [EHentaiItem(i) for i in gl1t_items]
