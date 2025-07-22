import json
import os
from utils.api_request import AnimeTrace, BaiDu, Bing, Copyseeker, EHentai, GoogleLens, SauceNAO, Tineye


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

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

DEFAULT_CONFIG = {
    "proxies": "http://127.0.0.1:7897",
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
            "country": "HK"
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
        "google_lens": "AEC=AVh_V2j1uy574ZdQHejl0WJ64XptEwJrMKAFHVh9Z6jWX2NC8USYut_F-Q; NID=525=CAWgxic9AizZ0Ss6iBoG8HF00e5E6qRk1e_t5cUcEGiDEFQgavZH2pIFg_TayKhhtzVYqAS_OAYQYztukxUTEkXYVY1IEUm8j5mDMP1deKuJ21D1Sx45a8vyRbfNx81SJ7AtuwPFGiELykCR1j89hlJzAIitP2A9VwXz0Gh3XKNY9E3eJTmaLUbtdfaQaaD2o-HbjqznBA07YoPdwEGL4uQpqAxFHA; DV=02HpwPZoP-Me0J-HU_sc0eeCc8Yvgxk",
        "saucenao": None,
        "tineye": None,
    }
}

try:
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    PROXIES = config.get("proxies", DEFAULT_CONFIG["proxies"])
    DEFAULT_PARAMS = config.get("default_params", DEFAULT_CONFIG["default_params"])
    DEFAULT_COOKIES = config.get("default_cookies", DEFAULT_CONFIG["default_cookies"])
except (FileNotFoundError, json.JSONDecodeError):
    print(f"配置文件 {CONFIG_FILE} 不存在或格式错误，使用默认配置。")
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
    PROXIES = DEFAULT_CONFIG["proxies"]
    DEFAULT_PARAMS = DEFAULT_CONFIG["default_params"]
    DEFAULT_COOKIES = DEFAULT_CONFIG["default_cookies"]

__all__ = ["PROXIES", "ENGINE_MAP", "DEFAULT_PARAMS", "DEFAULT_COOKIES"]
