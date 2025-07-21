import asyncio
from typing import Optional
from demo.code.config import PROXIES, get_image_path
from utils import Network, Tineye
from utils.model import TineyeItem, TineyeResponse

file = get_image_path("test.jpg")
show_unavailable_domains = False
domain = ""
tags = ""
sort = "score"
order = "desc"


async def demo_async() -> None:
    async with Network(proxies=PROXIES) as client:
        tineye = Tineye(client=client)
        resp = await tineye.search(
            file=file,
            show_unavailable_domains=show_unavailable_domains,
            domain=domain,
            tags=tags,
            sort=sort,
            order=order,
        )
        show_result(resp, "Initial Search")
        if resp.total_pages > 1:
            resp2 = await tineye.next_page(resp)
            show_result(resp2, "Next Page")
            if resp2:
                resp3 = await tineye.next_page(resp2)
                show_result(resp3, "Next Page")
                if resp3:
                    resp4 = await tineye.pre_page(resp3)
                    show_result(resp4, "Previous Page")


def show_result(resp: Optional[TineyeResponse], title: str = "") -> None:
    if resp and not resp.raw:
        print(f"Origin Response: {resp.origin}")
    if not resp or not resp.raw:
        print(f"{title}: No results found.")
        return
    lines = []
    for i, item in enumerate(resp.raw):
        lines.append("-" * 50)
        lines.append(show_match_details(i, item))
    print(*lines, "-" * 50, sep="\n")


def show_match_details(match_index: int, match_item: TineyeItem) -> str:
    return (
        f"原图链接: {match_item.image_url}\n"
        f"来源网页: {match_item.url}"
    )


if __name__ == "__main__":
    asyncio.run(demo_async())
