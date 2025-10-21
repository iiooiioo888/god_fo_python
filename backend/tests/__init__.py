"""
WebCrawler Commander - 後端測試包

測試組織結構：
├── conftest.py          - 測試配置和修件
├── test_config_manager.py     - 配置管理器測試
├── test_logger_service.py     - 日誌服務測試
├── test_rbac_manager.py       - RBAC權限測試
├── test_encryption_service.py - 加密服務測試
├── test_system_monitor.py     - 系統監控測試
├── test_crawler_engine.py     - 爬蟲引擎測試
├── test_data_processor.py     - 數據處理測試
└── test_integration.py        - 集成測試 (已存在)

作者: Jerry開發工作室
版本: v1.0.0
"""

import os
import sys
from pathlib import Path

# 添加backend目錄到Python路徑
backend_path = Path(__file__).parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

# 設置測試環境變數
os.environ.setdefault('WEBCRAWLER_ENV', 'testing')
os.environ.setdefault('PYTHONPATH', str(backend_path))

# 導出自定義測試工具
from .conftest import *
from .test_utils import *

__version__ = "1.0.0"
__all__ = ['conftest', 'test_utils']
