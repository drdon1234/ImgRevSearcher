import asyncio
from typing import Optional
import json

from demo.code.config import PROXIES, get_image_path
from utils import EHentai, Network
from utils.model import EHentaiResponse

file = get_image_path("test.jpg")

# Note: EXHentai search requires cookies if to be used
cookies: Optional[str] = "" # "ipb_member_id=; ipb_pass_hash=; yay=louder; igneous="

# Use EXHentai search or not, it's recommended to use bool(cookies), i.e. use EXHentai search if cookies is configured
is_ex = False

# Whenever possible, avoid timeouts that return an empty document
timeout = 60

async def demo_async() -> None:
    async with Network(proxies=PROXIES, cookies=cookies, timeout=timeout) as client:
        ehentai = EHentai(is_ex=is_ex, client=client)
        # resp = await ehentai.search(url=url)
        resp = await ehentai.search(file=file)
        show_result(resp)


def show_result(resp: EHentaiResponse, translations_file: str = "ehviewer_translations.json") -> None:
    with open(translations_file, 'r', encoding='utf-8') as f:
        translations = json.load(f)

    categorized_tags = {}

    for tag in resp.raw[0].tags:
        if ':' in tag:
            category, tag_name = tag.split(':', 1)

            category_cn = translations.get('rows', {}).get(category, category)

            tag_name_cn = tag_name
            if category in translations:
                tag_name_cn = translations[category].get(tag_name, tag_name)

            if category_cn not in categorized_tags:
                categorized_tags[category_cn] = []
            categorized_tags[category_cn].append(tag_name_cn)

    tag_lines = []
    for category, tags in categorized_tags.items():
        tag_line = f"{category}: {'; '.join(tags)}"
        tag_lines.append(tag_line)

    type_cn = translations.get('reclass', {}).get(resp.raw[0].type.lower(), resp.raw[0].type)

    lines = [
        "-" * 50,
        f"链接: {resp.raw[0].url}",
        f"上传时间: {resp.raw[0].date}",
        f"标题: {resp.raw[0].title}",
        f"类型: {type_cn}",
        f"页数: {resp.raw[0].pages}",
        "标签:",
    ]
    lines.extend([f"  {tag_line}" for tag_line in tag_lines])
    lines.append("-" * 50)

    print("\n".join(lines))


if __name__ == "__main__":
    asyncio.run(demo_async())