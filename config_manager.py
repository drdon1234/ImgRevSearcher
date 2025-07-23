import json
from pathlib import Path
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

CONFIG_FILE = Path(__file__).parent / "config.json"

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
        "google_lens": "AEC=AVh_V2hkwlmGyy-4B-rPZXcc6b0BRLbZMHRB3K3RQudJOfMNniBKHrFvhus; NID=525=fPc2vhi78mV9p7_Zy9EYX2w6POynvO6dA_gh6WgWeRunOgwCshviIrexMQnGq3oi58-t4U5LHLB5sQWN-Er6stXkbKz-UHtzX7MsGcnzjyaeN5COmfji5rfqzb6Omm0g4C0u1ztZgm7h--stbnM8x6zzYrWBMgiVs_2STsIZYd4h5xwZd-Eb97JdQ53QIxsm8bj91sKgjXVIJYuWzGxQ7OYvG0K5jl3ikXeNh3lvl17KsowpkMljgg2y03SsbZPlous; DV=owmVHxhdQYEX0J-HU_sc0eeyR4h5gxk",
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
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
    PROXIES = DEFAULT_CONFIG["proxies"]
    DEFAULT_PARAMS = DEFAULT_CONFIG["default_params"]
    DEFAULT_COOKIES = DEFAULT_CONFIG["default_cookies"]

__all__ = ["PROXIES", "ENGINE_MAP", "DEFAULT_PARAMS", "DEFAULT_COOKIES"]
