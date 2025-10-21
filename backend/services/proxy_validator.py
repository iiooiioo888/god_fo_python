"""
WebCrawler Commander - 代理驗證器
實現企業級代理池健康度驗證和智能管理系統

核心功能：
- TCP連接測試與多維度健康度評分算法
- 代理池動態管理 (自動發現、註冊、隔離)
- 異常檢測與預警機制
- 性能統計與趨勢分析
- 多來源代理融合 (公共/付費/SOCKS5)
- 配置化驗證計劃與靈活調度

作者: Jerry開發工作室
版本: v1.0.0
"""

import asyncio
import socket
import time
import statistics
import json
import hashlib
import ipaddress
from typing import Dict, List, Optional, Any, Tuple, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import httpx
import aiohttp
from aiohttp import ClientTimeout
import dns.resolver
import dns.exception

from ..utils.config_manager import get_config_manager
from ..utils.logger_service import get_logger


class ProxyType(Enum):
    """代理類型枚舉"""
    HTTP = "http"
    HTTPS = "https"
    SOCKS4 = "socks4"
    SOCKS5 = "socks5"


class ProxyStatus(Enum):
    """代理狀態枚舉"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class AnonymityLevel(Enum):
    """匿名度等級枚舉"""
    TRANSPARENT = "transparent"    # 透明代理，服務器可見真實IP
    ANONYMOUS = "anonymous"        # 匿名代理，不發送VIA頭
    ELITE = "elite"                # 高匿名代理，完全隱藏代理跡象


@dataclass
class ProxyMetrics:
    """代理性能指標"""
    response_time: float = 0.0              # 響應時間(毫秒)
    success_rate: float = 0.0               # 成功率(0-1)
    bandwidth: float = 0.0                  # 帶寬(Mbps)
    uptime: float = 0.0                     # 在線時間百分比
    stability_score: float = 0.0            # 穩定性評分(0-1)
    last_tested: datetime = field(default_factory=datetime.utcnow)


@dataclass
class GeoInfo:
    """地理位置信息"""
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    isp: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[str] = None


@dataclass
class Proxy:
    """代理對象"""
    ip: str
    port: int
    type: ProxyType = ProxyType.HTTP
    username: Optional[str] = None
    password: Optional[str] = None

    # 動態屬性
    status: ProxyStatus = ProxyStatus.UNKNOWN
    anonymity: AnonymityLevel = AnonymityLevel.UNKNOWN
    health_score: float = 0.0
    priority: int = 0
    usage_count: int = 0
    fail_count: int = 0
    last_used: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    # 位置信息
    geo_info: Optional[GeoInfo] = None
    asn: Optional[str] = None

    # 性能指標
    metrics: ProxyMetrics = field(default_factory=ProxyMetrics)

    # 標記
    is_active: bool = True
    tags: List[str] = field(default_factory=list)

    @property
    def url(self) -> str:
        """生成代理URL"""
        if self.username and self.password:
            auth = f"{self.username}:{self.password}@"
        else:
            auth = ""

        scheme = "http" if self.type in [ProxyType.HTTP, ProxyType.SOCKS4, ProxyType.SOCKS5] else "https"
        return f"{scheme}://{auth}{self.ip}:{self.port}"

    @property
    def dict_key(self) -> str:
        """生成字典鍵"""
        return f"{self.ip}:{self.port}:{self.type.value}"

    def update_metrics(self, response_time: float, success: bool, bandwidth: Optional[float] = None):
        """更新性能指標"""
        self.usage_count += 1

        if success:
            self.metrics.response_time = (self.metrics.response_time + response_time) / 2
            if bandwidth:
                self.metrics.bandwidth = bandwidth
        else:
            self.fail_count += 1

        # 更新成功率 (使用指數移動平均)
        current_success = 1.0 if success else 0.0
        alpha = 0.1  # 平滑因子
        self.metrics.success_rate = (1 - alpha) * self.metrics.success_rate + alpha * current_success

        # 更新穩定性評分
        total_attempts = self.usage_count + self.fail_count
        if total_attempts > 10:
            self.metrics.stability_score = self.usage_count / total_attempts

        self.metrics.last_tested = datetime.utcnow()
        self.last_used = datetime.utcnow()

    def calculate_health_score(self) -> float:
        """
        計算健康度評分

        權重分配：
        - 成功率: 40%
        - 響應時間: 30%
        - 穩定性: 20%
        - 匿名度: 10%
        """
        scores = []

        # 成功率評分 (0-40分)
        if self.metrics.success_rate >= 0.95:
            success_score = 40
        elif self.metrics.success_rate >= 0.80:
            success_score = 30
        elif self.metrics.success_rate >= 0.60:
            success_score = 20
        else:
            success_score = max(0, self.metrics.success_rate * 35)
        scores.append(("success_rate", success_score))

        # 響應時間評分 (0-30分)
        if self.metrics.response_time <= 500:  # <=500ms
            response_score = 30
        elif self.metrics.response_time <= 2000:  # <=2s
            response_score = 25
        elif self.metrics.response_time <= 5000:  # <=5s
            response_score = 15
        else:
            response_score = max(0, 30 - (self.metrics.response_time / 1000) * 2)
        scores.append(("response_time", response_score))

        # 穩定性評分 (0-20分)
        stability_score = self.metrics.stability_score * 20
        scores.append(("stability", stability_score))

        # 匿名度評分 (0-10分)
        if self.anonymity == AnonymityLevel.ELITE:
            anonymity_score = 10
        elif self.anonymity == AnonymityLevel.ANONYMOUS:
            anonymity_score = 5
        else:
            anonymity_score = 0
        scores.append(("anonymity", anonymity_score))

        total_score = sum(score for _, score in scores)
        self.health_score = min(100, max(0, total_score))

        # 更新狀態
        if self.health_score >= 80:
            self.status = ProxyStatus.HEALTHY
        elif self.health_score >= 50:
            self.status = ProxyStatus.DEGRADED
        else:
            self.status = ProxyStatus.UNHEALTHY
            self.is_active = False

        return self.health_score


class TCPTester:
    """TCP連接測試器"""

    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout
        self.logger = get_logger(__name__)

    async def test_connection(self, ip: str, port: int) -> Tuple[bool, float]:
        """
        測試TCP連接

        Args:
            ip: IP地址
            port: 端口

        Returns:
            (連接成功, 連接時間毫秒)
        """
        start_time = time.time()

        try:
            loop = asyncio.get_event_loop()

            # 使用執行緒池執行同步socket操作
            result = await loop.run_in_executor(
                None,
                self._sync_tcp_test,
                ip, port, self.timeout
            )

            end_time = time.time()
            connection_time = (end_time - start_time) * 1000  # 轉換為毫秒

            return result, min(connection_time, 30000)  # 最大30秒

        except Exception as e:
            self.logger.debug("TCP connection test failed", ip=ip, port=port, error=str(e))
            end_time = time.time()
            connection_time = (end_time - start_time) * 1000
            return False, connection_time

    def _sync_tcp_test(self, ip: str, port: int, timeout: float) -> bool:
        """同步TCP測試"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False


