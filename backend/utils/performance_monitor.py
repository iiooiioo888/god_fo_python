"""
WebCrawler Commander - 性能監控指標系統
提供企業級性能監控和優化基準

功能特色：
- 多維度性能指標收集
- 實時性能健康度評估
- 性能基準對比分析
- 資源使用趨勢預測
- 瓶頸自動識別與建議
"""

import os
import psutil
import time
import threading
import asyncio
from typing import Dict, List, Optional, Any, Union, Callable, Tuple
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from collections import defaultdict, deque
import statistics
import json

from .logger_service import get_logger


class MetricType(Enum):
    """指標類型枚舉"""
    COUNTER = "COUNTER"          # 累計計數器
    GAUGE = "GAUGE"             # 瞬時值
    HISTOGRAM = "HISTOGRAM"      # 直方圖分佈
    TIMER = "TIMER"             # 時間計時器


class MetricScope(Enum):
    """指標範圍枚舉"""
    SYSTEM = "SYSTEM"           # 系統級指標
    COMPONENT = "COMPONENT"      # 組件級指標
    OPERATION = "OPERATION"      # 操作級指標
    REQUEST = "REQUEST"          # 請求級指標


@dataclass
class MetricThreshold:
    """指標閾值配置"""
    warning_threshold: Union[int, float]  # 警告閾值
    critical_threshold: Union[int, float]  # 嚴重閾值
    unit: str = ""              # 單位
    description: str = ""       # 描述
    direction: str = "higher"   # higher/lower 表示高值還是低值有風險


@dataclass
class PerformanceBenchmark:
    """性能基準"""
    metric_name: str
    expected_value: Union[int, float]
    tolerance_percent: float = 10.0  # 容忍度百分比
    benchmark_date: datetime = field(default_factory=datetime.utcnow)
    environment: str = "production"  # 基準環境


@dataclass
class MetricValue:
    """指標值"""
    name: str
    value: Union[int, float]
    timestamp: datetime
    type: MetricType
    scope: MetricScope
    labels: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceHealthScore:
    """性能健康度評分"""
    overall_score: float  # 整體評分 (0-100)
    component_scores: Dict[str, float] = field(default_factory=dict)  # 各組件評分
    bottleneck_identifiers: List[str] = field(default_factory=list)  # 瓶頸識別
    optimization_suggestions: List[str] = field(default_factory=list)  # 優化建議
    risk_indicators: Dict[str, str] = field(default_factory=dict)  # 風險指標
    trend_analysis: Dict[str, str] = field(default_factory=dict)  # 趨勢分析


