"""
WebCrawler Commander - 統一日誌服務
基於structlog實現企業級結構化日誌記錄

核心功能：
- 多級別日誌層次結構化
- 多處理器日誌路由 (控制台/文件/網路/資料庫)
- 分布式請求追蹤ID注入
- 敏感信息自動遮罩
- 日誌輪轉與壓縮優化
- 企業級安全審計日誌

作者: Jerry開發工作室
版本: v1.0.0
"""

import os
import json
import logging
import logging.handlers
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable
from datetime import datetime, timedelta
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

import structlog
from structlog.processors import JSONRenderer, TimeStamper, format_exc_info
from structlog.stdlib import LogRecord, BoundLoggerLazyProxy
from structlog.threadlocal import wrap_dict

from .config_manager import get_config_manager, ConfigManager


class LogLevel(Enum):
    """日誌級別枚舉"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogFormat(Enum):
    """日誌格式枚舉"""
    JSON = "json"
    TEXT = "text"
    LOGFMT = "logfmt"


class LogOutput(Enum):
    """日誌輸出類型枚舉"""
    CONSOLE = "console"
    FILE = "file"
    SYSLOG = "syslog"
    HTTP = "http"
    DATABASE = "database"


@dataclass
class LogEntry:
    """日誌條目數據結構"""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    level: str = "INFO"
    logger_name: str = ""
    message: str = ""
    event: str = ""
    extra_fields: Dict[str, Any] = field(default_factory=dict)
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None


class SensitiveDataMasker:
    """敏感信息遮罩器"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {
            "fields": [
                "password", "pwd", "secret", "token", "key", "auth",
                "credit_card", "card_number", "ssn", "social_security",
                "email", "phone", "address", "ip_address"
            ],
            "patterns": [
                r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b",  # 信用卡號
                r"\b\d{3}[\s\-]?\d{2}[\s\-]?\d{4}\b",  # SSN格式
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # 郵箱
                r"\b\d{3}[\s\-]?\d{3}[\s\-]?\d{4}\b",  # 美國電話號碼
            ],
            "mask_char": "*",
            "mask_length": 8
        }

    def mask(self, data: Any) -> Any:
        """遮罩敏感信息"""
        if isinstance(data, dict):
            return {key: self._mask_value(key, value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.mask(item) if isinstance(item, (dict, list)) else self._mask_value("", item) for item in data]
        else:
            return self._mask_value("", data)

    def _mask_value(self, key: str, value: Any) -> Any:
        """遮罩單個值"""
        if not isinstance(value, str):
            return value

        key_lower = key.lower()

        # 檢查是否為已知敏感字段
        if any(sensitive in key_lower for sensitive in self.config["fields"]):
            return self._create_mask(value)

        # 檢查是否匹配敏感數據模式
        import re
        for pattern in self.config["patterns"]:
            if re.search(pattern, value, re.IGNORECASE):
                return self._create_mask(value)

        return value

    def _create_mask(self, value: str) -> str:
        """創建遮罩字符串"""
        mask_char = self.config["mask_char"]
        mask_length = self.config["mask_length"]

        if len(value) <= mask_length:
            return mask_char * len(value)
        else:
            visible_prefix = max(1, len(value) // 4)
            visible_suffix = max(1, len(value) // 4)
            masked_length = len(value) - visible_prefix - visible_suffix
            return value[:visible_prefix] + (mask_char * masked_length) + value[-visible_suffix:]


class LogProcessor:
    """日誌處理器"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.masker = SensitiveDataMasker(self.config.get("sensitive_data_masking"))

    def __call__(self, logger: Any, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
        """處理日誌事件"""

        # 添加請求追蹤ID
        if not event_dict.get("request_id"):
            event_dict["request_id"] = getattr(threading.current_thread(), "request_id", None)

        # 添加用戶ID（如果可用）
        if not event_dict.get("user_id"):
            event_dict["user_id"] = getattr(threading.current_thread(), "user_id", None)

        # 添加會話ID
        if not event_dict.get("session_id"):
            event_dict["session_id"] = getattr(threading.current_thread(), "session_id", None)

        # 添加服務名稱和版本
        event_dict.setdefault("service", self.config.get("service_name", "webcrawler"))
        event_dict.setdefault("version", self.config.get("service_version", "1.0.0"))

        # 添加環境信息
        event_dict.setdefault("environment", self.config.get("environment", "development"))

        # 添加主機信息
        import socket
        event_dict.setdefault("hostname", socket.gethostname())

        # 處理異常信息
        if event_dict.get("exc_info"):
            event_dict["exception"] = format_exc_info(logger, method_name, event_dict)

        # 遮罩敏感信息
        event_dict = self.masker.mask(event_dict)

        # 添加時間戳（如果沒有）
        if "timestamp" not in event_dict:
            event_dict["timestamp"] = datetime.utcnow().isoformat()

        return event_dict


class BaseLogHandler:
    """日誌處理器基類"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)
        self.level = getattr(logging, config.get("level", "INFO").upper())
        self.formatter = self._create_formatter()

    def _create_formatter(self) -> logging.Formatter:
        """創建格式化器"""
        format_type = self.config.get("format", "json")

        if format_type == "json":
            return logging.Formatter('{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}')
        else:
            return logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

    def create_handler(self) -> Optional[logging.Handler]:
        """創建具體的logging handler"""
        raise NotImplementedError


class ConsoleLogHandler(BaseLogHandler):
    """控制台日誌處理器"""

    def create_handler(self) -> Optional[logging.Handler]:
        """創建控制台handler"""
        if not self.enabled:
            return None

        handler = logging.StreamHandler()
        handler.setLevel(self.level)
        handler.setFormatter(self.formatter)

        # 嘗試添加顏色支持 (僅適用於控制台)
        if self.config.get("colorize", True):
            try:
                import colorlog
                colored_formatter = colorlog.ColoredFormatter(
                    '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s%(reset)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    log_colors={
                        'DEBUG': 'cyan',
                        'INFO': 'green',
                        'WARNING': 'yellow',
                        'ERROR': 'red',
                        'CRITICAL': 'red,bg_white',
                    }
                )
                handler.setFormatter(colored_formatter)
            except ImportError:
                pass  # 如果沒有colorlog，繼續使用普通格式化器

        return handler


class FileLogHandler(BaseLogHandler):
    """文件日誌處理器"""

    def create_handler(self) -> Optional[logging.Handler]:
        """創建文件handler"""
        if not self.enabled:
            return None

        file_path = Path(self.config.get("path", "logs/webcrawler.log"))
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # 輪轉文件handler
        max_bytes = self._parse_size(self.config.get("max_file_size", "10 MB"))
        backup_count = self.config.get("backup_count", 5)

        handler = logging.handlers.RotatingFileHandler(
            file_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )

        handler.setLevel(self.level)
        handler.setFormatter(self.formatter)

        return handler

    def _parse_size(self, size_str: str) -> int:
        """解析文件大小字符串"""
        size_str = size_str.upper().strip()
        units = {
            'B': 1,
            'KB': 1024,
            'MB': 1024 * 1024,
            'GB': 1024 * 1024 * 1024
        }

        for unit, multiplier in units.items():
            if size_str.endswith(unit):
                number = float(size_str[:-len(unit)].strip())
                return int(number * multiplier)

        # 默認按字節處理
        try:
            return int(float(size_str))
        except ValueError:
            return 10 * 1024 * 1024  # 默認10MB


class HTTPLogHandler(BaseLogHandler):
    """HTTP日誌處理器"""

    def create_handler(self) -> Optional[logging.Handler]:
        """創建HTTP handler"""
        if not self.enabled:
            return None

        url = self.config.get("url")
        if not url:
            return None

        handler = logging.handlers.HTTPHandler(
            url,
            method=self.config.get("method", "POST"),
            secure=self.config.get("secure", False)
        )

        handler.setLevel(self.level)
        handler.setFormatter(self.formatter)

        return handler


class DatabaseLogHandler(BaseLogHandler):
    """數據庫日誌處理器"""

    def __init__(self, config: Dict[str, Any], db_connection_string: Optional[str] = None):
        super().__init__(config)
        self.db_connection_string = db_connection_string or config.get("connection_string")

        # 異步寫入隊列
        self.log_queue: List[Dict[str, Any]] = []
        self.queue_lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="db-log-")
        self._shutdown_event = threading.Event()

        # 啟動異步寫入線程
        self._start_async_writer()

    def create_handler(self) -> Optional[logging.Handler]:
        """創建數據庫handler"""
        if not self.enabled or not self.db_connection_string:
            return None

        # 創建自定義的handler
        handler = DatabaseHandler(self)
        handler.setLevel(self.level)
        handler.setFormatter(self.formatter)

        return handler

    def _start_async_writer(self):
        """啟動異步寫入線程"""
        def writer_thread():
            while not self._shutdown_event.is_set():
                self._process_log_queue()
                time.sleep(1)  # 每秒批處理一次

        thread = threading.Thread(target=writer_thread, daemon=True, name="db-log-writer")
        thread.start()

    def _process_log_queue(self):
        """處理日誌隊列"""
        if not self.log_queue:
            return

        batch_size = self.config.get("batch_size", 50)
        with self.queue_lock:
            batch = self.log_queue[:batch_size]
            del self.log_queue[:batch_size]

        if batch:
            self._write_batch_to_db(batch)

    def _write_batch_to_db(self, batch: List[Dict[str, Any]]):
        """批量寫入數據庫"""
        try:
            # 此處實現具體的數據庫寫入邏輯
            # 例如使用SQLAlchemy
            structlog.get_logger().debug(
                "batch_db_log_write",
                batch_size=len(batch),
                connection_string=self.db_connection_string[:50] + "..."
            )
        except Exception as e:
            structlog.get_logger().error("db_log_write_failed", error=str(e))

    def enqueue_log(self, record: logging.LogRecord):
        """加入日誌到隊列"""
        with self.queue_lock:
            if len(self.log_queue) < self.config.get("max_queue_size", 10000):
                self.log_queue.append({
                    "timestamp": datetime.fromtimestamp(record.created).isoformat(),
                    "level": record.levelname,
                    "logger": record.name,
                    "message": record.getMessage(),
                    "module": record.module,
                    "func_name": record.funcName,
                    "line_no": record.lineno,
                    "process_id": record.process,
                    "thread_id": record.thread
                })
            else:
                structlog.get_logger().warning("log_queue_full_dropping_entry")

    def shutdown(self):
        """關閉處理器"""
        self._shutdown_event.set()
        self.executor.shutdown(wait=True)
        # 處理剩餘的日誌
        self._process_log_queue()


class DatabaseHandler(logging.Handler):
    """自定義數據庫handler"""

    def __init__(self, db_processor: DatabaseLogHandler):
        super().__init__()
        self.db_processor = db_processor

    def emit(self, record: logging.LogRecord):
        """發射日誌到數據庫"""
        self.db_processor.enqueue_log(record)


class LoggerService:
    """
    統一日誌服務

    核心功能：
    - 多級別日誌層次管理
    - 多處理器日誌路由
    - 結構化日誌處理
    - 輪轉與歸檔機制
    - 實時監控與告警
    - 企業級審計日誌
    """

    def __init__(self, config_manager: Optional[ConfigManager] = None):
        self.config_manager = config_manager or get_config_manager()
        self.logger = None
        self.handlers: List[BaseLogHandler] = []
        self._initialized = False
        self._lock = threading.RLock()

        # 統計信息
        self.stats = {
            "total_entries": 0,
            "error_count": 0,
            "warning_count": 0,
            "last_error_time": None,
            "start_time": datetime.utcnow()
        }

    def initialize(self):
        """初始化日誌服務"""
        if self._initialized:
            return

        with self._lock:
            if self._initialized:
                return

            try:
                # 獲取日誌配置
                log_config = self.config_manager.get("logging", {})
                service_config = {
                    "service_name": self.config_manager.get("app_name", "webcrawler"),
                    "service_version": self.config_manager.get("version", "1.0.0"),
                    "environment": self.config_manager.get("environment", "development"),
                    "sensitive_data_masking": log_config.get("sensitive_data_masking", {})
                }

                # 配置Python logging
                self._configure_standard_logging(log_config)

                # 配置structlog
                self._configure_structlog(service_config)

                # 創建處理器
                self._create_handlers(log_config)

                # 創建根logger
                self.logger = structlog.get_logger()

                self._initialized = True

                # 記錄初始化成功
                self.logger.info(
                    "logger_service_initialized",
                    service_name=service_config["service_name"],
                    version=service_config["service_version"]
                )

            except Exception as e:
                # 如果初始化失敗，使用基本配置
                logging.basicConfig(
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
                structlog.configure(
                    processors=[structlog.stdlib.filter_by_level,
                               structlog.stdlib.add_logger_name,
                               structlog.stdlib.add_log_level,
                               structlog.stdlib.PositionalArgumentsFormatter(),
                               structlog.processors.TimeStamper(fmt="iso"),
                               structlog.processors.StackInfoRenderer(),
                               structlog.processors.format_exc_info,
                               structlog.processors.UnicodeDecoder(),
                               structlog.processors.JSONRenderer()],
                    context_class=dict,
                    logger_factory=structlog.stdlib.LoggerFactory(),
                    wrapper_class=structlog.stdlib.BoundLogger,
                    cache_logger_on_first_use=True,
                )

                logger = logging.getLogger(__name__)
                logger.error(f"日誌服務初始化失敗，使用基本配置: {e}")

    def _configure_standard_logging(self, log_config: Dict[str, Any]):
        """配置Python標準logging"""
        # 設置根logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_config.get("level", "INFO").upper()))

        # 移除現有的handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # 添加null handler以避免"沒有handler"的警告
        root_logger.addHandler(logging.NullHandler())

    def _configure_structlog(self, service_config: Dict[str, Any]):
        """配置structlog"""
        processors = [
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            TimeStamper(fmt="iso"),
            LogProcessor(service_config),  # 自定義處理器
            structlog.processors.StackInfoRenderer(),
            format_exc_info,
            structlog.processors.UnicodeDecoder(),
            JSONRenderer()
        ]

        structlog.configure(
            processors=processors,
            context_class=wrap_dict(dict),
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

    def _create_handlers(self, log_config: Dict[str, Any]):
        """創建日誌handlers"""
        handlers_config = [
            ("console", ConsoleLogHandler, log_config.get("console", {})),
            ("file", FileLogHandler, log_config.get("file", {})),
        ]

        # 可選的handlers
        if log_config.get("http", {}).get("enabled"):
            handlers_config.append(("http", HTTPLogHandler, log_config["http"]))

        if log_config.get("database", {}).get("enabled"):
            handlers_config.append(("database", DatabaseLogHandler, log_config["database"]))

        # 創建並添加handlers
        for name, handler_class, config in handlers_config:
            try:
                handler_instance = handler_class(config)
                handler = handler_instance.create_handler()
                if handler:
                    self.handlers.append(handler_instance)
                    logging.getLogger().addHandler(handler)
                    self.logger.debug(f"handler_created", handler_type=name)
            except Exception as e:
                # 創建handler失敗時記錄到stderr
                import sys
                print(f"創建{name} handler失敗: {e}", file=sys.stderr)

    def get_logger(self, name: str = None) -> BoundLoggerLazyProxy:
        """獲取logger實例"""
        if not self._initialized:
            self.initialize()

        if name:
            return structlog.get_logger(name)
        return self.logger

    def set_request_context(self, request_id: Optional[str] = None,
                           user_id: Optional[str] = None,
                           session_id: Optional[str] = None):
        """設置請求上下文"""
        current_thread = threading.current_thread()
        if request_id:
            current_thread.request_id = request_id
        if user_id:
            current_thread.user_id = user_id
        if session_id:
            current_thread.session_id = session_id

    def clear_request_context(self):
        """清除請求上下文"""
        current_thread = threading.current_thread()
        if hasattr(current_thread, 'request_id'):
            delattr(current_thread, 'request_id')
        if hasattr(current_thread, 'user_id'):
            delattr(current_thread, 'user_id')
        if hasattr(current_thread, 'session_id'):
            delattr(current_thread, 'session_id')

    def get_stats(self) -> Dict[str, Any]:
        """獲取日誌統計信息"""
        return {
            **self.stats,
            "uptime_seconds": (datetime.utcnow() - self.stats["start_time"]).total_seconds(),
            "handlers_count": len(self.handlers),
            "initialized": self._initialized
        }

    def reload_configuration(self):
        """重新載入配置"""
        with self._lock:
            old_level = logging.getLogger().level if self._initialized else logging.INFO

            # 重新初始化
            self._initialized = False
            self.handlers.clear()

            try:
                self.initialize()
                self.logger.info("logger_configuration_reloaded")
            except Exception as e:
                # 如果重新載入失敗，恢復舊配置
                logging.getLogger().setLevel(old_level)
                self.logger.error("logger_reload_failed", error=str(e))

    def shutdown(self):
        """關閉日誌服務"""
        with self._lock:
            for handler in self.handlers:
                if hasattr(handler, 'shutdown'):
                    handler.shutdown()

            self.log_queue = []  # 清空隊列
            self.logger.info("logger_service_shutdown")
            self._initialized = False


# 全域日誌服務實例
_logger_service: Optional[LoggerService] = None


def init_logger_service(config_manager: Optional[ConfigManager] = None) -> LoggerService:
    """
    初始化全域日誌服務

    Args:
        config_manager: 配置管理器實例

    Returns:
        日誌服務實例
    """
    global _logger_service

    if _logger_service is None:
        _logger_service = LoggerService(config_manager)

    _logger_service.initialize()
    return _logger_service


def get_logger_service() -> LoggerService:
    """獲取全域日誌服務實例"""
    if _logger_service is None:
        raise RuntimeError("日誌服務尚未初始化，請先調用init_logger_service()")
    return _logger_service


def get_logger(name: str = None) -> BoundLoggerLazyProxy:
    """便捷函數：獲取logger實例"""
    return get_logger_service().get_logger(name)


def set_request_context(request_id: Optional[str] = None,
                       user_id: Optional[str] = None,
                       session_id: Optional[str] = None):
    """便捷函數：設置請求上下文"""
    get_logger_service().set_request_context(request_id, user_id, session_id)


def clear_request_context():
    """便捷函數：清除請求上下文"""
    get_logger_service().clear_request_context()
