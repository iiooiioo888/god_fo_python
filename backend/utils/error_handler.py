"""
WebCrawler Commander - 統一錯誤處理框架
提供企業級錯誤處理和恢復機制

功能特色：
- 分層異常處理架構
- 錯誤分類與標準化
- 自動恢復策略
- 錯誤追蹤與日誌
- 性能指標監控
"""

import os
import sys
import traceback
import functools
import asyncio
import threading
from typing import Dict, List, Optional, Any, Union, Callable, Type
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor
import json
import http

from .logger_service import get_logger


class ErrorLevel(Enum):
    """錯誤等級枚舉"""
    CRITICAL = "CRITICAL"  # 系統級嚴重錯誤
    ERROR = "ERROR"        # 業務邏輯錯誤
    WARNING = "WARNING"    # 警告級別錯誤
    INFO = "INFO"         # 資訊級別通知
    DEBUG = "DEBUG"       # 調試級別


class ErrorCategory(Enum):
    """錯誤分類枚舉"""
    NETWORK = "NETWORK"           # 網路相關錯誤
    DATABASE = "DATABASE"         # 數據庫相關錯誤
    VALIDATION = "VALIDATION"     # 數據驗證錯誤
    PROCESSING = "PROCESSING"     # 數據處理錯誤
    SECURITY = "SECURITY"         # 安全相關錯誤
    CONFIGURATION = "CONFIGURATION" # 配置相關錯誤
    EXTERNAL_API = "EXTERNAL_API"   # 外部API錯誤
    RESOURCE = "RESOURCE"         # 資源相關錯誤
    SYSTEM = "SYSTEM"             # 系統級錯誤


@dataclass
class ErrorContext:
    """錯誤上下文信息"""
    component: str                    # 錯誤發生的組件名稱
    operation: str                    # 錯誤發生的操作名稱
    user_id: Optional[str] = None     # 相關用戶ID
    session_id: Optional[str] = None  # 會話ID
    request_id: Optional[str] = None  # 請求ID
    ip_address: Optional[str] = None  # IP地址
    user_agent: Optional[str] = None  # 用戶代理
    metadata: Dict[str, Any] = field(default_factory=dict)  # 附加元數據


