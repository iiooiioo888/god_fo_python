# CH3 代碼示例 - 3.2 資料源健康監測核心實現

## 健康監測引擎核心實現

### HealthMonitor 主服務類

```python
import logging
import time
import asyncio
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import aiohttp
import dns.resolver
import ssl
from urllib.parse import urlparse

class HealthStatus(Enum):
    """健康狀態枚舉"""
    HEALTHY = "healthy"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

class CheckType(Enum):
    """檢測類型"""
    HTTP_CONNECTION = "http_connection"
    DNS_RESOLUTION = "dns_resolution"
    SSL_CERTIFICATE = "ssl_certificate"
    RESPONSE_TIME = "response_time"
    CONTENT_VALIDATION = "content_validation"
    CUSTOM = "custom"

class DataSourceHealthMonitor:
    """資料源健康監測核心服務"""
    
    def __init__(
        self,
        db: 'Database',
        alert_service: 'AlertService',
        config: Dict
    ):
        self.db = db
        self.alert_service = alert_service
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 監測配置
        self.check_timeout = config.get('check_timeout', 30)
        self.retry_attempts = config.get('retry_attempts', 3)
        self.alert_thresholds = config.get('alert_thresholds', {
            'response_time_ms': 5000,
            'error_rate_percent': 10,
            'availability_percent': 95
        })
    
    async def perform_health_check(
        self,
        datasource_id: str,
        datasource_info: Dict,
        user_id: str
    ) -> Dict:
        """
        執行完整的健康檢測
        
        Args:
            datasource_id: 資料源 ID
            datasource_info: 資料源信息
                {
                    'url': 'https://api.example.com',
                    'type': 'api',
                    'connection_config': {...}
                }
            user_id: 用戶 ID
            
        Returns:
            完整的健康檢測結果
        """
        try:
            check_results = {
                'datasource_id': datasource_id,
                'check_time': datetime.utcnow().isoformat(),
                'checks': {},
                'metrics': {},
                'overall_status': HealthStatus.UNKNOWN.value
            }
            
            # 1. HTTP 連接測試
            http_check = await self._check_http_connection(datasource_info)
            check_results['checks']['http_connection'] = http_check
            
            # 2. DNS 解析驗證
            dns_check = await self._check_dns_resolution(datasource_info)
            check_results['checks']['dns_resolution'] = dns_check
            
            # 3. SSL 證書檢查
            if datasource_info.get('url', '').startswith('https'):
                ssl_check = await self._check_ssl_certificate(datasource_info)
                check_results['checks']['ssl_certificate'] = ssl_check
            
            # 4. 響應時間測量
            response_check = await self._measure_response_time(datasource_info)
            check_results['checks']['response_time'] = response_check
            
            # 5. 內容驗證
            if http_check.get('success'):
                content_check = await self._validate_content(datasource_info, http_check)
                check_results['checks']['content_validation'] = content_check
            
            # 6. 計算指標
            metrics = self._calculate_health_metrics(check_results['checks'])
            check_results['metrics'] = metrics
            
            # 7. 判定總體狀態
            check_results['overall_status'] = self._determine_overall_status(metrics)
            
            # 8. 保存檢測結果
            self._save_health_check(check_results, user_id)
            
            # 9. 觸發告警（如需要）
            await self._trigger_alerts(datasource_id, check_results)
            
            self.logger.info(
                f"Health check completed for {datasource_id}: {check_results['overall_status']}"
            )
            
            return check_results
            
        except Exception as e:
            self.logger.error(f"Health check failed for {datasource_id}: {str(e)}")
            raise
    
    async def _check_http_connection(self, datasource_info: Dict) -> Dict:
        """檢測 HTTP/HTTPS 連接"""
        url = datasource_info.get('url', '')
        
        check_result = {
            'type': CheckType.HTTP_CONNECTION.value,
            'success': False,
            'status_code': None,
            'error_message': None,
            'response_time_ms': 0
        }
        
        try:
            start_time = time.time()
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(self.check_timeout)) as session:
                async with session.head(url, allow_redirects=True) as response:
                    check_result['status_code'] = response.status
                    check_result['success'] = 200 <= response.status < 400
                    check_result['response_time_ms'] = int((time.time() - start_time) * 1000)
                    
                    if not check_result['success']:
                        check_result['error_message'] = f"HTTP {response.status}"
            
        except asyncio.TimeoutError:
            check_result['error_message'] = "Connection timeout"
        except Exception as e:
            check_result['error_message'] = str(e)
        
        return check_result
    
    async def _check_dns_resolution(self, datasource_info: Dict) -> Dict:
        """檢測 DNS 解析"""
        url = datasource_info.get('url', '')
        domain = urlparse(url).netloc.split(':')[0]
        
        check_result = {
            'type': CheckType.DNS_RESOLUTION.value,
            'success': False,
            'domain': domain,
            'resolved_ips': [],
            'error_message': None
        }
        
        try:
            # 使用非同步 DNS 解析
            loop = asyncio.get_event_loop()
            answers = await loop.run_in_executor(
                None,
                lambda: dns.resolver.resolve(domain, 'A')
            )
            
            resolved_ips = [rdata.address for rdata in answers]
            check_result['resolved_ips'] = resolved_ips
            check_result['success'] = len(resolved_ips) > 0
            
        except dns.resolver.NXDOMAIN:
            check_result['error_message'] = f"Domain not found: {domain}"
        except dns.resolver.Timeout:
            check_result['error_message'] = "DNS resolution timeout"
        except Exception as e:
            check_result['error_message'] = str(e)
        
        return check_result
    
    async def _check_ssl_certificate(self, datasource_info: Dict) -> Dict:
        """檢測 SSL 證書有效性"""
        url = datasource_info.get('url', '')
        domain = urlparse(url).netloc.split(':')[0]
        port = urlparse(url).port or 443
        
        check_result = {
            'type': CheckType.SSL_CERTIFICATE.value,
            'success': False,
            'domain': domain,
            'issued_to': None,
            'issuer': None,
            'valid_from': None,
            'valid_until': None,
            'days_remaining': None,
            'error_message': None
        }
        
        try:
            # 建立 SSL 連接
            context = ssl.create_default_context()
            loop = asyncio.get_event_loop()
            
            cert_dict = await loop.run_in_executor(
                None,
                lambda: ssl.create_default_context().check_hostname,
                domain
            )
            
            # 獲取證書信息
            import socket
            conn = socket.create_connection((domain, port), timeout=self.check_timeout)
            context = ssl.create_default_context()
            sock = context.wrap_socket(conn, server_hostname=domain)
            
            der_cert = sock.getpeercert()
            sock.close()
            conn.close()
            
            if der_cert:
                # 解析證書
                from OpenSSL import SSL, crypto
                cert_text = ssl.DER_cert_to_PEM_cert(der_cert['der'])
                x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert_text)
                
                check_result['issued_to'] = dict(x509.get_subject().get_components())
                check_result['issuer'] = dict(x509.get_issuer().get_components())
                
                # 計算有效期
                not_after = datetime.strptime(
                    x509.get_notAfter().decode('utf-8'),
                    '%Y%m%d%H%M%SZ'
                )
                check_result['valid_until'] = not_after.isoformat()
                check_result['days_remaining'] = (not_after - datetime.utcnow()).days
                check_result['success'] = check_result['days_remaining'] > 0
                
        except Exception as e:
            check_result['error_message'] = str(e)
        
        return check_result
    
    async def _measure_response_time(self, datasource_info: Dict) -> Dict:
        """測量響應時間"""
        url = datasource_info.get('url', '')
        
        check_result = {
            'type': CheckType.RESPONSE_TIME.value,
            'response_times_ms': [],
            'avg_response_time_ms': 0,
            'min_response_time_ms': 0,
            'max_response_time_ms': 0
        }
        
        response_times = []
        
        for attempt in range(self.retry_attempts):
            try:
                start_time = time.time()
                
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(self.check_timeout)) as session:
                    async with session.get(url) as response:
                        response_time = int((time.time() - start_time) * 1000)
                        response_times.append(response_time)
                        
            except Exception as e:
                self.logger.warning(f"Response time measurement attempt {attempt + 1} failed: {str(e)}")
        
        if response_times:
            check_result['response_times_ms'] = response_times
            check_result['avg_response_time_ms'] = int(sum(response_times) / len(response_times))
            check_result['min_response_time_ms'] = min(response_times)
            check_result['max_response_time_ms'] = max(response_times)
        
        return check_result
    
    async def _validate_content(
        self,
        datasource_info: Dict,
        http_check: Dict
    ) -> Dict:
        """驗證內容"""
        url = datasource_info.get('url', '')
        
        check_result = {
            'type': CheckType.CONTENT_VALIDATION.value,
            'success': False,
            'content_size_bytes': 0,
            'content_type': None,
            'error_message': None
        }
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(self.check_timeout)) as session:
                async with session.get(url) as response:
                    content = await response.read()
                    
                    check_result['content_size_bytes'] = len(content)
                    check_result['content_type'] = response.headers.get('Content-Type')
                    check_result['success'] = len(content) > 0
                    
        except Exception as e:
            check_result['error_message'] = str(e)
        
        return check_result
    
    def _calculate_health_metrics(self, checks: Dict) -> Dict:
        """計算健康指標"""
        metrics = {
            'availability': 100.0,
            'response_time_ms': 0,
            'error_rate_percent': 0.0,
            'quality_score': 0.0
        }
        
        # 計算可用性
        successful_checks = sum(1 for check in checks.values() if check.get('success', False))
        total_checks = len(checks)
        metrics['availability'] = (successful_checks / total_checks * 100) if total_checks > 0 else 0
        
        # 計算響應時間
        if 'response_time' in checks and checks['response_time'].get('avg_response_time_ms'):
            metrics['response_time_ms'] = checks['response_time']['avg_response_time_ms']
        
        # 計算錯誤率
        metrics['error_rate_percent'] = 100.0 - metrics['availability']
        
        # 計算品質評分 (0-100)
        quality_score = 100.0
        
        # 根據可用性扣分
        if metrics['availability'] < 99:
            quality_score -= (100 - metrics['availability']) * 0.5
        
        # 根據響應時間扣分
        if metrics['response_time_ms'] > 5000:
            quality_score -= min(20, (metrics['response_time_ms'] - 5000) / 1000)
        
        metrics['quality_score'] = max(0, min(100, quality_score))
        
        return metrics
    
    def _determine_overall_status(self, metrics: Dict) -> str:
        """判定總體狀態"""
        if metrics['availability'] >= 99 and metrics['response_time_ms'] < 3000:
            return HealthStatus.HEALTHY.value
        elif metrics['availability'] >= 95 and metrics['response_time_ms'] < 5000:
            return HealthStatus.WARNING.value
        elif metrics['availability'] >= 90:
            return HealthStatus.ERROR.value
        else:
            return HealthStatus.CRITICAL.value
    
    def _save_health_check(self, check_result: Dict, user_id: str):
        """保存檢測結果"""
        sql = """
        INSERT INTO health_check_records (
            datasource_id, check_time, overall_status, metrics, 
            check_details, created_by, created_at
        ) VALUES (
            %(datasource_id)s, %(check_time)s, %(overall_status)s, 
            %(metrics)s, %(check_details)s, %(user_id)s, %(created_at)s
        )
        """
        
        params = {
            'datasource_id': check_result['datasource_id'],
            'check_time': check_result['check_time'],
            'overall_status': check_result['overall_status'],
            'metrics': json.dumps(check_result['metrics']),
            'check_details': json.dumps(check_result['checks']),
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat()
        }
        
        self.db.execute(sql, params)
    
    async def _trigger_alerts(self, datasource_id: str, check_result: Dict):
        """觸發告警"""
        status = check_result['overall_status']
        metrics = check_result['metrics']
        
        if status == HealthStatus.CRITICAL.value:
            await self.alert_service.send_alert({
                'level': 'critical',
                'datasource_id': datasource_id,
                'message': f"Data source is in CRITICAL status",
                'metrics': metrics
            })
        elif status == HealthStatus.ERROR.value:
            if metrics['availability'] < self.alert_thresholds.get('availability_percent', 95):
                await self.alert_service.send_alert({
                    'level': 'error',
                    'datasource_id': datasource_id,
                    'message': f"Data source availability below threshold",
                    'metrics': metrics
                })
```

