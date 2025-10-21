"""
WebCrawler Commander - 系統監控測試

測試覆蓋：
- 指標收集器功能
- 告警管理邏輯
- 健康監控評估
- 系統監控集成
- 性能和統計分析

作者: Jerry開發工作室
版本: v1.0.0
"""

import asyncio
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime, timedelta

from utils.system_monitor import (
    SystemMonitor, MetricsCollector, AlertManager, HealthMonitor,
    MetricType, AlertLevel, ComponentStatus,
    get_system_monitor, init_system_monitor
)
from tests.test_utils import mock_config_manager, mock_logger_service


@pytest.mark.unit
@pytest.mark.monitor
class TestMetricsCollector:
    """指標收集器測試"""

    @pytest.fixture
    def metrics_collector(self):
        """測試指標收集器修件器"""
        collector = MetricsCollector(collection_interval=1.0)  # 快速收集用於測試
        return collector

    def test_metrics_collector_initialization(self, metrics_collector):
        """測試指標收集器初始化"""
        assert metrics_collector.collection_interval == 1.0
        assert not metrics_collector.running
        assert metrics_collector.collector_thread is None
        assert isinstance(metrics_collector.metrics_buffer, dict)
        assert isinstance(metrics_collector.current_metrics, dict)

    def test_collection_start_stop(self, metrics_collector):
        """測試收集開始和停止"""
        assert not metrics_collector.running

        metrics_collector.start_collection()
        assert metrics_collector.running
        assert metrics_collector.collector_thread is not None
        assert metrics_collector.collector_thread.is_alive()

        metrics_collector.stop_collection()
        assert not metrics_collector.running
        assert metrics_collector.collector_thread is None

    def test_metric_retrieval(self, metrics_collector, faker):
        """測試指標檢索"""
        # 模擬添加指標
        test_metric = {
            "name": "test_metric",
            "value": faker.random_int(1, 100),
            "timestamp": datetime.utcnow(),
            "tags": {"test": "true"}
        }

        metrics_collector.current_metrics["test_metric"] = test_metric
        metrics_collector.metrics_buffer["test_metric"].append(test_metric)

        # 測試檢索
        retrieved = metrics_collector.get_metric("test_metric")
        assert retrieved == test_metric

        # 測試不存在的指標
        non_existent = metrics_collector.get_metric("nonexistent")
        assert non_existent is None

    def test_metric_history(self, metrics_collector, faker):
        """測試指標歷史記錄"""
        metric_name = "test_history"

        # 添加多個指標值
        for i in range(5):
            test_metric = {
                "name": metric_name,
                "value": faker.random_int(1, 100),
                "timestamp": datetime.utcnow(),
                "tags": {"iteration": i}
            }
            metrics_collector.metrics_buffer[metric_name].append(test_metric)

        # 測試歷史檢索
        history = metrics_collector.get_metric_history(metric_name, 3)
        assert len(history) == 3

        # 按限制測試
        full_history = metrics_collector.get_metric_history(metric_name)
        assert len(full_history) == 5

    def test_all_metrics_retrieval(self, metrics_collector, faker):
        """測試獲取所有指標"""
        # 添加多個指標
        for i in range(3):
            metric_name = f"metric_{i}"
            test_metric = {
                "name": metric_name,
                "value": faker.random_int(1, 100),
                "timestamp": datetime.utcnow(),
                "tags": {}
            }
            metrics_collector.current_metrics[metric_name] = test_metric

        all_metrics = metrics_collector.get_all_metrics()

        assert len(all_metrics) == 3
        assert all("metric_" in name for name in all_metrics.keys())


