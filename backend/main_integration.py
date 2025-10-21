#!/usr/bin/env python3
"""
WebCrawler Commander - 主整合啟動器
系統統一入口點，負責初始化和管理所有服務組件

作者: Jerry開發工作室
版本: v1.0.0
"""

import asyncio
import signal
import sys
import time
from typing import Dict, Any, Optional
from pathlib import Path

# 統一框架組件
from utils.framework_initializer import FrameworkInitializer
from utils.config_manager import get_config_manager
from utils.logger_service import get_logger
from utils.error_handler import get_error_handler
from utils.performance_monitor import get_performance_monitor
from utils.audit_logger import get_audit_logger

# 核心業務服務
from utils.rbac_manager import get_rbac_manager, init_rbac_manager
from utils.encryption_service import get_encryption_service, init_encryption_service
from utils.system_monitor import get_system_monitor, init_system_monitor

# 應用服務
from main import WebCrawlerApp
from data_processing.data_processor import get_data_processor
from services.crawler_engine import get_crawler_engine

# 創建日誌器
logger = get_logger(__name__)


class SystemIntegrationManager:
    """
    系統整合管理器

    負責統籌所有服務的初始化、啟動、運行和關閉
    """

    def __init__(self):
        self.config_manager = get_config_manager()
        self.framework_initializer = FrameworkInitializer()
        self.services: Dict[str, Any] = {}

        # 系統組件
        self.components = {
            'config': self.config_manager,
            'logger': get_logger,
            'error_handler': get_error_handler,
            'performance_monitor': get_performance_monitor,
            'audit_logger': get_audit_logger
        }

        # 系統狀態
        self.system_started = False
        self.system_healthy = False

        logger.info("system_integration_manager_initialized")

    async def initialize_system(self) -> bool:
        """
        初始化系統

        Returns:
            初始化是否成功
        """
        try:
            logger.info("starting_system_initialization")

            # 階段1: 框架初始化
            await self._initialize_framework()

            # 階段2: 核心服務初始化
            await self._initialize_core_services()

            # 階段3: 應用服務初始化
            await self._initialize_application_services()

            # 階段4: 系統健康檢查
            await self._perform_system_health_check()

            self.system_started = True
            self.system_healthy = True

            logger.info("system_initialization_completed",
                       component_count=len(self.services))
            return True

        except Exception as e:
            logger.error("system_initialization_failed", error=str(e))
            await self._shutdown_system()
            return False

    async def _initialize_framework(self):
        """初始化框架層"""
        logger.info("initializing_framework_components")

        # 統一框架初始化
        framework_components = [
            'error_handler',
            'performance_monitor',
            'audit_logger'
        ]

        for component in framework_components:
            try:
                success = await self.framework_initializer.initialize_component(component)
                if not success:
                    raise RuntimeError(f"Failed to initialize {component}")

                logger.info("framework_component_initialized",
                           component=component)

            except Exception as e:
                logger.error("framework_component_init_error",
                           component=component, error=str(e))
                raise

    async def _initialize_core_services(self):
        """初始化核心服務"""
        logger.info("initializing_core_services")

        # RBAC權限管理系統
        init_rbac_manager(self.config_manager)
        self.services['rbac_manager'] = get_rbac_manager()

        # 資料加密服務
        init_encryption_service(self.config_manager)
        self.services['encryption_service'] = get_encryption_service()

        # 系統監控服務
        init_system_monitor(self.config_manager)
        self.services['system_monitor'] = get_system_monitor()

        logger.info("core_services_initialized",
                   service_count=len(self.services))

    async def _initialize_application_services(self):
        """初始化應用服務"""
        logger.info("initializing_application_services")

        # Web爬蟲應用
        web_app = WebCrawlerApp()
        await web_app.initialize()
        self.services['web_app'] = web_app

        # 數據處理器
        data_processor = get_data_processor()
        await data_processor.initialize()
        self.services['data_processor'] = data_processor

        # 爬蟲引擎
        crawler_engine = get_crawler_engine()
        await crawler_engine.initialize()
        self.services['crawler_engine'] = crawler_engine

        logger.info("application_services_initialized")

    async def _perform_system_health_check(self):
        """執行系統健康檢查"""
        logger.info("performing_system_health_check")

        health_monitor = self.services.get('system_monitor')
        if health_monitor:
            # 檢查關鍵服務健康
            health_checks = [
                ("core_framework", self._check_framework_health),
                ("security_services", self._check_security_health),
                ("application_services", self._check_application_health)
            ]

            for component_name, check_func in health_checks:
                health_check = await health_monitor.perform_health_check(
                    component_name, check_func
                )

                if health_check.status in ['unhealthy', 'down']:
                    logger.warning("health_check_failed",
                                 component=component_name,
                                 status=health_check.status,
                                 score=health_check.score)

                logger.debug("health_check_completed",
                           component=component_name,
                           status=health_check.status,
                           score=health_check.score)

        logger.info("system_health_check_completed")

    async def _check_framework_health(self) -> Dict[str, Any]:
        """檢查框架健康"""
        framework_healthy = True
        components_status = {}

        for name, component in self.components.items():
            try:
                # 簡單的組件可用性檢查
                if callable(component):
                    instance = component(__name__ if name == 'logger' else None)
                else:
                    instance = component

                components_status[name] = "operational"
            except Exception as e:
                framework_healthy = False
                components_status[name] = f"error: {str(e)}"
                logger.warning("framework_component_health_issue",
                             component=name, error=str(e))

        return {
            "framework_healthy": framework_healthy,
            "components": components_status,
            "overall_score": 90 if framework_healthy else 30
        }

    async def _check_security_health(self) -> Dict[str, Any]:
        """檢查安全服務健康"""
        rbac_ok = False
        encryption_ok = False
        audit_ok = False

        # 檢查RBAC
        try:
            rbac_manager = self.services.get('rbac_manager')
            if rbac_manager:
                stats = rbac_manager.get_system_stats()
                rbac_ok = stats.get('total_users', 0) >= 0
        except Exception as e:
            logger.warning("rbac_health_check_error", error=str(e))

        # 檢查加密服務
        try:
            encryption_service = self.services.get('encryption_service')
            if encryption_service:
                stats = encryption_service.get_encryption_stats()
                encryption_ok = stats.get('active_keys', 0) > 0
        except Exception as e:
            logger.warning("encryption_health_check_error", error=str(e))

        # 檢查審計日誌
        try:
            audit_logger = get_audit_logger()
            audit_ok = audit_logger is not None
        except Exception as e:
            logger.warning("audit_health_check_error", error=str(e))

        security_score = (rbac_ok + encryption_ok + audit_ok) / 3 * 100

        return {
            "rbac_operational": rbac_ok,
            "encryption_operational": encryption_ok,
            "audit_operational": audit_ok,
            "overall_score": security_score
        }

    async def _check_application_health(self) -> Dict[str, Any]:
        """檢查應用服務健康"""
        app_services_ok = []
        issues = []

        for service_name in ['web_app', 'data_processor', 'crawler_engine']:
            service = self.services.get(service_name)
            if service:
                try:
                    # 檢查服務狀態
                    status = getattr(service, 'get_status', lambda: {'status': 'unknown'})()
                    if status.get('status') == 'running':
                        app_services_ok.append(service_name)
                    else:
                        issues.append(f"{service_name}: {status.get('status', 'unknown')}")
                except Exception as e:
                    issues.append(f"{service_name}: error - {str(e)}")
                    logger.warning("service_health_check_error",
                                 service=service_name, error=str(e))

        application_score = len(app_services_ok) / 3 * 100 if len(app_services_ok) > 0 else 0

        return {
            "services_operational": app_services_ok,
            "issues": issues,
            "overall_score": application_score
        }

    async def start_system_services(self) -> bool:
        """
        啟動系統服務

        Returns:
            啟動是否成功
        """
        try:
            logger.info("starting_system_services")

            # 啟動監控服務
            monitor = self.services.get('system_monitor')
            if monitor:
                monitor.start_monitoring()
                self.services['monitor_task'] = monitor

            # 啟動Web應用
            web_app = self.services.get('web_app')
            if web_app:
                await web_app.start()

            logger.info("system_services_started")
            return True

        except Exception as e:
            logger.error("system_services_start_failed", error=str(e))
            return False

    async def run_system(self) -> None:
        """運行系統主循環"""
        try:
            logger.info("system_running_main_loop",
                       startup_time=int(time.time()),
                       healthy=self.system_healthy)

            # 設置信號處理
            self._setup_signal_handlers()

            # 系統運行統計
            start_time = time.time()

            # 主循環
            while self.system_started:
                try:
                    await asyncio.sleep(30)  # 每30秒檢查一次

                    # 定期健康檢查
                    await self._perform_periodic_health_check()

                    # 記錄運行統計
                    uptime = int(time.time() - start_time)
                    if uptime % 300 == 0:  # 每5分鐘記錄一次
                        self._log_system_stats(uptime)

                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error("system_loop_error", error=str(e))

        except Exception as e:
            logger.error("system_run_error", error=str(e))
        finally:
            await self._shutdown_system()

    def _setup_signal_handlers(self):
        """設置信號處理器"""
        def signal_handler(signum, frame):
            logger.info("received_shutdown_signal", signal=signum)
            self.system_started = False

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    async def _perform_periodic_health_check(self):
        """執行定期健康檢查"""
        try:
            health_monitor = self.services.get('system_monitor')
            if health_monitor:
                overall_health = health_monitor.get_overall_health_score()

                # 如果系統健康分數過低，記錄警告
                if overall_health < 70:
                    logger.warning("low_system_health_score",
                                 score=overall_health,
                                 threshold=70)

        except Exception as e:
            logger.warning("periodic_health_check_error", error=str(e))

    def _log_system_stats(self, uptime: int):
        """記錄系統統計"""
        try:
            stats = {
                "uptime_seconds": uptime,
                "service_count": len(self.services),
                "system_healthy": self.system_healthy
            }

            if 'system_monitor' in self.services:
                monitor = self.services['system_monitor']
                monitor_stats = monitor.get_monitoring_stats()
                stats.update(monitor_stats)

            logger.info("system_stats", **stats)

        except Exception as e:
            logger.warning("stats_logging_error", error=str(e))

    async def _shutdown_system(self):
        """關閉系統"""
        logger.info("initiating_system_shutdown")

        # 按依賴順序關閉服務
        shutdown_order = [
            'web_app',
            'data_processor',
            'crawler_engine',
            'rbac_manager',
            'encryption_service',
            'system_monitor'
        ]

        for service_name in shutdown_order:
            try:
                service = self.services.get(service_name)
                if service and hasattr(service, 'shutdown'):
                    await service.shutdown()
                    logger.info("service_shutdown_completed",
                              service=service_name)

            except Exception as e:
                logger.error("service_shutdown_error",
                           service=service_name,
                           error=str(e))

        # 關閉框架組件
        try:
            await self.framework_initializer.shutdown_all_components()
            logger.info("framework_components_shutdown_completed")
        except Exception as e:
            logger.error("framework_shutdown_error", error=str(e))

        self.system_started = False
        self.system_healthy = False

        logger.info("system_shutdown_completed")


async def main():
    """主入口點"""
    print("🚀 WebCrawler Commander 啟動中...")
    print("=" * 50)

    # 創建系統整合管理器
    integration_manager = SystemIntegrationManager()

    try:
        # 初始化系統
        print("📋 初始化系統組件...")
        init_success = await integration_manager.initialize_system()

        if not init_success:
            print("❌ 系統初始化失敗")
            sys.exit(1)

        print("✅ 系統初始化完成")

        # 啟動服務
        print("⚡ 啟動系統服務...")
        start_success = await integration_manager.start_system_services()

        if not start_success:
            print("❌ 服務啟動失敗")
            sys.exit(1)

        print("✅ 服務啟動完成")
        print("🎯 系統運行就緒!")

        # 運行主循環
        await integration_manager.run_system()

    except KeyboardInterrupt:
        print("\n🛑 收到停止信號，正在關閉系統...")
    except Exception as e:
        print(f"❌ 系統運行錯誤: {str(e)}")
        logger.error("main_execution_error", error=str(e))
    finally:
        print("🔌 關閉系統...")
        await integration_manager._shutdown_system()
        print("👋 系統已停止")


def run_sync():
    """同步模式運行"""
    asyncio.run(main())


if __name__ == "__main__":
    run_sync()
