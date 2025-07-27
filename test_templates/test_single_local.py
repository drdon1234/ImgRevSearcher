import asyncio
from model import BaseSearchModel
from config_manager import get_cookie


test_file = "test_imgs/test_img.jpg"


async def test_single_engine():
    model = BaseSearchModel()
    print(f"{'=' * 30} 测试 Google Lens API {'=' * 30}")
    
    # 显示是否使用自动获取的cookie
    cookie = get_cookie("google_lens")
    print(f"使用{'自动获取' if cookie else '默认'}的Google Lens cookie")
    
    try:
        result = await model.search(api="google_lens", file=test_file)
        print(result)
    except Exception as e:
        print(f"❌ Google Lens 搜索失败: {e}")


if __name__ == "__main__":
    asyncio.run(test_single_engine())
