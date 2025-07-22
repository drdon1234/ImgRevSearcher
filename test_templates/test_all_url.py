import asyncio
from model import BaseSearchModel


test_url = "https://wallpaperaccess.com/full/7741398.jpg"


async def test_all_engines():
    model = BaseSearchModel()
    engines = model.get_supported_engines()
    print(f"支持的引擎数量: {len(engines)}")
    print(f"引擎列表: {', '.join(engines)}\n")

    for api in engines:
        print(f"{'=' * 30} 测试 {api.upper()} API {'=' * 30}")
        try:
            result = await model.search(api=api, url=test_url)
            print(result)
        except Exception as e:
            print(f"❌ {api} 搜索失败: {e}")
        print()


if __name__ == "__main__":
    asyncio.run(test_all_engines())
