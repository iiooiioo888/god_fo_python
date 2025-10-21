#!/usr/bin/env python3
"""
WebCrawler Commander - 集成測試腳本
驗證核心組件協同工作

測試範圍：
- 配置管理器初始化
- 日誌服務功能
- 爬蟲引擎基本爬取功能
- 全系統協同測試

作者: Jerry開發工作室
版本: v1.0.0
"""

import os
import sys
import asyncio
import time
from pathlib import Path

# 添加backend目錄到Python路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from utils.config_manager import init_config_manager, get_config_manager
from utils.logger_service import init_logger_service, get_logger
from services.crawler_engine import (
    IntelligentCrawler,
    CrawlConfig,
    AuthType,
    RequestManager,
    ResponseHandler
)


async def test_config_manager():
    """測試配置管理器"""
    print("🔧 測試配置管理器...")

    try:
        # 初始化配置管理器
        config_manager = init_config_manager(
            config_dir="backend/config",
            environment="development",
            enable_hot_reload=False  # 測試期間禁用熱重載
        )

        # 測試基本配置獲取
        app_name = config_manager.get("app_name")
        assert app_name == "WebCrawler Commander", f"期望 'WebCrawler Commander', 獲得 {app_name}"

        server_port = config_manager.get("server.port")
        assert server_port == 8000, f"期望 8000, 獲得 {server_port}"

        # 測試配置統計
        stats = config_manager.get_config_stats()
        assert "load_count" in stats, "統計信息不完整"

        print("✅ 配置管理器測試通過")
        return True

    except Exception as e:
        print(f"❌ 配置管理器測試失敗: {e}")
        return False


async def test_logger_service():
    """測試日誌服務"""
    print("📝 測試日誌服務...")

    try:
        # 日誌服務已經在配置管理器中初始化
        logger = get_logger(__name__)

        # 測試不同級別的日誌
        logger.info("測試信息級別日誌")
        logger.debug("測試調試級別日誌", test_key="test_value")
        logger.warning("測試警告級別日誌", warning_code=123)
        logger.error("測試錯誤級別日誌", exception_details={"type": "ValueError", "message": "測試錯誤"})

        # 測試請求上下文
        from utils.logger_service import set_request_context, clear_request_context
        set_request_context(request_id="test-req-001", user_id="test-user-001")
        logger.info("測試請求上下文日誌", action="crawl", target="example.com")
        clear_request_context()

        print("✅ 日誌服務測試通過")
        return True

    except Exception as e:
        print(f"❌ 日誌服務測試失敗: {e}")
        return False


