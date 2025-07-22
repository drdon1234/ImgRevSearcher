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

"""
搜索参数说明

# AnimeTrace:
此方法支持三种搜索方式：
    1. 通过图片URL搜索
    2. 通过上传本地图片文件搜索  
    3. 通过提供base64编码图片搜索

参数：
    url (可选[str]): 要搜索的图片URL。
    file (Union[str, bytes, Path, None]): 本地图片文件，可以是路径字符串、字节数据或Path对象。
    base64 (可选[str]): Base64编码的图片数据。
    model (可选[str]): 要使用的识别模型，默认为None。
        可用模型：'anime_model_lovelive'、'pre_stable'、'anime'、'full_game_model_kira'。
    **kwargs (Any): 传递给请求的其他参数。

返回值：
    AnimeTraceResponse: 包含以下内容的对象：
        - 检测到的角色及其来源作品
        - 边界框坐标
        - 其他元数据（trace_id、AI检测标识）

异常：
    ValueError: 如果未提供`url`、`file`或`base64`中的任何一个。

注意：
    - 只能提供`url`、`file`或`base64`中的一个。
    - URL和base64搜索使用JSON POST请求。
    - 文件上传使用multipart/form-data POST请求。

# GoogleLens:
参数：
    base_url (str): Google Lens搜索的基础URL。默认为"https://lens.google.com"。
    search_url (str): Google搜索结果的基础URL。默认为"https://www.google.com"。
    search_type (Literal["all", "products", "visual_matches", "exact_matches"]): 要执行的搜索类型。
        默认为"all"。
    q (可选[str]): 搜索的可选查询参数。默认为None。不适用于'exact_matches'类型。
    hl (str): 语言的hl参数。默认为"en"。选项参见
        https://www.searchapi.io/docs/parameters/google/hl
    country (str): 区域设置的country参数。默认为"US"。选项参见
        https://www.searchapi.io/docs/parameters/google-lens/country
    **request_kwargs (Any): 网络请求的其他参数。

异常：
    ValueError: 如果search_type为'exact_matches'且提供了q参数。
    ValueError: 如果search_type不是'all'、'products'、'visual_matches'、'exact_matches'之一。

# Baidu:
此方法支持两种搜索方式：
    1. 通过图片URL搜索
    2. 通过上传本地图片文件搜索

搜索过程包含多个步骤：
    1. 上传图片或提交URL到百度
    2. 访问返回的URL获取搜索结果页面
    3. 从页面中提取和解析卡片数据
    4. 如果找到相似图片，获取详细结果

参数：
    url (可选[str]): 要搜索的图片URL。
    file (Union[str, bytes, Path, None]): 本地图片文件，可以是路径字符串、字节数据或Path对象。
    **kwargs (Any): 传递给父类的其他参数。

返回值：
    BaiDuResponse: 包含搜索结果和元数据的对象。
        如果未找到匹配项或存在'noresult'卡片，则返回空结果。

异常：
    ValueError: 如果既未提供`url`也未提供`file`。

注意：
    - 只能提供`url`或`file`中的一个。
    - 搜索过程涉及对百度API的多次HTTP请求。
    - 响应格式因是否找到匹配项而异。

# Bing:
此方法支持两种搜索方式：
    1. 通过图片URL搜索
    2. 通过上传本地图片文件搜索

参数：
    url (可选[str]): 要搜索的图片URL。
    file (Union[str, bytes, Path, None]): 本地图片文件，可以是路径字符串、字节数据或Path对象。
    **kwargs (Any): 传递给父类的其他参数。

返回值：
    BingResponse: 包含搜索结果和元数据的对象。

异常：
    ValueError: 如果既未提供`url`也未提供`file`。
    ValueError: 如果上传图片时无法找到BCID。

注意：
    - 只能提供`url`或`file`中的一个。
    - 搜索过程涉及对必应API的多次HTTP请求。

# Copyseeker:
此方法支持两种搜索方式：
    1. 通过图片URL搜索
    2. 通过上传本地图片文件搜索

搜索过程包含两个步骤：
    1. 获取发现ID
    2. 使用发现ID检索搜索结果

参数：
    url (可选[str]): 要搜索的图片URL。
    file (Union[str, bytes, Path, None]): 本地图片文件，可以是路径字符串、字节数据或Path对象。
    **kwargs (Any): 传递给父类的其他参数。

返回值：
    CopyseekerResponse: 包含搜索结果和元数据的对象。
        如果无法获得发现ID，则返回空响应。

异常：
    ValueError: 如果既未提供`url`也未提供`file`。

注意：
    - 只能提供`url`或`file`中的一个。
    - 搜索过程涉及对Copyseeker API的多次HTTP请求。

# EHentai/ExHentai:
此方法支持两种搜索方式：
    1. 通过图片URL搜索
    2. 通过上传本地图片文件搜索

参数：
    url (可选[str]): 要搜索的图片URL。
    file (Union[str, bytes, Path, None]): 本地图片文件，可以是路径字符串、字节数据或Path对象。
    **kwargs (Any): 传递给父类的其他参数。

返回值：
    EHentaiResponse: 包含搜索结果和元数据，包括：
        - 相似图库条目
        - 图库URL和标题
        - 相似度评分
        - 搜索结果中的其他元数据

异常：
    ValueError: 如果既未提供`url`也未提供`file`。
    RuntimeError: 如果在ExHentai上搜索时没有适当的身份验证。

注意：
    - 只能提供`url`或`file`中的一个。
    - 对于ExHentai搜索，必须在request_kwargs中提供有效的cookies。
    - 搜索行为受初始化时设置的covers、similar和exp标志影响。

# SauceNAO:
此方法支持两种搜索方式：
    1. 通过图片URL搜索
    2. 通过上传本地图片文件搜索

参数：
    url (可选[str]): 要搜索的图片URL。
    file (Union[str, bytes, Path, None]): 本地图片文件，可以是路径字符串、字节数据或Path对象。
    **kwargs (Any): 传递给父类的其他参数。

返回值：
    SauceNAOResponse: 包含以下内容的对象：
        - 带有相似度评分的搜索结果
        - 来源信息和缩略图
        - 其他元数据（状态码、搜索配额）

异常：
    ValueError: 如果既未提供`url`也未提供`file`。

注意：
    - 只能提供`url`或`file`中的一个。
    - API限制因账户类型和API密钥使用情况而异。
    - 免费账户限制为：
        * 每天150次搜索
        * 每30秒4次搜索
    - 结果按相似度评分降序排列。

# Tineye:
此方法支持两种搜索方式：
    1. 通过图片URL搜索
    2. 通过上传本地图片文件搜索

初始搜索后，检索匹配图片的域名信息。

参数：
    url (可选[str]): 要搜索的图片URL。
    file (Union[str, bytes, Path, None]): 要搜索的本地图片文件路径。
    show_unavailable_domains (bool): 是否包含来自不可用域名的结果。
        默认为False。
    domain (str): 过滤结果以仅包含来自此域名的匹配项（仅允许一个域名）。
        默认为""。
    sort (str): 结果的排序标准。可以是"size"、"score"或"crawl_date"。
        默认为"score"。
        - "score"（配合`order="desc"`）：最佳匹配优先（默认）。
        - "score"（配合`order="asc"`）：最多变化优先。
        - "crawl_date"（配合`order="desc"`）：最新图片优先。
        - "crawl_date"（配合`order="asc"`）：最旧图片优先。
        - "size"（配合`order="desc"`）：最大图片优先。
    order (str): 排序顺序。可以是"asc"（升序）或"desc"（降序）。默认为"desc"。
    tags (str): 逗号分隔的标签用于过滤结果。例如"stock,collection"。默认为""。
    **kwargs (Any): 传递给底层网络客户端的其他关键字参数。

返回值：
    TineyeResponse: 包含搜索结果、域名信息和元数据的`TineyeResponse`对象。

异常：
    ValueError: 如果既未提供`url`也未提供`file`。

注意：
    - 只能提供`url`或`file`中的一个。
"""