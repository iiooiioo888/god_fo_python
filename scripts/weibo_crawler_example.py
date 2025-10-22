#!/usr/bin/env python3
"""
微博USID爬蟲使用示例

此腳本演示如何使用微博USID爬蟲來收集女性用戶信息
"""

import asyncio
import sys
import os
from pathlib import Path

# 添加後端路徑到Python路徑
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# 初始化框架組件
from utils.config_manager import init_config_manager
from utils.logger_service import init_logger_service

# 初始化配置管理器
config_manager = init_config_manager(
    config_dir=str(backend_path / "config"),
    environment="development",
    enable_hot_reload=False
)

# 初始化日誌服務
logger_service = init_logger_service(config_manager)

from services.weibo_usid_crawler import (
    get_weibo_crawler,
    create_weibo_config,
    DataSource,
    WeibouserConfig
)


async def example_range_scan():
    """範圍掃描示例"""
    print("🕷️ 微博USID爬蟲 - 範圍掃描示例")
    print("=" * 50)

    # 創建配置
    config = create_weibo_config(
        data_source=DataSource.RANGE_SCAN,
        uid_range_start=1669879400,  # 示例UID範圍
        uid_range_end=1669879500,    # 小範圍測試
        max_concurrent=2,
        request_delay=1.5,
        csv_output_path="data/weibo_female_users_range.csv",
        cookie=""  # 請設置您的微博cookie
    )

    print(f"掃描範圍: {config.uid_range_start} - {config.uid_range_end}")
    print(f"並發數: {config.max_concurrent}")
    print(f"請求間隔: {config.request_delay}秒")
    print()

    # 運行爬蟲
    crawler = get_weibo_crawler()

    try:
        results = await crawler.crawl_female_users(config)

        print(f"✅ 爬取完成!")
        print(f"找到女性用戶: {len(results)}")

        if results:
            print("\n📊 前3個結果:")
            for i, user in enumerate(results[:3]):
                print(f"{i+1}. UID: {user.uid}, 用戶名: {user.username}, "
                      f"性別: {user.gender.value}, 相片數: {user.photos_count}")

        print(f"\n💾 結果已保存到: {config.csv_output_path}")

    except Exception as e:
        print(f"❌ 爬取失敗: {e}")

    finally:
        await crawler.close()


async def example_following_list():
    """關注列表示例"""
    print("🕷️ 微博USID爬蟲 - 關注列表示例")
    print("=" * 50)

    # 注意: 需要有效的微博登錄cookie
    cookie = ""  # 請設置您的微博cookie

    if not cookie:
        print("❌ 請先設置微博登錄cookie")
        print("獲取方法:")
        print("1. 登錄 https://weibo.cn")
        print("2. 使用瀏覽器開發者工具獲取cookie")
        print("3. 在配置中設置cookie字段")
        return

    # 創建配置
    config = create_weibo_config(
        data_source=DataSource.FOLLOWING_LIST,
        cookie=cookie,
        max_concurrent=3,
        request_delay=2.0,
        csv_output_path="data/weibo_female_users_following.csv"
    )

    print("數據源: 關注列表")
    print(f"並發數: {config.max_concurrent}")
    print(f"請求間隔: {config.request_delay}秒")
    print()

    # 運行爬蟲
    crawler = get_weibo_crawler()

    try:
        results = await crawler.crawl_female_users(config)

        print(f"✅ 爬取完成!")
        print(f"關注的女性用戶: {len(results)}")

        if results:
            print("\n📊 結果樣本:")
            for i, user in enumerate(results[:5]):
                print(f"{i+1}. UID: {user.uid}, 用戶名: {user.username}")

        print(f"\n💾 結果已保存到: {config.csv_output_path}")

    except Exception as e:
        print(f"❌ 爬取失敗: {e}")

    finally:
        await crawler.close()


async def interactive_example():
    """交互式示例"""
    print("🕷️ 微博USID爬蟲 - 交互式配置")
    print("=" * 50)

    # 選擇數據源
    print("選擇數據源:")
    print("1. 範圍掃描 (掃描指定UID範圍)")
    print("2. 關注列表 (使用當前用戶的關注列表)")
    choice = input("請選擇 (1或2): ").strip()

    data_source = None
    config_kwargs = {}

    if choice == "1":
        data_source = DataSource.RANGE_SCAN

        start = input("輸入起始UID (默認: 1000000000): ").strip()
        end = input("輸入結束UID (默認: 1000010000): ").strip()

        config_kwargs.update({
            "uid_range_start": int(start) if start else 1000000000,
            "uid_range_end": int(end) if end else 1000010000
        })

    elif choice == "2":
        data_source = DataSource.FOLLOWING_LIST

        cookie = input("輸入微博cookie (必填): ").strip()
        if not cookie:
            print("❌ Cookie為必填項")
            return

        config_kwargs["cookie"] = cookie
    else:
        print("❌ 無效選擇")
        return

    # 共用參數
    concurrent = input("最大並發數 (默認: 3): ").strip()
    delay = input("請求間隔(秒) (默認: 2.0): ").strip()
    output = input("輸出CSV路徑 (默認: data/weibo_female_users.csv): ").strip()

    config_kwargs.update({
        "max_concurrent": int(concurrent) if concurrent else 3,
        "request_delay": float(delay) if delay else 2.0,
        "csv_output_path": output if output else "data/weibo_female_users.csv"
    })

    # 創建配置
    config = create_weibo_config(data_source, **config_kwargs)

    print("\n🔧 配置總結:")
    print(f"數據源: {data_source.value}")
    if data_source == DataSource.RANGE_SCAN:
        print(f"UID範圍: {config.uid_range_start} - {config.uid_range_end}")
    print(f"並發數: {config.max_concurrent}")
    print(f"請求間隔: {config.request_delay}秒")
    print(f"輸出路徑: {config.csv_output_path}")
    print()

    confirm = input("開始爬取? (y/N): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return

    # 運行爬蟲
    crawler = get_weibo_crawler()

    try:
        results = await crawler.crawl_female_users(config)

        print(f"\n✅ 爬取完成!")
        print(f"找到女性用戶: {len(results)}")

        if results:
            print("\n📊 結果樣本:")
            for i, user in enumerate(results[:10]):
                print(f"{i+1}. {user.uid} - {user.username} - {user.gender.value}")

        print(f"\n💾 結果已保存到: {config.csv_output_path}")

    except Exception as e:
        print(f"\n❌ 爬取失敗: {e}")

    finally:
        await crawler.close()


def main():
    """主函數"""
    print("微博USID爬蟲示例")
    print("=" * 30)

    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "range":
            asyncio.run(example_range_scan())
        elif mode == "following":
            asyncio.run(example_following_list())
        else:
            print(f"未知模式: {mode}")
            print("使用方法: python weibo_crawler_example.py [range|following|interactive]")
    else:
        print("\n選擇運行模式:")
        print("1. 範圍掃描示例 (python weibo_crawler_example.py range)")
        print("2. 關注列表示例 (python weibo_crawler_example.py following)")
        print("3. 交互式配置 (運行此腳本不加參數)")
        print()
        asyncio.run(interactive_example())


if __name__ == "__main__":
    # 確保數據目錄存在
    Path("data").mkdir(exist_ok=True)

    main()