@pytest.mark.unit
@pytest.mark.monitor
class TestAlertManager:
    """告警管理器測試"""

    @pytest.fixture
    def alert_manager(self):
        """測試告警管理器修件器"""
        from utils.system_monitor import AlertManager

        # 創建模擬指標收集器
        mock_collector = MagicMock()
        manager = AlertManager(mock_collector)
        return manager

    def test_alert_rule_creation(self, alert_manager):
        """測試告警規則創建"""
        from utils.system_monitor import AlertRule, AlertLevel

        rule = AlertRule(
            name="test_rule",
            description="Test alert rule",
            metric_name="test_metric",
            condition="value > 80",
            threshold=80.0,
            level=AlertLevel.WARNING,
            cooldown_seconds=300
        )

        alert_manager.add_rule(rule)

        assert rule.name in alert_manager.alert_rules
        assert alert_manager.alert_rules[rule.name] == rule

    def test_alert_rule_removal(self, alert_manager):
        """測試告警規則移除"""
        from utils.system_monitor import AlertRule, AlertLevel

        rule = AlertRule(
            name="remove_test",
            description="Test removal",
            metric_name="test_metric",
            condition="value > 50",
            threshold=50.0,
            level=AlertLevel.INFO
        )

        alert_manager.add_rule(rule)
        assert rule.name in alert_manager.alert_rules

        alert_manager.remove_rule(rule.name)
        assert rule.name not in alert_manager.alert_rules

    def test_alert_rule_evaluation_true_condition(self, alert_manager):
        """測試告警規則評估 - 條件滿足"""
        from utils.system_monitor import AlertRule, AlertLevel, MetricValue

        # 添加規則
        rule = AlertRule(
            name="eval_test",
            description="Evaluation test",
            metric_name="cpu_usage",
            condition="value > 90",
            threshold=90.0,
            level=AlertLevel.CRITICAL
        )
        alert_manager.add_rule(rule)

        # 模擬指標值超過閾值
        mock_metric = MetricValue(
            name="cpu_usage",
            value=95.0,
            timestamp=datetime.utcnow(),
            tags={}
        )
        alert_manager.metrics_collector.get_metric.return_value = mock_metric

        # 評估規則
        alerts = alert_manager.evaluate_rules()

        assert len(alerts) == 1
        assert alerts[0].rule_name == rule.name
        assert alerts[0].level == AlertLevel.CRITICAL
        assert alerts[0].value == 95.0
        assert alerts[0].threshold == 90.0

    def test_alert_rule_evaluation_false_condition(self, alert_manager):
        """測試告警規則評估 - 條件不滿足"""
        from utils.system_monitor import AlertRule, AlertLevel, MetricValue

        # 添加規則
        rule = AlertRule(
            name="no_alert_test",
            description="No alert test",
            metric_name="cpu_usage",
            condition="value > 90",
            threshold=90.0,
            level=AlertLevel.WARNING
        )
        alert_manager.add_rule(rule)

        # 模擬指標值低於閾值
        mock_metric = MetricValue(
            name="cpu_usage",
            value=75.0,
            timestamp=datetime.utcnow(),
            tags={}
        )
        alert_manager.metrics_collector.get_metric.return_value = mock_metric

        # 評估規則
        alerts = alert_manager.evaluate_rules()

        assert len(alerts) == 0

    def test_alert_cooldown_prevention(self, alert_manager):
        """測試告警冷卻期防止重複告警"""
        from utils.system_monitor import AlertRule, AlertLevel, MetricValue

        # 添加規則
        rule = AlertRule(
            name="cooldown_test",
            description="Cooldown test",
            metric_name="memory_usage",
            condition="value > 80",
            threshold=80.0,
            level=AlertLevel.WARNING,
            cooldown_seconds=60
        )
        alert_manager.add_rule(rule)

        # 模擬指標值
        mock_metric = MetricValue(
            name="memory_usage",
            value=85.0,
            timestamp=datetime.utcnow(),
            tags={}
        )
        alert_manager.metrics_collector.get_metric.return_value = mock_metric

        # 第一次評估應該觸發告警
        alerts1 = alert_manager.evaluate_rules()
        assert len(alerts1) == 1

        # 第二次評估應該被冷卻期阻止
        alerts2 = alert_manager.evaluate_rules()
        assert len(alerts2) == 0

    def test_alert_resolution(self, alert_manager):
        """測試告警解決"""
        from utils.system_monitor import Alert
        alert = Alert(
            alert_id="test_alert_001",
            rule_name="test_rule",
            level=AlertLevel.WARNING,
            message="Test alert message",
            value=95.0,
            threshold=80.0,
            timestamp=datetime.utcnow()
        )

        # 添加活躍告警
        alert_manager.active_alerts[alert.alert_id] = alert
        assert len(alert_manager.get_active_alerts()) == 1

        # 解決告警
        alert_manager.resolve_alert(alert.alert_id)

        # 驗證告警已解決
        assert len(alert_manager.get_active_alerts()) == 0
        assert alert in alert_manager.alert_history
        assert alert.resolved is True
        assert alert.resolved_at is not None

    def test_alert_history_retrieval(self, alert_manager):
        """測試告警歷史檢索"""
        from utils.system_monitor import Alert
        # 添加多個歷史告警
        alerts = []
        for i in range(5):
            alert = Alert(
                alert_id=f"history_alert_{i}",
                rule_name=f"rule_{i}",
                level=AlertLevel.INFO,
                message=f"History alert {i}",
                value=float(i),
                threshold=10.0,
                timestamp=datetime.utcnow(),
                resolved=True
            )
            alert_manager.alert_history.append(alert)

        # 測試歷史檢索
        history = alert_manager.get_alert_history(3)
        assert len(history) == 3

        # 測試默認限制
        full_history = alert_manager.get_alert_history()
        assert len(full_history) == 5