---

## 健康監測調度器

```python
class HealthCheckScheduler:
    """健康檢測排程管理"""
    
    def __init__(
        self,
        health_monitor: DataSourceHealthMonitor,
        db: 'Database',
        config: Dict
    ):
        self.health_monitor = health_monitor
        self.db = db
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 排程配置
        self.check_intervals = config.get('check_intervals', {
            'critical': 60,      # 每分鐘
            'error': 300,        # 每 5 分鐘
            'warning': 600,      # 每 10 分鐘
            'healthy': 3600      # 每小時
        })
    
    async def schedule_health_checks(self):
        """排程所有健康檢測"""
        while True:
            try:
                # 獲取所有需要檢測的資料源
                datasources = self.db.fetchall(
                    "SELECT * FROM data_sources WHERE status = 'active'"
                )
                
                tasks = []
                for datasource in datasources:
                    # 判斷是否需要執行檢測
                    should_check, interval = self._should_check_now(datasource)
                    
                    if should_check:
                        task = self.health_monitor.perform_health_check(
                            datasource['id'],
                            datasource,
                            'system'
                        )
                        tasks.append(task)
                
                # 並行執行所有檢測
                if tasks:
                    await asyncio.gather(*tasks)
                
                # 等待後再執行下一輪
                await asyncio.sleep(60)  # 每分鐘檢查一次
                
            except Exception as e:
                self.logger.error(f"Scheduling error: {str(e)}")
                await asyncio.sleep(60)
    
    def _should_check_now(self, datasource: Dict) -> Tuple[bool, int]:
        """判斷是否應該檢測"""
        # 獲取上次檢測時間和當前狀態
        last_check_time = datasource.get('last_health_check')
        current_status = datasource.get('health_status', HealthStatus.UNKNOWN.value)
        
        if not last_check_time:
            return True, 0
        
        # 根據狀態決定檢測間隔
        interval = self.check_intervals.get(current_status, 3600)
        
        elapsed = (datetime.utcnow() - datetime.fromisoformat(last_check_time)).total_seconds()
        
        return elapsed >= interval, interval
```

---

## 相關文件引用

- **主文檔**: [3.2 詳細功能清單](../ch3-2-詳細功能清單.md)
- **監測告警**: [代碼示例 - 監測告警](ch3-code-02-alert-system.md)
- **數據庫架構**: [代碼示例 - 數據庫定義](ch3-code-03-database-schema.md)
- **API 示例**: [代碼示例 - API 端點](ch3-code-04-api-examples.md)
