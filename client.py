import os

import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *

app_id = os.getenv("FEISHU_APP_ID")
app_secret = os.getenv("FEISHU_APP_SECRET")
feishu_client = lark.Client.builder() \
    .app_id(app_id) \
    .app_secret(app_secret) \
    .log_level(lark.LogLevel.DEBUG) \
    .build()
