"""
WebCrawler Commander - pytest 配置和共用修件器

提供測試環境初始化、模擬工具、測試數據生成等功能

作者: Jerry開發工作室
版本: v1.0.0
"""

import asyncio
import os
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Generator, AsyncGenerator, Optional
from unittest.mock import MagicMock, patch

import pytest
import pytest_asyncio
from faker import Faker

# 設定測試環境
os.environ['WEBCRAWLER_ENV'] = 'testing'
os.environ['PYTHONPATH'] = str(Path(__file__).parent.parent)

# 導入應用模塊
from utils.config_manager import ConfigManager
from utils.logger_service import LoggerService
from utils.rbac_manager import RBACManager
from utils.encryption_service import EncryptionService
from utils.system_monitor import SystemMonitor


# 全域測試配置
class TestConfig:
    """測試配置常量"""
    TEST_DB_URL = "sqlite:///:memory:"
    TEST_REDIS_URL = "redis://localhost:6379/1"
    TEST_TIMEOUT = 30
    TEST_WORKERS = 2

    # 測試數據目錄
    TEST_DATA_DIR = Path(__file__).parent / "test_data"
    TEST_CONFIG_DIR = Path(__file__).parent / "test_configs"

    # 創建測試目錄
    TEST_DATA_DIR.mkdir(exist_ok=True)
    TEST_CONFIG_DIR.mkdir(exist_ok=True)


