"""
视频解析通用模块
使用 videodl 库解析各种视频平台
"""

from videodl.modules.sources.bilibili import BilibiliVideoClient
from videodl.modules.sources.douyin import DouyinVideoClient
from videodl.modules.sources.xigua import XiguaVideoClient
from videodl.modules.sources.kuaishou import KuaishouVideoClient
from videodl.modules.sources.rednote import RednoteVideoClient
from videodl.modules.sources.weishi import WeishiVideoClient
from videodl.modules.sources.youtube import YouTubeVideoClient
from videodl.modules.sources.iqiyi import IQiyiVideoClient
from videodl.modules.sources.tencent import TencentVideoClient
from videodl.modules.sources.youku import YoukuVideoClient
from videodl.modules.sources.weibo import WeiboVideoClient
from .table import create_record

# 视频平台映射表
VIDEO_PLATFORMS = {
    # B站
    "bilibili": {
        "domains": ["bilibili.com", "b23.tv"],
        "client": BilibiliVideoClient,
        "source_name": "B站",
    },
    # 抖音
    "douyin": {
        "domains": ["douyin.com"],
        "client": DouyinVideoClient,
        "source_name": "抖音",
    },
    # 西瓜视频
    "xigua": {
        "domains": ["ixigua.com"],
        "client": XiguaVideoClient,
        "source_name": "西瓜视频",
    },
    # 快手
    "kuaishou": {
        "domains": ["kuaishou.com"],
        "client": KuaishouVideoClient,
        "source_name": "快手",
    },
    # 小红书
    "rednote": {
        "domains": ["rednote.com", "xiaohongshu.com"],
        "client": RednoteVideoClient,
        "source_name": "小红书",
    },
    # 微视
    "weishi": {
        "domains": ["weishi.com"],
        "client": WeishiVideoClient,
        "source_name": "微视",
    },
    # YouTube
    "youtube": {
        "domains": ["youtube.com", "youtu.be"],
        "client": YouTubeVideoClient,
        "source_name": "YouTube",
    },
    # 爱奇艺
    "iqiyi": {
        "domains": ["iqiyi.com"],
        "client": IQiyiVideoClient,
        "source_name": "爱奇艺",
    },
    # 腾讯视频
    "tencent": {
        "domains": ["v.qq.com"],
        "client": TencentVideoClient,
        "source_name": "腾讯视频",
    },
    # 优酷
    "youku": {
        "domains": ["youku.com"],
        "client": YoukuVideoClient,
        "source_name": "优酷",
    },
    # 微博
    "weibo": {
        "domains": ["weibo.com", "m.weibo.cn"],
        "client": WeiboVideoClient,
        "source_name": "微博",
    },
}


def detect_platform(url: str) -> str | None:
    """
    检测 URL 所属的视频平台

    Args:
        url: 视频链接

    Returns:
        平台名称，如果不支持返回 None
    """
    for platform_name, platform_info in VIDEO_PLATFORMS.items():
        for domain in platform_info["domains"]:
            if domain in url.lower():
                return platform_name
    return None


def parse_video_info(video_info: dict, source_name: str) -> dict:
    """
    解析视频信息，提取通用字段

    Args:
        video_info: videodl 返回的视频信息
        source_name: 平台名称

    Returns:
        解析后的视频信息字典
    """
    # 提取通用字段
    title = video_info.get("title", "")
    cover_url = video_info.get("cover_url", "")
    download_url = video_info.get("download_url", "")

    # 尝试从 raw_data 中提取更多信息
    raw_data = video_info.get("raw_data", {})

    # 不同平台的特殊字段处理
    description = ""
    pubdate = 0
    author = ""

    if source_name == "B站":
        view_data = raw_data.get("x/web-interface/view", {}).get("data", {})
        description = view_data.get("desc", "")
        pubdate = view_data.get("pubdate", 0)
        author = view_data.get("owner", {}).get("name", "")

    elif source_name == "抖音":
        # 抖音数据结构
        video_data = raw_data.get("loaderData", {}).get("video_(id)/page", {}).get("videoInfoRes", {}).get("item_list", [])
        if video_data:
            video = video_data[0]
            description = video.get("desc", "")
            pubdate = video.get("create_time", 0)
            author = video.get("author", {}).get("nickname", "")

    return {
        "title": title,
        "cover_url": cover_url,
        "download_url": download_url,
        "description": description,
        "pubdate": pubdate,
        "author": author,
        "source": source_name,
    }


async def parse_video(url: str) -> dict:
    """
    解析视频链接

    Args:
        url: 视频链接

    Returns:
        解析后的视频信息字典
    """
    platform = detect_platform(url)

    if not platform:
        raise ValueError(f"不支持的视频平台: {url}")

    platform_info = VIDEO_PLATFORMS[platform]
    client_class = platform_info["client"]
    source_name = platform_info["source_name"]

    # 创建客户端并解析
    client = client_class()
    info = client.parsefromurl(url)

    if not info or len(info) == 0:
        raise ValueError(f"无法解析视频: {url}")

    # 解析视频信息
    video_info = parse_video_info(info[0], source_name)

    # 写入飞书表格
    # TODO: 替换为实际的 app_token 和 table_id
    app_token = "BAeHbTgMLa2rqTsJBGKcYXe4n8e"
    table_id = "tblWnM504LF63nim"

    # 飞书 DateTime 字段需要毫秒时间戳
    pubdate_ms = video_info["pubdate"] * 1000 if video_info["pubdate"] else 0

    field = {
        "标题": video_info["title"],
        "作者": video_info["author"],
        "来源": video_info["source"],
        "发布日期": pubdate_ms,
        "主要内容": video_info["description"][:500] if video_info["description"] else "",
        "封面链接": {"text": video_info["cover_url"], "url": video_info["cover_url"]},
        "下载链接": {"text": video_info["download_url"], "url": video_info["download_url"]},
    }

    res = create_record(app_token, table_id, field)
    print(f"飞书表格写入结果: {res}")

    return video_info


def get_supported_platforms() -> list:
    """
    获取支持的视频平台列表

    Returns:
        支持的平台列表
    """
    return list(VIDEO_PLATFORMS.keys())
