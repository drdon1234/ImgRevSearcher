from utils.api_request import AnimeTrace, BaiDu, Bing, Copyseeker, EHentai, GoogleLens, SauceNAO, Tineye


PROXIES: str = "http://127.0.0.1:7897"

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

DEFAULT_PARAMS = {
    "anime_trace": {"model": "full_game_model_kira"},
    "baidu": {},
    "bing": {},
    "copyseeker": {},
    "ehentai": {"is_ex": False},
    "google_lens": {"search_type": "exact_matches", "hl": "en", "country": "HK"},
    "saucenao": {"api_key": "a4ab3f81009b003528f7e31aed187fa32a063f58", "hide": 3},
    "tineye": {"show_unavailable_domains": False, "domain": "", "tags": "", "sort": "score", "order": "desc"},
}

DEFAULT_COOKIES = {
    "anime_trace": None,
    "baidu": None,
    "bing": None,
    "copyseeker": None,
    "ehentai": None, # "ipb_member_id=; ipb_pass_hash=; igneous="
    "google_lens": "AEC=AVh_V2j1uy574ZdQHejl0WJ64XptEwJrMKAFHVh9Z6jWX2NC8USYut_F-Q; NID=525=CAWgxic9AizZ0Ss6iBoG8HF00e5E6qRk1e_t5cUcEGiDEFQgavZH2pIFg_TayKhhtzVYqAS_OAYQYztukxUTEkXYVY1IEUm8j5mDMP1deKuJ21D1Sx45a8vyRbfNx81SJ7AtuwPFGiELykCR1j89hlJzAIitP2A9VwXz0Gh3XKNY9E3eJTmaLUbtdfaQaaD2o-HbjqznBA07YoPdwEGL4uQpqAxFHA; DV=02HpwPZoP-Me0J-HU_sc0eeCc8Yvgxk",
    "saucenao": None,
    "tineye": None,
}


__all__ = ["PROXIES", "ENGINE_MAP", "DEFAULT_PARAMS", "DEFAULT_COOKIES"]
