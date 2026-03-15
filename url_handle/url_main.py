from .video_parser import parse_video, detect_platform, get_supported_platforms


async def url_main(url: str) -> dict:
    """
    视频链接解析入口函数

    Args:
        url: 视频链接

    Returns:
        解析后的视频信息字典
    """
    # 检测平台
    platform = detect_platform(url)

    if not platform:
        supported = ", ".join(get_supported_platforms())
        raise ValueError(f"不支持的 URL，当前支持的平台: {supported}")

    # 解析视频
    result = await parse_video(url)
    print(f"解析成功: {result['title']} ({result['source']})")

    return result
