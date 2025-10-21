#!/usr/bin/env python3
"""
WebCrawler Commander - 主入口文件

企業級爬蟲管理系統的後端服務啟動腳本

功能：
- 初始化配置管理器
- 初始化日誌服務
- 啟動REST API服務器
- 提供系統健康檢查

作者: Jerry開發工作室
版本: v1.0.0
"""

import os
import sys
import signal
import asyncio
from contextlib import asynccontextmanager
from typing import Optional

# 添加backend目錄到Python路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.config_manager import init_config_manager, get_config_manager
from utils.logger_service import init_logger_service, get_logger

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


# 全域變數
app: Optional[FastAPI] = None
shutdown_event = asyncio.Event()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """應用生命週期管理"""
    logger = get_logger(__name__)

    # 啟動階段
    logger.info("application_startup_begin")

    # 在此處可以添加數據庫連接、快取初始化等

    logger.info("application_startup_complete")

    yield

    # 關閉階段
    logger.info("application_shutdown_begin")

    # 在此處可以添加清理資源的邏輯

    shutdown_event.set()
    logger.info("application_shutdown_complete")


def create_application() -> FastAPI:
    """創建FastAPI應用"""
    global app

    # 獲取配置
    config = get_config_manager()
    logger = get_logger(__name__)

    # 創建FastAPI應用
    app = FastAPI(
        title=config.get("app_name", "WebCrawler Commander"),
        description="企業級爬蟲管理與數據分析系統",
        version=config.get("version", "1.0.0"),
        lifespan=lifespan
    )

    # 配置CORS
    cors_origins = config.get("security.cors_origins", ["http://localhost:3000"])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 根路由
    @app.get("/")
    async def root():
        """根路由"""
        return {
            "service": config.get("app_name"),
            "version": config.get("version"),
            "status": "running",
            "environment": config.get("environment")
        }

    # 健康檢查路由
    @app.get("/health")
    async def health_check():
        """健康檢查端點"""
        return {
            "status": "healthy",
            "timestamp": "2024-01-20T10:00:00Z",
            "version": config.get("version"),
            "checks": {
                "config": "ok",
                "logging": "ok",
                "database": "degraded",  # 尚未實現
                "redis": "degraded"     # 尚未實現
            }
        }

    # 詳細的就緒檢查
    @app.get("/ready")
    async def readiness_check():
        """就緒檢查"""
        # 在此處可以添加依賴服務的檢查
        # 比如數據庫連接、外部服務可達性等
        return {"status": "ready"}

    # 系統狀態路由
    @app.get("/status")
    async def system_status():
        """系統狀態詳情"""
        config_mgr = get_config_manager()

        return {
            "service": config.get("app_name"),
            "version": config.get("version"),
            "environment": config.get("environment"),
            "config": config_mgr.get_config_stats(),
            "logging": {
                "initialized": True,
                "error_count": 0
            },
            "uptime": "0 days, 0 hours, 0 minutes"
        }

    # 全域異常處理
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """全域異常處理器"""
        logger = get_logger(__name__)

        # 根據異常類型決定狀態碼和響應
        if isinstance(exc, HTTPException):
            status_code = exc.status_code
            detail = exc.detail
        else:
            status_code = 500
            detail = "Internal server error"
            logger.error("unhandled_exception",
                        exception_type=type(exc).__name__,
                        exception_message=str(exc),
                        url=str(request.url),
                        method=request.method)

        return JSONResponse(
            status_code=status_code,
            content={
                "error": {
                    "type": type(exc).__name__,
                    "message": detail,
                    "timestamp": "2024-01-20T10:00:00Z"
                }
            }
        )

    # 在此處添加API路由器
    # 例如：
    # app.include_router(crawler_router, prefix="/api/crawlers", tags=["crawlers"])
    # app.include_router(data_router, prefix="/api/data", tags=["data"])

    logger.info("fastapi_application_created", routes_count=len(app.routes))

    return app


def init_services():
    """初始化所有服務"""
    # 1. 初始化配置管理器
    config_manager = init_config_manager(
        config_dir=os.path.join(os.path.dirname(__file__), "config"),
        environment=os.getenv("WEBCRAWLER_ENV"),
        enable_hot_reload=True  # 開發環境啟用熱重載
    )

    # 2. 初始化日誌服務 (依賴配置管理器)
    logger_service = init_logger_service(config_manager)

    # 3. 設置全域logger
    logger = get_logger(__name__)
    logger.info("services_initialized")


def signal_handler(signum, frame):
    """信號處理器"""
    logger = get_logger(__name__)
    logger.info("shutdown_signal_received", signal=signum)

    if not shutdown_event.is_set():
        shutdown_event.set()


def main():
    """主入口函數"""
    try:
        # 初始化所有服務
        init_services()

        # 獲取配置
        config = get_config_manager()
        logger = get_logger(__name__)

        # 創建FastAPI應用
        app = create_application()

        # 設置信號處理
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # 啟動服務器
        server_config = config.get("server", {})
        host = server_config.get("host", "0.0.0.0")
        port = server_config.get("port", 8000)
        workers = server_config.get("workers", 1)

        logger.info("starting_server", host=host, port=port, workers=workers)

        # 使用uvicorn啟動服務器
        uvicorn.run(
            "main:create_application",
            factory=True,
            host=host,
            port=port,
            workers=workers,
            reload=config.get("environment") == "development",
            log_level=config.get("logging.level", "info").lower(),
            access_log=True
        )

    except KeyboardInterrupt:
        logger = get_logger(__name__)
        logger.info("server_shutdown_keyboard_interrupt")
    except Exception as e:
        print(f"服務啟動失敗: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
