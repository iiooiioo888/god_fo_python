"""
WebCrawler Commander - 微博USID爬蟲服務
專門用於爬取weibo.cn用戶信息，只收錄女性用戶

核心功能：
- 支持10位數字UID範圍掃描
- 支持使用登錄cookie獲取關注列表
- 從多個頁面提取用戶信息：info頁面、相冊、發佈記錄
- 性別識別和篩選
- CSV格式輸出

作者: Cline (基於Jerry開發工作室框架)
版本: v1.0.0
"""

import asyncio
import csv
import json
import random
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

import httpx
from bs4 import BeautifulSoup

import sys
from pathlib import Path

# 確保backend在路徑中
backend_path = Path(__file__).parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from utils.config_manager import get_config_manager
from utils.logger_service import get_logger
from services.crawler_engine import IntelligentCrawler, CrawlConfig, AuthType
from services.content_parser import get_content_parser, ContentRule


class Gender(Enum):
    """性別枚舉"""
    FEMALE = "女"
    MALE = "男"
    UNKNOWN = "未知"


class DataSource(Enum):
    """數據來源類型"""
    RANGE_SCAN = "range_scan"  # 範圍掃描
    FOLLOWING_LIST = "following_list"  # 關注列表


@dataclass
class WeibouserInfo:
    """微博用戶信息"""
    uid: str
    username: Optional[str] = None
    gender: Gender = Gender.UNKNOWN
    last_post_time: Optional[datetime] = None
    photos_count: int = 0
    is_valid: bool = False
    error_message: Optional[str] = None
    crawled_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class WeibouserConfig:
    """微博爬蟲配置"""
    data_source: DataSource
    cookie: str = ""  # 微博登錄cookie
    uid_range_start: Optional[int] = None
    uid_range_end: Optional[int] = None
    max_concurrent: int = 5
    request_delay: float = 1.0  # 請求間隔(秒)
    csv_output_path: str = "weibo_female_users.csv"
    retry_attempts: int = 3
    timeout: float = 15.0


