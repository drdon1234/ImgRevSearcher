import asyncio
from demo.code.config import PROXIES, get_image_path
from utils import Network, SauceNAO
from utils.model import SauceNAOResponse

file = get_image_path("test.jpg")
api_key = "a4ab3f81009b003528f7e31aed187fa32a063f58"


async def demo_async() -> None:
    async with Network(proxies=PROXIES) as client:
        saucenao = SauceNAO(api_key=api_key, hide=3, client=client)
        resp = await saucenao.search(file=file)
        show_result(resp)


def show_result(resp: SauceNAOResponse) -> None:
    result = (
        "-" * 50 +
        f"\n相似度: {resp.raw[0].similarity}%\n"
        f"标题: {resp.raw[0].title}\n"
        f"作者: {resp.raw[0].author}\n"
        f"作者链接: {resp.raw[0].author_url}\n"
        f"作者链接（备用）: {resp.raw[0].source}\n"
        f"作品链接: {resp.raw[0].url}\n"
        f"更多相关链接: {resp.raw[0].ext_urls}\n"
        + "-" * 50
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(demo_async())
