import asyncio
from model import BaseSearchModel


test_file = "test_img.jpg"


async def test_single_engine():
    model = BaseSearchModel()

    print(f"{'=' * 30} 测试 BAIDU API {'=' * 30}")
    try:
        result = await model.search(api="baidu", file=test_file)
        print(result)
    except Exception as e:
        print(f"❌ BAIDU 搜索失败: {e}")


if __name__ == "__main__":
    asyncio.run(test_single_engine())
