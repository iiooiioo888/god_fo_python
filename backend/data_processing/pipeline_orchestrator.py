"""
WebCrawler Commander - 數據處理管道協調器
企業級數據處理流程自動化編排系統

功能特色：
- 可配置處理管道
- 動態組件裝載
- 智能錯誤處理與恢復
- 實時性能監控
- 流水線優化與負載均衡
- 高可用性與故障轉移

作者: Jerry開發工作室
版本: v1.0.0
"""

import asyncio
import time
import json
from typing import Dict, List, Optional, Any, Callable, Union, Type
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from collections import defaultdict, deque
import statistics

from ..utils.config_manager import get_config_manager
from ..utils.logger_service import get_logger
from ..utils.error_handler import get_error_handler, with_error_handling, RecoveryStrategy, RecoveryConfig, ErrorContext
from ..utils.performance_monitor import get_performance_monitor, performance_monitor, benchmark_operation
from ..utils.audit_logger import get_audit_logger, audit_log, AuditLevel, AuditCategory

from .data_processor import DataRecord, ProcessingResult, DataQualityMetrics


class PipelineStage(Enum):
    """管道階段枚舉"""
    INGESTION = "ingestion"           # 數據攝入
    VALIDATION = "validation"         # 驗證階段
    CLEANING = "cleaning"            # 清理階段
    ENRICHMENT = "enrichment"         # 數據豐富
    TRANSFORMATION = "transformation"  # 數據轉換
    DEDUPLICATION = "deduplication"   # 去重階段
    QUALITY_GATE = "quality_gate"     # 品質門檻
    EXPORT = "export"               # 數據輸出


class PipelineMode(Enum):
    """管道運行模式"""
    SEQUENTIAL = "sequential"         # 順序執行
    PARALLEL = "parallel"            # 並行執行
    PIPELINED = "pipelined"          # 流水線模式
    HYBRID = "hybrid"               # 混合模式


@dataclass
class PipelineComponent:
    """管道組件配置"""
    name: str
    component_class: Type
    config: Dict[str, Any] = field(default_factory=dict)
    stage: PipelineStage = PipelineStage.TRANSFORMATION
    priority: int = 0
    dependencies: List[str] = field(default_factory=list)
    max_retries: int = 3
    timeout_seconds: float = 300.0
    parallel_enabled: bool = False
    batch_size: int = 1000


@dataclass
class PipelineMetrics:
    """管道性能指標"""
    total_processed: int = 0
    success_count: int = 0
    error_count: int = 0
    avg_processing_time: float = 0.0
    throughput_per_second: float = 0.0
    stage_metrics: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    start_time: datetime = field(default_factory=datetime.utcnow)


