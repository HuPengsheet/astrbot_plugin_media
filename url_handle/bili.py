import re
import asyncio
from bilibili_api import video
from table import create_record


def extract_bvid(url: str) -> str | None:
    """从 B 站视频 URL 或字符串中提取 BV 号。"""
    # BV 号格式: BV + 10 位字母数字（Base58）
    match = re.search(r'BV[a-zA-Z0-9]{10}', url)
    return match.group(0) if match else None


async def bili_url_content(bvid: str) -> None:
    # 实例化 Video 类
    v = video.Video(bvid=bvid)
    # 获取信息
    info = await v.get_info()
    data = info["pubdate"]
    field = {"标题":info["title"],"作者":info["owner"]["name"],"来源":"B站","发布时间":data,"主要内容":"","封面链接":""}
    res = create_record("BAeHbTgMLa2rqTsJBGKcYXe4n8e","tblWnM504LF63nim",field)
    print(res)
    return info




def bili_run(url: str) -> None:
    bvid = extract_bvid(url)
    if not bvid:
        raise ValueError(f"无法从 URL 中提取 BV 号: {url}")
    res = asyncio.run(bili_url_content(bvid))
    print(res)
