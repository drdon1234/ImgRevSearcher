import asyncio
from model import BaseSearchModel


test_url = "https://wallpaperaccess.com/full/7741398.jpg"


async def test_single_engine():
    model = BaseSearchModel()
    print(f"{'=' * 30} 测试 BAIDU API {'=' * 30}")
    try:
        result = await model.search(api="baidu", url=test_url)
        print(result)
    except Exception as e:
        print(f"❌ BAIDU 搜索失败: {e}")


if __name__ == "__main__":
    asyncio.run(test_single_engine())