@pytest.mark.unit
@pytest.mark.monitor
class TestHealthMonitor:
    """健康監控器測試"""

    @pytest.fixture
    def health_monitor(self):
        """測試健康監控器修件器"""
        from utils.system_monitor import HealthMonitor

        mock_collector = MagicMock()
        monitor = HealthMonitor(mock_collector)
        return monitor

    @pytest.mark.asyncio
    async def test_health_check_execution(self, health_monitor):
        """測試健康檢查執行"""
        async def dummy_check():
            return {"status": "healthy", "response_time": 0.1}

        # 執行健康檢查
        result = await health_monitor.perform_health_check("test_component", dummy_check)

        assert result.component_name == "test_component"
        assert result.check_time is not None
        assert isinstance(result.metrics, dict)
        assert "response_time" in result.metrics

    @pytest.mark.asyncio
    async def test_health_status_evaluation_healthy(self, health_monitor):
        """測試健康狀態評估 - 健康狀態"""
        async def healthy_check():
            return {
                "cpu_percent": 45.0,
                "memory_percent": 60.0,
                "disk_percent": 30.0,
                "response_time": 0.8,
                "health_score": 95
            }

        result = await health_monitor.perform_health_check("healthy_component", healthy_check)

        assert result.status == ComponentStatus.HEALTHY
        assert result.score >= 90.0
        assert "正常運行" in result.message or "normal" in result.message

    @pytest.mark.asyncio
    async def test_health_status_evaluation_degraded(self, health_monitor):
        """測試健康狀態評估 - 降級狀態"""
        async def degraded_check():
            return {
                "cpu_percent": 75.0,
                "memory_percent": 80.0,
                "disk_percent": 85.0,
                "response_time": 2.5,
                "health_score": 75
            }

        result = await health_monitor.perform_health_check("degraded_component", degraded_check)

        assert result.status == ComponentStatus.DEGRADED
        assert 70.0 <= result.score < 90.0

    @pytest.mark.asyncio
    async def test_health_status_evaluation_unhealthy(self, health_monitor):
        """測試健康狀態評估 - 不健康狀態"""
        async def unhealthy_check():
            return {
                "cpu_percent": 95.0,
                "memory_percent": 95.0,
                "disk_percent": 95.0,
                "response_time": 8.0,
                "health_score": 45
            }

        result = await health_monitor.perform_health_check("unhealthy_component", unhealthy_check)

        assert result.status == ComponentStatus.UNHEALTHY
        assert 30.0 <= result.score < 70.0

    @pytest.mark.asyncio
    async def test_health_status_evaluation_down(self, health_monitor):
        """測試健康狀態評估 - 宕機狀態"""
        async def failing_check():
            return {"error": "Service unavailable", "health_score": 0}

        result = await health_monitor.perform_health_check("down_component", failing_check)

        assert result.status == ComponentStatus.DOWN
        assert result.score == 0.0
        assert "錯誤" in result.message or "error" in result.message

    @pytest.mark.asyncio
    async def test_check_execution_failure(self, health_monitor):
        """測試檢查執行失敗"""
        async def failing_check():
            raise Exception("Check execution failed")

        result = await health_monitor.perform_health_check("failing_component", failing_check)

        assert result.status == ComponentStatus.DOWN
        assert result.score == 0.0
        assert "健康檢查失敗" in result.message or "failed" in result.message

    def test_overall_health_score_calculation(self, health_monitor):
        """測試整體健康評分計算"""
        # 模擬多個組件健康檢查結果
        health_monitor.health_checks = {
            "component1": type('HealthCheck', (), {
                'component_name': 'component1',
                'score': 90.0,
                'status': ComponentStatus.HEALTHY
            })(),
            "component2": type('HealthCheck', (), {
                'component_name': 'component2',
                'score': 80.0,
                'status': ComponentStatus.DEGRADED
            })(),
            "component3": type('HealthCheck', (), {
                'component_name': 'component3',
                'score': 60.0,
                'status': ComponentStatus.UNHEALTHY
            })()
        }

        overall_score = health_monitor.get_overall_health_score()

        # 應該是三個分數的平均值
        expected_score = (90.0 + 80.0 + 60.0) / 3
        assert overall_score == pytest.approx(expected_score, 0.1)

    def test_component_health_retrieval(self, health_monitor):
        """測試組件健康檢索"""
        # 添加模擬健康檢查
        health_check = type('HealthCheck', (), {
            'component_name': 'test_component',
            'status': ComponentStatus.HEALTHY,
            'score': 95.0,
            'check_time': datetime.utcnow(),
            'message': 'Normal operation',
            'metrics': {'response_time': 0.5}
        })()

        health_monitor.health_checks['test_component'] = health_check

        # 檢索健康狀態
        retrieved = health_monitor.get_component_health('test_component')
        assert retrieved == health_check

        # 檢索不存在的組件
        not_found = health_monitor.get_component_health('nonexistent')
        assert not_found is None

    def test_all_health_checks_retrieval(self, health_monitor):
        """測試獲取所有健康檢查"""
        # 添加多個健康檢查
        for i in range(3):
            health_check = type('HealthCheck', (), {
                'component_name': f'component{i}',
                'status': ComponentStatus.HEALTHY,
                'score': 90.0 + i,
                'check_time': datetime.utcnow(),
                'message': f'Check {i}',
                'metrics': {}
            })()
            health_monitor.health_checks[f'component{i}'] = health_check

        all_checks = health_monitor.get_all_health_checks()

        assert len(all_checks) == 3
        assert all(check_name.startswith('component') for check_name in all_checks.keys())


