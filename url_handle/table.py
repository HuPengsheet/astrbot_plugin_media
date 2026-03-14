"""
飞书多维表格 API 封装
参考文档: feishu-open-docs/uUDN04SN0QjL1QDN/bitable-v1/
"""
import json
import logging
from typing import Any, Dict, List, Optional

import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *

from .client import feishu_client

logger = logging.getLogger(__name__)


def _parse_response(response: lark.BaseResponse) -> Dict[str, Any]:
    """解析响应，返回完整 json 数据。code 为 0 表示成功。失败时打日志并仍返回解析后的 body。"""
    json_data = json.loads(response.raw.content)
    if not response.success():
        logger.error(
            "bitable api failed, code: %s, msg: %s, log_id: %s, resp: %s",
            response.code,
            response.msg,
            response.get_log_id(),
            json.dumps(json_data, indent=2, ensure_ascii=False),
        )
    return json_data


# ==================== 多维表格 App ====================


def get_app(app_token: str) -> Dict[str, Any]:
    """获取多维表格元数据。"""
    request = GetAppRequest.builder().app_token(app_token).build()
    response = feishu_client.bitable.v1.app.get(request)
    return _parse_response(response)


def update_app(app_token: str, name: Optional[str] = None) -> Dict[str, Any]:
    """更新多维表格元数据。"""
    body = UpdateAppRequestBody.builder()
    if name is not None:
        body.name(name)
    request = UpdateAppRequest.builder().app_token(app_token).request_body(body.build()).build()
    response = feishu_client.bitable.v1.app.update(request)
    return _parse_response(response)


def copy_app(app_token: str, name: str, folder_token: str) -> Dict[str, Any]:
    """复制多维表格。"""
    body = CopyAppRequestBody.builder().name(name).folder_token(folder_token).build()
    request = CopyAppRequest.builder().app_token(app_token).request_body(body).build()
    response = feishu_client.bitable.v1.app.copy(request)
    return _parse_response(response)


# ==================== 数据表 Table ====================


