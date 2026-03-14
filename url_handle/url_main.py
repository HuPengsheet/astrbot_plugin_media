from .bili import bili_run


async def url_main(url: str) -> None:
    if url.startswith("https://www.bilibili.com/video/"):
        await bili_run(url)
    else:
        print("不支持的 URL")