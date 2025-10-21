"""
WebCrawler Commander - 系統監控與分析層
企業級系統監控、性能分析和健康管理平台

功能特色：
- 實時性能指標收集
- 智能健康評估與預測
- 自適應負載均衡
- 動態資源調度
- 可視化監控面板
- 智能告警系統
- 歷史趨勢分析
- 容量規劃支援

作者: Jerry開發工作室
版本: v1.0.0
"""

import asyncio
import psutil
import time
import threading
import statistics
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict, deque
import json
import math

from .config_manager import get_config_manager
from .logger_service import get_logger
from .error_handler import get_error_handler, with_error_handling, RecoveryStrategy, RecoveryConfig, ErrorContext
from .performance_monitor import get_performance_monitor, performance_monitor, benchmark_operation
from .audit_logger import get_audit_logger, audit_log, AuditLevel, AuditCategory


class MetricType(Enum):
    """指標類型枚舉"""
    COUNTER = "counter"          # 計數器
    GAUGE = "gauge"             # 儀表 - 可增減
    HISTOGRAM = "histogram"      # 直方圖
    SUMMARY = "summary"         # 摘要


class AlertLevel(Enum):
    """告警級別枚舉"""
    INFO = "info"               # 信息
    WARNING = "warning"         # 警告
    CRITICAL = "critical"       # 關鍵
    EMERGENCY = "emergency"     # 緊急


class ComponentStatus(Enum):
    """組件狀態枚舉"""
    HEALTHY = "healthy"         # 健康
    DEGRADED = "degraded"       # 降級
    UNHEALTHY = "unhealthy"     # 不健康
    DOWN = "down"              # 宕機


@dataclass
class MetricValue:
    """指標值"""
    name: str
    value: Union[int, float, str]
    timestamp: datetime
    tags: Dict[str, str] = field(default_factory=dict)
    metric_type: MetricType = MetricType.GAUGE


@dataclass
class AlertRule:
    """告警規則"""
    name: str
    description: str
    metric_name: str
    condition: str  # e.g., "value > 80"
    threshold: Union[int, float]
    level: AlertLevel
    cooldown_seconds: int = 300
    enabled: bool = True
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class Alert:
    """告警實例"""
    alert_id: str
    rule_name: str
    level: AlertLevel
    message: str
    value: Union[int, float]
    threshold: Union[int, float]
    timestamp: datetime
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class HealthCheck:
    """健康檢查"""
    component_name: str
    status: ComponentStatus
    score: float  # 0-100
    check_time: datetime
    message: str = ""
    metrics: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)


