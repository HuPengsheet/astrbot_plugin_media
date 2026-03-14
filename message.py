"""
飞书 IM 消息 API 封装
参考文档: feishu-open-docs/im-v1/message/
"""
import json
from typing import Any, Dict, Optional

import lark_oapi as lark
from lark_oapi.api.im.v1 import *

from .client import feishu_client


def _infer_receive_id_type(receive_id: str) -> str:
    """根据 receive_id 前缀推断 ID 类型。oc_=群聊, ou_=用户 open_id, on_=union_id"""
    if not receive_id:
        return "chat_id"
    if receive_id.startswith("oc_"):
        return "chat_id"
    if receive_id.startswith("ou_"):
        return "open_id"
    if receive_id.startswith("on_"):
        return "union_id"
    if receive_id.startswith("u-") or (len(receive_id) > 10 and "@" not in receive_id):
        return "user_id"
    if "@" in receive_id and "." in receive_id:
        return "email"
    return "chat_id"


def _parse_response(response: lark.BaseResponse) -> Dict[str, Any]:
    """解析响应，返回完整 json 数据。code 为 0 表示成功。"""
    json_data = json.loads(response.raw.content)
    return json_data


def send_message(
    receive_id: str,
    content: str,
    msg_type: str = "text",
    receive_id_type: Optional[str] = None,
    uuid: Optional[str] = None,
) -> Dict[str, Any]:
    """
    发送消息。
    receive_id: 消息接收者 ID（群 chat_id 以 oc_ 开头，用户 open_id 以 ou_ 开头）
    content: 消息内容，JSON 字符串。文本消息格式: '{"text":"内容"}'
    msg_type: 消息类型，text/post/image/file/audio/media/sticker/interactive/share_chat/share_user
    receive_id_type: 接收者 ID 类型。不传则根据 receive_id 前缀自动推断
    uuid: 可选，用于去重，1 小时内相同 uuid 至多成功一条
    """
    if receive_id_type is None:
        receive_id_type = _infer_receive_id_type(receive_id)
    body_builder = CreateMessageRequestBody.builder().receive_id(receive_id).msg_type(msg_type).content(content)
    if uuid:
        body_builder.uuid(uuid)
    body = body_builder.build()
    request = CreateMessageRequest.builder().receive_id_type(receive_id_type).request_body(body).build()
    response = feishu_client.im.v1.message.create(request)
    return _parse_response(response)


def send_text_message(
    receive_id: str,
    text: str,
    receive_id_type: Optional[str] = None,
    uuid: Optional[str] = None,
) -> Dict[str, Any]:
    """发送文本消息的便捷方法。receive_id 支持群 chat_id(oc_) 或用户 open_id(ou_)，不传 receive_id_type 时自动推断。"""
    content = json.dumps({"text": text}, ensure_ascii=False)
    return send_message(receive_id, content, msg_type="text", receive_id_type=receive_id_type, uuid=uuid)


def reply_message(
    message_id: str,
    content: str,
    msg_type: str = "text",
    reply_in_thread: Optional[bool] = None,
    uuid: Optional[str] = None,
) -> Dict[str, Any]:
    """
    回复消息。
    message_id: 待回复的消息 ID
    content: 消息内容，JSON 字符串。文本格式: '{"text":"内容"}'
    msg_type: 消息类型
    reply_in_thread: 是否以话题形式回复
    """
    body_builder = ReplyMessageRequestBody.builder().content(content).msg_type(msg_type)
    if reply_in_thread is not None:
        body_builder.reply_in_thread(reply_in_thread)
    if uuid:
        body_builder.uuid(uuid)
    body = body_builder.build()
    request = ReplyMessageRequest.builder().message_id(message_id).request_body(body).build()
    response = feishu_client.im.v1.message.reply(request)
    return _parse_response(response)


def reply_text_message(
    message_id: str,
    text: str,
    reply_in_thread: Optional[bool] = None,
    uuid: Optional[str] = None,
) -> Dict[str, Any]:
    """回复文本消息的便捷方法。"""
    content = json.dumps({"text": text}, ensure_ascii=False)
    return reply_message(message_id, content, msg_type="text", reply_in_thread=reply_in_thread, uuid=uuid)


def get_message(message_id: str) -> Dict[str, Any]:
    """获取单条消息。"""
    request = GetMessageRequest.builder().message_id(message_id).build()
    response = feishu_client.im.v1.message.get(request)
    return _parse_response(response)


def delete_message(message_id: str) -> Dict[str, Any]:
    """撤回/删除消息。"""
    request = DeleteMessageRequest.builder().message_id(message_id).build()
    response = feishu_client.im.v1.message.delete(request)
    return _parse_response(response)


def update_message(message_id: str, content: str, msg_type: str = "text") -> Dict[str, Any]:
    """更新消息内容。仅支持编辑 text、post 类型。"""
    body_builder = UpdateMessageRequestBody.builder().content(content).msg_type(msg_type)
    body = body_builder.build()
    request = UpdateMessageRequest.builder().message_id(message_id).request_body(body).build()
    response = feishu_client.im.v1.message.update(request)
    return _parse_response(response)