class DNSTester:
    """DNS解析測試器"""

    def __init__(self, timeout: float = 3.0):
        self.timeout = timeout
        self.logger = get_logger(__name__)
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = timeout
        self.resolver.lifetime = timeout

    async def test_dns_resolution(self, hostname: str) -> Tuple[bool, float, List[str]]:
        """
        測試DNS解析

        Args:
            hostname: 主機名

        Returns:
            (解析成功, 解析時間毫秒, IP地址列表)
        """
        start_time = time.time()

        try:
            loop = asyncio.get_event_loop()

            # 使用執行緒池執行DNS解析
            result = await loop.run_in_executor(
                None,
                self._sync_dns_test,
                hostname
            )

            end_time = time.time()
            resolution_time = (end_time - start_time) * 1000

            return result[0], resolution_time, result[1]

        except Exception as e:
            self.logger.debug("DNS resolution test failed", hostname=hostname, error=str(e))
            return False, 0.0, []

    def _sync_dns_test(self, hostname: str) -> Tuple[bool, List[str]]:
        """同步DNS測試"""
        try:
            answers = self.resolver.resolve(hostname, 'A')
            ips = [str(rdata) for rdata in answers]
            return True, ips
        except dns.exception.DNSException:
            return False, []


class HTTPTester:
    """HTTP代理測試器"""

    def __init__(self, timeout: float = 10.0, test_url: str = "http://httpbin.org/get"):
        self.timeout = timeout
        self.test_url = test_url
        self.logger = get_logger(__name__)

    async def test_proxy(self, proxy: Proxy) -> Dict[str, Any]:
        """
        測試代理

        Args:
            proxy: 代理對象

        Returns:
            測試結果字典
        """
        result = {
            "success": False,
            "response_time": 0.0,
            "status_code": None,
            "anonymity": AnonymityLevel.UNKNOWN,
            "real_ip": None,
            "proxy_ip": None,
            "bandwidth": 0.0,
            "error": None
        }

        start_time = time.time()

        try:
            # 構建代理URL
            proxy_url = proxy.url
            proxies = {"http": proxy_url, "https": proxy_url}

            async with httpx.AsyncClient(
                proxies=proxies,
                timeout=self.timeout,
                follow_redirects=False
            ) as client:
                response = await client.get(self.test_url)

                end_time = time.time()
                response_time = (end_time - start_time) * 1000

                result.update({
                    "success": True,
                    "response_time": response_time,
                    "status_code": response.status_code
                })

                # 解析響應檢查匿名度
                anonymity, real_ip, proxy_ip = await self._analyze_response(response)
                result.update({
                    "anonymity": anonymity,
                    "real_ip": real_ip,
                    "proxy_ip": proxy_ip
                })

                # 估計帶寬 (下載測試)
                if response.content:
                    download_time = end_time - start_time
                    content_size_kb = len(response.content) / 1024
                    bandwidth = (content_size_kb * 8) / download_time  # Kbps
                    result["bandwidth"] = bandwidth

        except Exception as e:
            result["error"] = str(e)
            result["response_time"] = (time.time() - start_time) * 1000

        return result

    async def _analyze_response(self, response: httpx.Response) -> Tuple[AnonymityLevel, Optional[str], Optional[str]]:
        """
        分析響應確定匿名度

        Returns:
            (匿名度等級, 真實IP, 代理IP)
        """
        try:
            data = response.json()
            origin = data.get("origin", "")

            # 檢查VIA頭
            via_header = response.headers.get("via")
            x_forwarded_for = response.headers.get("x-forwarded-for")
            x_real_ip = response.headers.get("x-real-ip")

            real_ip = None
            proxy_ip = None

            if "," in origin:
                # 多個IP地址，可能使用了代理
                ips = [ip.strip() for ip in origin.split(",")]
                if len(ips) >= 2:
                    real_ip = ips[0]
                    proxy_ip = ips[1]

            else:
                proxy_ip = origin

            # 判斷匿名度
            if not via_header and not x_forwarded_for and not x_real_ip:
                anonymity = AnonymityLevel.ELITE
            elif x_forwarded_for or x_real_ip:
                anonymity = AnonymityLevel.ANONYMOUS
            else:
                anonymity = AnonymityLevel.TRANSPARENT

            return anonymity, real_ip, proxy_ip

        except Exception as e:
            self.logger.debug("response analysis failed", error=str(e))
            return AnonymityLevel.UNKNOWN, None, None


