"""
WebCrawler Commander - 測試工具函數

提供測試框架的輔助函數、聲明和共用方法

作者: Jerry開發工作室
版本: v1.0.0
"""

import asyncio
import json
import time
import tempfile
import unittest.mock
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable, Awaitable, TypeVar
from unittest.mock import MagicMock, AsyncMock, patch

import pytest
from faker import Faker

# 測試常量
TEST_TIMEOUT = 30  # 測試超時時間（秒）
MOCK_DATA_SIZE = 1024  # 測試數據大小
MAX_RETRIES = 3  # 測試重試次數

# 全域Faker實例
faker = Faker(['zh_TW', 'en_US'])

# 類型變數
T = TypeVar('T')


class AsyncTestCase(unittest.TestCase):
    """異步測試用例基類"""

    def setUp(self):
        """設置測試環境"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        """清理測試環境"""
        if hasattr(self, 'loop'):
            self.loop.close()

    def async_test(self, coro):
        """運行異步測試"""
        return self.loop.run_until_complete(coro)


class TestDataFactory:
    """測試數據工廠"""

    @staticmethod
    def create_user(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """創建測試用戶數據"""
        base_data = {
            "user_id": faker.uuid4(),
            "username": faker.user_name(),
            "email": faker.email(),
            "full_name": faker.name(),
            "roles": ["user"],
            "is_active": True,
            "created_at": faker.iso8601(),
            "last_login": faker.iso8601(),
            "preferences": {
                "theme": "light",
                "language": "zh_TW"
            }
        }

        if overrides:
            base_data.update(overrides)

        return base_data

    @staticmethod
    def create_crawler(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """創建測試爬蟲數據"""
        selectors = {
            "title": "h1",
            "content": ".content",
            "date": ".date",
            "author": ".author"
        }

        base_data = {
            "crawler_id": faker.uuid4(),
            "name": faker.company() + "爬蟲",
            "description": faker.text(max_nb_chars=100),
            "url_pattern": f"https://{faker.domain_name()}/{{}}",
            "selectors": selectors,
            "schedule": {
                "frequency": "daily",
                "time": "09:00",
                "enabled": True
            },
            "config": {
                "max_pages": faker.random_int(10, 100),
                "delay": faker.random_float(0.1, 2.0),
                "timeout": 30,
                "user_agent": faker.user_agent()
            },
            "status": "active",
            "created_by": faker.uuid4(),
            "created_at": faker.iso8601(),
            "tags": [faker.word() for _ in range(3)]
        }

        if overrides:
            base_data.update(overrides)

        return base_data

    @staticmethod
    def create_crawl_task(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """創建測試爬取任務數據"""
        base_data = {
            "task_id": faker.uuid4(),
            "crawler_id": faker.uuid4(),
            "url": faker.url(),
            "status": "pending",
            "priority": faker.random_int(1, 10),
            "max_retries": 3,
            "retry_count": 0,
            "timeout": faker.random_int(10, 60),
            "created_at": faker.iso8601(),
            "started_at": None,
            "completed_at": None,
            "result": None,
            "error_message": None
        }

        if overrides:
            base_data.update(overrides)

        return base_data

    @staticmethod
    def create_data_record(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """創建測試數據記錄"""
        base_data = {
            "record_id": faker.uuid4(),
            "source_url": faker.url(),
            "title": faker.sentence(),
            "content": faker.text(max_nb_chars=500),
            "author": faker.name(),
            "publish_date": faker.iso8601(),
            "tags": [faker.word() for _ in range(faker.random_int(1, 5))],
            "metadata": {
                "source": faker.company(),
                "category": faker.word(),
                "quality_score": faker.random_int(1, 100)
            },
            "created_at": faker.iso8601(),
            "updated_at": faker.iso8601(),
            "version": 1
        }

        if overrides:
            base_data.update(overrides)

        return base_data


@contextmanager
def temp_file(content: str = "", suffix: str = ".txt", mode: str = "w"):
    """臨時文件上下文管理器"""
    with tempfile.NamedTemporaryFile(mode=mode, suffix=suffix, delete=False) as f:
        if content:
            f.write(content)
        f.flush()
        file_path = Path(f.name)

    try:
        yield file_path
    finally:
        if file_path.exists():
            file_path.unlink()


@asynccontextmanager
async def temp_async_file(content: str = "", suffix: str = ".txt"):
    """異步臨時文件上下文管理器"""
    import aiofiles

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
        file_path = Path(f.name)

    try:
        if content:
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(content)

        yield file_path
    finally:
        if file_path.exists():
            file_path.unlink()


class MockManager:
    """測試模彙管理器"""

    def __init__(self):
        self.mocks: Dict[str, MagicMock] = {}

    def create_mock(self, name: str, **kwargs) -> MagicMock:
        """創建并存儲模彙"""
        mock = MagicMock(**kwargs)
        self.mocks[name] = mock
        return mock

    def get_mock(self, name: str) -> Optional[MagicMock]:
        """獲取已存儲的模彙"""
        return self.mocks.get(name)

    def reset_all(self):
        """重置所有模彙"""
        for mock in self.mocks.values():
            mock.reset_mock()

    def clear_all(self):
        """清除所有模彙"""
        self.mocks.clear()


def mock_config_manager(**overrides) -> MagicMock:
    """模彙配置管理器"""
    mock = MagicMock()

    # 默認配置數據
    default_config = {
        "app": {
            "name": "WebCrawler Commander Test",
            "version": "1.0.0-test",
            "environment": "testing"
        },
        "server": {
            "host": "localhost",
            "port": 8001,
            "workers": 2
        },
        "logging": {
            "level": "DEBUG",
            "format": "test"
        }
    }

    # 合併覆蓋
    default_config.update(overrides)

    # 設置模彙方法
    mock.get.side_effect = lambda key, default=None: _get_nested_value(default_config, key, default)
    mock.set.return_value = True
    mock.reload.return_value = True
    mock.get_config_stats.return_value = {"load_count": 1}

    return mock


def _get_nested_value(data: Dict, key_path: str, default=None):
    """從嵌套字典中獲取值"""
    keys = key_path.split(".")
    current = data

    try:
        for key in keys:
            current = current[key]
        return current
    except (KeyError, TypeError):
        return default


def mock_logger_service() -> MagicMock:
    """模彙日誌服務"""
    mock = MagicMock()

    # 模彙日誌方法
    mock.info.return_value = None
    mock.warning.return_value = None
    mock.error.return_value = None
    mock.debug.return_value = None

    return mock


async def wait_for_condition(condition_func: Callable[[], bool],
                           timeout: float = 5.0,
                           interval: float = 0.1) -> bool:
    """等待條件滿足"""
    start_time = time.time()

    while time.time() - start_time < timeout:
        if condition_func():
            return True
        await asyncio.sleep(interval)

    return False


def assert_eventually(condition_func: Callable[[], bool],
                     timeout: float = 5.0,
                     message: str = "Condition was not met within timeout"):
    """聲明終將滿足條件"""
    import time

    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition_func():
            return
        time.sleep(0.1)

    pytest.fail(message)


async def assert_async_eventually(async_condition_func: Callable[[], Awaitable[bool]],
                                timeout: float = 5.0,
                                message: str = "Async condition was not met within timeout"):
    """異步聲明終將滿足條件"""
    import time

    start_time = time.time()
    while time.time() - start_time < timeout:
        if await async_condition_func():
            return
        await asyncio.sleep(0.1)

    pytest.fail(message)


class PerformanceProfiler:
    """性能分析器"""

    def __init__(self):
        self.start_times: Dict[str, float] = {}

    def start(self, name: str):
        """開始計時"""
        self.start_times[name] = time.time()

    def end(self, name: str) -> float:
        """結束計時并返回耗時"""
        if name not in self.start_times:
            raise ValueError(f"No start time recorded for '{name}'")

        elapsed = time.time() - self.start_times[name]
        del self.start_times[name]
        return elapsed

    @contextmanager
    def measure(self, name: str):
        """計時上下文管理器"""
        self.start(name)
        try:
            yield self
        finally:
            elapsed = self.end(name)
            print(f"Measured {name}: {elapsed:.3f}s")

    def assert_performance_threshold(self, name: str, threshold: float,
                                   operator: str = "lt", unit: str = "s"):
        """斷言性能閾值"""
        if name not in self.start_times:
            raise ValueError(f"No performance measurement for '{name}'")

        elapsed = time.time() - self.start_times[name]

        if operator == "lt" and elapsed > threshold:
            pytest.fail(f"Performance check failed: {name} took {elapsed:.3f}{unit} "
                       f"(threshold: {threshold}{unit})")
        elif operator == "gt" and elapsed < threshold:
            pytest.fail(f"Performance check failed: {name} took {elapsed:.3f}{unit} "
                       f"(threshold: {threshold}{unit})")


# 全局測試實例
test_data_factory = TestDataFactory()
mock_manager = MockManager()
performance_profiler = PerformanceProfiler()
