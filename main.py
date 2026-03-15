from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from .url_handle.url_main import url_main
import re

@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("astrbot_plugin_media")
    async def run(self, event: AstrMessageEvent):
        """解析视频链接并写入飞书表格"""
        message_str = event.message_str  # 用户发的纯文本消息字符串

        # 提取所有 URL
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, message_str)

        if not urls:
            yield event.plain_result("未检测到视频链接，请输入有效的 URL")
            return

        results = []
        for url in urls:
            try:
                result = await url_main(url)
                results.append(f"✓ 解析成功: {result['title']} ({result['source']})")
            except Exception as e:
                results.append(f"✗ 解析失败: {url} - {str(e)}")

        # 返回结果
        result_text = "\n".join(results)
        yield event.plain_result(f"视频解析结果:\n{result_text}")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用该方法。"""