class WeibolusIDCrawler:
    """
    微博USID爬蟲主類

    實現微博用戶信息爬取，專注於識別和收集女性用戶信息
    """

    def __init__(self, config_manager=None):
        self.config_manager = config_manager or get_config_manager()
        self.logger = get_logger(__name__)

        # 初始化組件
        self.crawler = IntelligentCrawler()
        self.content_parser = get_content_parser()

        # 數據存儲
        self.results: List[WeibouserInfo] = []
        self.stats = {
            "total_processed": 0,
            "female_users": 0,
            "errors": 0,
            "start_time": None
        }

        # 自定義提取規則
        self._setup_extraction_rules()

        self.logger.info("weibo_usid_crawler_initialized")

    def _setup_extraction_rules(self):
        """設置內容提取規則"""
        # 用戶信息頁面規則
        self.user_info_rules = [
            ContentRule(
                name="username",
                selector=".u, .username, .name",
                content_type="text",
                required=True
            ),
            ContentRule(
                name="gender",
                selector=".info td:contains('性別'), .profile td:contains('性別')",
                content_type="text"
            )
        ]

        # 主頁面規則 (獲取最近發佈時間)
        self.homepage_rules = [
            ContentRule(
                name="last_post",
                selector=".ct",
                content_type="text"
            )
        ]

        # 相冊頁面規則
        self.album_rules = [
            ContentRule(
                name="photo_links",
                selector="a[href*='photo']",
                attribute="href",
                content_type="array"
            )
        ]

    async def crawl_female_users(self, config: WeibouserConfig) -> List[WeibouserInfo]:
        """
        爬取女性用戶信息

        Args:
            config: 爬蟲配置

        Returns:
            女性用戶信息列表
        """
        self.stats["start_time"] = datetime.utcnow()
        self.logger.info("starting_female_users_crawl",
                        data_source=config.data_source.value,
                        concurrent=config.max_concurrent)

        try:
            # 獲取UID列表
            uid_list = await self._get_uid_list(config)

            if not uid_list:
                self.logger.warning("no_uids_to_process")
                return []

            # 批量處理UID
            semaphore = asyncio.Semaphore(config.max_concurrent)

            tasks = []
            for uid in uid_list:
                task = asyncio.create_task(
                    self._process_single_user(uid, config, semaphore)
                )
                tasks.append(task)

            # 等待所有任務完成
            await asyncio.gather(*tasks, return_exceptions=True)

            # 保存結果到CSV
            await self._save_to_csv(config.csv_output_path)

            # 統計信息
            duration = datetime.utcnow() - self.stats["start_time"]
            self.logger.info("crawl_completed",
                            total_processed=self.stats["total_processed"],
                            female_users=self.stats["female_users"],
                            errors=self.stats["errors"],
                            duration_seconds=duration.total_seconds())

            return [r for r in self.results if r.is_valid and r.gender == Gender.FEMALE]

        except Exception as e:
            self.logger.error("crawl_failed", error=str(e))
            raise

    async def _get_uid_list(self, config: WeibouserConfig) -> List[str]:
        """獲取要處理的UID列表"""
        if config.data_source == DataSource.RANGE_SCAN:
            return self._generate_uid_range(config.uid_range_start,
                                          config.uid_range_end)
        elif config.data_source == DataSource.FOLLOWING_LIST:
            return await self._get_following_uids(config.cookie)
        else:
            raise ValueError(f"不支持的數據源類型: {config.data_source}")

    def _generate_uid_range(self, start: Optional[int], end: Optional[int]) -> List[str]:
        """生成UID範圍"""
        if start is None:
            start = 1000000000  # 默認10位數起始
        if end is None:
            end = 9999999999    # 默認10位數結束

        # 限制範圍大小，避免過大
        max_range = 100000
        if end - start > max_range:
            self.logger.warning("uid_range_too_large", range_size=end-start, max_allowed=max_range)
            end = start + max_range

        return [str(uid) for uid in range(start, end + 1)]

    async def _get_following_uids(self, cookie: str) -> List[str]:
        """獲取關注用戶的UID列表"""
        uids = []

        try:
            # 訪問關注頁面
            following_url = "https://weibo.cn/attention"

            crawl_config = CrawlConfig(
                url=following_url,
                method="GET",
                timeout=30.0,
                custom_cookies=self._parse_cookie_string(cookie),
                follow_redirects=True
            )

            result = await self.crawler.crawl(crawl_config)

            if not result.success:
                self.logger.error("failed_to_get_following_list", status=result.status_code)
                return []

            # 解析關注列表
            soup = BeautifulSoup(result.text, 'lxml')

            # 查找用戶鏈接
            user_links = soup.find_all('a', href=re.compile(r'/u/\d+'))

            for link in user_links:
                href = link.get('href')
                match = re.search(r'/u/(\d+)', href)
                if match:
                    uids.append(match.group(1))

            # 去重
            uids = list(set(uids))

            self.logger.info("following_uids_extracted", count=len(uids))

        except Exception as e:
            self.logger.error("get_following_uids_error", error=str(e))

        return uids

    def _parse_cookie_string(self, cookie_str: str) -> Dict[str, str]:
        """解析cookie字符串"""
        cookies = {}

        if not cookie_str:
            return cookies

        # 分割cookie字符串
        cookie_pairs = cookie_str.split(';')

        for pair in cookie_pairs:
            pair = pair.strip()
            if '=' in pair:
                key, value = pair.split('=', 1)
                cookies[key.strip()] = value.strip()

        return cookies

    async def _process_single_user(self, uid: str, config: WeibouserConfig,
                                 semaphore: asyncio.Semaphore) -> None:
        """處理單個用戶"""
        async with semaphore:
            try:
                self.stats["total_processed"] += 1

                # 添加請求間隔
                if config.request_delay > 0:
                    await asyncio.sleep(config.request_delay)

                user_info = WeibouserInfo(uid=uid)

                # 獲取用戶基本信息
                success = await self._get_user_basic_info(uid, user_info, config)
                if not success:
                    self.stats["errors"] += 1
                    return

                # 檢查性別
                if user_info.gender != Gender.FEMALE:
                    return  # 只處理女性用戶

                # 獲取附加信息
                await self._get_user_additional_info(uid, user_info, config)

                # 標記為有效
                user_info.is_valid = True
                self.results.append(user_info)
                self.stats["female_users"] += 1

                self.logger.debug("female_user_found",
                                uid=uid,
                                username=user_info.username)

            except Exception as e:
                self.stats["errors"] += 1
                self.logger.error("process_user_error", uid=uid, error=str(e))

                # 記錄錯誤信息
                error_info = WeibouserInfo(
                    uid=uid,
                    is_valid=False,
                    error_message=str(e)
                )
                self.results.append(error_info)

    async def _get_user_basic_info(self, uid: str, user_info: WeibouserInfo,
                                 config: WeibouserConfig) -> bool:
        """獲取用戶基本信息 (info頁面)"""
        try:
            info_url = f"https://weibo.cn/{uid}/info"

            crawl_config = CrawlConfig(
                url=info_url,
                method="GET",
                timeout=config.timeout,
                max_retries=config.retry_attempts,
                custom_cookies=self._parse_cookie_string(config.cookie),
                follow_redirects=True
            )

            result = await self.crawler.crawl(crawl_config)

            if not result.success or result.status_code != 200:
                self.logger.debug("info_page_failed", uid=uid, status=result.status_code)
                return False

            # 解析用戶信息
            soup = BeautifulSoup(result.text, 'lxml')

            # 提取用戶名
            username_elem = soup.select_one('.u, .username, .name')
            if username_elem:
                user_info.username = username_elem.get_text().strip()

            # 判斷性別
            user_info.gender = self._extract_gender_from_html(result.text)

            # 檢查是否有有效的數據
            if user_info.username and user_info.gender != Gender.UNKNOWN:
                return True
            else:
                self.logger.debug("insufficient_user_data", uid=uid)
                return False

        except Exception as e:
            self.logger.warning("get_basic_info_error", uid=uid, error=str(e))
            return False

    def _extract_gender_from_html(self, html_content: str) -> Gender:
        """從HTML內容中提取性別信息"""
        soup = BeautifulSoup(html_content, 'lxml')

        # 查找包含性別的行
        info_rows = soup.find_all(['tr', 'div'], class_=re.compile('info|profile'))

        for row in info_rows:
            text = row.get_text().strip()

            # 查找性別相關文字
            if '性別' in text:
                if '女' in text:
                    return Gender.FEMALE
                elif '男' in text:
                    return Gender.MALE

        # 嘗試其他方式
        full_text = soup.get_text()
        if '女' in full_text and '性別' in full_text:
            return Gender.FEMALE
        elif '男' in full_text and '性別' in full_text:
            return Gender.MALE

        return Gender.UNKNOWN

    async def _get_user_additional_info(self, uid: str, user_info: WeibouserInfo,
                                      config: WeibouserConfig) -> None:
        """獲取用戶附加信息 (最近發佈時間和相冊)"""
        try:
            # 獲取最近發佈時間
            await self._get_last_post_time(uid, user_info, config)

            # 獲取相冊相片數量
            await self._get_photos_count(uid, user_info, config)

        except Exception as e:
            self.logger.warning("get_additional_info_error", uid=uid, error=str(e))

    async def _get_last_post_time(self, uid: str, user_info: WeibouserInfo,
                                config: WeibouserConfig) -> None:
        """獲取用戶最近發佈時間"""
        try:
            home_url = f"https://weibo.cn/{uid}"

            crawl_config = CrawlConfig(
                url=home_url,
                method="GET",
                timeout=config.timeout,
                max_retries=config.retry_attempts,
                custom_cookies=self._parse_cookie_string(config.cookie),
                follow_redirects=True
            )

            result = await self.crawler.crawl(crawl_config)

            if not result.success:
                return

            # 查找時間信息
            soup = BeautifulSoup(result.text, 'lxml')

            # 查找發佈時間標籤
            time_elements = soup.select('.ct')

            for time_elem in time_elements:
                time_text = time_elem.get_text().strip()

                # 解析時間 - 微博通常顯示為 "2023-01-01 12:00:00" 或相對時間
                parsed_time = self._parse_weibo_time(time_text)
                if parsed_time:
                    user_info.last_post_time = parsed_time
                    break

        except Exception as e:
            self.logger.debug("get_last_post_time_error", uid=uid, error=str(e))

    def _parse_weibo_time(self, time_text: str) -> Optional[datetime]:
        """解析微博時間格式"""
        try:
            # 處理相對時間
            now = datetime.utcnow()

            if '分鐘前' in time_text:
                minutes = int(re.search(r'(\d+)分鐘前', time_text).group(1))
                return now - timedelta(minutes=minutes)
            elif '小時前' in time_text:
                hours = int(re.search(r'(\d+)小時前', time_text).group(1))
                return now - timedelta(hours=hours)
            elif '今天' in time_text:
                # 提取時間部分
                time_match = re.search(r'(\d{1,2}):(\d{1,2})', time_text)
                if time_match:
                    hour, minute = map(int, time_match.groups())
                    return now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            else:
                # 嘗試解析絕對時間
                # 微博格式通常為: 01月01日 12:00
                time_match = re.search(r'(\d{1,2})月(\d{1,2})日\s+(\d{1,2}):(\d{1,2})', time_text)
                if time_match:
                    month, day, hour, minute = map(int, time_match.groups())
                    return now.replace(month=month, day=day, hour=hour, minute=minute, second=0, microsecond=0)

            return None

        except Exception:
            return None

    async def _get_photos_count(self, uid: str, user_info: WeibouserInfo,
                              config: WeibouserConfig) -> None:
        """獲取用戶相冊相片數量"""
        try:
            album_url = f"https://weibo.cn/{uid}/album"

            crawl_config = CrawlConfig(
                url=album_url,
                method="GET",
                timeout=config.timeout,
                max_retries=config.retry_attempts,
                custom_cookies=self._parse_cookie_string(config.cookie),
                follow_redirects=True
            )

            result = await self.crawler.crawl(crawl_config)

            if not result.success:
                return

            soup = BeautifulSoup(result.text, 'lxml')

            # 查找相片鏈接
            photo_links = soup.select("a[href*='photo'], a[href*='album']")

            # 統計相片數量
            user_info.photos_count = len(photo_links)

        except Exception as e:
            self.logger.debug("get_photos_count_error", uid=uid, error=str(e))

    async def _save_to_csv(self, filepath: str) -> None:
        """保存結果到CSV文件"""
        try:
            # 確保輸出目錄存在
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)

            # 過濾出有效的女性用戶數據
            valid_female_users = [
                r for r in self.results
                if r.is_valid and r.gender == Gender.FEMALE
            ]

            if not valid_female_users:
                self.logger.warning("no_female_users_to_save")
                return

            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['uid', 'username', 'gender', 'last_post_time', 'photos_count', 'crawled_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # 寫入標題行
                writer.writeheader()

                # 寫入數據行
                for user in valid_female_users:
                    writer.writerow({
                        'uid': user.uid,
                        'username': user.username or '',
                        'gender': user.gender.value,
                        'last_post_time': user.last_post_time.isoformat() if user.last_post_time else '',
                        'photos_count': user.photos_count,
                        'crawled_at': user.crawled_at.isoformat()
                    })

            self.logger.info("csv_saved",
                            filepath=filepath,
                            female_users_count=len(valid_female_users))

        except Exception as e:
            self.logger.error("save_csv_error", error=str(e))
            raise

    async def close(self) -> None:
        """關閉爬蟲資源"""
        await self.crawler.close()
        self.logger.info("weibo_crawler_closed")


# 全域微博USID爬蟲實例
_weibo_crawler: Optional[WeibolusIDCrawler] = None


def get_weibo_crawler() -> WeibolusIDCrawler:
    """獲取微博USID爬蟲實例"""
    global _weibo_crawler

    if _weibo_crawler is None:
        _weibo_crawler = WeibolusIDCrawler()

    return _weibo_crawler


def create_weibo_config(data_source: DataSource, **kwargs) -> WeibouserConfig:
    """創建微博爬蟲配置"""
    config = WeibouserConfig(data_source=data_source)

    # 設置可選參數
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)

    return config