@dataclass
class ErrorDetails:
    """錯誤詳情"""
    code: str                         # 錯誤代碼
    message: str                      # 錯誤訊息
    level: ErrorLevel                # 錯誤等級
    category: ErrorCategory          # 錯誤分類
    context: ErrorContext            # 錯誤上下文
    exception_type: Optional[str] = None  # 原始異常類型
    stack_trace: Optional[str] = None   # 堆疊追蹤
    timestamp: datetime = field(default_factory=datetime.utcnow)
    retry_count: int = 0             # 重試次數
    recovery_attempts: List[str] = field(default_factory=list)  # 恢復嘗試記錄

    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典"""
        return {
            "code": self.code,
            "message": self.message,
            "level": self.level.value,
            "category": self.category.value,
            "context": {
                "component": self.context.component,
                "operation": self.context.operation,
                "user_id": self.context.user_id,
                "session_id": self.context.session_id,
                "request_id": self.context.request_id,
                "ip_address": self.context.ip_address,
                "metadata": self.context.metadata
            },
            "exception_type": self.exception_type,
            "timestamp": self.timestamp.isoformat(),
            "retry_count": self.retry_count,
            "recovery_attempts": self.recovery_attempts
        }


class RecoveryStrategy(Enum):
    """恢復策略枚舉"""
    RETRY = "RETRY"              # 重試操作
    FALLBACK = "FALLBACK"        # 使用備用方案
    CIRCUIT_BREAKER = "CIRCUIT_BREAKER"  # 熔斷器模式
    DEGRADED_MODE = "DEGRADED_MODE"      # 降級模式
    SKIP = "SKIP"                # 跳過錯誤繼續處理
    TERMINATE = "TERMINATE"      # 終止處理


@dataclass
class RecoveryConfig:
    """恢復配置"""
    strategy: RecoveryStrategy
    max_retries: int = 3
    retry_delay: float = 1.0  # 秒
    exponential_backoff: bool = True
    circuit_breaker_threshold: int = 5  # 連續失敗次數閾值
    fallback_function: Optional[Callable] = None
    degraded_response: Any = None


class ErrorHandler:
    """
    統一錯誤處理器

    提供企業級錯誤處理服務：
    - 錯誤捕獲與分類
    - 自動恢復策略
    - 日誌記錄與追蹤
    - 性能指標監控
    """

    def __init__(self, component_name: str):
        self.component_name = component_name
        self.logger = get_logger(f"error_handler.{component_name}")

        # 錯誤統計
        self.error_stats = {
            "total_errors": 0,
            "errors_by_category": {},
            "errors_by_level": {},
            "recovery_attempts": 0,
            "successful_recoveries": 0,
            "circuit_breaker_tripped": 0
        }

        # 恢復配置
        self.recovery_configs: Dict[str, RecoveryConfig] = {}

        # 熔斷器狀態
        self.circuit_breaker_open = {}
        self.consecutive_failures = {}

        # 鎖用於線程安全
        self._lock = threading.Lock()

    def register_recovery_config(self, operation: str, config: RecoveryConfig):
        """註冊恢復配置"""
        self.recovery_configs[operation] = config
        self.logger.info("recovery_config_registered",
                        operation=operation,
                        strategy=config.strategy.value)

    def handle_error(self, error: Exception, context: ErrorContext,
                    operation: Optional[str] = None) -> ErrorDetails:
        """
        處理異常並生成錯誤詳情

        Args:
            error: 原始異常
            context: 錯誤上下文
            operation: 操作名稱（用於確定恢復策略）

        Returns:
            錯誤詳情對象
        """
        # 分類錯誤
        category, level, code = self._classify_error(error, context)

        # 生成錯誤詳情
        error_details = ErrorDetails(
            code=code,
            message=str(error),
            level=level,
            category=category,
            context=context,
            exception_type=type(error).__name__,
            stack_trace=traceback.format_exc()
        )

        # 更新統計
        with self._lock:
            self.error_stats["total_errors"] += 1
            self.error_stats["errors_by_category"][category.value] = \
                self.error_stats["errors_by_category"].get(category.value, 0) + 1
            self.error_stats["errors_by_level"][level.value] = \
                self.error_stats["errors_by_level"].get(level.value, 0) + 1

        # 記錄錯誤
        self._log_error(error_details)

        # 嘗試恢復（如果有操作名稱）
        if operation and operation in self.recovery_configs:
            recovery_success = self._attempt_recovery(error_details, operation)
            if recovery_success:
                with self._lock:
                    self.error_stats["successful_recoveries"] += 1
            else:
                with self._lock:
                    self.error_stats["recovery_attempts"] += 1

        return error_details

    def _classify_error(self, error: Exception, context: ErrorContext) \
                       -> tuple[ErrorCategory, ErrorLevel, str]:
        """
        分類錯誤並確定等級和代碼

        Returns:
            (分類, 等級, 代碼)
        """
        error_type = type(error).__name__
        error_msg = str(error).lower()

        # 網路相關錯誤
        if any(keyword in error_type.lower() or keyword in error_msg for keyword in
               ['connection', 'timeout', 'network', 'http', 'ssl', 'dns']):
            return ErrorCategory.NETWORK, ErrorLevel.ERROR, "NET_001"

        # 數據庫相關錯誤
        if any(keyword in error_type.lower() or keyword in error_msg for keyword in
               ['database', 'sql', 'mongo', 'redis', 'connection', 'cursor']):
            return ErrorCategory.DATABASE, ErrorLevel.ERROR, "DB_001"

        # 驗證相關錯誤
        if any(keyword in error_msg for keyword in
               ['validation', 'invalid', 'required', 'format', 'constraint']):
            return ErrorCategory.VALIDATION, ErrorLevel.WARNING, "VAL_001"

        # 安全相關錯誤
        if any(keyword in error_type.lower() or keyword in error_msg for keyword in
               ['permission', 'authentication', 'authorization', 'security']):
            return ErrorCategory.SECURITY, ErrorLevel.ERROR, "SEC_001"

        # 配置相關錯誤
        if any(keyword in error_msg for keyword in
               ['config', 'configuration', 'missing', 'invalid']):
            return ErrorCategory.CONFIGURATION, ErrorLevel.WARNING, "CFG_001"

        # 資源相關錯誤
        if any(keyword in error_type.lower() or keyword in error_msg for keyword in
               ['memory', 'disk', 'resource', 'ioerror', 'outofmemory']):
            return ErrorCategory.RESOURCE, ErrorLevel.ERROR, "RES_001"

        # 外部API錯誤
        if any(keyword in error_msg for keyword in ['api', 'external', 'third_party']):
            return ErrorCategory.EXTERNAL_API, ErrorLevel.WARNING, "API_001"

        # 處理相關錯誤
        if any(keyword in error_msg for keyword in ['processing', 'transform', 'parse']):
            return ErrorCategory.PROCESSING, ErrorLevel.WARNING, "PRC_001"

        # 系統級錯誤
        if any(keyword in error_type.lower() for keyword in ['systemexit', 'keyboardinterrupt']):
            return ErrorCategory.SYSTEM, ErrorLevel.CRITICAL, "SYS_001"

        # 默認分類為處理錯誤
        return ErrorCategory.PROCESSING, ErrorLevel.ERROR, "GEN_001"

    def _log_error(self, error_details: ErrorDetails):
        """記錄錯誤到日誌"""
        log_data = error_details.to_dict()
        log_data.pop('stack_trace', None)  # 不在基本日誌中包含堆疊追蹤

        if error_details.level == ErrorLevel.CRITICAL:
            self.logger.critical("error_occurred", **log_data, stack_trace=error_details.stack_trace)
        elif error_details.level == ErrorLevel.ERROR:
            self.logger.error("error_occurred", **log_data)
        elif error_details.level == ErrorLevel.WARNING:
            self.logger.warning("error_occurred", **log_data)
        else:
            self.logger.info("error_occurred", **log_data)

    def _attempt_recovery(self, error_details: ErrorDetails, operation: str) -> bool:
        """嘗試恢復操作"""
        config = self.recovery_configs[operation]
        recovery_attempts = []

        try:
            # 檢查熔斷器狀態
            if self._is_circuit_breaker_open(operation):
                recovery_attempts.append("circuit_breaker_open_skipped")
                return False

            if config.strategy == RecoveryStrategy.RETRY:
                return self._retry_operation(error_details, config, recovery_attempts)

            elif config.strategy == RecoveryStrategy.FALLBACK:
                return self._fallback_operation(error_details, config, recovery_attempts)

            elif config.strategy == RecoveryStrategy.DEGRADED_MODE:
                return self._degraded_mode_operation(error_details, config, recovery_attempts)

            elif config.strategy == RecoveryStrategy.SKIP:
                recovery_attempts.append("operation_skipped")
                return True

            elif config.strategy == RecoveryStrategy.TERMINATE:
                recovery_attempts.append("operation_terminated")
                return False

        finally:
            error_details.recovery_attempts = recovery_attempts

        return False

    def _is_circuit_breaker_open(self, operation: str) -> bool:
        """檢查熔斷器是否打開"""
        if operation in self.circuit_breaker_open:
            if datetime.utcnow() < self.circuit_breaker_open[operation]:
                return True
            else:
                # 熔斷器恢復期過了，重置狀態
                self.circuit_breaker_open.pop(operation, None)
                self.consecutive_failures[operation] = 0

        return False

    def _retry_operation(self, error_details: ErrorDetails,
                        config: RecoveryConfig,
                        recovery_attempts: List[str]) -> bool:
        """重試操作"""
        for attempt in range(config.max_retries + 1):  # +1 是因為初始嘗試
            try:
                # 在實際實現中，這裡應該調用原始操作
                # 這裡只是示例邏輯
                recovery_attempts.append(f"retry_attempt_{attempt + 1}")
                error_details.retry_count = attempt + 1

                # 模擬重試邏輯（實際實現需要具體操作函數）
                if attempt < config.max_retries:
                    delay = config.retry_delay
                    if config.exponential_backoff:
                        delay *= (2 ** attempt)
                    asyncio.sleep(delay)

                # 如果這裡成功，應該返回True
                return True

            except Exception as retry_error:
                if attempt == config.max_retries:
                    # 最終失敗，觸發熔斷器
                    with self._lock:
                        self.consecutive_failures[operation] = \
                            self.consecutive_failures.get(operation, 0) + 1

                    if self.consecutive_failures[operation] >= config.circuit_breaker_threshold:
                        self.circuit_breaker_open[operation] = \
                            datetime.utcnow() + timedelta(seconds=60)  # 60秒熔斷
                        with self._lock:
                            self.error_stats["circuit_breaker_tripped"] += 1

                    return False

        return False

    def _fallback_operation(self, error_details: ErrorDetails,
                           config: RecoveryConfig,
                           recovery_attempts: List[str]) -> bool:
        """備用操作"""
        try:
            if config.fallback_function:
                config.fallback_function(error_details)
                recovery_attempts.append("fallback_function_executed")
                return True
            else:
                recovery_attempts.append("fallback_function_not_available")
                return False
        except Exception as fallback_error:
            recovery_attempts.append(f"fallback_failed: {str(fallback_error)}")
            return False

    def _degraded_mode_operation(self, error_details: ErrorDetails,
                                config: RecoveryConfig,
                                recovery_attempts: List[str]) -> bool:
        """降級模式操作"""
        # 降級模式通常返回一個簡化的結果
        recovery_attempts.append("degraded_mode_response_used")
        # 設置降級響應（在實際實現中應該修改操作結果）
        return True

    def get_error_stats(self) -> Dict[str, Any]:
        """獲取錯誤統計信息"""
        with self._lock:
            stats = self.error_stats.copy()

        stats["recovery_success_rate"] = (
            stats["successful_recoveries"] / max(stats["recovery_attempts"], 1)
        ) * 100 if stats["recovery_attempts"] > 0 else 0.0

        return stats

    def reset_stats(self):
        """重置統計信息"""
        with self._lock:
            self.error_stats = {
                "total_errors": 0,
                "errors_by_category": {},
                "errors_by_level": {},
                "recovery_attempts": 0,
                "successful_recoveries": 0,
                "circuit_breaker_tripped": 0
            }


# 全局錯誤處理器實例
_error_handlers: Dict[str, ErrorHandler] = {}


def get_error_handler(component_name: str) -> ErrorHandler:
    """獲取或創建組件的錯誤處理器"""
    if component_name not in _error_handlers:
        _error_handlers[component_name] = ErrorHandler(component_name)

    return _error_handlers[component_name]


def with_error_handling(operation: str, recovery_config: Optional[RecoveryConfig] = None):
    """
    錯誤處理裝飾器

    Args:
        operation: 操作名稱，用於確定恢復策略
        recovery_config: 恢復配置
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            handler = get_error_handler(func.__module__)

            # 註冊恢復配置
            if recovery_config:
                handler.register_recovery_config(operation, recovery_config)

            # 創建錯誤上下文
            context = ErrorContext(
                component=func.__module__,
                operation=operation,
                metadata={
                    "function": func.__name__,
                    "args_count": len(args) - (1 if 'self' in func.__code__.co_varnames[:len(args)] else 0),
                    "kwargs_keys": list(kwargs.keys())
                }
            )

            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as error:
                error_details = handler.handle_error(error, context, operation)
                raise error  # 重新拋出原始異常

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            handler = get_error_handler(func.__module__)

            # 註冊恢復配置
            if recovery_config:
                handler.register_recovery_config(operation, recovery_config)

            # 創建錯誤上下文
            context = ErrorContext(
                component=func.__module__,
                operation=operation,
                metadata={
                    "function": func.__name__,
                    "args_count": len(args) - (1 if 'self' in func.__code__.co_varnames[:len(args)] else 0),
                    "kwargs_keys": list(kwargs.keys())
                }
            )

            try:
                result = func(*args, **kwargs)
                return result
            except Exception as error:
                error_details = handler.handle_error(error, context, operation)
                raise error  # 重新拋出原始異常

        # 選擇合適的包裝器
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def http_status_to_error_category(status_code: int) -> ErrorCategory:
    """將HTTP狀態碼轉換為錯誤分類"""
    if status_code >= 500:
        return ErrorCategory.EXTERNAL_API
    elif status_code >= 400:
        return ErrorCategory.VALIDATION
    elif status_code >= 300:
        return ErrorCategory.NETWORK
    else:
        return ErrorCategory.SYSTEM


def create_error_context(component: str, operation: str, **kwargs) -> ErrorContext:
    """便捷的錯誤上下文創建函數"""
    context = ErrorContext(component=component, operation=operation)
    for key, value in kwargs.items():
        if hasattr(context, key):
            setattr(context, key, value)
        else:
            context.metadata[key] = value

    return context
