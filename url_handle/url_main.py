from .bili import bili_run


def url_main(url: str) -> None:
    if url.startswith("https://www.bilibili.com/video/"):
        bili_run(url)
    else:
        print("不支持的 URL")