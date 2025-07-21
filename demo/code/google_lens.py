import asyncio
from typing import Union
from demo.code.config import PROXIES, get_image_path
from utils import GoogleLens, Network
from utils.model import GoogleLensExactMatchesResponse, GoogleLensResponse

file = get_image_path("test.jpg")
cookies = "AEC=AVh_V2js0n1JT6JiPSstZJIHs0OvhRX9QTmHhjLrfrlREatNPLw9tM6WHU8; NID=525=ITCtMZSsSt437frcz5GWljMHdYDFvlxA5UotRrp1MHUw7cPj-ICk56tXZAs5hcvDieDgP4NN5RHXO68nUmXkJCuEKWYLU8sgL8heXQ7h33ZM6eNorLdz2cu-LgJbZrRfyfB4QQ9QGzW-TRTtsohitXydkg909mB2dbBwRZPk_9QvzRlEasrR6LXKoQuG_6rTb1GVruJFFoyZBmK-_CoIJiBdhRc1728TTcZ1yXcSwLHgY7bxj9fCUZRzHgs3FOs9W2Sd4s46epFDAdxBFuLU_V7kUQ0ny51gyfipDyWfyENtCrsocil5xGk8HVcbAA"


async def demo_async() -> None:
    async with Network(proxies=PROXIES, cookies=cookies) as client:
        google_lens_exact = GoogleLens(client=client, search_type="exact_matches", hl="en", country="HK")
        resp_all = await google_lens_exact.search(file=file)
        show_result(resp_all, search_type="exact_matches")


def show_result(resp: Union[GoogleLensResponse, GoogleLensExactMatchesResponse], search_type: str) -> None:
    if not isinstance(resp, GoogleLensResponse) and resp.raw:
        lines = ["精确匹配的结果:", "-" * 50]
        for item in resp.raw:
            lines.append(f"标题: {item.title}")
            lines.append(f"链接: {item.url}")
            lines.append("-" * 50)
        print("\n".join(lines))


if __name__ == "__main__":
    asyncio.run(demo_async())
