import json
import time
from datetime import datetime
from pathlib import Path
from utils.api_request import AnimeTrace, BaiDu, Bing, Copyseeker, EHentai, GoogleLens, SauceNAO, Tineye
from utils.cookie_manager import GoogleImagesCookieExtractor


ENGINE_MAP = {
    "anime_trace": AnimeTrace,
    "baidu": BaiDu,
    "bing": Bing,
    "copyseeker": Copyseeker,
    "ehentai": EHentai,
    "google_lens": GoogleLens,
    "saucenao": SauceNAO,
    "tineye": Tineye,
}

CONFIG_FILE = Path(__file__).parent / "config.json"

DEFAULT_CONFIG = {
    "proxies": None, # "http://localhost:port"
    "default_params": {
        "anime_trace": {
            "model": "full_game_model_kira",
            "is_multi": None,
            "ai_detect": None,
            "base64": None
        },
        "baidu": {},
        "bing": {},
        "copyseeker": {},
        "ehentai": {
            "is_ex": False,
            "covers": False,
            "similar": True,
            "exp": False
        },
        "google_lens": {
            "search_type": "exact_matches",
            "q": None,
            "hl": "en",
            "country": "HK",
            "max_results": 50
        },
        "saucenao": {
            "api_key": "a4ab3f81009b003528f7e31aed187fa32a063f58",
            "hide": 3,
            "numres": 5,
            "minsim": 30,
            "output_type": 2,
            "testmode": 0,
            "dbmask": None,
            "dbmaski": None,
            "db": 999,
            "dbs": None
        },
        "tineye": {
            "show_unavailable_domains": False,
            "domain": "",
            "tags": "",
            "sort": "score",
            "order": "desc"
        },
    },
    "default_cookies": {
        "anime_trace": None,
        "baidu": None,
        "bing": None,
        "copyseeker": None,
        "ehentai": None, # "ipb_member_id=; ipb_pass_hash=; igneous="
        "google_lens": None,
        "saucenao": None,
        "tineye": None,
    },
    "cookie_manager": {
        "google_lens": {
            "auto_fetch": True,
            "use_remote": False,
            "remote_server": "http://localhost:4444/wd/hub",
            "update_interval": 43200,
            "last_update": ""
        }
    }
}


def load_config(config_path: Path = CONFIG_FILE) -> dict:
    """加载配置，如果配置文件不存在或格式错误则使用默认配置"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"配置文件 {config_path} 不存在或格式错误，使用默认配置。错误: {e}")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
        return DEFAULT_CONFIG


def save_config(config_data: dict, config_path: Path = CONFIG_FILE) -> None:
    """保存配置到文件"""
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)


def update_last_cookie_update_time(engine: str, config_data: dict = None) -> dict:
    """更新指定引擎的最后cookie更新时间"""
    if config_data is None:
        config_data = load_config()
    if "cookie_manager" in config_data and engine in config_data["cookie_manager"]:
        config_data["cookie_manager"][engine]["last_update"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        save_config(config_data)
    return config_data


def is_cookie_expired(engine: str, config_data: dict = None) -> bool:
    """检查指定引擎的cookie是否已过期"""
    if config_data is None:
        config_data = load_config()
    if "cookie_manager" not in config_data or engine not in config_data["cookie_manager"]:
        return False
    cookie_config = config_data["cookie_manager"][engine]
    last_update_str = cookie_config.get("last_update", "")
    if not last_update_str:
        return True
    try:
        last_update = datetime.strptime(last_update_str, "%Y/%m/%d %H:%M:%S")
        update_interval = cookie_config.get("update_interval", 3600)
        current_time = datetime.now()
        seconds_since_update = (current_time - last_update).total_seconds()
        return seconds_since_update >= update_interval
    except ValueError:
        return True


def get_cookie(engine: str) -> str:
    """获取指定引擎的cookie，如果配置为自动获取则尝试自动更新"""
    config_data = load_config()
    cookie = config_data.get("default_cookies", {}).get(engine)
    if "cookie_manager" in config_data and engine in config_data["cookie_manager"]:
        cookie_config = config_data["cookie_manager"][engine]
        if cookie_config.get("auto_fetch", False) and is_cookie_expired(engine, config_data):
            print(f"正在自动获取 {engine} 的cookie...")
            if engine == "google_lens":
                remote_addr = cookie_config.get("remote_server") if cookie_config.get("use_remote", False) else None
                extractor = GoogleImagesCookieExtractor(
                    remote_addr=remote_addr,
                    headless=True,
                    timeout=30
                )
                result = extractor.quick_run()
                if result and "cookie" in result:
                    cookie = result["cookie"]
                    # 更新配置文件中的cookie和最后更新时间
                    config_data["default_cookies"][engine] = cookie
                    config_data = update_last_cookie_update_time(engine, config_data)
                    save_config(config_data)
                    print(f"{engine} cookie 获取成功！")
                else:
                    print(f"{engine} cookie 获取失败，使用现有cookie")
    return cookie


config = load_config()
PROXIES = config.get("proxies", DEFAULT_CONFIG["proxies"])
DEFAULT_PARAMS = config.get("default_params", DEFAULT_CONFIG["default_params"])
DEFAULT_COOKIES = config.get("default_cookies", DEFAULT_CONFIG["default_cookies"])
COOKIE_MANAGER = config.get("cookie_manager", DEFAULT_CONFIG["cookie_manager"])

__all__ = ["PROXIES", "ENGINE_MAP", "DEFAULT_PARAMS", "DEFAULT_COOKIES", "COOKIE_MANAGER", "get_cookie"]