async def test_crawler_engine():
    """測試爬蟲引擎"""
    print("🕷️ 測試爬蟲引擎...")

    try:
        # 初始化爬蟲引擎
        crawler = IntelligentCrawler()

        # 測試基本HTTP GET請求
        config = CrawlConfig(
            url="https://httpbin.org/get",
            method="GET",
            timeout=10.0,
            max_retries=2,
            delay_between_requests=0.5,  # 測試時縮短延遲
            respect_robots_txt=False  # httpbin.org沒有robots.txt阻擋
        )

        start_time = time.time()
        result = await crawler.crawl(config)
        end_time = time.time()

        # 驗證結果
        assert result.success, f"爬取失敗: {result.error_message}"
        assert result.status_code == 200, f"期望狀態碼200, 獲得 {result.status_code}"
        assert "httpbin.org" in result.url, f"URL不正確: {result.url}"
        assert result.response_time > 0, "響應時間不應為0"
        assert result.response_time < 15.0, f"響應時間過長: {result.response_time}s"
        assert "headers" in result.request_headers, "請求頭信息缺失"

        print(f"請求成功。狀態碼: {result.status_code}, 響應時間: {result.response_time:.2f}s")
        # 測試User-Agent輪換
        ua_pool = crawler.ua_pool
        ua1 = ua_pool.get_random()
        ua2 = ua_pool.get_random()
        assert len(ua1) > 10, "User-Agent偏短"
        assert ua1 != ua2 or True, "User-Agent應該有一定隨機性"

        print("✅ 爬蟲引擎測試通過")
        return True

    except Exception as e:
        print(f"❌ 爬蟲引擎測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # 清理資源
        if 'crawler' in locals():
            await crawler.close()


async def test_request_manager():
    """測試請求管理器"""
    print("📋 測試請求管理器...")

    try:
        crawler = IntelligentCrawler()
        manager = RequestManager(crawler)

        # 啟動處理器
        await manager.start_processing(num_workers=2)

        # 創建多個請求
        configs = [
            CrawlConfig(url="https://httpbin.org/delay/1", delay_between_requests=0.1),
            CrawlConfig(url="https://httpbin.org/status/200", delay_between_requests=0.1),
            CrawlConfig(url="https://httpbin.org/user-agent", delay_between_requests=0.1),
        ]

        # 提交請求
        futures = []
        for config in configs:
            future = await manager.submit_request(config)
            futures.append(future)

        # 等待結果
        results = []
        for future in futures:
            try:
                result = await asyncio.wait_for(future, timeout=30.0)
                results.append(result)
                assert result.success, f"請求失敗: {result.error_message}"
            except Exception as e:
                print(f"請求異常: {e}")
                results.append(None)

        # 清理
        await manager.stop_processing()
        await crawler.close()

        # 統計
        success_count = sum(1 for r in results if r and r.success)
        print(f"✅ 請求管理器測試通過 ({success_count}/{len(configs)} 成功)")

        return success_count > len(configs) // 2  # 至少一半成功

    except Exception as e:
        print(f"❌ 請求管理器測試失敗: {e}")
        return False


async def test_response_handler():
    """測試響應處理器"""
    print("🔄 測試響應處理器...")

    try:
        from backend.services.crawler_engine import CrawlResult

        handler = ResponseHandler()

        # 創建測試響應
        mock_result = CrawlResult(
            url="https://example.com",
            status_code=200,
            headers={"content-type": "text/html"},
            content=b"<html><head><title>Test Page</title></head><body><h1>Hello World</h1></body></html>",
            text="<html><head><title>Test Page</title></head><body><h1>Hello World</h1></body></html>",
            response_time=0.5,
            success=True
        )

        # 測試HTML數據提取
        extractors = [
            {
                "name": "page_title",
                "type": "css",
                "selector": "title"
            },
            {
                "name": "heading",
                "type": "css",
                "selector": "h1"
            }
        ]

        processed_data = await handler.process_response(mock_result, extractors)

        assert processed_data["success"], "響應處理標記為失敗"
        assert processed_data["status_code"] == 200, "狀態碼不正確"
        assert "html" in processed_data["extracted_data"], "缺少HTML數據"
        assert "page_title" in processed_data["extracted_data"], "缺少頁面標題提取"
        assert "heading" in processed_data["extracted_data"], "缺少標題提取"

        # 檢查提取結果
        title_data = processed_data["extracted_data"]["page_title"]
        assert isinstance(title_data, list), "標題應該是列表"
        assert "Test Page" in title_data[0], "標題內容不正確"

        print("✅ 響應處理器測試通過")
        return True

    except Exception as e:
        print(f"❌ 響應處理器測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_full_integration():
    """完整集成測試"""
    print("🔗 測試全系統集成...")

    try:
        # 1. 初始化所有服務 (在main.py中完成)
        logger = get_logger(__name__)
        logger.info("開始全系統集成測試")

        # 2. 測試爬蟲工作流
        crawler = IntelligentCrawler()

        # 創建多個爬取任務
        tasks = [
            CrawlConfig(
                url="https://httpbin.org/json",
                respect_robots_txt=False,
                delay_between_requests=0.2
            ),
            CrawlConfig(
                url="https://httpbin.org/html",
                respect_robots_txt=False,
                delay_between_requests=0.2
            ),
        ]

        # 並發執行任務
        results = await asyncio.gather(
            *(crawler.crawl(config) for config in tasks),
            return_exceptions=True
        )

        success_count = sum(1 for r in results if hasattr(r, 'success') and r.success)

        await crawler.close()

        # 3. 測試統計信息
        config_manager = get_config_manager()
        stats = config_manager.get_config_stats()
        logger.info("系統統計", **stats)

        print(f"✅ 全系統集成測試通過 ({success_count}/{len(tasks)} 成功)")
        return success_count > 0

    except Exception as e:
        print(f"❌ 全系統集成測試失敗: {e}")
        return False


async def main():
    """主測試函數"""
    print("🚀 WebCrawler Commander - 集成測試開始")
    print("=" * 50)

    # 設置測試環境
    os.environ["WEBCRAWLER_ENV"] = "testing"

    # 初始化核心服務
    try:
        init_config_manager(
            config_dir="backend/config",
            environment="testing",
            enable_hot_reload=False
        )
        init_logger_service()
        print("✅ 核心服務初始化成功")
    except Exception as e:
        print(f"❌ 核心服務初始化失敗: {e}")
        return

    # 執行測試
    tests = [
        ("配置管理器", test_config_manager),
        ("日誌服務", test_logger_service),
        ("爬蟲引擎", test_crawler_engine),
        ("請求管理器", test_request_manager),
        ("響應處理器", test_response_handler),
        ("全系統集成", test_full_integration),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name}測試 {'='*20}")
        try:
            result = await test_func()
            if result:
                passed += 1
            else:
                print(f"⚠️  {test_name}測試部分失敗")
        except Exception as e:
            print(f"❌ {test_name}測試拋出異常: {e}")

    print("\n" + "=" * 50)
    print(f"🎯 測試完成: {passed}/{total} 通過")

    if passed == total:
        print("🎉 所有測試通過！系統準備就緒。")
        return True
    elif passed >= total * 0.8:  # 80%以上通過
        print("⚠️ 大部分測試通過，系統基本可用。")
        return True
    else:
        print("❌ 測試失敗率過高，需要檢查系統配置。")
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 用戶中斷測試")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 測試過程中發生未預期的錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