class PerformanceMonitor:
    """
    性能監控器

    提供全面的性能監控功能：
    - 實時指標收集與存儲
    - 性能基準建立與對比
    - 健康度評估與瓶頸識別
    - 自動優化建議生成
    """

    def __init__(self, component_name: str):
        self.component_name = component_name
        self.logger = get_logger(f"performance_monitor.{component_name}")

        # 指標存儲
        self.metrics_storage: Dict[str, List[MetricValue]] = defaultdict(list)
        self.max_metrics_per_type = 1000  # 每個指標類型最大存儲數量

        # 基準配置
        self.benchmarks: Dict[str, PerformanceBenchmark] = {}

        # 閾值配置
        self.thresholds: Dict[str, MetricThreshold] = self._load_default_thresholds()

        # 健康評估
        self.health_check_interval = 30  # 健康檢查間隔（秒）
        self.last_health_check = datetime.utcnow()

        # 系統資源監控
        self.system_monitoring_enabled = True
        self.resource_stats: Dict[str, deque] = {
            "cpu_percent": deque(maxlen=100),
            "memory_percent": deque(maxlen=100),
            "disk_usage": deque(maxlen=100),
            "network_io": deque(maxlen=100)
        }

        # 啟動背景監控任務
        self._start_background_monitoring()

    def _load_default_thresholds(self) -> Dict[str, MetricThreshold]:
        """載入默認閾值配置"""
        return {
            "cpu_usage_percent": MetricThreshold(
                warning_threshold=70.0,
                critical_threshold=85.0,
                unit="%",
                description="CPU使用率",
                direction="higher"
            ),
            "memory_usage_percent": MetricThreshold(
                warning_threshold=80.0,
                critical_threshold=90.0,
                unit="%",
                description="記憶體使用率",
                direction="higher"
            ),
            "response_time_ms": MetricThreshold(
                warning_threshold=500.0,
                critical_threshold=2000.0,
                unit="ms",
                description="響應時間",
                direction="higher"
            ),
            "error_rate_percent": MetricThreshold(
                warning_threshold=5.0,
                critical_threshold=15.0,
                unit="%",
                description="錯誤率",
                direction="higher"
            ),
            "throughput_per_second": MetricThreshold(
                warning_threshold=10.0,
                critical_threshold=5.0,
                unit="req/s",
                description="吞吐量",
                direction="lower"
            )
        }

    def _start_background_monitoring(self):
        """啟動背景監控任務"""
        # 系統資源監控線程
        if self.system_monitoring_enabled:
            monitor_thread = threading.Thread(
                target=self._system_monitoring_loop,
                daemon=True,
                name=f"perf_monitor_{self.component_name}"
            )
            monitor_thread.start()

    def _system_monitoring_loop(self):
        """系統資源監控循環"""
        while True:
            try:
                # CPU使用率
                cpu_percent = psutil.cpu_percent(interval=1)
                self.record_metric("cpu_usage_percent", cpu_percent,
                                 MetricType.GAUGE, MetricScope.SYSTEM)

                # 記憶體使用率
                memory = psutil.virtual_memory()
                self.record_metric("memory_usage_percent", memory.percent,
                                 MetricType.GAUGE, MetricScope.SYSTEM)

                # 磁盤使用率
                disk = psutil.disk_usage('/')
                self.record_metric("disk_usage_percent", disk.percent,
                                 MetricType.GAUGE, MetricScope.SYSTEM)

                # 網路I/O
                network = psutil.net_io_counters()
                if network:
                    total_io = network.bytes_sent + network.bytes_recv
                    self.record_metric("network_io_total", total_io,
                                     MetricType.COUNTER, MetricScope.SYSTEM)

            except Exception as e:
                self.logger.warning("system_monitoring_error", error=str(e))

            time.sleep(self.health_check_interval)

    def record_metric(self, name: str, value: Union[int, float],
                     metric_type: MetricType = MetricType.GAUGE,
                     scope: MetricScope = MetricScope.COMPONENT,
                     labels: Optional[Dict[str, str]] = None) -> MetricValue:
        """
        記錄指標值

        Args:
            name: 指標名稱
            value: 指標值
            metric_type: 指標類型
            scope: 指標範圍
            labels: 標籤

        Returns:
            記錄的指標值對象
        """
        labels = labels or {}

        metric_value = MetricValue(
            name=name,
            value=value,
            timestamp=datetime.utcnow(),
            type=metric_type,
            scope=scope,
            labels=labels.copy()
        )

        # 存儲指標
        self.metrics_storage[name].append(metric_value)

        # 限制存儲大小
        if len(self.metrics_storage[name]) > self.max_metrics_per_type:
            self.metrics_storage[name] = self.metrics_storage[name][-self.max_metrics_per_type:]

        # 檢查閾值並告警
        self._check_thresholds(metric_value)

        return metric_value

    def _check_thresholds(self, metric_value: MetricValue):
        """檢查指標閾值並發出告警"""
        if metric_value.name in self.thresholds:
            threshold = self.thresholds[metric_value.name]

            alert_level = None
            if threshold.direction == "higher":
                if metric_value.value >= threshold.critical_threshold:
                    alert_level = "critical"
                elif metric_value.value >= threshold.warning_threshold:
                    alert_level = "warning"
            elif threshold.direction == "lower":
                if metric_value.value <= threshold.critical_threshold:
                    alert_level = "critical"
                elif metric_value.value <= threshold.warning_threshold:
                    alert_level = "warning"

            if alert_level:
                self.logger.warning("performance_threshold_breached",
                                  metric_name=metric_value.name,
                                  value=metric_value.value,
                                  threshold=threshold.critical_threshold if alert_level == "critical"
                                          else threshold.warning_threshold,
                                  alert_level=alert_level,
                                  unit=threshold.unit)

    def set_benchmark(self, metric_name: str, expected_value: Union[int, float],
                     tolerance_percent: float = 10.0, environment: str = "production"):
        """設置性能基準"""
        benchmark = PerformanceBenchmark(
            metric_name=metric_name,
            expected_value=expected_value,
            tolerance_percent=tolerance_percent,
            environment=environment
        )

        self.benchmarks[metric_name] = benchmark
        self.logger.info("performance_benchmark_set",
                        metric_name=metric_name,
                        expected_value=expected_value,
                        tolerance_percent=tolerance_percent)

    def timer(self, operation_name: str, labels: Optional[Dict[str, str]] = None):
        """計時器裝飾器"""
        def decorator(func: Callable):
            def wrapper(*args, **kwargs):
                start_time = time.perf_counter()

                try:
                    result = func(*args, **kwargs)

                    # 記錄執行時間
                    end_time = time.perf_counter()
                    duration_ms = (end_time - start_time) * 1000

                    self.record_metric(
                        f"operation_duration_{operation_name}",
                        duration_ms,
                        MetricType.TIMER,
                        MetricScope.OPERATION,
                        labels
                    )

                    return result

                except Exception as e:
                    # 即使出錯也要記錄時間
                    end_time = time.perf_counter()
                    duration_ms = (end_time - start_time) * 1000

                    self.record_metric(
                        f"operation_duration_{operation_name}",
                        duration_ms,
                        MetricType.TIMER,
                        MetricScope.OPERATION,
                        {**(labels or {}), "status": "error"}
                    )

                    raise e

            return wrapper
        return decorator

    def async_timer(self, operation_name: str, labels: Optional[Dict[str, str]] = None):
        """異步計時器裝飾器"""
        def decorator(func: Callable):
            async def wrapper(*args, **kwargs):
                start_time = time.perf_counter()

                try:
                    result = await func(*args, **kwargs)

                    # 記錄執行時間
                    end_time = time.perf_counter()
                    duration_ms = (end_time - start_time) * 1000

                    self.record_metric(
                        f"async_operation_duration_{operation_name}",
                        duration_ms,
                        MetricType.TIMER,
                        MetricScope.OPERATION,
                        labels
                    )

                    return result

                except Exception as e:
                    # 即使出錯也要記錄時間
                    end_time = time.perf_counter()
                    duration_ms = (end_time - start_time) * 1000

                    self.record_metric(
                        f"async_operation_duration_{operation_name}",
                        duration_ms,
                        MetricType.TIMER,
                        MetricScope.OPERATION,
                        {**(labels or {}), "status": "error"}
                    )

                    raise e

            return wrapper
        return decorator

    def get_performance_health_score(self) -> PerformanceHealthScore:
        """獲取當前性能健康度評分"""
        current_time = datetime.utcnow()

        # 如果距離上次檢查不夠久，直接返回快取的結果
        if (current_time - self.last_health_check).total_seconds() < self.health_check_interval:
            return self._cached_health_score

        self.last_health_check = current_time

        # 計算各組件的評分
        component_scores = {}
        bottleneck_identifiers = []
        risk_indicators = {}
        trend_analysis = {}

        # 分析系統資源
        component_scores["system"] = self._calculate_system_health_score()

        # 分析組件性能
        component_scores["application"] = self._calculate_application_health_score()

        # 識別瓶頸
        bottleneck_identifiers = self._identify_bottlenecks()

        # 生成風險指標
        risk_indicators = self._generate_risk_indicators()

        # 趨勢分析
        trend_analysis = self._analyze_performance_trends()

        # 優化建議
        optimization_suggestions = self._generate_optimization_suggestions(
            component_scores, bottleneck_identifiers, risk_indicators
        )

        # 計算整體評分
        overall_score = sum(component_scores.values()) / len(component_scores)

        health_score = PerformanceHealthScore(
            overall_score=overall_score,
            component_scores=component_scores,
            bottleneck_identifiers=bottleneck_identifiers,
            optimization_suggestions=optimization_suggestions,
            risk_indicators=risk_indicators,
            trend_analysis=trend_analysis
        )

        # 快取結果
        self._cached_health_score = health_score

        return health_score

    def _calculate_system_health_score(self) -> float:
        """計算系統健康度評分"""
        score = 100.0

        # CPU使用率評分
        cpu_metrics = self.get_metrics("cpu_usage_percent", hours=1)
        if cpu_metrics:
            avg_cpu = statistics.mean(m.value for m in cpu_metrics)
            if avg_cpu > 80:
                score -= 20
            elif avg_cpu > 60:
                score -= 10

        # 記憶體使用率評分
        memory_metrics = self.get_metrics("memory_usage_percent", hours=1)
        if memory_metrics:
            avg_memory = statistics.mean(m.value for m in memory_metrics)
            if avg_memory > 85:
                score -= 25
            elif avg_memory > 70:
                score -= 15

        return max(0.0, score)

    def _calculate_application_health_score(self) -> float:
        """計算應用健康度評分"""
        score = 100.0

        # 響應時間評分
        response_metrics = [m for metrics in self.metrics_storage.values()
                           for m in metrics if "response_time" in m.name]
        if response_metrics:
            avg_response = statistics.mean(m.value for m in response_metrics)
            if avg_response > 1000:  # 1秒
                score -= 20
            elif avg_response > 500:  # 0.5秒
                score -= 10

        # 錯誤率評分
        error_metrics = [m for metrics in self.metrics_storage.values()
                        for m in metrics if "error_rate" in m.name]
        if error_metrics:
            avg_error_rate = statistics.mean(m.value for m in error_metrics)
            score -= avg_error_rate * 2  # 錯誤率直接扣分

        return max(0.0, score)

    def _identify_bottlenecks(self) -> List[str]:
        """識別性能瓶頸"""
        bottlenecks = []

        # 高CPU使用率
        cpu_metrics = self.get_metrics("cpu_usage_percent", hours=1)
        if cpu_metrics and statistics.mean(m.value for m in cpu_metrics) > 80:
            bottlenecks.append("高CPU使用率 - 考慮增加CPU資源或優化算法")

        # 記憶體不足
        memory_metrics = self.get_metrics("memory_usage_percent", hours=1)
        if memory_metrics and statistics.mean(m.value for m in memory_metrics) > 85:
            bottlenecks.append("記憶體不足 - 考慮增加RAM或優化記憶體使用")

        # 慢響應時間
        slow_responses = [m for metrics in self.metrics_storage.values()
                         for m in metrics if m.value > 2000]  # 超過2秒
        if slow_responses:
            bottlenecks.append(f"發現{slow_responses[-1].name}響應過慢")

        # 錯誤率過高
        high_error_rates = [m for metrics in self.metrics_storage.values()
                           for m in metrics if "error_rate" in m.name and m.value > 10]
        if high_error_rates:
            bottlenecks.append(f"{high_error_rates[-1].name}錯誤率超過10%")

        return bottlenecks

    def _generate_risk_indicators(self) -> Dict[str, str]:
        """生成風險指標"""
        risks = {}

        # 檢查趨勢風險
        trends = self._analyze_performance_trends()

        for metric_name, trend in trends.items():
            if "deteriorating" in trend.lower():
                risks[metric_name] = f"性能指標{metric_name}出現惡化趨勢"
            elif "improving" in trend.lower():
                risks[metric_name] = f"性能指標{metric_name}呈現改善趨勢（正面）"

        return risks

    def _analyze_performance_trends(self) -> Dict[str, str]:
        """分析性能趨勢"""
        trends = {}

        for metric_name, metrics in self.metrics_storage.items():
            if len(metrics) < 10:  # 數據點太少無法分析
                continue

            # 按時間排序
            sorted_metrics = sorted(metrics, key=lambda m: m.timestamp)

            # 分成兩半比較
            midpoint = len(sorted_metrics) // 2
            first_half = sorted_metrics[:midpoint]
            second_half = sorted_metrics[midpoint:]

            first_avg = statistics.mean(m.value for m in first_half)
            second_avg = statistics.mean(m.value for m in second_half)

            if second_avg > first_avg * 1.1:  # 上升10%以上
                trends[metric_name] = "deteriorating"
            elif second_avg < first_avg * 0.9:  # 下降10%以上
                trends[metric_name] = "improving"
            else:
                trends[metric_name] = "stable"

        return trends

    def _generate_optimization_suggestions(self, component_scores: Dict[str, float],
                                         bottlenecks: List[str],
                                         risks: Dict[str, str]) -> List[str]:
        """生成優化建議"""
        suggestions = []

        # 基於瓶頸的建議
        if any("CPU" in bottleneck for bottleneck in bottlenecks):
            suggestions.append("優化CPU密集型操作，考慮使用多進程或異步處理")

        if any("記憶體" in bottleneck for bottleneck in bottlenecks):
            suggestions.append("優化記憶體使用，避免大型數據結構長時間駐留記憶體")

        if any("響應" in bottleneck for bottleneck in bottlenecks):
            suggestions.append("優化I/O操作，考慮使用連接池和快取")

        # 基於評分的建議
        for component, score in component_scores.items():
            if score < 70:
                suggestions.append(f"{component}組件性能不佳，需要重點優化")
            elif score < 85:
                suggestions.append(f"{component}組件性能一般，可進一步優化")

        # 通用建議
        if not suggestions:
            suggestions.append("系統性能表現良好，繼續監控關鍵指標")
            suggestions.append("考慮實施定期性能基準測試")

        return suggestions

    def get_metrics(self, name: Optional[str] = None, hours: int = 24,
                   scope: Optional[MetricScope] = None) -> List[MetricValue]:
        """獲取指標數據"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        if name:
            metrics = [m for m in self.metrics_storage.get(name, [])
                      if m.timestamp >= cutoff_time]
            if scope:
                metrics = [m for m in metrics if m.scope == scope]
            return metrics
        else:
            all_metrics = []
            for metrics_list in self.metrics_storage.values():
                filtered = [m for m in metrics_list if m.timestamp >= cutoff_time]
                if scope:
                    filtered = [m for m in filtered if m.scope == scope]
                all_metrics.extend(filtered)
            return sorted(all_metrics, key=lambda m: m.timestamp)

    def export_metrics(self, format: str = "json") -> str:
        """導出指標數據"""
        if format == "json":
            export_data = {}
            for name, metrics in self.metrics_storage.items():
                export_data[name] = [m.__dict__ for m in metrics]
            return json.dumps(export_data, default=str, indent=2)
        else:
            return "Unsupported format"

    def clear_old_metrics(self, days_to_keep: int = 30):
        """清理舊指標數據"""
        cutoff_time = datetime.utcnow() - timedelta(days=days_to_keep)

        for name, metrics in self.metrics_storage.items():
            self.metrics_storage[name] = [
                m for m in metrics if m.timestamp >= cutoff_time
            ]

        self.logger.info("old_metrics_cleared",
                        days_to_keep=days_to_keep,
                        retained_metrics=sum(len(metrics) for metrics in self.metrics_storage.values()))

    def compare_to_benchmarks(self) -> Dict[str, Dict[str, Any]]:
        """與基準進行對比"""
        results = {}

        for metric_name, benchmark in self.benchmarks.items():
            current_metrics = self.get_metrics(metric_name, hours=1) if benchmark.environment == "production" else self.get_metrics(metric_name, hours=24)

            if not current_metrics:
                results[metric_name] = {"status": "no_data"}
                continue

            current_value = statistics.mean(m.value for m in current_metrics)
            benchmark_value = benchmark.expected_value

            tolerance_range = benchmark_value * (benchmark.tolerance_percent / 100)
            lower_bound = benchmark_value - tolerance_range
            upper_bound = benchmark_value + tolerance_range

            if lower_bound <= current_value <= upper_bound:
                status = "within_tolerance"
            elif current_value < lower_bound:
                status = "below_benchmark"
            else:
                status = "above_benchmark"

            deviation_percent = ((current_value - benchmark_value) / benchmark_value) * 100

            results[metric_name] = {
                "current_value": round(current_value, 2),
                "benchmark_value": benchmark_value,
                "tolerance_percent": benchmark.tolerance_percent,
                "status": status,
                "deviation_percent": round(deviation_percent, 2)
            }

        return results


# 全局性能監控器實例
_performance_monitors: Dict[str, PerformanceMonitor] = {}


def get_performance_monitor(component_name: str) -> PerformanceMonitor:
    """獲取或創建組件的性能監控器"""
    if component_name not in _performance_monitors:
        _performance_monitors[component_name] = PerformanceMonitor(component_name)

    return _performance_monitors[component_name]


def performance_monitor(func: Callable) -> Callable:
    """性能監控裝飾器"""
    func_name = func.__name__
    monitor = get_performance_monitor(func.__module__)

    if asyncio.iscoroutinefunction(func):
        return monitor.async_timer(func_name)(func)
    else:
        return monitor.timer(func_name)(func)


def benchmark_operation(operation_name: str, expected_max_time_ms: float = None):
    """基準測試裝飾器"""
    def decorator(func: Callable):
        monitor = get_performance_monitor(func.__module__)

        if asyncio.iscoroutinefunction(func):
            timed_func = monitor.async_timer(operation_name)(func)
        else:
            timed_func = monitor.timer(operation_name)(func)

        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = timed_func(*args, **kwargs)
            end_time = time.perf_counter()

            duration_ms = (end_time - start_time) * 1000

            if expected_max_time_ms and duration_ms > expected_max_time_ms:
                monitor.logger.warning("operation_performance_warning",
                                     operation=operation_name,
                                     duration_ms=round(duration_ms, 2),
                                     expected_max_ms=expected_max_time_ms)

            return result

        async def async_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = await timed_func(*args, **kwargs)
            end_time = time.perf_counter()

            duration_ms = (end_time - start_time) * 1000

            if expected_max_time_ms and duration_ms > expected_max_time_ms:
                monitor.logger.warning("operation_performance_warning",
                                     operation=operation_name,
                                     duration_ms=round(duration_ms, 2),
                                     expected_max_ms=expected_max_time_ms)

            return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return wrapper

    return decorator
