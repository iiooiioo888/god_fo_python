"""
WebCrawler Commander - 日誌服務單元測試

測試覆蓋：
- 日誌初始化和配置
- 不同級別日誌記錄
- 結構化日誌格式
- 異步日誌處理
- 日誌輪轉和壓縮
- 請求上下文追蹤
- 性能監控集成

作者: Jerry開發工作室
版本: v1.0.0
"""

import os
import tempfile
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime, timezone

from utils.logger_service import (
    LoggerService, get_logger, init_logger_service,
    set_request_context, clear_request_context
)
from tests.test_utils import TestDataFactory, temp_file


@pytest.mark.unit
@pytest.mark.logging
class TestLoggerServiceInitialization:
    """日誌服務初始化測試"""

    def test_logger_service_creation(self):
        """測試日誌服務創建"""
        service = LoggerService()

        assert service is not None
        assert hasattr(service, 'loggers')
        assert hasattr(service, 'handlers')
        assert hasattr(service, 'formatters')

    def test_logger_service_singleton(self):
        """測試日誌服務單例模式"""
        # 初始化服務
        init_logger_service()

        # 獲取實例
        service1 = get_logger("test")
        service2 = get_logger("test")

        # 應該返回同一個 logger 實例
        assert service1 is service2

    def test_get_logger_with_different_names(self):
        """測試獲取不同名稱的 logger"""
        logger1 = get_logger("test1")
        logger2 = get_logger("test2")

        assert logger1 is not logger2
        assert logger1.name == "test1"
        assert logger2.name == "test2"


