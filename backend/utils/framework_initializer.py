"""
WebCrawler Commander - 統一框架初始化器
負責所有後端框架的統一初始化和配置

功能特色：
- 統一框架初始化順序
- 配置驗證與健康檢查
- 各組件依賴注入
- 啟動時系統健康評估
- 運行時狀態監控
"""

import asyncio
import threading
import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
import json

from .logger_service import get_logger
from .config_manager import get_config_manager
from .error_handler import get_error_handler
from .performance_monitor import get_performance_monitor
from .audit_logger import get_audit_logger, audit_log, AuditLevel, AuditCategory

from ..data_processing.data_processor import init_data_processor, get_data_processor
from ..services.pii_detector import init_pii_detector, get_pii_detector
from ..services.proxy_validator import get_proxy_validator
from ..services.task_scheduler import get_task_scheduler
from ..services.template_manager import get_template_manager
from ..services.content_parser import get_content_parser
from ..services.data_validator import get_data_validator


class SystemHealthStatus:
    """系統健康狀態"""
    def __init__(self):
        self.overall_status = "initializing"
        self.component_statuses: Dict[str, Dict[str, Any]] = {}
        self.last_health_check = datetime.utcnow()
        self.initialization_time = datetime.utcnow()
        self.startup_warnings: List[str] = []
        self.critical_errors: List[str] = []

    def update_component_status(self, component_name: str,
                               status: str, details: Optional[Dict[str, Any]] = None):
        """更新組件狀態"""
        self.component_statuses[component_name] = {
            "status": status,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details or {}
        }

    def get_health_summary(self) -> Dict[str, Any]:
        """獲取健康摘要"""
        healthy_components = sum(1 for comp in self.component_statuses.values()
                               if comp["status"] == "healthy")

        total_components = len(self.component_statuses)

        return {
            "overall_status": self.overall_status,
            "healthy_components": healthy_components,
            "total_components": total_components,
            "health_percentage": (healthy_components / total_components * 100) if total_components > 0 else 0,
            "last_health_check": self.last_health_check.isoformat(),
            "uptime_seconds": (datetime.utcnow() - self.initialization_time).total_seconds(),
            "startup_warnings": self.startup_warnings,
            "critical_errors": self.critical_errors,
            "component_statuses": self.component_statuses
        }