@dataclass
class PipelineResult:
    """管道處理結果"""
    success: bool
    total_records: int
    processed_records: int
    failed_records: int
    processing_time: float
    quality_score: float
    stage_results: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class PipelineOrchestrator:
    """
    數據處理管道協調器

    提供企業級數據處理自動化：
    - 智能組件調度與依賴管理
    - 動態流水線優化
    - 實時性能監控與自動調優
    - 故障恢復與高可用性
    - 分布式處理支援
    """

    def __init__(self, config_manager=None):
        self.config_manager = config_manager or get_config_manager()
        self.logger = get_logger(__name__)

        # 初始化統一框架組件
        self.error_handler = get_error_handler(__name__)
        self.performance_monitor = get_performance_monitor(__name__)
        self.audit_logger = get_audit_logger()

        # 管道組件註冊表
        self.component_registry: Dict[str, PipelineComponent] = {}
        self.active_components: Dict[str, Any] = {}

        # 管道配置
        self.pipeline_config: Dict[str, Any] = {}
        self.execution_mode: PipelineMode = PipelineMode.SEQUENTIAL

        # 性能指標
        self.metrics = PipelineMetrics()

        # 執行器池
        self.thread_executor = ThreadPoolExecutor(max_workers=8)
        self.process_executor = ProcessPoolExecutor(max_workers=4)

        # 錯誤恢復配置
        self._setup_error_recovery_configs()

        # 性能基準
        self._setup_performance_benchmarks()

        self.logger.info("pipeline_orchestrator_initialized")

    def _setup_error_recovery_configs(self):
        """設置錯誤恢復配置"""
        # 管道階段錯誤恢復
        pipeline_error_config = RecoveryConfig(
            strategy=RecoveryStrategy.RETRY,
            max_retries=3,
            retry_delay=5.0,
            exponential_backoff=True
        )
        self.error_handler.register_recovery_config("pipeline_stage", pipeline_error_config)

        # 組件故障恢復
        component_error_config = RecoveryConfig(
            strategy=RecoveryStrategy.FALLBACK,
            fallback_function=self._fallback_component,
            max_retries=2
        )
        self.error_handler.register_recovery_config("component_failure", component_error_config)

        # 數據處理錯誤恢復
        data_error_config = RecoveryConfig(
            strategy=RecoveryStrategy.SKIP,
            max_retries=1
        )
        self.error_handler.register_recovery_config("data_processing", data_error_config)

    def _setup_performance_benchmarks(self):
        """設置性能基準"""
        # 管道吞吐量基準
        self.performance_monitor.set_benchmark(
            "pipeline_throughput_records_per_second",
            1000.0,  # 1000 records/second
            tolerance_percent=50,
            environment="production"
        )

        # 管道處理時間基準
        self.performance_monitor.set_benchmark(
            "pipeline_processing_time_hours",
            2.0,  # 最多2小時處理
            tolerance_percent=100,
            environment="production"
        )

        # 組件並行度基準
        self.performance_monitor.set_benchmark(
            "pipeline_component_utilization",
            80.0,  # 80% 組件利用率
            tolerance_percent=20,
            environment="production"
        )

    async def _fallback_component(self, error_details) -> None:
        """組件故障備用策略"""
        self.logger.warning("using_fallback_component_strategy",
                           component=error_details.get("component_name", "unknown"),
                           original_error=error_details.message)

    def register_component(self, component: PipelineComponent) -> None:
        """
        註冊管道組件

        Args:
            component: 管道組件配置
        """
        if component.name in self.component_registry:
            raise ValueError(f"組件 {component.name} 已經註冊")

        self.component_registry[component.name] = component

        # 驗證依賴關係
        for dep in component.dependencies:
            if dep not in self.component_registry:
                self.logger.warning("component_dependency_missing",
                                   component=component.name,
                                   missing_dependency=dep)

        self.logger.info("component_registered",
                        name=component.name,
                        stage=component.stage.value,
                        priority=component.priority)

    def unregister_component(self, component_name: str) -> None:
        """
        取消註冊組件

        Args:
            component_name: 組件名稱
        """
        if component_name in self.component_registry:
            del self.component_registry[component_name]

            # 清理活躍組件
            if component_name in self.active_components:
                del self.active_components[component_name]

            self.logger.info("component_unregistered", name=component_name)

    def configure_pipeline(self, config: Dict[str, Any]) -> None:
        """
        配置處理管道

        Args:
            config: 管道配置
        """
        self.pipeline_config = config

        # 解析執行模式
        mode_str = config.get("execution_mode", "sequential").lower()
        self.execution_mode = PipelineMode(mode_str)

        # 配置組件參數
        for component_name, component_config in config.get("components", {}).items():
            if component_name in self.component_registry:
                self.component_registry[component_name].config.update(component_config)

        # 構建執行順序
        self._build_execution_order()

        self.logger.info("pipeline_configured",
                        mode=self.execution_mode.value,
                        components=len(self.component_registry))

    def _build_execution_order(self) -> None:
        """構建組件執行順序"""
        # 基於依賴關係和優先級的拓撲排序
        visited = set()
        temp_visit = set()
        order = []

        def visit(component_name: str):
            if component_name in temp_visit:
                raise ValueError(f"循環依賴檢測到: {component_name}")
            if component_name in visited:
                return

            temp_visit.add(component_name)

            # 訪問依賴項
            component = self.component_registry[component_name]
            for dep in component.dependencies:
                visit(dep)

            temp_visit.remove(component_name)
            visited.add(component_name)
            order.append(component_name)

        # 按優先級排序處理
        all_components = sorted(
            self.component_registry.keys(),
            key=lambda x: self.component_registry[x].priority,
            reverse=True
        )

        for component_name in all_components:
            if component_name not in visited:
                visit(component_name)

        self.execution_order = order
        self.logger.debug("execution_order_built", order=order)

    @performance_monitor
    @benchmark_operation("pipeline_execution", expected_max_time_ms=7200000)  # 2小時
    @with_audit_trail("data_pipeline_processing")
    @with_error_handling("pipeline_stage")
    async def execute_pipeline(self, records: List[DataRecord],
                              pipeline_config: Optional[Dict[str, Any]] = None) -> PipelineResult:
        """
        執行數據處理管道

        Args:
            records: 輸入數據記錄
            pipeline_config: 管道配置覆蓋

        Returns:
            管道處理結果
        """
        start_time = time.time()
        self.metrics = PipelineMetrics()
        self.metrics.total_processed = len(records)

        # 應用配置覆蓋
        if pipeline_config:
            self.configure_pipeline(pipeline_config)

        self.logger.info("pipeline_execution_started",
                        record_count=len(records),
                        mode=self.execution_mode.value,
                        components=len(self.execution_order))

        # 記錄審計事件
        audit_log(
            level=AuditLevel.ACCESS,
            category=AuditCategory.DATA_ACCESS,
            action="pipeline_execution_started",
            actor="pipeline_orchestrator",
            target="data_processing_pipeline",
            result="STARTED",
            details={
                "record_count": len(records),
                "execution_mode": self.execution_mode.value,
                "component_count": len(self.execution_order)
            }
        )

        try:
            # 根據執行模式選擇處理策略
            if self.execution_mode == PipelineMode.SEQUENTIAL:
                result = await self._execute_sequential(records)
            elif self.execution_mode == PipelineMode.PARALLEL:
                result = await self._execute_parallel(records)
            elif self.execution_mode == PipelineMode.PIPELINED:
                result = await self._execute_pipelined(records)
            else:  # HYBRID
                result = await self._execute_hybrid(records)

            # 計算最終指標
            processing_time = time.time() - start_time
            result.processing_time = processing_time
            result.quality_score = self._calculate_pipeline_quality()

            # 更新性能統計
            self._update_performance_metrics(result, processing_time)

            # 記錄成功審計事件
            audit_log(
                level=AuditLevel.ACCESS,
                category=AuditCategory.DATA_ACCESS,
                action="pipeline_execution_completed",
                actor="pipeline_orchestrator",
                target="data_processing_pipeline",
                result="SUCCESS",
                details={
                    "processed_records": result.processed_records,
                    "processing_time_seconds": round(processing_time, 2),
                    "quality_score": round(result.quality_score, 2)
                }
            )

            self.logger.info("pipeline_execution_completed",
                           processed=result.processed_records,
                           failed=result.failed_records,
                           processing_time=round(processing_time, 2),
                           quality_score=round(result.quality_score, 2))

            return result

        except Exception as e:
            processing_time = time.time() - start_time

            # 記錄失敗審計事件
            audit_log(
                level=AuditLevel.SECURITY,
                category=AuditCategory.SECURITY_EVENT,
                action="pipeline_execution_failed",
                actor="pipeline_orchestrator",
                target="data_processing_pipeline",
                result="FAILED",
                details={
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "processing_time_seconds": round(processing_time, 2)
                }
            )

            self.logger.error("pipeline_execution_failed", error=str(e))

            # 返回失敗結果
            return PipelineResult(
                success=False,
                total_records=len(records),
                processed_records=self.metrics.success_count,
                failed_records=self.metrics.error_count,
                processing_time=processing_time,
                quality_score=0.0,
                errors=[str(e)]
            )

    async def _execute_sequential(self, records: List[DataRecord]) -> PipelineResult:
        """順序執行模式"""
        current_records = records.copy()
        stage_results = {}

        for component_name in self.execution_order:
            component = await self._get_or_create_component(component_name)

            if not component:
                self.logger.warning("component_not_available", name=component_name)
                continue

            try:
                self.logger.debug("executing_component",
                                name=component_name,
                                input_count=len(current_records))

                # 執行組件
                stage_start = time.time()
                result = await self._execute_component(component, current_records)
                stage_time = time.time() - stage_start

                # 更新指標
                self._update_stage_metrics(component_name, result, stage_time)

                # 保存階段結果
                stage_results[component_name] = {
                    "success": result["success"],
                    "processed": len(result.get("processed_records", [])),
                    "processing_time": stage_time,
                    "quality_improvement": result.get("quality_improvement", 0.0)
                }

                current_records = result.get("processed_records", current_records)

            except Exception as e:
                self.logger.error("component_execution_failed",
                                component=component_name,
                                error=str(e))

                stage_results[component_name] = {
                    "success": False,
                    "error": str(e)
                }

                # 決定是否繼續執行
                if self.pipeline_config.get("fail_fast", False):
                    break

        return PipelineResult(
            success=True,
            total_records=len(records),
            processed_records=len(current_records),
            failed_records=len(records) - len(current_records),
            processing_time=0.0,  # 將在上级設置
            quality_score=0.0,     # 將在上级設置
            stage_results=stage_results
        )

    async def _execute_parallel(self, records: List[DataRecord]) -> PipelineResult:
        """並行執行模式"""
        # 識別無依賴的組件進行並行執行
        parallel_groups = self._group_independent_components()

        current_records = records.copy()
        stage_results = {}

        for group in parallel_groups:
            if len(group) == 1:
                # 單個組件，正常執行
                component_name = group[0]
                component = await self._get_or_create_component(component_name)

                if component:
                    result = await self._execute_component(component, current_records)
                    stage_results[component_name] = result
                    current_records = result.get("processed_records", current_records)
            else:
                # 多個組件並行執行
                tasks = []
                for component_name in group:
                    component = await self._get_or_create_component(component_name)
                    if component:
                        task = asyncio.create_task(
                            self._execute_component(component, current_records.copy())
                        )
                        tasks.append((component_name, task))

                # 等待所有任務完成
                for component_name, task in tasks:
                    try:
                        result = await task
                        stage_results[component_name] = result

                        # 合併結果（需要實現具體的合併邏輯）
                        current_records = self._merge_parallel_results(
                            current_records, result.get("processed_records", [])
                        )

                    except Exception as e:
                        self.logger.error("parallel_component_failed",
                                        component=component_name,
                                        error=str(e))

                        stage_results[component_name] = {"success": False, "error": str(e)}

        return PipelineResult(
            success=True,
            total_records=len(records),
            processed_records=len(current_records),
            failed_records=len(records) - len(current_records),
            processing_time=0.0,
            quality_score=0.0,
            stage_results=stage_results
        )

    async def _execute_pipelined(self, records: List[DataRecord]) -> PipelineResult:
        """流水線執行模式"""
        # 實現真正的流水線處理（生產者-消費者模式）
        # 這是一個簡化的實現

        pipeline_queues = {}
        for i, component_name in enumerate(self.execution_order):
            pipeline_queues[component_name] = asyncio.Queue(maxsize=1000)

        # 啟動處理任務
        processing_tasks = []
        for component_name in self.execution_order:
            task = asyncio.create_task(
                self._process_pipeline_stage(component_name, pipeline_queues)
            )
            processing_tasks.append(task)

        # 送入初始數據
        await pipeline_queues[self.execution_order[0]].put(records)

        # 等待所有任務完成
        results = await asyncio.gather(*processing_tasks, return_exceptions=True)

        # 收集最終結果
        final_queue = pipeline_queues.get(self.execution_order[-1])
        if final_queue:
            final_records = await final_queue.get()
        else:
            final_records = records

        stage_results = {}
        for i, component_name in enumerate(self.execution_order):
            stage_results[component_name] = {
                "success": True,
                "processed": len(final_records)
            }

        return PipelineResult(
            success=True,
            total_records=len(records),
            processed_records=len(final_records),
            failed_records=len(records) - len(final_records),
            processing_time=0.0,
            quality_score=0.0,
            stage_results=stage_results
        )

    async def _execute_hybrid(self, records: List[DataRecord]) -> PipelineResult:
        """混合執行模式"""
        # 結合順序和並行的優點
        current_records = records.copy()
        stage_results = {}

        for component_name in self.execution_order:
            component = await self._get_or_create_component(component_name)

            if component:
                config = self.component_registry[component_name]

                if config.parallel_enabled:
                    # 並行處理該組件
                    result = await self._execute_component_parallel(component, current_records)
                else:
                    # 順序處理
                    result = await self._execute_component(component, current_records)

                stage_results[component_name] = result
                current_records = result.get("processed_records", current_records)

        return PipelineResult(
            success=True,
            total_records=len(records),
            processed_records=len(current_records),
            failed_records=len(records) - len(current_records),
            processing_time=0.0,
            quality_score=0.0,
            stage_results=stage_results
        )

    async def _get_or_create_component(self, component_name: str) -> Optional[Any]:
        """獲取或創建組件實例"""
        if component_name in self.active_components:
            return self.active_components[component_name]

        if component_name not in self.component_registry:
            return None

        config = self.component_registry[component_name]

        try:
            # 動態實例化組件
            component_instance = config.component_class(config.config)
            self.active_components[component_name] = component_instance

            self.logger.debug("component_created", name=component_name)
            return component_instance

        except Exception as e:
            self.logger.error("component_creation_failed",
                            name=component_name,
                            error=str(e))
            return None

    async def _execute_component(self, component: Any, records: List[DataRecord]) -> Dict[str, Any]:
        """執行單個組件"""
        try:
            # 根據組件類型執行對應的方法
            if hasattr(component, 'process_data'):
                result = await component.process_data(records)
            elif hasattr(component, 'validate_records'):
                validated_records, metrics = await component.validate_records(records)
                result = ProcessingResult(
                    success=True,
                    input_count=len(records),
                    output_count=len(validated_records),
                    processing_time=0.0,
                    quality_metrics=metrics
                )
            elif hasattr(component, 'clean_data'):
                cleaned_records = await component.clean_data(records)
                result = ProcessingResult(
                    success=True,
                    input_count=len(records),
                    output_count=len(cleaned_records),
                    processing_time=0.0,
                    quality_metrics=DataQualityMetrics()
                )
            else:
                raise ValueError(f"不支援的組件類型: {type(component)}")

            return {
                "success": result.success,
                "processed_records": validated_records if 'validated_records' in locals() else records,
                "processing_time": result.processing_time,
                "quality_improvement": getattr(result.quality_metrics, 'completeness_score', 0.0)
            }

        except Exception as e:
            self.logger.error("component_execution_error", error=str(e))

            return {
                "success": False,
                "error": str(e),
                "processed_records": records  # 傳遞原始記錄
            }

    def _group_independent_components(self) -> List[List[str]]:
        """將無依賴關係的組件分組"""
        # 簡單的實現：依序處理（實際實現會更複雜）
        return [[name] for name in self.execution_order]

    async def _execute_component_parallel(self, component: Any,
                                       records: List[DataRecord]) -> Dict[str, Any]:
        """並行執行組件"""
        # 使用線程池進行並行處理
        batch_size = self.pipeline_config.get("batch_size", 1000)
        batches = [records[i:i + batch_size] for i in range(0, len(records), batch_size)]

        tasks = []
        for batch in batches:
            task = asyncio.get_event_loop().run_in_executor(
                self.thread_executor,
                lambda: asyncio.run(self._execute_component(component, batch))
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 合併結果
        all_processed = []
        total_time = 0.0
        quality_improvement = 0.0

        for result in results:
            if isinstance(result, Exception):
                self.logger.error("parallel_batch_failed", error=str(result))
                continue

            if result["success"]:
                all_processed.extend(result["processed_records"])
                total_time += result["processing_time"]
                quality_improvement += result.get("quality_improvement", 0.0)

        return {
            "success": len(all_processed) > 0,
            "processed_records": all_processed,
            "processing_time": total_time / len(tasks) if tasks else 0.0,
            "quality_improvement": quality_improvement / len(tasks) if tasks else 0.0
        }

    def _merge_parallel_results(self, original: List[DataRecord],
                              processed: List[DataRecord]) -> List[DataRecord]:
        """合併並行處理結果"""
        # 簡單的合併策略：保留所有成功處理的記錄
        return processed if processed else original

    async def _process_pipeline_stage(self, component_name: str,
                                    queues: Dict[str, asyncio.Queue]) -> None:
        """處理流水線階段"""
        input_queue = queues[component_name]

        # 找到輸出隊列
        current_index = self.execution_order.index(component_name)
        if current_index < len(self.execution_order) - 1:
            output_queue = queues[self.execution_order[current_index + 1]]
        else:
            output_queue = None  # 最後一個階段

        component = await self._get_or_create_component(component_name)
        if not component:
            return

        try:
            while True:
                try:
                    # 從輸入隊列獲取數據
                    records = await asyncio.wait_for(input_queue.get(), timeout=1.0)
                    input_queue.task_done()

                    # 處理數據
                    result = await self._execute_component(component, records)

                    if result["success"] and output_queue:
                        # 發送到輸出隊列
                        await output_queue.put(result["processed_records"])

                except asyncio.TimeoutError:
                    # 檢查是否所有上游任務都完成了
                    break

        except Exception as e:
            self.logger.error("pipeline_stage_error",
                            stage=component_name,
                            error=str(e))

    def _update_stage_metrics(self, component_name: str,
                            result: Dict[str, Any], processing_time: float) -> None:
        """更新階段指標"""
        if component_name not in self.metrics.stage_metrics:
            self.metrics.stage_metrics[component_name] = {
                "execution_count": 0,
                "total_time": 0.0,
                "success_count": 0,
                "error_count": 0,
                "avg_processing_time": 0.0
            }

        metrics = self.metrics.stage_metrics[component_name]
        metrics["execution_count"] += 1
        metrics["total_time"] += processing_time

        if result.get("success", False):
            metrics["success_count"] += 1
            self.metrics.success_count += 1
        else:
            metrics["error_count"] += 1
            self.metrics.error_count += 1

        # 更新平均處理時間
        count = metrics["execution_count"]
        metrics["avg_processing_time"] = metrics["total_time"] / count

    def _update_performance_metrics(self, result: PipelineResult,
                                  total_time: float) -> None:
        """更新性能指標"""
        self.metrics.avg_processing_time = total_time
        self.metrics.throughput_per_second = result.processed_records / total_time if total_time > 0 else 0

    def _calculate_pipeline_quality(self) -> float:
        """計算管道整體品質評分"""
        if not self.metrics.stage_metrics:
            return 0.0

        # 基於各階段成功率和品質改進計算綜合評分
        total_stages = len(self.metrics.stage_metrics)
        successful_stages = sum(1 for m in self.metrics.stage_metrics.values()
                              if m["success_count"] > 0)

        success_rate = successful_stages / total_stages if total_stages > 0 else 0.0

        # 考慮處理記錄的比例
        record_success_rate = self.metrics.success_count / self.metrics.total_processed if self.metrics.total_processed > 0 else 0.0

        # 綜合評分
        overall_quality = (success_rate * 0.6 + record_success_rate * 0.4) * 100

        return round(overall_quality, 2)

    def get_pipeline_status(self) -> Dict[str, Any]:
        """獲取管道狀態"""
        return {
            "execution_mode": self.execution_mode.value,
            "active_components": len(self.active_components),
            "registered_components": len(self.component_registry),
            "last_execution_metrics": {
                "total_processed": self.metrics.total_processed,
                "success_count": self.metrics.success_count,
                "error_count": self.metrics.error_count,
                "avg_processing_time": round(self.metrics.avg_processing_time, 2),
                "throughput_per_second": round(self.metrics.throughput_per_second, 2)
            },
            "stage_metrics": self.metrics.stage_metrics
        }

    async def shutdown_pipeline(self) -> None:
        """關閉處理管道"""
        self.logger.info("pipeline_shutdown_initiated")

        # 清理活躍組件
        for component_name, component in self.active_components.items():
            try:
                if hasattr(component, 'close'):
                    await component.close()
            except Exception as e:
                self.logger.warning("component_shutdown_failed",
                                  component=component_name,
                                  error=str(e))

        self.active_components.clear()

        # 關閉執行器池
        self.thread_executor.shutdown(wait=True)
        self.process_executor.shutdown(wait=True)

        self.logger.info("pipeline_shutdown_completed")


# 全域管道協調器實例
_pipeline_orchestrator: Optional[PipelineOrchestrator] = None


def init_pipeline_orchestrator(config_manager=None) -> PipelineOrchestrator:
    """
    初始化全域管道協調器

    Args:
        config_manager: 配置管理器實例

    Returns:
        管道協調器實例
    """
    global _pipeline_orchestrator

    if _pipeline_orchestrator is None:
        _pipeline_orchestrator = PipelineOrchestrator(config_manager)

    return _pipeline_orchestrator


def get_pipeline_orchestrator() -> PipelineOrchestrator:
    """獲取全域管道協調器實例"""
    if _pipeline_orchestrator is None:
        raise RuntimeError("管道協調器尚未初始化，請先調用init_pipeline_orchestrator()")
    return _pipeline_orchestrator