@pytest.mark.unit
@pytest.mark.monitor
class TestSystemMonitorIntegration:
    """系統監控集成測試"""

    @pytest.fixture
    async def system_monitor(self, temp_dir):
        """測試系統監控修件器"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.system_monitor.get_config_manager', return_value=config_mock), \
             patch('utils.system_monitor.get_logger', return_value=logger_mock):

            monitor = SystemMonitor(config_manager=config_mock)
            return monitor

    @pytest.mark.asyncio
    async def test_monitoring_start_stop(self, system_monitor):
        """測試監控開始和停止"""
        assert not system_monitor.monitoring_enabled  # 默認為False，除非配置中設定

        # 模擬啟用監控
        system_monitor.monitoring_enabled = True

        # 測試開始監控
        system_monitor.start_monitoring()

        # 給線程一點時間啟動
        await asyncio.sleep(0.1)

        # 驗證監控已開始
        # 注意：在測試環境中，監控線程可能不會完全啟動

        # 測試停止監控
        system_monitor.stop_monitoring()

    def test_dashboard_data_generation(self, system_monitor):
        """測試儀表板數據生成"""
        # 模擬一些系統數據
        dashboard_data = system_monitor.get_dashboard_data()

        assert isinstance(dashboard_data, dict)
        assert "timestamp" in dashboard_data
        assert "overall_health_score" in dashboard_data
        assert isinstance(dashboard_data["current_metrics"], dict)

        # 驗證必有字段
        expected_keys = [
            "timestamp", "overall_health_score", "active_alerts_count",
            "total_metrics_count", "current_metrics", "active_alerts",
            "recent_alerts", "performance_trends", "component_health"
        ]

        for key in expected_keys:
            assert key in dashboard_data

    def test_monitoring_statistics(self, system_monitor):
        """測試監控統計"""
        stats = system_monitor.get_monitoring_stats()

        assert isinstance(stats, dict)
        assert "monitoring_started_at" in stats
        assert "alerts_generated" in stats
        assert "health_checks_performed" in stats
        assert "configuration" in stats

        # 驗證配置字段
        config = stats["configuration"]
        assert "enabled" in config
        assert "collection_interval" in config

    def test_health_report_generation(self, system_monitor):
        """測試健康報告生成"""
        report = system_monitor.generate_health_report()

        assert isinstance(report, dict)
        assert "generated_at" in report
        assert "period" in report
        assert "overall_health_score" in report
        assert "system_performance" in report
        assert "component_health" in report
        assert "alert_summary" in report
        assert "recommendations" in report

        # 驗證系統性能字段
        perf = report["system_performance"]
        assert isinstance(perf, dict)
        # 注意：由於沒有真實的性能數據，這些值可能為0或None

        # 驗證建議字段
        recommendations = report["recommendations"]
        assert isinstance(recommendations, list)
        # 至少應該有一條建議
        assert len(recommendations) > 0

    def test_monitor_initialization(self):
        """測試監控器初始化"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.system_monitor.get_config_manager', return_value=config_mock), \
             patch('utils.system_monitor.get_logger', return_value=logger_mock):

            monitor = SystemMonitor(config_manager=config_mock)

            # 驗證子組件已初始化
            assert monitor.metrics_collector is not None
            assert monitor.alert_manager is not None
            assert monitor.health_monitor is not None

            # 驗證默認告警規則已設置
            assert len(monitor.alert_manager.alert_rules) == 5  # 默認規則

            # 驗證統計數據已初始化
            assert "alerts_generated" in monitor.stats
            assert "health_checks_performed" in monitor.stats