def list_tables(app_token: str, page_token: Optional[str] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
    """列出多维表格中的所有数据表。"""
    builder = ListAppTableRequest.builder().app_token(app_token)
    if page_token:
        builder.page_token(page_token)
    if page_size is not None:
        builder.page_size(page_size)
    request = builder.build()
    response = feishu_client.bitable.v1.app_table.list(request)
    return _parse_response(response)


def create_table(app_token: str, table: ReqTable) -> Dict[str, Any]:
    """新增数据表。"""
    body = CreateAppTableRequestBody.builder().table(table).build()
    request = CreateAppTableRequest.builder().app_token(app_token).request_body(body).build()
    response = feishu_client.bitable.v1.app_table.create(request)
    return _parse_response(response)


def delete_table(app_token: str, table_id: str) -> Dict[str, Any]:
    """删除数据表。"""
    request = DeleteAppTableRequest.builder().app_token(app_token).table_id(table_id).build()
    response = feishu_client.bitable.v1.app_table.delete(request)
    return _parse_response(response)


def patch_table(app_token: str, table_id: str, name: Optional[str] = None) -> Dict[str, Any]:
    """更新数据表。"""
    body = PatchAppTableRequestBody.builder()
    if name is not None:
        body.name(name)
    request = PatchAppTableRequest.builder().app_token(app_token).table_id(table_id).request_body(body.build()).build()
    response = feishu_client.bitable.v1.app_table.patch(request)
    return _parse_response(response)


# ==================== 记录 Record ====================


def list_records(
    app_token: str,
    table_id: str,
    view_id: Optional[str] = None,
    page_token: Optional[str] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """列出记录（简单分页）。"""
    builder = ListAppTableRecordRequest.builder().app_token(app_token).table_id(table_id)
    if view_id:
        builder.view_id(view_id)
    if page_token:
        builder.page_token(page_token)
    if page_size is not None:
        builder.page_size(page_size)
    request = builder.build()
    response = feishu_client.bitable.v1.app_table_record.list(request)
    return _parse_response(response)


def search_records(
    app_token: str,
    table_id: str,
    body: Optional[SearchAppTableRecordRequestBody] = None,
    page_token: Optional[str] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """查询记录（支持筛选、排序等）。"""
    builder = SearchAppTableRecordRequest.builder().app_token(app_token).table_id(table_id)
    if body:
        builder.request_body(body)
    else:
        builder.request_body(SearchAppTableRecordRequestBody.builder().build())
    if page_token:
        builder.page_token(page_token)
    if page_size is not None:
        builder.page_size(page_size)
    request = builder.build()
    response = feishu_client.bitable.v1.app_table_record.search(request)
    return _parse_response(response)


def get_record(app_token: str, table_id: str, record_id: str) -> Dict[str, Any]:
    """检索单条记录。"""
    request = GetAppTableRecordRequest.builder().app_token(app_token).table_id(table_id).record_id(record_id).build()
    response = feishu_client.bitable.v1.app_table_record.get(request)
    return _parse_response(response)


def create_record(app_token: str, table_id: str, fields: Dict[str, Any]) -> Dict[str, Any]:
    """新增一条记录。"""
    body = AppTableRecord.builder().fields(fields).build()
    request = CreateAppTableRecordRequest.builder().app_token(app_token).table_id(table_id).request_body(body).build()
    response = feishu_client.bitable.v1.app_table_record.create(request)
    return _parse_response(response)


def batch_create_records(
    app_token: str, table_id: str, records: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """新增多条记录。单次最多 1000 条。"""
    recs = [AppTableRecord.builder().fields(r.get("fields", r)).build() for r in records]
    body = BatchCreateAppTableRecordRequestBody.builder().records(recs).build()
    request = BatchCreateAppTableRecordRequest.builder().app_token(app_token).table_id(table_id).request_body(body).build()
    response = feishu_client.bitable.v1.app_table_record.batch_create(request)
    return _parse_response(response)


def update_record(app_token: str, table_id: str, record_id: str, fields: Dict[str, Any]) -> Dict[str, Any]:
    """更新一条记录。"""
    body = AppTableRecord.builder().fields(fields).build()
    request = UpdateAppTableRecordRequest.builder()
    request = request.app_token(app_token).table_id(table_id).record_id(record_id).request_body(body).build()
    response = feishu_client.bitable.v1.app_table_record.update(request)
    return _parse_response(response)


def batch_update_records(
    app_token: str, table_id: str, records: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """更新多条记录。每条需包含 record_id 和 fields。"""
    recs = [
        AppTableRecord.builder().record_id(r["record_id"]).fields(r.get("fields", {})).build()
        for r in records
    ]
    body = BatchUpdateAppTableRecordRequestBody.builder().records(recs).build()
    request = BatchUpdateAppTableRecordRequest.builder().app_token(app_token).table_id(table_id).request_body(body).build()
    response = feishu_client.bitable.v1.app_table_record.batch_update(request)
    return _parse_response(response)


def delete_record(app_token: str, table_id: str, record_id: str) -> Dict[str, Any]:
    """删除一条记录。"""
    request = DeleteAppTableRecordRequest.builder().app_token(app_token).table_id(table_id).record_id(record_id).build()
    response = feishu_client.bitable.v1.app_table_record.delete(request)
    return _parse_response(response)


def batch_delete_records(app_token: str, table_id: str, record_ids: List[str]) -> Dict[str, Any]:
    """删除多条记录。records 为 record_id 字符串列表。"""
    body = BatchDeleteAppTableRecordRequestBody.builder().records(record_ids).build()
    request = BatchDeleteAppTableRecordRequest.builder().app_token(app_token).table_id(table_id).request_body(body).build()
    response = feishu_client.bitable.v1.app_table_record.batch_delete(request)
    return _parse_response(response)


def batch_get_records(
    app_token: str,
    table_id: str,
    record_ids: List[str],
    with_shared_url: Optional[bool] = None,
    automatic_fields: Optional[bool] = None,
) -> Dict[str, Any]:
    """批量获取记录。最多 100 条。"""
    body = BatchGetAppTableRecordRequestBody.builder().record_ids(record_ids)
    if with_shared_url is not None:
        body.with_shared_url(with_shared_url)
    if automatic_fields is not None:
        body.automatic_fields(automatic_fields)
    request = BatchGetAppTableRecordRequest.builder().app_token(app_token).table_id(table_id).request_body(body.build()).build()
    response = feishu_client.bitable.v1.app_table_record.batch_get(request)
    return _parse_response(response)


def get_field_values(
    app_token: str,
    table_id: str,
    field_name: str,
    view_id: Optional[str] = None,
    max_records: Optional[int] = None,
) -> List[Any]:
    """
    获取多维表格某字段的所有值，返回列表。
    通过分页查询记录并提取指定字段的值，自动处理分页。
    """
    values: List[Any] = []
    page_token: Optional[str] = None
    body = SearchAppTableRecordRequestBody.builder().field_names([field_name]).build()

    while True:
        resp = search_records(app_token, table_id, body=body, page_token=page_token, page_size=500)
        if resp.get("code") != 0:
            return values
        data = resp.get("data", {})
        items = data.get("items", [])
        for rec in items:
            fields = rec.get("fields", {})
            if field_name in fields:
                values.append(fields[field_name])
        if max_records is not None and len(values) >= max_records:
            return values[:max_records]
        if not data.get("has_more", False):
            break
        page_token = data.get("page_token")
        if not page_token:
            break
    return values


# ==================== 视图 View ====================


def list_views(
    app_token: str,
    table_id: str,
    page_token: Optional[str] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """列出视图。"""
    builder = ListAppTableViewRequest.builder().app_token(app_token).table_id(table_id)
    if page_token:
        builder.page_token(page_token)
    if page_size is not None:
        builder.page_size(page_size)
    request = builder.build()
    response = feishu_client.bitable.v1.app_table_view.list(request)
    return _parse_response(response)


def get_view(app_token: str, table_id: str, view_id: str) -> Dict[str, Any]:
    """检索视图。"""
    request = GetAppTableViewRequest.builder().app_token(app_token).table_id(table_id).view_id(view_id).build()
    response = feishu_client.bitable.v1.app_table_view.get(request)
    return _parse_response(response)


def create_view(app_token: str, table_id: str, view: ReqView) -> Dict[str, Any]:
    """新增视图。"""
    request = CreateAppTableViewRequest.builder().app_token(app_token).table_id(table_id).request_body(view).build()
    response = feishu_client.bitable.v1.app_table_view.create(request)
    return _parse_response(response)


def patch_view(
    app_token: str,
    table_id: str,
    view_id: str,
    view_name: Optional[str] = None,
    view_property: Optional[Any] = None,
) -> Dict[str, Any]:
    """更新视图。view_name 或 view_property 至少传一个。"""
    body_builder = PatchAppTableViewRequestBody.builder()
    if view_name is not None:
        body_builder.view_name(view_name)
    if view_property is not None:
        body_builder.property(view_property)
    body = body_builder.build()
    request = PatchAppTableViewRequest.builder()
    request = request.app_token(app_token).table_id(table_id).view_id(view_id).request_body(body).build()
    response = feishu_client.bitable.v1.app_table_view.patch(request)
    return _parse_response(response)


def delete_view(app_token: str, table_id: str, view_id: str) -> Dict[str, Any]:
    """删除视图。"""
    request = DeleteAppTableViewRequest.builder().app_token(app_token).table_id(table_id).view_id(view_id).build()
    response = feishu_client.bitable.v1.app_table_view.delete(request)
    return _parse_response(response)


# ==================== 字段 Field ====================


def list_fields(
    app_token: str,
    table_id: str,
    view_id: Optional[str] = None,
    page_token: Optional[str] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """列出字段。"""
    builder = ListAppTableFieldRequest.builder().app_token(app_token).table_id(table_id)
    if view_id:
        builder.view_id(view_id)
    if page_token:
        builder.page_token(page_token)
    if page_size is not None:
        builder.page_size(page_size)
    request = builder.build()
    response = feishu_client.bitable.v1.app_table_field.list(request)
    return _parse_response(response)


def create_field(app_token: str, table_id: str, field: AppTableField) -> Dict[str, Any]:
    """新增字段。"""
    request = CreateAppTableFieldRequest.builder().app_token(app_token).table_id(table_id).request_body(field).build()
    response = feishu_client.bitable.v1.app_table_field.create(request)
    return _parse_response(response)


def update_field(app_token: str, table_id: str, field_id: str, field: AppTableField) -> Dict[str, Any]:
    """更新字段。"""
    request = UpdateAppTableFieldRequest.builder()
    request = request.app_token(app_token).table_id(table_id).field_id(field_id).request_body(field).build()
    response = feishu_client.bitable.v1.app_table_field.update(request)
    return _parse_response(response)


def delete_field(app_token: str, table_id: str, field_id: str) -> Dict[str, Any]:
    """删除字段。"""
    request = DeleteAppTableFieldRequest.builder().app_token(app_token).table_id(table_id).field_id(field_id).build()
    response = feishu_client.bitable.v1.app_table_field.delete(request)
    return _parse_response(response)


# ==================== 仪表盘 Dashboard ====================


def list_dashboards(
    app_token: str,
    page_token: Optional[str] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """列出仪表盘。"""
    builder = ListAppDashboardRequest.builder().app_token(app_token)
    if page_token:
        builder.page_token(page_token)
    if page_size is not None:
        builder.page_size(page_size)
    request = builder.build()
    response = feishu_client.bitable.v1.app_dashboard.list(request)
    return _parse_response(response)


def copy_dashboard(app_token: str, block_id: str, name: str) -> Dict[str, Any]:
    """复制仪表盘。"""
    body = CopyAppDashboardRequestBody.builder().name(name).build()
    request = CopyAppDashboardRequest.builder().app_token(app_token).block_id(block_id).request_body(body).build()
    response = feishu_client.bitable.v1.app_dashboard.copy(request)
    return _parse_response(response)


# ==================== 兼容旧接口 ====================


def get_multidimensional_table_row_data(app_token: str) -> Dict[str, Any]:
    """获取多维表格元数据（兼容旧接口，原参数名 table_id 实际应为 app_token）。"""
    return get_app(app_token)
