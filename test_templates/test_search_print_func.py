import asyncio
from model import BaseSearchModel


async def test_search_and_print():
    model = BaseSearchModel()
    await model.search_and_print(api="baidu", file="test_imgs/test_img.jpg")

if __name__ == "__main__":
    asyncio.run(test_search_and_print())