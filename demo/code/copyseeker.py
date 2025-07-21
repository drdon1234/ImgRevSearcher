import asyncio

from demo.code.config import PROXIES, get_image_path
from utils import Copyseeker, Network
from utils.model import CopyseekerResponse

file = get_image_path("test.jpg")


async def demo_async() -> None:
    async with Network(proxies=PROXIES) as client:
        copyseeker = Copyseeker(client=client)
        resp = await copyseeker.search(file=file)
        show_result(resp)

def show_result(resp: CopyseekerResponse) -> None:
    lines = [
        "-" * 50,
        f"匹配图源：{resp.raw[0].url if resp.raw else '无'}",
        "相似图片："
    ]
    lines.extend([f"  {url}" for url in resp.similar_image_urls])
    lines.append("-" * 50)
    print('\n'.join(lines))


if __name__ == "__main__":
    asyncio.run(demo_async())
