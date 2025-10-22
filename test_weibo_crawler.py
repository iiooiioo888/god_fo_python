#!/usr/bin/env python3
"""
微博USID爬蟲測試腳本

測試基本的導入和功能
"""

import asyncio
import sys
import os
from pathlib import Path

# 添加後端路徑到Python路徑
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# 初始化框架組件
from utils.config_manager import init_config_manager
from utils.logger_service import init_logger_service

# 初始化配置管理器
config_manager = init_config_manager(
    config_dir=str(backend_path / "config"),
    environment="development",
    enable_hot_reload=False
)

# 初始化日誌服務
logger_service = init_logger_service(config_manager)

# 測試導入
print("測試導入...")
try:
    from services.weibo_usid_crawler import (
        get_weibo_crawler,
        create_weibo_config,
        DataSource,
        Gender
    )
    print("✅ 導入成功")
except Exception as e:
    print(f"❌ 導入失敗: {e}")
    sys.exit(1)

# 測試配置創建
print("\n測試配置創建...")
try:
    config = create_weibo_config(
        data_source=DataSource.RANGE_SCAN,
        uid_range_start=1000000000,
        uid_range_end=1000000010,
        max_concurrent=1,
        request_delay=0.1,
        csv_output_path="test_output.csv"
    )
    print("✅ 配置創建成功")
    print(f"   數據源: {config.data_source.value}")
    print(f"   範圍: {config.uid_range_start} - {config.uid_range_end}")
except Exception as e:
    print(f"❌ 配置創建失敗: {e}")
    sys.exit(1)

# 測試基本功能 (不實際請求)
print("\n測試基本功能...")
try:
    crawler = get_weibo_crawler()

    # 測試UID範圍生成
    uid_list = crawler._generate_uid_range(1000000000, 1000000005)
    print(f"✅ UID範圍生成成功: {uid_list}")

    # 測試cookie解析
    test_cookie = "test=value; another=test2"
    parsed = crawler._parse_cookie_string(test_cookie)
    print(f"✅ Cookie解析成功: {parsed}")

    # 關閉
    asyncio.run(crawler.close())

    print("✅ 基本功能測試通過")

except Exception as e:
    print(f"❌ 基本功能測試失敗: {e}")
    sys.exit(1)

print("\n🎉 所有測試通過！微博USID爬蟲準備就緒。")

# 清理測試文件
import os
if os.path.exists("test_output.csv"):
    os.remove("test_output.csv")
    print("清理測試文件")