# 測試修件器 (Fixtures)
@pytest.fixture(scope="session")
def event_loop():
    """創建事件循環用於異步測試"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def faker():
    """隨機數據生成器"""
    return Faker(['zh_TW', 'en_US'])


@pytest.fixture(scope="session")
def temp_dir():
    """臨時目錄修件器"""
    temp_path = tempfile.mkdtemp(prefix="webcrawler_test_")
    yield Path(temp_path)
    # 清理
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture(scope="session")
async def test_config_manager(temp_dir):
    """測試配置管理器修件器"""
    config_dir = temp_dir / "config"

    # 創建測試配置目錄
    config_dir.mkdir(exist_ok=True)

    # 創建測試配置文件
    test_config = {
        "app": {
            "name": "WebCrawler Commander Test",
            "version": "1.0.0-test",
            "environment": "testing"
        },
        "server": {
            "host": "localhost",
            "port": 8001,
            "workers": TestConfig.TEST_WORKERS
        },
        "database": {
            "url": TestConfig.TEST_DB_URL
        },
        "redis": {
            "url": TestConfig.TEST_REDIS_URL
        },
        "logging": {
            "level": "DEBUG",
            "format": "test"
        },
        "security": {
            "secret_key": "test_secret_key_change_in_production",
            "token_expire_hours": 24
        }
    }

    # 寫入配置
    config_file = config_dir / "config.yaml"
    import yaml
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.dump(test_config, f, default_flow_style=False, allow_unicode=True)

    # 初始化配置管理器
    config_manager = ConfigManager(
        config_dir=str(config_dir),
        environment="testing",
        enable_hot_reload=False
    )

    yield config_manager


@pytest.fixture(scope="session")
async def test_logger_service(test_config_manager, temp_dir):
    """測試日誌服務修件器"""
    from utils.logger_service import init_logger_service

    # 設置測試日誌目錄
    log_dir = temp_dir / "logs"
    log_dir.mkdir(exist_ok=True)

    # 修補日誌配置
    with patch('utils.logger_service.get_config_manager') as mock_config:
        mock_config.return_value = test_config_manager

        # 初始化日誌服務
        logger_service = init_logger_service()

        yield logger_service

        # 清理
        await logger_service.shutdown()


@pytest.fixture(scope="function")
async def test_rbac_manager(test_config_manager, temp_dir):
    """測試RBAC權限管理器修件器"""
    from utils.rbac_manager import RBACManager

    # 創建測試數據庫目錄
    db_dir = temp_dir / "rbac_db"
    db_dir.mkdir(exist_ok=True)

    manager = RBACManager(config_manager=test_config_manager)

    # 初始化測試用戶和角色
    await manager.initialize_test_data()

    yield manager

    # 清理
    await manager.cleanup()


@pytest.fixture(scope="function")
async def test_encryption_service(test_config_manager, temp_dir):
    """測試加密服務修件器"""
    from utils.encryption_service import EncryptionService

    # 創建密鑰目錄
    keys_dir = temp_dir / "keys"
    keys_dir.mkdir(exist_ok=True)

    service = EncryptionService(config_manager=test_config_manager)

    yield service

    # 清理臨時密鑰
    shutil.rmtree(keys_dir, ignore_errors=True)


@pytest.fixture(scope="function")
async def test_system_monitor(test_config_manager):
    """測試系統監控修件器"""
    from utils.system_monitor import SystemMonitor

    monitor = SystemMonitor(config_manager=test_config_manager)

    yield monitor

    # 停止監控
    await monitor.stop_monitoring()


@pytest.fixture(scope="function")
def mock_crawler_response():
    """模擬爬蟲響應修件器"""
    from services.crawler_engine import CrawlResult

    mock_result = CrawlResult(
        url="https://example.com/test",
        status_code=200,
        headers={"content-type": "text/html"},
        content=b"<html><body><h1>Test Page</h1></body></html>",
        text="<html><body><h1>Test Page</h1></body></html>",
        response_time=0.5,
        success=True,
        request_headers={"user-agent": "TestBot/1.0"},
        crawled_at="2024-01-15T10:00:00Z"
    )

    return mock_result


@pytest.fixture(scope="function")
def mock_network_response():
    """模擬網路響應修件器"""
    import aiohttp

    class MockResponse:
        def __init__(self, status=200, data=None, headers=None):
            self.status = status
            self._data = data or b"mock response data"
            self.headers = headers or {"content-type": "application/json"}
            self.url = "https://api.example.com/test"

        async def read(self):
            return self._data

        async def text(self):
            return self._data.decode('utf-8')

        async def json(self):
            import json
            return json.loads(self._data.decode('utf-8'))

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    return MockResponse


# 自定義標記
def pytest_configure(config):
    """pytest配置鉤子"""
    # 註冊自定義標記
    config.addinivalue_line("markers", "unit: 單元測試")
    config.addinivalue_line("markers", "integration: 集成測試")
    config.addinivalue_line("markers", "e2e: 端到端測試")
    config.addinivalue_line("markers", "smoke: 冒煙測試")
    config.addinivalue_line("markers", "config: 配置相關測試")
    config.addinivalue_line("markers", "logging: 日誌相關測試")
    config.addinivalue_line("markers", "security: 安全相關測試")
    config.addinivalue_line("markers", "crawler: 爬蟲相關測試")
    config.addinivalue_line("markers", "data: 數據處理相關測試")
    config.addinivalue_line("markers", "monitor: 監控相關測試")
    config.addinivalue_line("markers", "slow: 慢速測試")
    config.addinivalue_line("markers", "skip_ci: CI環境中跳過")
    config.addinivalue_line("markers", "flaky: 不穩定測試")


def pytest_collection_modifyitems(config, items):
    """測試收集修飾鉤子"""
    # 為沒有標記的測試添加默認標記
    for item in items:
        if not any(marker in item.keywords for marker in ['unit', 'integration', 'e2e']):
            item.add_marker(pytest.mark.unit)


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_artifacts():
    """清理測試產物修件器"""
    yield

    # 清理可能的測試產物
    import gc
    gc.collect()


# 工具函數
def create_test_user(user_id: str = "test_user", **kwargs) -> Dict[str, Any]:
    """創建測試用戶數據"""
    return {
        "user_id": user_id,
        "username": kwargs.get("username", f"user_{user_id}"),
        "email": kwargs.get("email", f"user_{user_id}@example.com"),
        "roles": kwargs.get("roles", ["user"]),
        "is_active": kwargs.get("is_active", True),
        "created_at": kwargs.get("created_at", "2024-01-01T00:00:00Z")
    }


def create_test_crawler(crawler_id: str = "test_crawler", **kwargs) -> Dict[str, Any]:
    """創建測試爬蟲數據"""
    return {
        "crawler_id": crawler_id,
        "name": kwargs.get("name", f"Crawler {crawler_id}"),
        "description": kwargs.get("description", "Test crawler"),
        "url_pattern": kwargs.get("url_pattern", "https://example.com/*"),
        "config": kwargs.get("config", {}),
        "status": kwargs.get("status", "active"),
        "created_by": kwargs.get("created_by", "test_user")
    }