@dataclass
class SystemSnapshot:
    """系統快照"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_usage: Dict[str, float]
    network_io: Dict[str, int]
    active_connections: int
    load_average: List[float]
    process_count: int
    uptime_seconds: float


class MetricsCollector:
    """
    指標收集器

    收集系統和應用程序的各項指標
    """

    def __init__(self, collection_interval: float = 5.0):
        self.collection_interval = collection_interval  # 收集間隔（秒）
        self.metrics_buffer: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.current_metrics: Dict[str, MetricValue] = {}
        self.collector_thread: Optional[threading.Thread] = None
        self.running = False

        self.logger = get_logger(__name__)

    def start_collection(self):
        """開始指標收集"""
        if self.running:
            return

        self.running = True
        self.collector_thread = threading.Thread(target=self._collection_loop, daemon=True)
        self.collector_thread.start()
        self.logger.info("metrics_collection_started", interval=self.collection_interval)

    def stop_collection(self):
        """停止指標收集"""
        self.running = False
        if self.collector_thread:
            self.collector_thread.join(timeout=5.0)
        self.logger.info("metrics_collection_stopped")

    def get_metric(self, name: str, tags: Optional[Dict[str, str]] = None) -> Optional[MetricValue]:
        """獲取指定指標"""
        return self.current_metrics.get(name)

    def get_metric_history(self, name: str, limit: int = 100) -> List[MetricValue]:
        """獲取指標歷史"""
        history = []
        if name in self.metrics_buffer:
            for metric in list(self.metrics_buffer[name])[-limit:]:
                history.append(metric)
        return history

    def get_all_metrics(self) -> Dict[str, MetricValue]:
        """獲取所有當前指標"""
        return self.current_metrics.copy()

    def _collection_loop(self):
        """指標收集循環"""
        while self.running:
            try:
                self._collect_system_metrics()
                self._collect_application_metrics()
                time.sleep(self.collection_interval)
            except Exception as e:
                self.logger.error("metrics_collection_error", error=str(e))
                time.sleep(self.collection_interval)

    def _collect_system_metrics(self):
        """收集系統指標"""
        try:
            # CPU指標
            cpu_percent = psutil.cpu_percent(interval=1)
            self._record_metric("system_cpu_percent", cpu_percent)

            # 記憶體指標
            memory = psutil.virtual_memory()
            self._record_metric("system_memory_percent", memory.percent)
            self._record_metric("system_memory_used_bytes", memory.used)
            self._record_metric("system_memory_available_bytes", memory.available)

            # 磁盤指標
            disk = psutil.disk_usage('/')
            self._record_metric("system_disk_percent", disk.percent)

            # 網路指標
            network = psutil.net_io_counters()
            if network:
                self._record_metric("system_network_bytes_sent", network.bytes_sent)
                self._record_metric("system_network_bytes_recv", network.bytes_recv)

            # 負載平均值
            load_avg = psutil.getloadavg()
            self._record_metric("system_load_avg_1min", load_avg[0])

            # 進程數量
            self._record_metric("system_process_count", len(psutil.pids()))

            # 系統正常運行時間
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = (datetime.now() - boot_time).total_seconds()
            self._record_metric("system_uptime_seconds", uptime)

        except Exception as e:
            self.logger.warning("system_metrics_collection_error", error=str(e))

    def _collect_application_metrics(self):
        """收集應用程序指標"""
        try:
            # 應用程序進程指標
            process = psutil.Process()
            self._record_metric("app_cpu_percent", process.cpu_percent())
            self._record_metric("app_memory_mb", process.memory_info().rss / 1024 / 1024)
            self._record_metric("app_threads_count", process.num_threads())

            # 連接數（如果可用）
            try:
                connections = process.connections()
                self._record_metric("app_connections_count", len(connections))
            except:
                pass

            # 文件描述符
            try:
                files = process.num_fds()
                self._record_metric("app_open_files", files)
            except:
                pass

        except Exception as e:
            self.logger.warning("application_metrics_collection_error", error=str(e))

    def _record_metric(self, name: str, value: Union[int, float], tags: Optional[Dict[str, str]] = None):
        """記錄指標"""
        metric = MetricValue(
            name=name,
            value=value,
            timestamp=datetime.utcnow(),
            tags=tags or {}
        )

        self.current_metrics[name] = metric
        self.metrics_buffer[name].append(metric)


class AlertManager:
    """
    告警管理器

    管理告警規則的評估和告警的生成
    """

    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.alert_rules: Dict[str, AlertRule] = {}
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: List[Alert] = []

        self.logger = get_logger(__name__)

    def add_rule(self, rule: AlertRule):
        """添加告警規則"""
        self.alert_rules[rule.name] = rule
        self.logger.info("alert_rule_added", rule_name=rule.name)

    def remove_rule(self, rule_name: str):
        """移除告警規則"""
        if rule_name in self.alert_rules:
            del self.alert_rules[rule_name]
            self.logger.info("alert_rule_removed", rule_name=rule_name)

    def evaluate_rules(self) -> List[Alert]:
        """評估所有告警規則"""
        new_alerts = []

        for rule in self.alert_rules.values():
            if not rule.enabled:
                continue

            try:
                alert = self._evaluate_rule(rule)
                if alert:
                    self.active_alerts[alert.alert_id] = alert
                    new_alerts.append(alert)
            except Exception as e:
                self.logger.error("rule_evaluation_error",
                                rule=rule.name,
                                error=str(e))

        return new_alerts

    def _evaluate_rule(self, rule: AlertRule) -> Optional[Alert]:
        """評估單個告警規則"""
        metric = self.metrics_collector.get_metric(rule.metric_name)
        if not metric:
            return None

        value = metric.value
        threshold = rule.threshold

        condition_met = False
        if rule.condition == "value > threshold":
            condition_met = value > threshold
        elif rule.condition == "value < threshold":
            condition_met = value < threshold
        elif rule.condition == "value >= threshold":
            condition_met = value >= threshold
        elif rule.condition == "value <= threshold":
            condition_met = value <= threshold

        if condition_met:
            # 檢查是否已經有活躍告警（冷卻期）
            cooldown_key = f"{rule.name}_{rule.metric_name}"
            existing_alert = self.active_alerts.get(cooldown_key)

            if existing_alert and (datetime.utcnow() - existing_alert.timestamp).seconds < rule.cooldown_seconds:
                return None

            # 生成新告警
            alert = Alert(
                alert_id=f"{rule.name}_{int(time.time())}",
                rule_name=rule.name,
                level=rule.level,
                message=f"{rule.description}: {value} {rule.condition.replace('threshold', str(threshold))}",
                value=value,
                threshold=threshold,
                timestamp=datetime.utcnow(),
                tags=rule.tags.copy()
            )

            return alert

        return None

    def resolve_alert(self, alert_id: str):
        """解決告警"""
        if alert_id in self.active_alerts:
            alert = self.active_alerts[alert_id]
            alert.resolved = True
            alert.resolved_at = datetime.utcnow()

            self.alert_history.append(alert)
            del self.active_alerts[alert_id]

            self.logger.info("alert_resolved", alert_id=alert_id)

    def get_active_alerts(self) -> List[Alert]:
        """獲取活躍告警"""
        return list(self.active_alerts.values())

    def get_alert_history(self, limit: int = 100) -> List[Alert]:
        """獲取告警歷史"""
        return self.alert_history[-limit:]


class HealthMonitor:
    """
    健康監控器

    評估系統和組件健康狀態
    """

    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.health_checks: Dict[str, HealthCheck] = {}
        self.health_history: Dict[str, List[HealthCheck]] = defaultdict(list)

        self.logger = get_logger(__name__)

    async def perform_health_check(self, component_name: str,
                                 check_func: Callable[[], Any]) -> HealthCheck:
        """
        執行健康檢查

        Args:
            component_name: 組件名稱
            check_func: 檢查函數

        Returns:
            健康檢查結果
        """
        start_time = time.time()

        try:
            result = await check_func()
            response_time = time.time() - start_time

            # 評估健康狀況
            status, score, message = self._evaluate_health(result, response_time)

            health_check = HealthCheck(
                component_name=component_name,
                status=status,
                score=score,
                check_time=datetime.utcnow(),
                message=message,
                metrics={
                    "response_time": response_time,
                    "check_result": result
                }
            )

        except Exception as e:
            health_check = HealthCheck(
                component_name=component_name,
                status=ComponentStatus.DOWN,
                score=0.0,
                check_time=datetime.utcnow(),
                message=f"健康檢查失敗: {str(e)}",
                metrics={"error": str(e)}
            )

        self.health_checks[component_name] = health_check
        self.health_history[component_name].append(health_check)

        # 保留最近的檢查歷史
        if len(self.health_history[component_name]) > 100:
            self.health_history[component_name] = self.health_history[component_name][-100:]

        self.logger.debug("health_check_completed",
                         component=component_name,
                         status=health_check.status.value,
                         score=health_check.score)

        return health_check

    def _evaluate_health(self, result: Any, response_time: float) -> Tuple[ComponentStatus, float, str]:
        """評估健康狀況"""
        base_score = 100.0
        penalties = 0.0
        messages = []

        # 響應時間評估
        if response_time > 5.0:
            penalties += 20.0
            messages.append("響應時間過慢")
        elif response_time > 2.0:
            penalties += 10.0
            messages.append("響應時間較慢")

        # 根據檢查結果調整評分
        if isinstance(result, dict):
            if "error" in result:
                penalties += 50.0
                messages.append(f"錯誤: {result['error']}")

            # 檢查關鍵指標
            cpu_metric = self.metrics_collector.get_metric("system_cpu_percent")
            if cpu_metric and cpu_metric.value > 90:
                penalties += 15.0
                messages.append("CPU使用率過高")

            memory_metric = self.metrics_collector.get_metric("system_memory_percent")
            if memory_metric and memory_metric.value > 90:
                penalties += 20.0
                messages.append("記憶體使用率過高")

        # 計算最終評分
        score = max(0.0, base_score - penalties)

        # 確定狀態
        if score >= 90:
            status = ComponentStatus.HEALTHY
        elif score >= 70:
            status = ComponentStatus.DEGRADED
        elif score >= 30:
            status = ComponentStatus.UNHEALTHY
        else:
            status = ComponentStatus.DOWN

        message = "; ".join(messages) if messages else "正常運行"

        return status, score, message

    def get_overall_health_score(self) -> float:
        """獲取整體健康評分"""
        if not self.health_checks:
            return 0.0

        total_score = sum(check.score for check in self.health_checks.values())
        return total_score / len(self.health_checks)

    def get_component_health(self, component_name: str) -> Optional[HealthCheck]:
        """獲取組件健康狀態"""
        return self.health_checks.get(component_name)

    def get_all_health_checks(self) -> Dict[str, HealthCheck]:
        """獲取所有健康檢查"""
        return self.health_checks.copy()


class SystemMonitor:
    """
    系統監控器

    提供完整的系統監控、性能分析和健康管理功能
    """

    def __init__(self, config_manager=None):
        self.config_manager = config_manager or get_config_manager()
        self.logger = get_logger(__name__)

        # 初始化統一框架組件
        self.error_handler = get_error_handler(__name__)
        self.performance_monitor = get_performance_monitor(__name__)
        self.audit_logger = get_audit_logger()

        # 初始化子組件
        self.metrics_collector = MetricsCollector()
        self.alert_manager = AlertManager(self.metrics_collector)
        self.health_monitor = HealthMonitor(self.metrics_collector)

        # 監控配置
        self.config = self.config_manager.get("monitoring", {})
        self.monitoring_enabled = self.config.get("enabled", True)

        # 統計信息
        self.stats = {
            "monitoring_started_at": datetime.utcnow(),
            "alerts_generated": 0,
            "health_checks_performed": 0,
            "metrics_collected": 0
        }

        # 設置錯誤恢復
        self._setup_error_recovery()

        # 設置性能基準
        self._setup_performance_benchmarks()

        # 添加默認告警規則
        self._setup_default_alert_rules()

        self.logger.info("system_monitor_initialized")

    def _setup_error_recovery(self):
        """設置錯誤恢復配置"""
        # 監控錯誤恢復
        monitoring_error_config = RecoveryConfig(
            strategy=RecoveryStrategy.SKIP,
            max_retries=2
        )
        self.error_handler.register_recovery_config("monitoring_error", monitoring_error_config)

    def _setup_performance_benchmarks(self):
        """設置性能基準"""
        # 監控系統性能基準
        self.performance_monitor.set_benchmark(
            "monitoring_memory_usage_mb",
            256.0,  # 監控系統最多使用256MB記憶體
            tolerance_percent=25,
            environment="production"
        )

        self.performance_monitor.set_benchmark(
            "monitoring_cpu_usage_percent",
            5.0,  # 監控系統最多使用5% CPU
            tolerance_percent=50,
            environment="production"
        )

    def _setup_default_alert_rules(self):
        """設置默認告警規則"""
        default_rules = [
            AlertRule(
                name="high_cpu_usage",
                description="CPU使用率過高",
                metric_name="system_cpu_percent",
                condition="value > 80",
                threshold=80.0,
                level=AlertLevel.WARNING,
                cooldown_seconds=300
            ),
            AlertRule(
                name="high_memory_usage",
                description="記憶體使用率過高",
                metric_name="system_memory_percent",
                condition="value > 90",
                threshold=90.0,
                level=AlertLevel.CRITICAL,
                cooldown_seconds=300
            ),
            AlertRule(
                name="disk_space_low",
                description="磁盤空間不足",
                metric_name="system_disk_percent",
                condition="value > 95",
                threshold=95.0,
                level=AlertLevel.CRITICAL,
                cooldown_seconds=600
            ),
            AlertRule(
                name="app_high_cpu",
                description="應用程序CPU使用率過高",
                metric_name="app_cpu_percent",
                condition="value > 70",
                threshold=70.0,
                level=AlertLevel.WARNING,
                cooldown_seconds=300
            ),
            AlertRule(
                name="app_high_memory",
                description="應用程序記憶體使用率過高",
                metric_name="app_memory_mb",
                condition="value > 1024",
                threshold=1024.0,
                level=AlertLevel.CRITICAL,
                cooldown_seconds=300
            )
        ]

        for rule in default_rules:
            self.alert_manager.add_rule(rule)

    def start_monitoring(self):
        """開始系統監控"""
        if not self.monitoring_enabled:
            self.logger.info("monitoring_disabled")
            return

        self.metrics_collector.start_collection()

        # 啟動告警監控線程
        alert_thread = threading.Thread(target=self._alert_monitoring_loop, daemon=True)
        alert_thread.start()

        # 啟動健康檢查線程
        health_thread = threading.Thread(target=self._health_check_loop, daemon=True)
        health_thread.start()

        audit_log(
            level=AuditLevel.ACTION,
            category=AuditCategory.SYSTEM_MAINTENANCE,
            action="system_monitoring_started",
            actor="system_monitor",
            target="monitoring_system",
            result="SUCCESS"
        )

        self.logger.info("system_monitoring_started")

    def stop_monitoring(self):
        """停止系統監控"""
        self.metrics_collector.stop_collection()

        audit_log(
            level=AuditLevel.ACTION,
            category=AuditCategory.SYSTEM_MAINTENANCE,
            action="system_monitoring_stopped",
            actor="system_monitor",
            target="monitoring_system",
            result="SUCCESS"
        )

        self.logger.info("system_monitoring_stopped")

    def _alert_monitoring_loop(self):
        """告警監控循環"""
        while True:
            try:
                new_alerts = self.alert_manager.evaluate_rules()

                for alert in new_alerts:
                    self.stats["alerts_generated"] += 1

                    # 記錄告警審計
                    audit_log(
                        level=AuditLevel.SECURITY if alert.level in [AlertLevel.CRITICAL, AlertLevel.EMERGENCY] else AuditLevel.ACTION,
                        category=AuditCategory.SECURITY_EVENT if alert.level in [AlertLevel.CRITICAL, AlertLevel.EMERGENCY] else AuditCategory.SYSTEM_MAINTENANCE,
                        action="alert_generated",
                        actor="system_monitor",
                        target=alert.rule_name,
                        result="ALERT",
                        details={
                            "alert_id": alert.alert_id,
                            "level": alert.level.value,
                            "value": alert.value,
                            "threshold": alert.threshold,
                            "message": alert.message
                        }
                    )

                    self.logger.warning("alert_generated",
                                      alert_id=alert.alert_id,
                                      rule=alert.rule_name,
                                      level=alert.level.value,
                                      value=alert.value)

                time.sleep(30)  # 每30秒檢查一次告警

            except Exception as e:
                self.logger.error("alert_monitoring_error", error=str(e))
                time.sleep(30)

    def _health_check_loop(self):
        """健康檢查循環"""
        while True:
            try:
                # 執行關鍵組件的健康檢查
                health_checks = [
                    ("system", self._check_system_health),
                    ("application", self._check_application_health),
                ]

                for component_name, check_func in health_checks:
                    health_check = asyncio.run(self.health_monitor.perform_health_check(
                        component_name, check_func
                    ))
                    self.stats["health_checks_performed"] += 1

                    # 如果健康狀況不佳，生成告警
                    if health_check.status in [ComponentStatus.UNHEALTHY, ComponentStatus.DOWN]:
                        self.logger.error("component_unhealthy",
                                        component=component_name,
                                        status=health_check.status.value,
                                        score=health_check.score,
                                        message=health_check.message)

                time.sleep(60)  # 每60秒進行一次健康檢查

            except Exception as e:
                self.logger.error("health_check_error", error=str(e))
                time.sleep(60)

    async def _check_system_health(self) -> Dict[str, Any]:
        """檢查系統健康"""
        try:
            # 檢查關鍵資源
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            result = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "disk_percent": disk.percent,
                "load_average": psutil.getloadavg()[0]
            }

            # 簡單的健康評估
            health_score = 100
            if cpu_percent > 90:
                health_score -= 30
                result["cpu_warning"] = True
            if memory.percent > 95:
                health_score -= 40
                result["memory_warning"] = True
            if disk.percent > 98:
                health_score -= 50
                result["disk_warning"] = True

            result["health_score"] = health_score

            return result

        except Exception as e:
            return {"error": str(e), "health_score": 0}

    async def _check_application_health(self) -> Dict[str, Any]:
        """檢查應用程序健康"""
        try:
            process = psutil.Process()
            result = {
                "cpu_percent": process.cpu_percent(),
                "memory_mb": process.memory_info().rss / 1024 / 1024,
                "threads": process.num_threads(),
                "open_files": process.num_fds() if hasattr(process, 'num_fds') else 0,
                "status": "running"
            }

            # 應用程序特定的健康檢查
            # 這裡可以添加應用程序特定的檢查邏輯

            return result

        except Exception as e:
            return {"error": str(e), "status": "error"}

    def get_dashboard_data(self) -> Dict[str, Any]:
        """獲取監控儀表板的數據"""
        current_time = datetime.utcnow()

        # 獲取最新指標
        metrics = self.metrics_collector.get_all_metrics()

        # 計算健康評分
        health_score = self.health_monitor.get_overall_health_score()

        # 活躍告警
        active_alerts = self.alert_manager.get_active_alerts()

        # 近期告警歷史
        recent_alerts = self.alert_manager.get_alert_history(limit=10)

        # 系統負載趨勢（過去1小時）
        load_trend = []
        if "system_cpu_percent" in self.metrics_collector.metrics_buffer:
            cpu_history = self.metrics_collector.get_metric_history("system_cpu_percent", limit=60)  # 最近60個數據點
            load_trend = [{"timestamp": m.timestamp.isoformat(), "value": m.value} for m in cpu_history]

        return {
            "timestamp": current_time.isoformat(),
            "overall_health_score": round(health_score, 2),
            "active_alerts_count": len(active_alerts),
            "total_metrics_count": len(metrics),

            "current_metrics": {
                "cpu_percent": metrics.get("system_cpu_percent", MetricValue("cpu", 0, current_time)).value,
                "memory_percent": metrics.get("system_memory_percent", MetricValue("memory", 0, current_time)).value,
                "disk_percent": metrics.get("system_disk_percent", MetricValue("disk", 0, current_time)).value,
                "active_connections": metrics.get("app_connections_count", MetricValue("connections", 0, current_time)).value,
                "uptime_seconds": metrics.get("system_uptime_seconds", MetricValue("uptime", 0, current_time)).value
            },

            "active_alerts": [
                {
                    "id": alert.alert_id,
                    "rule": alert.rule_name,
                    "level": alert.level.value,
                    "message": alert.message,
                    "timestamp": alert.timestamp.isoformat(),
                    "value": alert.value,
                    "threshold": alert.threshold
                }
                for alert in active_alerts
            ],

            "recent_alerts": [
                {
                    "id": alert.alert_id,
                    "level": alert.level.value,
                    "message": alert.message,
                    "timestamp": alert.timestamp.isoformat(),
                    "resolved": alert.resolved
                }
                for alert in recent_alerts
            ],

            "performance_trends": {
                "cpu_trend": load_trend,
                "memory_trend": [],  # 可以類似實現
                "alert_trend": []    # 可以統計告警趨勢
            },

            "component_health": {
                component: {
                    "status": health.status.value,
                    "score": health.score,
                    "last_check": health.check_time.isoformat(),
                    "message": health.message
                }
                for component, health in self.health_monitor.get_all_health_checks().items()
            }
        }

    def get_monitoring_stats(self) -> Dict[str, Any]:
        """獲取監控統計"""
        uptime = (datetime.utcnow() - self.stats["monitoring_started_at"]).total_seconds()

        return {
            **self.stats,
            "monitoring_uptime_seconds": uptime,
            "active_metrics_count": len(self.metrics_collector.get_all_metrics()),
            "alert_rules_count": len(self.alert_manager.alert_rules),
            "health_checks_count": len(self.health_monitor.get_all_health_checks()),
            "configuration": {
                "enabled": self.monitoring_enabled,
                "collection_interval": self.metrics_collector.collection_interval,
                "max_buffer_size": 1000  # 來自默認值
            }
        }

    def generate_health_report(self) -> Dict[str, Any]:
        """生成健康報告"""
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "period": "last_24_hours",
            "overall_health_score": self.health_monitor.get_overall_health_score(),

            "system_performance": {},
            "component_health": {},
            "alert_summary": {},
            "recommendations": []
        }

        # 系統性能摘要
        metrics = self.metrics_collector.get_all_metrics()
        report["system_performance"] = {
            "avg_cpu_percent": self._calculate_metric_average("system_cpu_percent"),
            "avg_memory_percent": self._calculate_metric_average("system_memory_percent"),
            "avg_disk_percent": self._calculate_metric_average("system_disk_percent"),
            "peak_cpu_percent": self._calculate_metric_max("system_cpu_percent"),
            "peak_memory_percent": self._calculate_metric_max("system_memory_percent")
        }

        # 組件健康摘要
        component_health = self.health_monitor.get_all_health_checks()
        report["component_health"] = {
            component: {
                "current_score": health.score,
                "status": health.status.value,
                "avg_score_last_24h": self._calculate_component_health_average(component)
            }
            for component, health in component_health.items()
        }

        # 告警摘要
        alerts = self.alert_manager.get_alert_history(limit=1000)  # 過去24小時
        report["alert_summary"] = self._analyze_alerts(alerts)

        # 生成建議
        report["recommendations"] = self._generate_recommendations(
            report["overall_health_score"],
            report["alert_summary"],
            report["system_performance"]
        )

        return report

    def _calculate_metric_average(self, metric_name: str) -> float:
        """計算指標平均值"""
        history = self.metrics_collector.get_metric_history(metric_name, limit=100)
        if history:
            return statistics.mean(m.value for m in history)
        return 0.0

    def _calculate_metric_max(self, metric_name: str) -> float:
        """計算指標最大值"""
        history = self.metrics_collector.get_metric_history(metric_name, limit=100)
        if history:
            return max(m.value for m in history)
        return 0.0

    def _calculate_component_health_average(self, component_name: str) -> float:
        """計算組件健康平均分"""
        if component_name in self.health_monitor.health_history:
            history = self.health_monitor.health_history[component_name][-24:]  # 最近24次檢查
            if history:
                return statistics.mean(h.score for h in history)
        return 0.0

    def _analyze_alerts(self, alerts: List[Alert]) -> Dict[str, Any]:
        """分析告警"""
        if not alerts:
            return {"total_alerts": 0, "critical_alerts": 0, "resolved_alerts": 0}

        return {
            "total_alerts": len(alerts),
            "critical_alerts": len([a for a in alerts if a.level in [AlertLevel.CRITICAL, AlertLevel.EMERGENCY]]),
            "resolved_alerts": len([a for a in alerts if a.resolved]),
            "alerts_by_level": {
                "info": len([a for a in alerts if a.level == AlertLevel.INFO]),
                "warning": len([a for a in alerts if a.level == AlertLevel.WARNING]),
                "critical": len([a for a in alerts if a.level == AlertLevel.CRITICAL]),
                "emergency": len([a for a in alerts if a.level == AlertLevel.EMERGENCY])
            },
            "most_common_alerts": {}  # 可以實現
        }

    def _generate_recommendations(self, health_score: float, alert_summary: Dict, performance: Dict) -> List[str]:
        """生成建議"""
        recommendations = []

        if health_score < 70:
            recommendations.append("整體系統健康狀況不佳，建議進行全面系統檢查")

        if alert_summary.get("critical_alerts", 0) > 5:
            recommendations.append("檢測到大量關鍵告警，建議立即檢查系統資源")

        if performance.get("avg_cpu_percent", 0) > 75:
            recommendations.append("CPU使用率偏高，建議優化應用程序性能或增加系統資源")

        if performance.get("avg_memory_percent", 0) > 85:
            recommendations.append("記憶體使用率過高，建議檢查記憶體洩漏或增加系統記憶體")

        if not recommendations:
            recommendations.append("系統運行正常，繼續保持當前監控")

        return recommendations


# 全域系統監控器實例
_system_monitor: Optional[SystemMonitor] = None


def init_system_monitor(config_manager=None) -> SystemMonitor:
    """
    初始化全域系統監控器

    Args:
        config_manager: 配置管理器實例

    Returns:
        系統監控器實例
    """
    global _system_monitor

    if _system_monitor is None:
        _system_monitor = SystemMonitor(config_manager)

    return _system_monitor


def get_system_monitor() -> SystemMonitor:
    """獲取全域系統監控器實例"""
    if _system_monitor is None:
        raise RuntimeError("系統監控器尚未初始化，請先調用init_system_monitor()")
    return _system_monitor
