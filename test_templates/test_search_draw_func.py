import asyncio
from model import BaseSearchModel


async def test_search_and_draw():
    model = BaseSearchModel()
    await model.search_and_draw(api="baidu", file="test_imgs/test_img.jpg", is_auto_save=True)

if __name__ == "__main__":
    asyncio.run(test_search_and_draw())