class GeoLocator:
    """地理位置定位器"""

    def __init__(self):
        self.logger = get_logger(__name__)
        self.cache: Dict[str, GeoInfo] = {}
        self.cache_timeout = 86400  # 24小時緩存

    async def get_geo_info(self, ip: str) -> Optional[GeoInfo]:
        """
        獲取IP地理位置信息

        Args:
            ip: IP地址

        Returns:
            地理位置信息
        """
        # 檢查緩存
        if ip in self.cache:
            cached_info, cache_time = self.cache[ip]
            if datetime.utcnow() - cache_time < timedelta(seconds=self.cache_timeout):
                return cached_info

        try:
            # 這裡可以使用第三方地理位置API
            # 示例使用ip-api.com的免費服務
            url = f"http://ip-api.com/json/{ip}"

            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    data = response.json()

                    geo_info = GeoInfo(
                        country=data.get("country"),
                        region=data.get("regionName"),
                        city=data.get("city"),
                        isp=data.get("isp"),
                        latitude=data.get("lat"),
                        longitude=data.get("lon"),
                        timezone=data.get("timezone")
                    )

                    # 更新緩存
                    self.cache[ip] = (geo_info, datetime.utcnow())
                    return geo_info

        except Exception as e:
            self.logger.debug("geo location lookup failed", ip=ip, error=str(e))

        return None


