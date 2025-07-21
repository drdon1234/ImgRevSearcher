import asyncio

from demo.code.config import PROXIES, get_image_path
from utils import Bing, Network
from utils.model import BingResponse

file = get_image_path("test.jpg")


async def demo_async() -> None:
    async with Network(proxies=PROXIES) as client:
        bing = Bing(client=client)
        resp = await bing.search(file=file)
        show_result(resp)

def show_result(resp: BingResponse) -> None:
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

    print('\n'.join(lines))


if __name__ == "__main__":
    asyncio.run(demo_async())
