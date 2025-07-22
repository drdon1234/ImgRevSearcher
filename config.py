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
    "google_lens": "AEC=AVh_V2js0n1JT6JiPSstZJIHs0OvhRX9QTmHhjLrfrlREatNPLw9tM6WHU8; NID=525=ITCtMZSsSt437frcz5GWljMHdYDFvlxA5UotRrp1MHUw7cPj-ICk56tXZAs5hcvDieDgP4NN5RHXO68nUmXkJCuEKWYLU8sgL8heXQ7h33ZM6eNorLdz2cu-LgJbZrRfyfB4QQ9QGzW-TRTtsohitXydkg909mB2dbBwRZPk_9QvzRlEasrR6LXKoQuG_6rTb1GVruJFFoyZBmK-_CoIJiBdhRc1728TTcZ1yXcSwLHgY7bxj9fCUZRzHgs3FOs9W2Sd4s46epFDAdxBFuLU_V7kUQ0ny51gyfipDyWfyENtCrsocil5xGk8HVcbAA",
    "saucenao": None,
    "tineye": None,
}


__all__ = ["PROXIES", "ENGINE_MAP", "DEFAULT_PARAMS", "DEFAULT_COOKIES"]
