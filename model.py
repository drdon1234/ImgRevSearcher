from pathlib import Path
from typing import Any, Optional, Union
import datetime
from utils import Network
from config_manager import PROXIES, ENGINE_MAP, DEFAULT_PARAMS, DEFAULT_COOKIES

try:
    from PIL import Image, ImageDraw, ImageFont

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class BaseSearchModel:
    def __init__(self, proxies: Optional[str] = PROXIES, cookies: Optional[str] = None,
                 timeout: int = 60, **kwargs: Any):
        self.proxies = proxies
        self.cookies = cookies
        self.timeout = timeout
        self.config = kwargs

    async def search(self, api: str, file: Union[str, bytes, Path, None] = None,
                     url: Optional[str] = None, **kwargs: Any) -> str:
        if api not in ENGINE_MAP:
            available = ", ".join(ENGINE_MAP.keys())
            raise ValueError(f"不支持的引擎: {api}，支持的引擎: {available}")
        if not file and not url:
            raise ValueError("必须提供 file 或 url 参数")
        if file and url:
            raise ValueError("file 和 url 参数不能同时提供")
        try:
            engine_class = ENGINE_MAP[api]
            default_params = DEFAULT_PARAMS.get(api, {})
            search_params = {**default_params, **kwargs}
            network_kwargs = {}
            if self.proxies:
                network_kwargs["proxies"] = self.proxies
            effective_cookies = self.cookies or DEFAULT_COOKIES.get(api)
            if effective_cookies:
                network_kwargs["cookies"] = effective_cookies
            if self.timeout:
                network_kwargs["timeout"] = self.timeout
            async with Network(**network_kwargs) as client:
                if api == "anime_trace":
                    is_multi = search_params.pop("is_multi", None)
                    ai_detect = search_params.pop("ai_detect", None)
                    base64 = search_params.pop("base64", None)
                    model = search_params.pop("model", None)
                    engine_instance = engine_class(is_multi=is_multi, ai_detect=ai_detect, client=client)
                    if base64:
                        response = await engine_instance.search(base64=base64, model=model, **search_params)
                    else:
                        response = await engine_instance.search(file=file, url=url, model=model, **search_params)
                    return response.show_result()
                elif api == "ehentai":
                    is_ex = search_params.pop("is_ex", False)
                    covers = search_params.pop("covers", False)
                    similar = search_params.pop("similar", True)
                    exp = search_params.pop("exp", False)
                    engine_instance = engine_class(is_ex=is_ex, covers=covers, similar=similar, exp=exp, client=client)
                elif api == "saucenao":
                    api_key = search_params.pop("api_key")
                    hide = search_params.pop("hide", 3)
                    numres = search_params.pop("numres", 5)
                    minsim = search_params.pop("minsim", 30)
                    output_type = search_params.pop("output_type", 2)
                    testmode = search_params.pop("testmode", 0)
                    dbmask = search_params.pop("dbmask", None)
                    dbmaski = search_params.pop("dbmaski", None)
                    db = search_params.pop("db", 999)
                    dbs = search_params.pop("dbs", None)
                    engine_instance = engine_class(
                        api_key=api_key, hide=hide, numres=numres, minsim=minsim,
                        output_type=output_type, testmode=testmode, dbmask=dbmask,
                        dbmaski=dbmaski, db=db, dbs=dbs, client=client
                    )
                elif api == "google_lens":
                    search_type = search_params.pop("search_type", "exact_matches")
                    hl = search_params.pop("hl", "en")
                    country = search_params.pop("country", "HK")
                    q = search_params.get("q", None)
                    max_results = search_params.pop("max_results", 50)
                    engine_instance = engine_class(
                        client=client, search_type=search_type, hl=hl, country=country, q=q, max_results=max_results
                    )
                else:
                    engine_instance = engine_class(client=client)
                response = await engine_instance.search(file=file, url=url, **search_params)
                return response.show_result()
        except Exception as e:
            return self._format_error(api, str(e))

    async def search_and_print(self, api: str, file: Union[str, bytes, Path, None] = None,
                               url: Optional[str] = None, **kwargs: Any) -> None:
        try:
            result = await self.search(api=api, file=file, url=url, **kwargs)
            print(result)
        except Exception as e:
            print(f"❌ {api} 搜索失败: {e}")

    async def search_and_draw(self, api: str, file: Union[str, bytes, Path, None] = None,
                              url: Optional[str] = None, is_auto_save: bool = False, **kwargs: Any) -> Image.Image:
        if not PIL_AVAILABLE:
            raise ImportError("需要安装Pillow库以使用图像绘制功能，请运行: pip install pillow")
        try:
            result = await self.search(api=api, file=file, url=url, **kwargs)
            margin = 20
            lines = result.split('\n')
            base_dir = Path(__file__).parent
            font_path = str(base_dir / "resource/font/arialuni.ttf")
            try:
                font = ImageFont.truetype(font_path, 18)
                title_font = ImageFont.truetype(font_path, 24)
            except IOError:
                font = ImageFont.load_default()
                title_font = ImageFont.load_default()
            title_text = f"{api.upper()} 搜索结果"
            if hasattr(title_font, "getbbox"):
                title_width = title_font.getbbox(title_text)[2] + margin * 2
            else:
                title_width = title_font.getsize(title_text)[0] + margin * 2
            max_text_width = 0
            for line in lines:
                if hasattr(font, "getbbox"):
                    line_width = font.getbbox(line)[2] + margin * 2
                else:
                    line_width = font.getsize(line)[0] + margin * 2
                max_text_width = max(max_text_width, line_width)
            width = max(800, title_width, max_text_width)
            if hasattr(font, "getbbox"):
                line_height = max(25, font.getbbox("Ay")[3] + 7)
            else:
                line_height = max(25, font.getsize("Ay")[1] + 7)
            header_height = 60
            content_height = margin + line_height * len(lines)
            total_height = header_height + content_height
            img = Image.new('RGB', (width, total_height), color='white')
            draw = ImageDraw.Draw(img)
            draw.rectangle([(0, 0), (width, header_height)], fill='#4a6ea9')
            draw.text((margin, margin), title_text, font=title_font, fill='white')
            y_position = header_height + margin
            for line in lines:
                if line.startswith('='):
                    draw.line([(margin, y_position), (width - margin, y_position)], fill='#cccccc', width=1)
                else:
                    draw.text((margin, y_position), line, font=font, fill='black')
                y_position += line_height
            if is_auto_save:
                save_dir = Path("search_results")
                save_dir.mkdir(exist_ok=True)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{api}_{timestamp}.jpeg"
                save_path = save_dir / file_name
                img.save(save_path, "JPEG", quality=85)
            return img
        except Exception as e:
            width, height = 600, 200
            img = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(img)
            draw.rectangle([(0, 0), (width, 60)], fill='#e74c3c')
            try:
                font_path = str(Path(__file__).parent / "resource/font/arialuni.ttf")
                font = ImageFont.truetype(font_path, 18)
                title_font = ImageFont.truetype(font_path, 24)
            except IOError:
                font = ImageFont.load_default()
                title_font = ImageFont.load_default()
            margin = 20
            draw.text((margin, margin), f"{api.upper()} 搜索失败", font=title_font, fill='white')
            draw.text((margin, 80), f"错误信息: {str(e)}", font=font, fill='black')
            if is_auto_save:
                save_dir = Path("search_results")
                save_dir.mkdir(exist_ok=True)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{api}_error_{timestamp}.jpeg"
                save_path = save_dir / file_name
                img.save(save_path, "JPEG", quality=85)
            return img

    def _format_error(self, api: str, error_msg: str) -> str:
        if "list index out of range" in error_msg.lower():
            friendly_msg = "未搜索到相关信息"
        else:
            friendly_msg = error_msg
        return f"""{'=' * 50}
{api.upper()} 搜索失败
{'=' * 50}
错误信息: {friendly_msg}
{'=' * 50}"""

    @classmethod
    def get_supported_engines(cls) -> list[str]:
        return list(ENGINE_MAP.keys())