class FrameworkInitializer:
    """
    框架初始化器

    負責整個後端框架的有序初始化：
    - 配置管理器初始化
    - 日誌系統初始化
    - 錯誤處理框架初始化
    - 性能監控系統初始化
    - 審計日誌系統初始化
    - 業務組件初始化
    - 健康檢查與驗證
    """

    def __init__(self):
        self.logger = None  # 將在初始化時設置
        self.config_manager = None
        self.error_handler = None
        self.performance_monitor = None
        self.audit_logger = None
        self.health_status = SystemHealthStatus()

        # 初始化順序 - 必須按此順序初始化
        self.init_sequence = [
            "config_manager",
            "logger_service",
            "error_handler",
            "performance_monitor",
            "audit_logger",
            "data_processor",
            "pii_detector",
            "proxy_validator",
            "task_scheduler",
            "template_manager",
            "content_parser",
            "data_validator",
            "health_verification"
        ]

    async def initialize_system(self) -> SystemHealthStatus:
        """
        初始化整個系統

        Returns:
            系統健康狀態
        """
        start_time = datetime.utcnow()
        self.health_status.initialization_time = start_time

        try:
            # 按順序初始化各組件
            for component in self.init_sequence:
                try:
                    await self._initialize_component(component)
                    self.health_status.update_component_status(component, "healthy", {"init_time": datetime.utcnow().isoformat()})
                except Exception as e:
                    error_msg = f"組件 {component} 初始化失敗: {str(e)}"
                    self.health_status.critical_errors.append(error_msg)
                    self.health_status.update_component_status(component, "failed", {"error": str(e)})

                    # 記錄到錯誤處理器（如果已初始化）
                    if self.error_handler:
                        context = ErrorContext(
                            component="framework_initializer",
                            operation=f"init_{component}",
                            metadata={"init_phase": "component_initialization"}
                        )
                        self.error_handler.handle_error(e, context)

            # 進行最終健康檢查
            await self._perform_final_health_check()

            # 設置整體狀態
            if self.health_status.critical_errors:
                self.health_status.overall_status = "degraded"
            else:
                self.health_status.overall_status = "healthy"

            # 記錄初始化完成
            total_time = (datetime.utcnow() - start_time).total_seconds()

            if self.audit_logger:
                audit_log(
                    level=AuditLevel.ACTION,
                    category=AuditCategory.SYSTEM_MAINTENANCE,
                    action="system_initialization",
                    actor="system",
                    target="webcrawler_commander",
                    result="SUCCESS" if not self.health_status.critical_errors else "PARTIAL_SUCCESS",
                    details={
                        "init_time_seconds": total_time,
                        "components_initialized": len(self.health_status.component_statuses),
                        "health_percentage": self.health_status.get_health_summary()["health_percentage"]
                    }
                )

            if self.logger:
                self.logger.info("system_initialization_completed",
                               init_time_seconds=round(total_time, 2),
                               overall_status=self.health_status.overall_status,
                               healthy_components=sum(1 for comp in self.health_status.component_statuses.values()
                                                    if comp["status"] == "healthy"))

        except Exception as e:
            self.health_status.overall_status = "failed"
            self.health_status.critical_errors.append(f"系統初始化失敗: {str(e)}")

            # 使用basic logging if available
            try:
                if self.logger:
                    self.logger.error("system_initialization_failed", error=str(e))
            except:
                print(f"CRITICAL: System initialization failed: {e}")

        return self.health_status

    async def _initialize_component(self, component_name: str):
        """初始化特定組件"""
        if component_name == "config_manager":
            # 配置管理器必須第一個初始化
            from .config_manager import get_config_manager
            self.config_manager = get_config_manager()
            # 驗證配置完整性
            await self._validate_config()

        elif component_name == "logger_service":
            # 日誌服務第二個初始化
            from .logger_service import get_logger
            self.logger = get_logger("framework_initializer")
            self.logger.info("logger_service_initialized")

        elif component_name == "error_handler":
            # 錯誤處理器
            self.error_handler = get_error_handler("system")
            self.logger.info("error_handler_initialized")

        elif component_name == "performance_monitor":
            # 性能監控器
            self.performance_monitor = get_performance_monitor("system")
            # 設置系統級性能基準
            self.performance_monitor.set_benchmark("system_memory_mb", 1024.0, 20, "production")
            self.performance_monitor.set_benchmark("system_cpu_percent", 80.0, 15, "production")
            self.logger.info("performance_monitor_initialized")

        elif component_name == "audit_logger":
            # 審計日誌器
            self.audit_logger = get_audit_logger()
            self.logger.info("audit_logger_initialized")

        elif component_name == "data_processor":
            # 數據處理器
            self.data_processor = init_data_processor(self.config_manager)
            self.logger.info("data_processor_initialized")

        elif component_name == "pii_detector":
            # PII檢測器
            self.pii_detector = init_pii_detector(self.config_manager)
            self.logger.info("pii_detector_initialized")

        elif component_name == "proxy_validator":
            # 代理驗證器
            self.proxy_validator = get_proxy_validator()
            self.logger.info("proxy_validator_initialized")

        elif component_name == "task_scheduler":
            # 任務調度器
            self.task_scheduler = get_task_scheduler()
            self.logger.info("task_scheduler_initialized")

        elif component_name == "template_manager":
            # 模板管理器
            self.template_manager = get_template_manager()
            self.logger.info("template_manager_initialized")

        elif component_name == "content_parser":
            # 內容解析器
            self.content_parser = get_content_parser()
            self.logger.info("content_parser_initialized")

        elif component_name == "data_validator":
            # 數據驗證器
            self.data_validator = get_data_validator()
            self.logger.info("data_validator_initialized")

        elif component_name == "health_verification":
            # 最終健康驗證
            await self._perform_component_health_checks()

    async def _validate_config(self):
        """驗證系統配置"""
        required_configs = [
            "data_processing",
            "pii_detection",
            "proxy_validation",
            "task_scheduling"
        ]

        missing_configs = []
        for config_key in required_configs:
            config = self.config_manager.get(config_key)
            if not config:
                missing_configs.append(config_key)

        if missing_configs:
            warning = f"缺少配置項: {', '.join(missing_configs)}"
            self.health_status.startup_warnings.append(warning)
            if self.logger:
                self.logger.warning("config_validation_warnings", missing_configs=missing_configs)

    async def _perform_component_health_checks(self):
        """執行組件健康檢查"""
        health_checks = {
            "data_processor": self._check_data_processor_health,
            "pii_detector": self._check_pii_detector_health,
            "proxy_validator": self._check_proxy_validator_health,
            "task_scheduler": self._check_task_scheduler_health
        }

        for component_name, check_func in health_checks.items():
            try:
                health_info = await check_func()
                self.health_status.update_component_status(
                    component_name,
                    "healthy" if health_info["healthy"] else "degraded",
                    health_info
                )
            except Exception as e:
                self.health_status.startup_warnings.append(f"{component_name} 健康檢查失敗: {str(e)}")
                self.health_status.update_component_status(component_name, "unhealthy", {"error": str(e)})

    async def _check_data_processor_health(self) -> Dict[str, Any]:
        """檢查數據處理器健康狀態"""
        try:
            processor = get_data_processor()
            # 執行簡單的測試處理
            test_record = DataRecord({"test_field": "test_value"})
            result = await processor.process_data([test_record])
            return {
                "healthy": result.success,
                "processed_records": result.output_count,
                "processing_time": result.processing_time
            }
        except Exception as e:
            return {"healthy": False, "error": str(e)}

    async def _check_pii_detector_health(self) -> Dict[str, Any]:
        """檢查PII檢測器健康狀態"""
        try:
            detector = get_pii_detector()
            health = await detector.health_check()
            return {
                "healthy": health["status"] == "healthy",
                "total_processed": health["stats"]["total_processed"],
                "anonymized_count": health["stats"]["anonymized_count"]
            }
        except Exception as e:
            return {"healthy": False, "error": str(e)}

    async def _check_proxy_validator_health(self) -> Dict[str, Any]:
        """檢查代理驗證器健康狀態"""
        try:
            validator = get_proxy_validator()
            # 簡單的健康檢查 - 驗證組件載入
            return {
                "healthy": True,
                "status": "component_loaded"
            }
        except Exception as e:
            return {"healthy": False, "error": str(e)}

    async def _check_task_scheduler_health(self) -> Dict[str, Any]:
        """檢查任務調度器健康狀態"""
        try:
            scheduler = get_task_scheduler()
            # 檢查是否有活躍任務
            return {
                "healthy": True,
                "status": "scheduler_active"
            }
        except Exception as e:
            return {"healthy": False, "error": str(e)}

    async def _perform_final_health_check(self):
        """執行最終系統健康檢查"""
        self.health_status.last_health_check = datetime.utcnow()

        # 檢查關鍵依賴
        critical_components = ["data_processor", "pii_detector", "proxy_validator"]
        critical_failures = []

        for component in critical_components:
            status = self.health_status.component_statuses.get(component, {})
            if status.get("status") != "healthy":
                critical_failures.append(component)

        if critical_failures:
            self.health_status.critical_errors.extend([
                f"關鍵組件失敗: {', '.join(critical_failures)}"
            ])

    def get_system_status(self) -> Dict[str, Any]:
        """獲取當前系統狀態"""
        return {
            **self.health_status.get_health_summary(),
            "framework_components": {
                "config_manager": bool(self.config_manager),
                "logger": bool(self.logger),
                "error_handler": bool(self.error_handler),
                "performance_monitor": bool(self.performance_monitor),
                "audit_logger": bool(self.audit_logger)
            }
        }

    async def shutdown_system(self):
        """優雅關閉系統"""
        self.logger.info("system_shutdown_initiated")

        shutdown_tasks = [
            self._shutdown_data_processor,
            self._shutdown_performance_monitor,
            self._shutdown_audit_logger
        ]

        for shutdown_task in shutdown_tasks:
            try:
                await shutdown_task()
            except Exception as e:
                if self.logger:
                    self.logger.warning("shutdown_task_failed",
                                      task=shutdown_task.__name__,
                                      error=str(e))

        self.logger.info("system_shutdown_completed")

    async def _shutdown_data_processor(self):
        """關閉數據處理器"""
        # 在這裡實現數據處理器的清理邏輯
        pass

    async def _shutdown_performance_monitor(self):
        """關閉性能監控器"""
        # 導出最後的性能指標
        if self.performance_monitor:
            try:
                export_data = self.performance_monitor.export_metrics()
                # 保存到文件或數據庫
            except Exception as e:
                if self.logger:
                    self.logger.warning("performance_data_export_failed", error=str(e))

    async def _shutdown_audit_logger(self):
        """關閉審計日誌器"""
        # 確保所有待處理的審計事件都被寫入
        if self.audit_logger:
            try:
                self.audit_logger._archive_old_events(force=True)
            except Exception as e:
                if self.logger:
                    self.logger.warning("audit_log_archive_failed", error=str(e))


# 全域框架初始化器實例
_framework_initializer: Optional[FrameworkInitializer] = None


async def initialize_framework() -> SystemHealthStatus:
    """
    初始化整個框架

    Returns:
        系統健康狀態
    """
    global _framework_initializer

    if _framework_initializer is None:
        _framework_initializer = FrameworkInitializer()

    return await _framework_initializer.initialize_system()


def get_framework_initializer() -> Optional[FrameworkInitializer]:
    """獲取框架初始化器實例"""
    return _framework_initializer


async def shutdown_framework():
    """關閉整個框架"""
    global _framework_initializer

    if _framework_initializer:
        await _framework_initializer.shutdown_system()


def quick_health_check() -> Dict[str, Any]:
    """快速健康檢查"""
    if _framework_initializer:
        return _framework_initializer.get_system_status()
    else:
        return {"status": "not_initialized"}


# 導入所需的模塊
from ..data_processing.data_processor import DataRecord
