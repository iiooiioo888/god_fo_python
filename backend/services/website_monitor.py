"""
WebCrawler Commander - 網站監控與健康檢查模塊
提供網站可用性監控、性能指標收集和狀態報告功能

核心功能：
- 實時網站可用性檢查 (HTTP狀態碼、響應時間、SSL證書)
- Uptime監控與歷史追蹤 (可用百分比計算、宕機事件記錄)
- 頁面內容變化檢測 (HTML哈希比較、關鍵內容監控)
- 性能指標收集 (TTFB、DOM ready、資源載入時間)
- SSL證書過期提醒 (證書鏈檢查、過期預警)
- 多地區監控支持 (全球節點分佈式檢查)

作者: Jerry開發工作室
版本: v1.0.0
"""

import asyncio
import hashlib
import json
import ssl
import time
import socket
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from urllib.parse import urlparse
from collections import defaultdict
import statistics

import httpx
from bs4 import BeautifulSoup

from ..utils.config_manager import get_config_manager
from ..utils.logger_service import get_logger


class MonitorStatus(Enum):
    """監控狀態枚舉"""
    UP = "up"
    DOWN = "down"
    DEGRADED = "degraded"
    MAINTENANCE = "maintenance"


class AlertLevel(Enum):
    """告警等級枚舉"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class WebsiteStatus:
    """網站狀態數據類"""
    url: str
    status: MonitorStatus
    http_status_code: Optional[int] = None
    response_time_ms: Optional[float] = None
    ssl_days_remaining: Optional[int] = None
    ssl_issuer: Optional[str] = None
    last_check: datetime = field(default_factory=datetime.utcnow)
    error_message: Optional[str] = None
    content_hash: Optional[str] = None
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    region: str = "global"


@dataclass
class UptimeRecord:
    """可用性記錄數據類"""
    url: str
    checks_total: int = 0
    checks_up: int = 0
    checks_down: int = 0
    uptime_percentage: float = 0.0
    current_streak: int = 0  # 連續成功次數
    downtime_events: List[Dict[str, Any]] = field(default_factory=list)
    last_downtime: Optional[datetime] = None
    total_downtime_seconds: int = 0
    average_response_time: float = 0.0
    response_times: List[float] = field(default_factory=list)


@dataclass
class ContentChange:
    """內容變化記錄數據類"""
    url: str
    previous_hash: Optional[str] = None
    current_hash: str = ""
    change_detected: bool = False
    change_timestamp: datetime = field(default_factory=datetime.utcnow)
    diff_summary: Optional[str] = None
    important_changes: List[str] = field(default_factory=list)


class SSLMonitor:
    """SSL證書監控器"""

    def __init__(self):
        self.logger = get_logger(__name__)

    async def check_ssl_certificate(self, hostname: str) -> Dict[str, Any]:
        """
        檢查SSL證書狀態

        Args:
            hostname: 目標主機名

        Returns:
            SSL證書信息字典
        """
        try:
            # 獲取SSL證書
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()

            # 解析證書信息
            not_after = ssl.cert_time_to_seconds(cert['notAfter'])
            days_remaining = max(0, int((not_after - time.time()) / (24 * 3600)))

            issuer = cert.get('issuer', [])
            issuer_str = ""
            if issuer:
                issuer_parts = []
                for part in issuer:
                    for key, value in part:
                        if key == 'organizationName':
                            issuer_parts.append(value)
                        elif key == 'commonName' and not issuer_parts:
                            issuer_parts.append(value)
                issuer_str = ', '.join(issuer_parts)

            return {
                "valid": True,
                "days_remaining": days_remaining,
                "issuer": issuer_str,
                "not_after": datetime.fromtimestamp(not_after).isoformat(),
                "subject": cert.get('subject', []),
                "warning_level": "critical" if days_remaining <= 7 else ("warning" if days_remaining <= 30 else "info")
            }

        except ssl.SSLError as e:
            return {
                "valid": False,
                "error": f"SSL錯誤: {str(e)}",
                "warning_level": "critical"
            }
        except Exception as e:
            return {
                "valid": False,
                "error": f"SSL檢查失敗: {str(e)}",
                "warning_level": "error"
            }


class ContentMonitor:
    """內容變化監控器"""

    def __init__(self):
        self.logger = get_logger(__name__)
        self.previous_hashes: Dict[str, str] = {}
        self.change_history: Dict[str, List[ContentChange]] = defaultdict(list)

    async def check_content_changes(self, url: str, html_content: str,
                                  monitored_selectors: Optional[List[str]] = None) -> ContentChange:
        """
        檢查頁面內容變化

        Args:
            url: 目標URL
            html_content: HTML內容
            monitored_selectors: 需要監控的CSS選擇器列表

        Returns:
            內容變化記錄
        """
        try:
            # 生成內容哈希
            current_hash = self._generate_content_hash(html_content, monitored_selectors)

            # 獲取之前的哈希
            previous_hash = self.previous_hashes.get(url)

            change = ContentChange(
                url=url,
                previous_hash=previous_hash,
                current_hash=current_hash,
                change_detected=previous_hash != current_hash
            )

            if change.change_detected:
                # 進行詳細比較
                diff = await self._compare_content_detailed(url, previous_hash, current_hash, html_content)
                change.diff_summary = diff.get("summary")
                change.important_changes = diff.get("important_changes", [])

                self.logger.info("content_change_detected",
                               url=url,
                               previous_hash=previous_hash[:8] if previous_hash else None,
                               current_hash=current_hash[:8],
                               important_changes=len(change.important_changes))

            # 更新哈希記錄
            self.previous_hashes[url] = current_hash

            # 保存到歷史記錄
            self.change_history[url].append(change)
            # 只保留最近100條記錄
            if len(self.change_history[url]) > 100:
                self.change_history[url] = self.change_history[url][-100:]

            return change

        except Exception as e:
            self.logger.error("content_check_error", url=url, error=str(e))
            return ContentChange(url=url, error=str(e))

    def _generate_content_hash(self, html_content: str,
                             monitored_selectors: Optional[List[str]] = None) -> str:
        """生成內容哈希"""
        try:
            if monitored_selectors:
                # 只監控特定選擇器的內容
                soup = BeautifulSoup(html_content, 'lxml')
                monitored_content = []

                for selector in monitored_selectors:
                    try:
                        elements = soup.select(selector)
                        for element in elements:
                            monitored_content.append(element.get_text().strip())
                    except:
                        continue

                if monitored_content:
                    content_to_hash = '\n'.join(monitored_content)
                else:
                    content_to_hash = soup.get_text()
            else:
                # 使用整個頁面文本
                soup = BeautifulSoup(html_content, 'lxml')
                content_to_hash = soup.get_text()

            # 生成SHA256哈希
            return hashlib.sha256(content_to_hash.encode('utf-8')).hexdigest()

        except Exception as e:
            # 降級到簡單哈希
            self.logger.warning("content_hash_error", error=str(e))
            return hashlib.md5(html_content.encode('utf-8')).hexdigest()

    async def _compare_content_detailed(self, url: str, previous_hash: str,
                                      current_hash: str, html_content: str) -> Dict[str, Any]:
        """詳細內容比較"""
        # 注意：這是一個簡化的實現
        # 在實際應用中，可以使用diff算法進行更詳細的比較

        try:
            result = {
                "summary": f"內容哈希從 {previous_hash[:8]} 變為 {current_hash[:8]}",
                "important_changes": []
            }

            # 檢查一些常見的變化指標
            soup = BeautifulSoup(html_content, 'lxml')

            # 檢查標題變化
            if soup.title:
                title = soup.title.get_text().strip()
                result["important_changes"].append(f"頁面標題: {title}")

            # 檢查關鍵元素數量變化
            article_count = len(soup.find_all('article'))
            if article_count > 0:
                result["important_changes"].append(f"發現 {article_count} 篇文章元素")

            # 檢查鏈接變化
            link_count = len(soup.find_all('a', href=True))
            result["important_changes"].append(f"頁面包含 {link_count} 個鏈接")

            return result

        except Exception as e:
            self.logger.warning("content_comparison_error", error=str(e))
            return {
                "summary": "內容比較失敗",
                "important_changes": [f"比較錯誤: {str(e)}"]
            }


class PerformanceCollector:
    """性能指標收集器"""

    def __init__(self):
        self.logger = get_logger(__name__)

    async def collect_performance_metrics(self, url: str,
                                        response: Optional[httpx.Response] = None) -> Dict[str, Any]:
        """
        收集性能指標

        Args:
            url: 目標URL
            response: HTTP響應對象

        Returns:
            性能指標字典
        """
        metrics = {
            "ttfb": None,  # Time to First Byte
            "dns_lookup": None,
            "tcp_connect": None,
            "ssl_handshake": None,
            "server_processing": None,
            "content_size": None,
            "content_type": None,
            "compression": None,
            "redirect_count": 0
        }

        try:
            if response:
                # 從響應頭獲取性能信息
                content_length = response.headers.get('content-length')
                if content_length and content_length.isdigit():
                    metrics["content_size"] = int(content_length)

                metrics["content_type"] = response.headers.get('content-type', '')

                # 檢查是否啟用壓縮
                content_encoding = response.headers.get('content-encoding', '')
                if content_encoding:
                    metrics["compression"] = content_encoding

                # 檢查是否有重定向
                if response.history:
                    metrics["redirect_count"] = len(response.history)

            # 注意：詳細的時間指標需要更底層的HTTP客戶端支持
            # 這裡只收集基本指標

            self.logger.debug("performance_metrics_collected", url=url, metrics=metrics)

            return metrics

        except Exception as e:
            self.logger.warning("performance_collection_error", url=url, error=str(e))
            return metrics


class WebsiteMonitorService:
    """
    網站監控服務主類
    整合所有監控功能，提供統一的網站健康檢查介面
    """

    def __init__(self):
        self.config = get_config_manager().get("monitor", {})
        self.logger = get_logger(__name__)

        # 初始化組件
        self.ssl_monitor = SSLMonitor()
        self.content_monitor = ContentMonitor()
        self.performance_collector = PerformanceCollector()

        # 狀態存儲
        self.status_cache: Dict[str, WebsiteStatus] = {}
        self.uptime_records: Dict[str, UptimeRecord] = {}
        self.alert_history: List[Dict[str, Any]] = []

        # 監控配置
        self.check_interval = self.config.get("check_interval_seconds", 60)
        self.timeout = self.config.get("timeout_seconds", 10)
        self.retry_attempts = self.config.get("retry_attempts", 2)

        # 區域配置
        self.regions = self.config.get("regions", ["global"])
        self.current_region = self.regions[0] if self.regions else "global"

        self.logger.info("website_monitor_service_initialized",
                        check_interval=self.check_interval,
                        regions=self.regions)

    async def check_website(self, url: str, full_check: bool = True) -> WebsiteStatus:
        """
        全面檢查網站狀態

        Args:
            url: 要檢查的網站URL
            full_check: 是否進行完整檢查 (包括SSL和內容)

        Returns:
            網站狀態對象
        """
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname

            if not hostname:
                return WebsiteStatus(
                    url=url,
                    status=MonitorStatus.DOWN,
                    error_message="無效的URL格式",
                    region=self.current_region
                )

            # HTTP可用性檢查
            status = await self._check_http_availability(url)

            if full_check and status.status == MonitorStatus.UP:
                # SSL證書檢查
                if parsed.scheme == 'https' and hostname:
                    ssl_info = await self.ssl_monitor.check_ssl_certificate(hostname)
                    status.ssl_days_remaining = ssl_info.get("days_remaining")
                    status.ssl_issuer = ssl_info.get("issuer")

                    # 檢查SSL相關告警
                    if not ssl_info.get("valid", True):
                        await self._create_alert(url, AlertLevel.CRITICAL,
                                               f"SSL證書錯誤: {ssl_info.get('error', '未知錯誤')}")

                # 性能指標收集
                status.performance_metrics = await self.performance_collector.collect_performance_metrics(
                    url, getattr(status, '_response', None)
                )

                # 內容變化檢查 (如果啟用)
                if self.config.get("content_monitoring_enabled", False) and hasattr(status, '_raw_content'):
                    content_change = await self.content_monitor.check_content_changes(
                        url, status._raw_content
                    )
                    status.content_hash = content_change.current_hash

                    if content_change.change_detected:
                        await self._create_alert(url, AlertLevel.INFO,
                                               f"頁面內容發生變化: {content_change.diff_summary}")

            # 更新狀態緩存
            self.status_cache[url] = status

            # 更新可用性記錄
            await self._update_uptime_record(url, status)

            self.logger.info("website_check_completed",
                           url=url,
                           status=status.status.value,
                           response_time=status.response_time_ms)

            return status

        except Exception as e:
            self.logger.error("website_check_error", url=url, error=str(e))

            status = WebsiteStatus(
                url=url,
                status=MonitorStatus.DOWN,
                error_message=str(e),
                region=self.current_region
            )

            # 更新緩存
            self.status_cache[url] = status
            await self._update_uptime_record(url, status)

            return status

    async def _check_http_availability(self, url: str) -> WebsiteStatus:
        """檢查HTTP可用性"""
        start_time = time.time()

        for attempt in range(self.retry_attempts + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                    response = await client.get(url)
                    response_time = (time.time() - start_time) * 1000  # 轉換為毫秒

                    status = MonitorStatus.UP if response.is_success else MonitorStatus.DEGRADED

                    website_status = WebsiteStatus(
                        url=url,
                        status=status,
                        http_status_code=response.status_code,
                        response_time_ms=round(response_time, 2),
                        region=self.current_region,
                        error_message=None if response.is_success else f"HTTP {response.status_code}"
                    )

                    # 保存響應內容以供進一步分析
                    website_status._response = response
                    website_status._raw_content = response.text

                    return website_status

            except httpx.TimeoutException:
                if attempt == self.retry_attempts:
                    return WebsiteStatus(
                        url=url,
                        status=MonitorStatus.DOWN,
                        error_message="請求超時",
                        region=self.current_region
                    )
                await asyncio.sleep(0.5)
                continue

            except Exception as e:
                if attempt == self.retry_attempts:
                    return WebsiteStatus(
                        url=url,
                        status=MonitorStatus.DOWN,
                        error_message=str(e),
                        region=self.current_region
                    )
                await asyncio.sleep(0.5)
                continue

        return WebsiteStatus(
            url=url,
            status=MonitorStatus.DOWN,
            error_message="所有重試都失敗",
            region=self.current_region
        )

    async def _update_uptime_record(self, url: str, status: WebsiteStatus):
        """更新可用性記錄"""
        if url not in self.uptime_records:
            self.uptime_records[url] = UptimeRecord(url=url)

        record = self.uptime_records[url]

        # 更新統計
        record.checks_total += 1
        if status.status == MonitorStatus.UP:
            record.checks_up += 1
            record.current_streak += 1
        else:
            record.checks_down += 1
            record.current_streak = 0
            record.last_downtime = datetime.utcnow()

            # 記錄宕機事件
            downtime_event = {
                "start_time": datetime.utcnow().isoformat(),
                "duration": None,  # 稍後計算
                "reason": status.error_message or "未知原因",
                "region": status.region
            }
            record.downtime_events.append(downtime_event)

        # 更新可用百分比
        if record.checks_total > 0:
            record.uptime_percentage = (record.checks_up / record.checks_total) * 100

        # 收集響應時間統計
        if status.response_time_ms is not None:
            record.response_times.append(status.response_time_ms)
            # 只保留最近100個樣本
            if len(record.response_times) > 100:
                record.response_times = record.response_times[-100:]

            if record.response_times:
                record.average_response_time = statistics.mean(record.response_times)

        # 檢查是否需要告警
        await self._check_uptime_alerts(url, record)

    async def _check_uptime_alerts(self, url: str, record: UptimeRecord):
        """檢查可用性告警"""
        # 可用率低於95%發出警告
        if record.uptime_percentage < 95.0 and record.checks_total >= 10:
            await self._create_alert(url, AlertLevel.WARNING,
                                   ".2f")

        # 連續失敗次數過多
        if record.current_streak == 0 and record.checks_down >= 3:
            await self._create_alert(url, AlertLevel.ERROR,
                                   f"連續 {record.checks_down} 次檢查失敗")

        # 響應時間異常
        if (record.average_response_time > 5000 and  # 5秒
            record.uptime_percentage > 95.0):  # 但系統正常運行
            await self._create_alert(url, AlertLevel.WARNING,
                                   ".2f")

    async def _create_alert(self, url: str, level: AlertLevel, message: str):
        """創建告警記錄"""
        alert = {
            "id": hashlib.md5(f"{url}:{datetime.utcnow().isoformat()}".encode()).hexdigest()[:8],
            "url": url,
            "level": level.value,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "region": self.current_region
        }

        self.alert_history.append(alert)

        # 只保留最近1000條告警記錄
        if len(self.alert_history) > 1000:
            self.alert_history = self.alert_history[-1000:]

        self.logger.warning("alert_created", alert=alert)

    def get_status(self, url: str) -> Optional[WebsiteStatus]:
        """獲取網站狀態"""
        return self.status_cache.get(url)

    def get_uptime_record(self, url: str) -> Optional[UptimeRecord]:
        """獲取可用性記錄"""
        return self.uptime_records.get(url)

    def get_alerts(self, limit: int = 50) -> List[Dict[str, Any]]:
        """獲取最近的告警記錄"""
        return self.alert_history[-limit:] if self.alert_history else []

    def get_all_status(self) -> List[WebsiteStatus]:
        """獲取所有監控中的網站狀態"""
        return list(self.status_cache.values())

    def get_uptime_summary(self) -> Dict[str, Any]:
        """獲取系統整體可用性總結"""
        total_sites = len(self.uptime_records)
        if total_sites == 0:
            return {"total_sites": 0}

        total_checks = sum(record.checks_total for record in self.uptime_records.values())
        total_up = sum(record.checks_up for record in self.uptime_records.values())

        overall_uptime = (total_up / total_checks * 100) if total_checks > 0 else 0

        return {
            "total_sites": total_sites,
            "total_checks": total_checks,
            "overall_uptime_percentage": round(overall_uptime, 2),
            "sites_up": sum(1 for record in self.uptime_records.values()
                          if self.status_cache.get(record.url) and
                          self.status_cache[record.url].status == MonitorStatus.UP),
            "sites_down": sum(1 for record in self.uptime_records.values()
                            if self.status_cache.get(record.url) and
                            self.status_cache[record.url].status == MonitorStatus.DOWN)
        }


class MonitorScheduler:
    """
    監控任務調度器
    負責定期執行網站檢查任務
    """

    def __init__(self, monitor_service: WebsiteMonitorService):
        self.monitor_service = monitor_service
        self.logger = get_logger(__name__)

        # 監控中的網站列表
        self.monitored_sites: List[Dict[str, Any]] = []
        self.scheduler_task: Optional[asyncio.Task] = None
        self.is_running = False

        self.config = get_config_manager().get("monitor", {})
        self.check_interval = self.config.get("check_interval_seconds", 60)

    def add_site(self, url: str, full_check: bool = True, content_selectors: Optional[List[str]] = None):
        """添加要監控的網站"""
        site_config = {
            "url": url,
            "full_check": full_check,
            "content_selectors": content_selectors,
            "added_at": datetime.utcnow().isoformat()
        }

        # 檢查是否已經存在
        if not any(site["url"] == url for site in self.monitored_sites):
            self.monitored_sites.append(site_config)
            self.logger.info("site_added_to_monitor", url=url, full_check=full_check)

    def remove_site(self, url: str) -> bool:
        """移除監控網站"""
        for i, site in enumerate(self.monitored_sites):
            if site["url"] == url:
                self.monitored_sites.pop(i)
                self.logger.info("site_removed_from_monitor", url=url)
                return True
        return False

    async def start_monitoring(self):
        """開始監控任務"""
        if self.is_running:
            self.logger.warning("monitor_scheduler_already_running")
            return

        self.is_running = True
        self.scheduler_task = asyncio.create_task(self._monitoring_loop())

        self.logger.info("monitor_scheduler_started",
                        sites_count=len(self.monitored_sites),
                        interval_seconds=self.check_interval)

    async def stop_monitoring(self):
        """停止監控任務"""
        self.is_running = False

        if self.scheduler_task:
            self.scheduler_task.cancel()
            try:
                await self.scheduler_task
            except asyncio.CancelledError:
                pass

        self.logger.info("monitor_scheduler_stopped")

    async def _monitoring_loop(self):
        """監控循環"""
        while self.is_running:
            try:
                # 並發檢查所有網站
                tasks = []
                for site in self.monitored_sites:
                    task = asyncio.create_task(
                        self.monitor_service.check_website(
                            site["url"],
                            site["full_check"]
                        )
                    )
                    tasks.append(task)

                if tasks:
                    results = await asyncio.gather(*tasks, return_exceptions=True)

                    # 處理結果
                    for i, result in enumerate(results):
                        site = self.monitored_sites[i]
                        if isinstance(result, Exception):
                            self.logger.error("site_check_failed",
                                            url=site["url"],
                                            error=str(result))
                        else:
                            self.logger.debug("site_check_completed",
                                            url=site["url"],
                                            status=result.status.value)

            except Exception as e:
                self.logger.error("monitoring_loop_error", error=str(e))

            # 等待下一次檢查
            await asyncio.sleep(self.check_interval)

    def get_monitored_sites(self) -> List[Dict[str, Any]]:
        """獲取監控中的網站列表"""
        return self.monitored_sites.copy()


# 全域實例
_website_monitor_service: Optional[WebsiteMonitorService] = None
_monitor_scheduler: Optional[MonitorScheduler] = None


def init_website_monitor() -> Tuple[WebsiteMonitorService, MonitorScheduler]:
    """
    初始化網站監控服務

    Returns:
        (監控服務實例, 調度器實例)
    """
    global _website_monitor_service, _monitor_scheduler

    if _website_monitor_service is None:
        _website_monitor_service = WebsiteMonitorService()

    if _monitor_scheduler is None:
        _monitor_scheduler = MonitorScheduler(_website_monitor_service)

    return _website_monitor_service, _monitor_scheduler


def get_website_monitor() -> WebsiteMonitorService:
    """獲取網站監控服務實例"""
    if _website_monitor_service is None:
        raise RuntimeError("網站監控服務尚未初始化，請先調用init_website_monitor()")
    return _website_monitor_service


def get_monitor_scheduler() -> MonitorScheduler:
    """獲取監控調度器實例"""
    if _monitor_scheduler is None:
        raise RuntimeError("監控調度器尚未初始化，請先調用init_website_monitor()")
    return _monitor_scheduler