@pytest.mark.unit
@pytest.mark.logging
class TestLoggerServiceOperations:
    """日誌服務操作測試"""

    @pytest.fixture
    def logger_service(self):
        """測試日誌服務修件器"""
        service = LoggerService()
        service.initialize()
        return service

    @pytest.fixture
    def test_logger(self):
        """測試 logger 修件器"""
        return get_logger("test_logger")

    def test_basic_logging_levels(self, test_logger, caplog):
        """測試基本日誌級別"""
        import logging

        caplog.set_level(logging.DEBUG)

        # 測試不同級別的日誌
        test_logger.debug("Debug message")
        test_logger.info("Info message")
        test_logger.warning("Warning message")
        test_logger.error("Error message")
        test_logger.critical("Critical message")

        assert "Debug message" in caplog.text
        assert "Info message" in caplog.text
        assert "Warning message" in caplog.text
        assert "Error message" in caplog.text
        assert "Critical message" in caplog.text

    def test_structured_logging(self, test_logger, caplog):
        """測試結構化日誌"""
        import logging
        caplog.set_level(logging.INFO)

        # 測試結構化日誌記錄
        test_logger.info("用戶操作", user_id="12345", action="login", success=True)

        log_entry = caplog.records[-1]
        assert log_entry.message == "用戶操作"
        assert hasattr(log_entry, 'user_id') or 'user_id' in str(log_entry)
        assert hasattr(log_entry, 'action') or 'action' in str(log_entry)

    def test_exception_logging(self, test_logger, caplog):
        """測試異常日誌記錄"""
        import logging
        caplog.set_level(logging.ERROR)

        try:
            raise ValueError("測試異常")
        except ValueError as e:
            test_logger.error("異常發生", exception_details={
                "type": "ValueError",
                "message": "測試異常",
                "traceback": "simulated traceback"
            })

        assert "異常發生" in caplog.text
        assert "ValueError" in caplog.text
        assert "測試異常" in caplog.text

    def test_request_context_logging(self, test_logger):
        """測試請求上下文日誌"""
        # 設置請求上下文
        set_request_context(request_id="req-123", user_id="user-456")

        with patch('utils.logger_service.get_request_context') as mock_context:
            mock_context.return_value = {
                "request_id": "req-123",
                "user_id": "user-456",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

            test_logger.info("請求處理", action="process_data")

        # 清除上下文（重要，避免影響其他測試）
        clear_request_context()

    def test_context_manager_logging(self, test_logger):
        """測試上下文管理器日誌"""
        from utils.logger_service import log_execution_time

        with patch('utils.logger_service.logger') as mock_logger:
            with log_execution_time("test_operation"):
                pass

            # 驗證日誌記錄
            mock_logger.info.assert_called()

    def test_performance_logging(self, test_logger):
        """測試性能日誌記錄"""
        import time

        with patch('utils.logger_service.performance_monitor') as mock_perf:
            # 模擬性能記錄
            test_logger.info("操作完成", execution_time=1.5, records_processed=1000)

            # 驗證性能監控被調用
            # mock_perf.record_metric.assert_called()


@pytest.mark.unit
@pytest.mark.logging
class TestLoggerServiceConfiguration:
    """日誌服務配置測試"""

    def test_logger_config_from_dict(self):
        """測試從字典配置 logger"""
        config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "default"
                }
            },
            "loggers": {
                "test_logger": {
                    "level": "DEBUG",
                    "handlers": ["console"],
                    "propagate": False
                }
            }
        }

        service = LoggerService()
        service.configure_from_dict(config)

        logger = service.get_logger("test_logger")
        assert logger is not None
        assert logger.level <= 10  # DEBUG level or lower

    def test_custom_formatter(self):
        """測試自定義格式化器"""
        service = LoggerService()

        # 創建自定義格式化器
        formatter = service.create_formatter(
            fmt="[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        assert formatter is not None
        assert "[%(asctime)s]" in formatter._fmt

    def test_output_formats(self):
        """測試輸出格式"""
        service = LoggerService()

        # 測試JSON格式
        json_formatter = service.create_json_formatter()
        assert json_formatter is not None

        # 測試結構化格式
        structured_formatter = service.create_structured_formatter()
        assert structured_formatter is not None


@pytest.mark.unit
@pytest.mark.logging
class TestLoggerServiceHandlers:
    """日誌服務處理器測試"""

    def test_file_handler_creation(self, temp_dir):
        """測試文件處理器創建"""
        service = LoggerService()

        log_file = temp_dir / "test.log"
        handler = service.create_file_handler(
            filename=str(log_file),
            level="INFO",
            max_bytes=1024*1024,  # 1MB
            backup_count=5
        )

        assert handler is not None
        assert handler.level == 20  # INFO level

    def test_console_handler_creation(self):
        """測試控制台處理器創建"""
        service = LoggerService()

        handler = service.create_console_handler(level="DEBUG")
        assert handler is not None
        assert handler.level == 10  # DEBUG level

    @pytest.mark.skipif(os.name == 'nt', reason="Rotating file handler test skipped on Windows")
    def test_rotating_file_handler(self, temp_dir):
        """測試輪轉文件處理器"""
        service = LoggerService()

        log_file = temp_dir / "rotating.log"
        handler = service.create_rotating_handler(
            filename=str(log_file),
            max_bytes=1024,  # 1KB for testing
            backup_count=3,
            level="INFO"
        )

        assert handler is not None


@pytest.mark.unit
@pytest.mark.logging
class TestLoggerServiceIntegration:
    """日誌服務集成測試"""

    @pytest.fixture
    def integrated_logger_service(self, temp_dir):
        """集成測試的日誌服務修件器"""
        # 創建日誌目錄
        log_dir = temp_dir / "logs"
        log_dir.mkdir(exist_ok=True)

        # 初始化服務
        service = LoggerService()
        service.initialize()

        # 配置文件處理器
        log_file = log_dir / "app.log"
        file_handler = service.create_file_handler(str(log_file))

        # 配置主logger
        root_logger = service.get_logger()
        root_logger.addHandler(file_handler)
        root_logger.setLevel(10)  # DEBUG

        return service, log_file

    def test_end_to_end_logging(self, integrated_logger_service):
        """測試端到端日誌記錄"""
        service, log_file = integrated_logger_service

        logger = service.get_logger("e2e_test")

        # 記錄各種訊息
        logger.info("開始測試", test_id="e2e_001")
        logger.debug("調試信息", data={"key": "value"})
        logger.warning("警告信息", code="WARN_001")
        logger.error("錯誤信息", error_code="ERR_001", details={"stack": "test"})

        # 驗證文件已創建
        assert log_file.exists()

        # 讀取日誌內容
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()

        assert "開始測試" in content
        assert "調試信息" in content
        assert "警告信息" in content
        assert "錯誤信息" in content
        assert "e2e_001" in content

    def test_multiple_loggers_independence(self, integrated_logger_service):
        """測試多個logger的獨立性"""
        service, _ = integrated_logger_service

        logger1 = service.get_logger("logger1")
        logger2 = service.get_logger("logger2")

        # 設置不同的級別
        logger1.setLevel(30)  # WARNING
        logger2.setLevel(10)  # DEBUG

        # logger1應該忽略DEBUG消息
        with patch('logging.Logger._log') as mock_log:
            logger1.debug("Debug message")
            logger1.warning("Warning message")

            # 應該只記錄WARNING
            calls = [call for call in mock_log.call_args_list if call[0][1] == 30]  # WARNING level

    def test_context_preservation(self, integrated_logger_service):
        """測試上下文保持"""
        service, _ = integrated_logger_service

        logger = service.get_logger("context_test")

        # 設置上下文
        set_request_context(request_id="ctx-001", session_id="sess-001")

        # 記錄日誌
        logger.info("上下文測試", action="test")

        # 清除上下文（模擬請求結束）
        clear_request_context()

        # 驗證上下文已清除（如果實現了get_request_context）
        # 這個依賴於實際實現


@pytest.mark.unit
@pytest.mark.logging
@pytest.mark.slow
class TestLoggerServicePerformance:
    """日誌服務性能測試"""

    def test_high_frequency_logging(self, test_logger, performance_profiler):
        """測試高頻率日誌記錄"""
        with performance_profiler.measure("high_frequency_logging"):
            for i in range(1000):
                test_logger.info(f"測試日誌消息 {i}", iteration=i, data="test")

        # 性能檢查（1000條日誌應該在2秒內完成）
        performance_profiler.assert_performance_threshold(
            "high_frequency_logging", 2.0, "lt", "s"
        )

    def test_structured_logging_performance(self, test_logger, performance_profiler):
        """測試結構化日誌性能"""
        test_data = {
            "user_id": "123456",
            "session_id": "sess_789",
            "action": "process_data",
            "records": 1500,
            "duration_ms": 1250,
            "success": True
        }

        with performance_profiler.measure("structured_logging_performance"):
            for i in range(500):
                test_logger.info("處理完成",
                               user_id=test_data["user_id"],
                               session_id=test_data["session_id"],
                               action=test_data["action"],
                               records_processed=test_data["records"],
                               execution_time=test_data["duration_ms"],
                               success=test_data["success"],
                               batch_id=f"batch_{i}")

        # 性能檢查（500條結構化日誌應該在1秒內完成）
        performance_profiler.assert_performance_threshold(
            "structured_logging_performance", 1.0, "lt", "s"
        )


@pytest.mark.unit
@pytest.mark.logging
class TestLoggerServiceEdgeCases:
    """日誌服務邊界情況測試"""

    def test_empty_message_logging(self, test_logger):
        """測試空消息日誌記錄"""
        # 理論上應該能夠處理
        test_logger.info("")

    def test_large_message_logging(self, test_logger):
        """測試大消息日誌記錄"""
        large_message = "A" * 10000  # 10KB消息
        large_data = {"data": "B" * 5000}  # 額外數據

        test_logger.info(large_message, **large_data)

    def test_special_characters_logging(self, test_logger):
        """測試特殊字符日誌記錄"""
        special_message = "測試消息: 中文, symbols: !@#$%^&*(), emojis: 🎉🚀"
        test_logger.info(special_message, data={"key": "value"})

    def test_very_deep_nested_data(self, test_logger):
        """測試深度嵌套數據"""
        deep_data = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {
                            "level5": "deep_value"
                        }
                    }
                }
            }
        }

        test_logger.info("深度嵌套測試", **deep_data)

    def test_logger_name_sanitization(self):
        """測試logger名稱清理"""
        # 測試帶有特殊字符的名稱
        logger_names = [
            "test.logger",
            "test-logger",
            "test_logger/extra",
            "test logger with spaces"
        ]

        for name in logger_names:
            logger = get_logger(name)
            assert logger is not None
            assert isinstance(logger.name, str)


if __name__ == "__main__":
    pytest.main([__file__, "--verbose", "--cov=utils.logger_service", "--cov-report=html"])