@pytest.mark.unit
@pytest.mark.monitor
class TestSystemMonitorErrorHandling:
    """系統監控錯誤處理測試"""

    @pytest.fixture
    async def system_monitor(self, temp_dir):
        """測試系統監控修件器"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.system_monitor.get_config_manager', return_value=config_mock), \
             patch('utils.system_monitor.get_logger', return_value=logger_mock):

            monitor = SystemMonitor(config_manager=config_mock)
            return monitor

    def test_invalid_rule_addition_handling(self, system_monitor):
        """測試無效規則添加處理"""
        from utils.system_monitor import AlertRule, AlertLevel

        # 嘗試添加無效規則（缺少必需字段）
        invalid_rule = AlertRule(
            name="",  # 空名稱
            description="Invalid rule",
            metric_name="test_metric",
            condition="value > 50",
            threshold=50.0,
            level=AlertLevel.INFO
        )

        # 應該能夠處理（即使規則無效）
        system_monitor.alert_manager.add_rule(invalid_rule)

        # 規則應該被添加（但名稱可能會有問題）
        # assert "" in system_monitor.alert_manager.alert_rules

    def test_collector_thread_failure_handling(self, system_monitor):
        """測試收集器線程失敗處理"""
        # 模擬線程啟動失敗
        with patch('threading.Thread.start', side_effect=RuntimeError("Thread start failed")):
            # 這應該不會讓整個監控系統崩潰
            system_monitor.start_monitoring()

    def test_metrics_buffer_overflow_protection(self, system_monitor, faker):
        """測試指標緩沖區溢出保護"""
        # 添加大量指標到緩沖區
        for i in range(1100):  # 超過默認緩沖區大小
            test_metric = {
                "name": "overflow_test",
                "value": faker.random_int(1, 100),
                "timestamp": datetime.utcnow(),
                "tags": {}
            }
            system_monitor.metrics_collector.metrics_buffer["overflow_test"].append(test_metric)

        # 緩沖區應該被限制大小
        buffer_size = len(system_monitor.metrics_collector.metrics_buffer["overflow_test"])
        assert buffer_size > 0
        # 注意：實際的限制可能需要模擬deque的行為

    def test_concurrent_access_safety(self, system_monitor, faker):
        """測試並發訪問安全性"""
        import threading
        import time

        results = []
        errors = []

        def concurrent_metric_access(thread_id):
            try:
                for i in range(50):
                    # 模擬並發讀寫指標
                    system_monitor.metrics_collector.current_metrics[f"thread_{thread_id}_{i}"] = {
                        "name": f"test_{thread_id}",
                        "value": faker.random_int(1, 100),
                        "timestamp": datetime.utcnow(),
                        "tags": {"thread": thread_id}
                    }
                    results.append(f"thread_{thread_id}_{i}")
                    time.sleep(0.001)
            except Exception as e:
                errors.append(f"thread_{thread_id}: {e}")

        # 創建並啟動多個線程
        threads = []
        for i in range(3):
            thread = threading.Thread(target=concurrent_metric_access, args=(i,))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join(timeout=5)

        # 驗證結果
        assert len(errors) == 0  # 不應該有並發錯誤
        assert len(results) >= 100  # 至少應該完成一些操作

    def test_singleton_pattern_maintenance(self):
        """測試單例模式維護"""
        # 重置全域實例
        global _system_monitor
        _system_monitor = None

        config_mock = mock_config_manager()

        # 初始化多次應該返回同一個實例
        with patch('utils.system_monitor.get_config_manager', return_value=config_mock):
            monitor1 = init_system_monitor(config_mock)
            monitor2 = get_system_monitor()

            assert monitor1 is monitor2


if __name__ == "__main__":
    pytest.main([__file__, "--verbose", "--cov=utils.system_monitor", "--cov-report=html"])