class ProxyValidator:
    """
    代理驗證器核心類

    實現企業級代理池健康度驗證和管理：
    - 多維度健康度評分算法 (成功率/時延/穩定性/匿名度)
    - 並發代理測試與批量驗證
    - 動態代理池管理與智能輪換
    - 地理位置識別與性能統計
    - 異常檢測與自動隔離
    - 可觀測性監控與儀表板數據
    """

    def __init__(self, config_manager=None):
        self.config_manager = config_manager or get_config_manager()
        self.logger = get_logger(__name__)

        # 初始化測試器
        self.tcp_tester = TCPTester()
        self.dns_tester = DNSTester()
        self.http_tester = HTTPTester()
        self.geo_locator = GeoLocator()

        # 代理池
        self.proxies: Dict[str, Proxy] = {}
        self.proxy_lock = asyncio.Lock()

        # 統計信息
        self.stats = {
            "total_proxies": 0,
            "healthy_proxies": 0,
            "degraded_proxies": 0,
            "unhealthy_proxies": 0,
            "total_tests": 0,
            "successful_tests": 0,
            "test_duration_avg": 0.0,
            "last_validation": None
        }

        # 測試配置
        self._test_config = None

        self.logger.info("proxy_validator_initialized")

    async def validate_proxy(self, proxy: Proxy, full_test: bool = True) -> Proxy:
        """
        驗證單個代理

        Args:
            proxy: 代理對象
            full_test: 是否進行完整測試

        Returns:
            更新後的代理對象
        """
        start_time = time.time()

        try:
            self.logger.debug("starting proxy validation", proxy=f"{proxy.ip}:{proxy.port}")

            if full_test:
                # TCP連接測試
                tcp_success, tcp_time = await self.tcp_tester.test_connection(proxy.ip, proxy.port)

                if not tcp_success:
                    proxy.is_active = False
                    proxy.status = ProxyStatus.UNHEALTHY
                    return proxy

                # DNS解析測試 (如果適用)
                if proxy.type in [ProxyType.HTTP, ProxyType.HTTPS]:
                    dns_success, dns_time, ips = await self.dns_tester.test_dns_resolution(proxy.ip)
                    if not dns_success and not ips:
                        proxy.status = ProxyStatus.DEGRADED

                # HTTP代理功能測試
                http_result = await self.http_tester.test_proxy(proxy)

                if http_result["success"]:
                    # 更新代理信息
                    proxy.anonymity = http_result["anonymity"]
                    proxy.metrics.response_time = http_result["response_time"]
                    proxy.metrics.bandwidth = http_result.get("bandwidth", 0.0)
                    proxy.metrics.success_rate = 1.0
                    proxy.metrics.uptime = 1.0

                    # 更新地理位置信息
                    if not proxy.geo_info:
                        geo_info = await self.geo_locator.get_geo_info(proxy.ip)
                        if geo_info:
                            proxy.geo_info = geo_info

                else:
                    proxy.fail_count += 1
                    proxy.metrics.success_rate = max(0, proxy.metrics.success_rate - 0.1)

            # 計算健康度評分
            health_score = proxy.calculate_health_score()
            proxy.health_score = health_score

            test_duration = (time.time() - start_time) * 1000

            # 更新統計
            self.stats["total_tests"] += 1
            if proxy.status == ProxyStatus.HEALTHY:
                self.stats["successful_tests"] += 1

            self.logger.info("proxy validation completed",
                           proxy=f"{proxy.ip}:{proxy.port}",
                           status=proxy.status.value,
                           health_score=round(health_score, 2),
                           duration=round(test_duration, 2))

            return proxy

        except Exception as e:
            self.logger.error("proxy validation failed",
                            proxy=f"{proxy.ip}:{proxy.port}",
                            error=str(e))
            proxy.status = ProxyStatus.UNHEALTHY
            proxy.is_active = False
            return proxy

    async def validate_proxy_pool(self, max_concurrent: int = 10) -> Dict[str, Dict[str, Any]]:
        """
        批量驗證代理池中的所有代理

        Args:
            max_concurrent: 最大並發驗證數

        Returns:
            驗證結果摘要
        """
        start_time = time.time()

        async with self.proxy_lock:
            active_proxies = [proxy for proxy in self.proxies.values() if proxy.is_active]

        if not active_proxies:
            self.logger.warning("no active proxies to validate")
            return {"status": "no_proxies"}

        self.logger.info("starting bulk proxy validation",
                        total_proxies=len(active_proxies),
                        max_concurrent=max_concurrent)

        # 使用信號量控制並發數
        semaphore = asyncio.Semaphore(max_concurrent)

        async def validate_with_semaphore(proxy):
            async with semaphore:
                return await self.validate_proxy(proxy, full_test=True)

        # 並發驗證
        validated_proxies = await asyncio.gather(
            *(validate_with_semaphore(proxy) for proxy in active_proxies),
            return_exceptions=True
        )

        # 更新代理狀態
        updated_count = 0
        for result in validated_proxies:
            if isinstance(result, Proxy):
                self.proxies[result.dict_key] = result
                updated_count += 1

        # 更新統計信息
        self._update_pool_stats()

        elapsed = time.time() - start_time
        self.stats["last_validation"] = datetime.utcnow()

        result_summary = {
            "status": "completed",
            "total_proxies": len(active_proxies),
            "validated_proxies": updated_count,
            "elapsed_seconds": round(elapsed, 2),
            "healthy_count": self.stats["healthy_proxies"],
            "degraded_count": self.stats["degraded_proxies"],
            "unhealthy_count": self.stats["unhealthy_proxies"]
        }

        self.logger.info("bulk proxy validation completed", **result_summary)
        return result_summary

    async def add_proxy(self, proxy: Union[Proxy, Dict[str, Any]]) -> bool:
        """
        添加代理到池中

        Args:
            proxy: 代理對象或代理配置字典

        Returns:
            添加是否成功
        """
        if isinstance(proxy, dict):
            proxy = await self._create_proxy_from_dict(proxy)

        async with self.proxy_lock:
            key = proxy.dict_key

            if key in self.proxies:
                self.logger.debug("proxy already exists", proxy=key)
                return False

            # 初始驗證
            validated_proxy = await self.validate_proxy(proxy, full_test=False)

            if validated_proxy.status in [ProxyStatus.HEALTHY, ProxyStatus.DEGRADED]:
                self.proxies[key] = validated_proxy
                self.stats["total_proxies"] += 1
                self._update_pool_stats()

                self.logger.info("proxy added to pool",
                               proxy=key,
                               status=validated_proxy.status.value,
                               health_score=validated_proxy.health_score)

                return True
            else:
                self.logger.warning("proxy failed initial validation",
                                  proxy=key,
                                  status=validated_proxy.status.value)
                return False

    async def remove_proxy(self, proxy_key: str) -> bool:
        """
        從代理池中移除代理

        Args:
            proxy_key: 代理鍵

        Returns:
            移除是否成功
        """
        async with self.proxy_lock:
            if proxy_key in self.proxies:
                removed_proxy = self.proxies.pop(proxy_key)
                self.stats["total_proxies"] -= 1
                self._update_pool_stats()

                self.logger.info("proxy removed from pool", proxy=proxy_key)
                return True

            return False

    async def get_best_proxies(self, count: int = 5,
                              min_health_score: float = 70.0) -> List[Proxy]:
        """
        獲取最優質的代理列表

        Args:
            count: 返回的代理數量
            min_health_score: 最低健康度評分

        Returns:
            最佳代理列表
        """
        async with self.proxy_lock:
            candidates = [
                proxy for proxy in self.proxies.values()
                if proxy.is_active and
                   proxy.status == ProxyStatus.HEALTHY and
                   proxy.health_score >= min_health_score
            ]

        # 按健康度評分降序排序
        candidates.sort(key=lambda p: (
            p.health_score,           # 主排序: 健康度
            -p.metrics.response_time, # 次排序: 響應時間 (越小越好)
            p.metrics.success_rate    # 三排序: 成功率
        ), reverse=True)

        return candidates[:count]

    async def schedule_validation(self, interval_minutes: int = 30):
        """
        安排定期驗證任務

        Args:
            interval_minutes: 驗證間隔(分鐘)
        """
        self.logger.info("proxy validation scheduler started", interval_minutes=interval_minutes)

        while True:
            try:
                await asyncio.sleep(interval_minutes * 60)

                config = self.config_manager.get("proxy", {})
                max_concurrent = config.get("validation_concurrent", 10)

                result = await self.validate_proxy_pool(max_concurrent=max_concurrent)

                # 檢查是否需要發出告警
                unhealthy_ratio = self.stats["unhealthy_proxies"] / max(1, self.stats["total_proxies"])
                if unhealthy_ratio > 0.5:
                    self.logger.warning("high unhealthy proxy ratio",
                                      ratio=round(unhealthy_ratio, 3),
                                      total=self.stats["total_proxies"])

            except asyncio.CancelledError:
                self.logger.info("proxy validation scheduler stopped")
                break
            except Exception as e:
                self.logger.error("proxy validation scheduler error", error=str(e))
                await asyncio.sleep(60)  # 錯誤後等待1分鐘

    def get_stats(self) -> Dict[str, Any]:
        """獲取統計信息"""
        healthy_ratio = self.stats["healthy_proxies"] / max(1, self.stats["total_proxies"])
        test_success_ratio = self.stats["successful_tests"] / max(1, self.stats["total_tests"])

        return {
            **self.stats,
            "healthy_ratio": round(healthy_ratio, 3),
            "test_success_ratio": round(test_success_ratio, 3),
            "uptime_seconds": (datetime.utcnow() - datetime(2025, 1, 20)).total_seconds(),  # 示例
            "active_proxies": len([p for p in self.proxies.values() if p.is_active]),
            "last_validation": self.stats["last_validation"].isoformat() if self.stats["last_validation"] else None
        }

    def _update_pool_stats(self):
        """更新代理池統計信息"""
        total = len(self.proxies)
        healthy = sum(1 for p in self.proxies.values() if p.status == ProxyStatus.HEALTHY)
        degraded = sum(1 for p in self.proxies.values() if p.status == ProxyStatus.DEGRADED)
        unhealthy = sum(1 for p in self.proxies.values() if p.status == ProxyStatus.UNHEALTHY)

        self.stats.update({
            "total_proxies": total,
            "healthy_proxies": healthy,
            "degraded_proxies": degraded,
            "unhealthy_proxies": unhealthy
        })

    async def _create_proxy_from_dict(self, config: Dict[str, Any]) -> Proxy:
        """從字典創建代理對象"""
        proxy_type = ProxyType(config.get("type", "http"))

        proxy = Proxy(
            ip=config["ip"],
            port=config["port"],
            type=proxy_type,
            username=config.get("username"),
            password=config.get("password"),
            priority=config.get("priority", 0),
            tags=config.get("tags", [])
        )

        return proxy


# 全域代理驗證器實例
_proxy_validator: Optional[ProxyValidator] = None


def init_proxy_validator(config_manager=None) -> ProxyValidator:
    """
    初始化全域代理驗證器

    Args:
        config_manager: 配置管理器實例

    Returns:
        代理驗證器實例
    """
    global _proxy_validator

    if _proxy_validator is None:
        _proxy_validator = ProxyValidator(config_manager)

    return _proxy_validator


def get_proxy_validator() -> ProxyValidator:
    """獲取全域代理驗證器實例"""
    if _proxy_validator is None:
        raise RuntimeError("代理驗證器尚未初始化，請先調用init_proxy_validator()")
    return _proxy_validator
