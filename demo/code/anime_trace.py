import asyncio

from demo.code.config import PROXIES, get_image_path, logger
from utils import AnimeTrace, Network
from utils.model import AnimeTraceResponse

file = get_image_path("test.jpg")


@logger.catch()
async def demo_async() -> None:
    async with Network(proxies=PROXIES) as client:
        anime_trace = AnimeTrace(client=client)
        resp = await anime_trace.search(file=file, model='full_game_model_kira')
        show_result(resp)

def show_result(resp: AnimeTraceResponse) -> None:
    lines = [f"是否为 AI 生成: {'是' if resp.ai else '否'}"]
    if resp.raw:
        if characters := resp.raw[0].characters:
            for character in characters:
                lines.append(f"作品名: {character.work}")
                lines.append(f"角色名: {character.name}")
    print("\n".join(lines))


if __name__ == "__main__":
    asyncio.run(demo_async())
