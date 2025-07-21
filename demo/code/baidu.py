import asyncio

from demo.code.config import get_image_path
from utils import BaiDu, Network
from utils.model import BaiDuResponse

file = get_image_path("test.jpg")

async def demo_async() -> None:
    async with Network() as client:
        baidu = BaiDu(client=client)
        resp = await baidu.search(file=file)
        show_result(resp)

def show_result(resp: BaiDuResponse) -> None:
    lines = [
        "-" * 50,
        "相关结果:",
        f"  链接: {resp.raw[0].url}",
    ]
    if resp.exact_matches:
        lines.extend([
            "-" * 50,
            "最佳结果:",
            f"  标题: {resp.exact_matches[0].title}",
            f"  链接: {resp.exact_matches[0].url}",
        ])
    lines.append("-" * 50)
    print("\n".join(lines))


if __name__ == "__main__":
    asyncio.run(demo_async())
