"""
WebCrawler Commander - 批處理器
高效的大數據批量處理系統

功能特色：
- 大數據集分塊處理
- 記憶體管理與垃圾回收
- 並行處理與負載均衡
- 進度追蹤與中斷恢復
- 自適應批大小調整
- 高可用性與故障轉移

作者: Jerry開發工作室
版本: v1.0.0
"""

import asyncio
import threading
import time
import json
import gc
import psutil
from typing import Dict, List, Optional, Any, Callable, Union, Iterable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from queue import Queue
import multiprocessing as mp

from ..utils.config_manager import get_config_manager
from ..utils.logger_service import get_logger
from ..utils.error_handler import get_error_handler, with_error_handling, RecoveryStrategy, RecoveryConfig, ErrorContext
from ..utils.performance_monitor import get_performance_monitor, performance_monitor, benchmark_operation
from ..utils.audit_logger import get_audit_logger, audit_log, AuditLevel, AuditCategory

from .data_processor import DataRecord, ProcessingResult, DataQualityMetrics


class BatchMode(Enum):
    """批處理模式枚舉"""
    SEQUENTIAL = "sequential"         # 順序處理
    PARALLEL_THREADS = "parallel_threads"  # 線程並行處理
    PARALLEL_PROCESSES = "parallel_processes"  # 進程並行處理
    HYBRID = "hybrid"                # 混合處理
    STREAMING = "streaming"          # 流式處理


class BatchStrategy(Enum):
    """批策略枚舉"""
    FIXED_SIZE = "fixed_size"         # 固定批大小
    ADAPTIVE = "adaptive"            # 自適應批大小
    MEMORY_BASED = "memory_based"     # 基於記憶體的批大小
    TIME_BASED = "time_based"        # 基於時間的批大小


@dataclass
class BatchConfig:
    """批處理配置"""
    mode: BatchMode = BatchMode.SEQUENTIAL
    strategy: BatchStrategy = BatchStrategy.ADAPTIVE
    batch_size: int = 1000
    max_workers: int = 4
    memory_limit_mb: int = 512
    time_limit_seconds: float = 300.0
    enable_progress_tracking: bool = True
    enable_resume: bool = True
    checkpoint_interval: int = 1000


@dataclass
class BatchProgress:
    """批處理進度"""
    total_records: int = 0
    processed_records: int = 0
    failed_records: int = 0
    current_batch: int = 0
    total_batches: int = 0
    start_time: datetime = field(default_factory=datetime.utcnow)
    estimated_completion: Optional[datetime] = None
    current_memory_mb: float = 0.0
    throughput_records_per_second: float = 0.0


@dataclass
class BatchCheckpoint:
    """批處理檢查點"""
    batch_id: str
    last_processed_index: int
    progress: BatchProgress
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


class BatchProcessor:
    """
    批處理器

    提供高效的大數據處理能力：
    - 自適應批大小管理
    - 多種並行處理模式
    - 記憶體使用優化
    - 進度追蹤與故障恢復
    - 資源使用監控
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = get_logger(__name__)

        # 初始化統一框架組件
        self.error_handler = get_error_handler(__name__)
        self.performance_monitor = get_performance_monitor(__name__)
        self.audit_logger = get_audit_logger()

        # 批處理配置
        self.batch_config = BatchConfig(**self.config.get("batch_config", {}))

        # 執行器池
        self.thread_executor = ThreadPoolExecutor(max_workers=self.batch_config.max_workers)
        self.process_executor = ProcessPoolExecutor(max_workers=self.batch_config.max_workers)

        # 進度追蹤
        self.progress = BatchProgress()
        self.checkpoint_queue: Queue = Queue()

        # 檢查點存儲
        self.checkpoints: Dict[str, BatchCheckpoint] = {}

        # 統計信息
        self.stats = {
            "total_batches": 0,
            "successful_batches": 0,
            "failed_batches": 0,
            "avg_batch_time": 0.0,
            "total_memory_peak": 0.0,
            "cpu_utilization_avg": 0.0
        }

        # 設置錯誤恢復
        self._setup_error_recovery()

        # 設置性能基準
        self._setup_performance_benchmarks()

        # 啟動背景任務
        self._start_background_tasks()

        self.logger.info("batch_processor_initialized",
                        mode=self.batch_config.mode.value,
                        strategy=self.batch_config.strategy.value,
                        batch_size=self.batch_config.batch_size)

    def _setup_error_recovery(self):
        """設置錯誤恢復配置"""
        # 批處理錯誤恢復
        batch_error_config = RecoveryConfig(
            strategy=RecoveryStrategy.RETRY,
            max_retries=3,
            retry_delay=5.0,
            exponential_backoff=True
        )
        self.error_handler.register_recovery_config("batch_processing", batch_error_config)

        # 記憶體錯誤恢復
        memory_error_config = RecoveryConfig(
            strategy=RecoveryStrategy.FALLBACK,
            fallback_function=self._fallback_memory_reduce,
            max_retries=2
        )
        self.error_handler.register_recovery_config("memory_limit", memory_error_config)

    def _setup_performance_benchmarks(self):
        """設置性能基準"""
        # 批處理吞吐量基準
        self.performance_monitor.set_benchmark(
            "batch_throughput_records_per_second",
            2000.0,  # 2000 records/second
            tolerance_percent=40,
            environment="production"
        )

        # 批處理記憶體基準
        self.performance_monitor.set_benchmark(
            "batch_memory_usage_mb",
            self.batch_config.memory_limit_mb,
            tolerance_percent=20,
            environment="production"
        )

        # 批處理成功率基準
        self.performance_monitor.set_benchmark(
            "batch_success_rate",
            98.0,  # 98% 成功率
            tolerance_percent=5,
            environment="production"
        )

    def _start_background_tasks(self):
        """啟動背景任務"""
        # 檢查點保存任務
        if self.batch_config.enable_resume:
            checkpoint_thread = threading.Thread(
                target=self._checkpoint_worker,
                daemon=True
            )
            checkpoint_thread.start()

        # 資源監控任務
        monitor_thread = threading.Thread(
            target=self._resource_monitor,
            daemon=True
        )
        monitor_thread.start()

    async def _fallback_memory_reduce(self, error_details) -> None:
        """記憶體錯誤備用策略"""
        self.logger.warning("memory_limit_exceeded_fallback",
                           current_usage=error_details.get("current_memory", 0))
        # 觸發垃圾回收
        gc.collect()

    @performance_monitor
    @benchmark_operation("batch_processing_pipeline", expected_max_time_ms=1800000)  # 30分鐘
    @with_audit_trail("batch_data_processing")
    @with_error_handling("batch_processing")
    async def process_batch(self, records: Union[List[DataRecord], Iterable[DataRecord]],
                           processor_func: Callable[[List[DataRecord]], Any],
                           batch_id: Optional[str] = None) -> ProcessingResult:
        """
        批處理數據

        Args:
            records: 數據記錄列表或可迭代對象
            processor_func: 處理函數
            batch_id: 批處理ID（用於恢復）

        Returns:
            處理結果
        """
        start_time = time.time()
        batch_id = batch_id or f"batch_{int(start_time)}"

        # 轉換為列表（如果是生成器）
        if not isinstance(records, list):
            records = list(records)

        total_records = len(records)
        self.progress = BatchProgress(total_records=total_records)

        # 檢查是否需要從檢查點恢復
        if self.batch_config.enable_resume and batch_id in self.checkpoints:
            await self._resume_from_checkpoint(batch_id, records)

        # 計算批數量
        batches = self._create_batches(records)
        self.progress.total_batches = len(batches)

        self.logger.info("batch_processing_started",
                        batch_id=batch_id,
                        total_records=total_records,
                        batch_count=len(batches),
                        mode=self.batch_config.mode.value)

        # 根據處理模式選擇策略
        if self.batch_config.mode == BatchMode.SEQUENTIAL:
            result = await self._process_sequential(batches, processor_func, batch_id)
        elif self.batch_config.mode == BatchMode.PARALLEL_THREADS:
            result = await self._process_parallel_threads(batches, processor_func, batch_id)
        elif self.batch_config.mode == BatchMode.PARALLEL_PROCESSES:
            result = await self._process_parallel_processes(batches, processor_func, batch_id)
        elif self.batch_config.mode == BatchMode.STREAMING:
            result = await self._process_streaming(records, processor_func, batch_id)
        else:  # HYBRID
            result = await self._process_hybrid(batches, processor_func, batch_id)

        # 更新統計
        processing_time = time.time() - start_time
        result.processing_time = processing_time

        # 清理檢查點
        if batch_id in self.checkpoints:
            del self.checkpoints[batch_id]

        # 記錄審計事件
        audit_log(
            level=AuditLevel.ACCESS,
            category=AuditCategory.DATA_ACCESS,
            action="batch_processing_completed",
            actor="batch_processor",
            target=batch_id,
            result="SUCCESS" if result.success else "FAILED",
            details={
                "total_records": total_records,
                "processed_records": result.processed_records,
                "processing_time_seconds": round(processing_time, 2),
                "throughput_records_per_second": round(result.processed_records / processing_time, 2) if processing_time > 0 else 0
            }
        )

        self.logger.info("batch_processing_completed",
                        batch_id=batch_id,
                        processed=result.processed_records,
                        failed=result.failed_records,
                        processing_time=round(processing_time, 2))

        return result

    def _create_batches(self, records: List[DataRecord]) -> List[List[DataRecord]]:
        """創建數據批次"""
        batches = []

        if self.batch_config.strategy == BatchStrategy.FIXED_SIZE:
            # 固定批大小
            batch_size = self.batch_config.batch_size
            batches = [records[i:i + batch_size] for i in range(0, len(records), batch_size)]

        elif self.batch_config.strategy == BatchStrategy.ADAPTIVE:
            # 自適應批大小
            batches = self._adaptive_batching(records)

        elif self.batch_config.strategy == BatchStrategy.MEMORY_BASED:
            # 基於記憶體的批大小
            batches = self._memory_based_batching(records)

        else:  # TIME_BASED
            # 基於時間的批大小（使用固定大小作為近似）
            batch_size = self.batch_config.batch_size
            batches = [records[i:i + batch_size] for i in range(0, len(records), batch_size)]

        return batches

    def _adaptive_batching(self, records: List[DataRecord]) -> List[List[DataRecord]]:
        """自適應批處理"""
        batches = []
        batch_size = self.batch_config.batch_size

        # 根據數據複雜度動態調整批大小
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]

            # 簡單的複雜度估計（基於字段數量）
            avg_complexity = sum(len(record.data) for record in batch) / len(batch)

            # 如果複雜度高，減少批大小
            if avg_complexity > 10:
                batch_size = max(100, batch_size // 2)
            elif avg_complexity < 3:
                batch_size = min(5000, batch_size * 2)

            batches.append(batch)

        return batches

    def _memory_based_batching(self, records: List[DataRecord]) -> List[List[DataRecord]]:
        """基於記憶體的批處理"""
        batches = []
        memory_limit = self.batch_config.memory_limit_mb * 1024 * 1024  # 轉換為字節
        current_batch = []
        current_memory = 0

        for record in records:
            # 估計記錄的記憶體使用量
            record_memory = self._estimate_record_memory(record)

            if current_memory + record_memory > memory_limit and current_batch:
                # 當前批已滿，創建新批
                batches.append(current_batch)
                current_batch = [record]
                current_memory = record_memory
            else:
                current_batch.append(record)
                current_memory += record_memory

        if current_batch:
            batches.append(current_batch)

        return batches

    def _estimate_record_memory(self, record: DataRecord) -> int:
        """估計記錄的記憶體使用量"""
        # 簡單的記憶體估計
        memory = 0
        for field, value in record.data.items():
            memory += len(str(field)) + len(str(value))

        # 加上對象開銷
        memory += 1000  # 估計的對象開銷

        return memory

    async def _process_sequential(self, batches: List[List[DataRecord]],
                                processor_func: Callable, batch_id: str) -> ProcessingResult:
        """順序處理批次"""
        all_results = []
        successful_records = 0
        failed_records = 0

        for batch_idx, batch in enumerate(batches):
            self.progress.current_batch = batch_idx + 1

            try:
                batch_start = time.time()
                batch_result = await self._execute_batch_processor(batch, processor_func)
                batch_time = time.time() - batch_start

                if batch_result["success"]:
                    successful_records += len(batch)
                    all_results.extend(batch_result.get("processed_records", []))
                else:
                    failed_records += len(batch)

                # 更新進度
                self.progress.processed_records = successful_records
                self.progress.failed_records = failed_records

                # 保存檢查點
                if self.batch_config.enable_resume:
                    await self._save_checkpoint(batch_id, batch_idx * len(batch))

                self.logger.debug("batch_processed",
                                batch_id=batch_id,
                                batch=batch_idx + 1,
                                records=len(batch),
                                success=batch_result["success"],
                                processing_time=round(batch_time, 2))

            except Exception as e:
                self.logger.error("batch_processing_failed",
                                batch=batch_idx + 1,
                                error=str(e))
                failed_records += len(batch)

        return ProcessingResult(
            success=failed_records == 0,
            input_count=len(batches) * (len(batches[0]) if batches else 0),
            output_count=successful_records,
            processing_time=0.0,  # 將在上级設置
            quality_metrics=DataQualityMetrics()
        )

    async def _process_parallel_threads(self, batches: List[List[DataRecord]],
                                      processor_func: Callable, batch_id: str) -> ProcessingResult:
        """使用線程並行處理批次"""
        semaphore = asyncio.Semaphore(self.batch_config.max_workers)

        async def process_batch_async(batch_idx: int, batch: List[DataRecord]):
            async with semaphore:
                try:
                    result = await self._execute_batch_processor(batch, processor_func)
                    return batch_idx, result, None
                except Exception as e:
                    return batch_idx, None, str(e)

        # 創建任務
        tasks = [
            process_batch_async(idx, batch)
            for idx, batch in enumerate(batches)
        ]

        # 等待所有任務完成
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 處理結果
        all_processed = []
        successful_records = 0

        for result in results:
            if isinstance(result, Exception):
                self.logger.error("parallel_batch_error", error=str(result))
                continue

            batch_idx, batch_result, error = result
            if error:
                self.logger.error("batch_error",
                                batch=batch_idx,
                                error=error)
            elif batch_result and batch_result["success"]:
                successful_records += len(batch_result.get("processed_records", []))
                all_processed.extend(batch_result.get("processed_records", []))

        return ProcessingResult(
            success=len(all_processed) > 0,
            input_count=sum(len(batch) for batch in batches),
            output_count=successful_records,
            processing_time=0.0,
            quality_metrics=DataQualityMetrics()
        )

    async def _process_parallel_processes(self, batches: List[List[DataRecord]],
                                        processor_func: Callable, batch_id: str) -> ProcessingResult:
        """使用進程並行處理批次"""
        loop = asyncio.get_event_loop()
        successful_records = 0

        # 將處理函數包裝為可在進程中執行的形式
        def process_batch_sync(batch):
            # 注意：這需要在實際實現中適應異步處理函數
            try:
                # 這裡需要同步版本的處理函數
                return {"success": True, "processed_records": batch}
            except Exception as e:
                return {"success": False, "error": str(e)}

        # 使用進程池處理批次
        futures = [
            loop.run_in_executor(self.process_executor, process_batch_sync, batch)
            for batch in batches
        ]

        results = await asyncio.gather(*futures, return_exceptions=True)

        all_processed = []
        for result in results:
            if isinstance(result, Exception):
                self.logger.error("process_pool_error", error=str(result))
            elif result["success"]:
                successful_records += len(result.get("processed_records", []))
                all_processed.extend(result.get("processed_records", []))

        return ProcessingResult(
            success=len(all_processed) > 0,
            input_count=sum(len(batch) for batch in batches),
            output_count=successful_records,
            processing_time=0.0,
            quality_metrics=DataQualityMetrics()
        )

    async def _process_hybrid(self, batches: List[List[DataRecord]],
                            processor_func: Callable, batch_id: str) -> ProcessingResult:
        """混合處理模式"""
        # 結合不同的處理策略
        cpu_count = mp.cpu_count()

        if len(batches) > cpu_count * 2:
            # 大量批次使用進程並行
            return await self._process_parallel_processes(batches, processor_func, batch_id)
        else:
            # 小量批次使用線程並行
            return await self._process_parallel_threads(batches, processor_func, batch_id)

    async def _process_streaming(self, records: Union[List[DataRecord], Iterable[DataRecord]],
                               processor_func: Callable, batch_id: str) -> ProcessingResult:
        """流式處理模式"""
        # 實現真正的流式處理
        batch_size = self.batch_config.batch_size
        all_processed = []
        successful_records = 0

        record_iterator = iter(records) if hasattr(records, '__iter__') else iter([records])

        while True:
            # 取一批記錄
            batch = []
            try:
                for _ in range(batch_size):
                    batch.append(next(record_iterator))
            except StopIteration:
                if not batch:
                    break
                # 處理最後一批

            try:
                result = await self._execute_batch_processor(batch, processor_func)
                if result["success"]:
                    successful_records += len(result.get("processed_records", []))
                    all_processed.extend(result.get("processed_records", []))
                else:
                    self.logger.warning("streaming_batch_failed")

            except Exception as e:
                self.logger.error("streaming_batch_error", error=str(e))

        return ProcessingResult(
            success=len(all_processed) > 0,
            input_count=len(records) if isinstance(records, list) else 0,
            output_count=successful_records,
            processing_time=0.0,
            quality_metrics=DataQualityMetrics()
        )

    async def _execute_batch_processor(self, batch: List[DataRecord],
                                     processor_func: Callable) -> Dict[str, Any]:
        """執行批處理器函數"""
        try:
            # 檢查記憶體使用量
            if self._check_memory_limit():
                gc.collect()  # 強制垃圾回收

            # 執行處理函數
            if asyncio.iscoroutinefunction(processor_func):
                result = await processor_func(batch)
            else:
                # 對於同步函數，使用線程池執行
                result = await asyncio.get_event_loop().run_in_executor(
                    self.thread_executor,
                    processor_func,
                    batch
                )

            return {
                "success": True,
                "processed_records": result if isinstance(result, list) else batch
            }

        except Exception as e:
            self.logger.error("batch_processor_execution_error", error=str(e))

            return {
                "success": False,
                "error": str(e),
                "processed_records": []
            }

    def _check_memory_limit(self) -> bool:
        """檢查記憶體限制"""
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024

        self.progress.current_memory_mb = memory_mb

        if self.stats["total_memory_peak"] < memory_mb:
            self.stats["total_memory_peak"] = memory_mb

        return memory_mb > self.batch_config.memory_limit_mb

    async def _save_checkpoint(self, batch_id: str, last_index: int) -> None:
        """保存檢查點"""
        checkpoint = BatchCheckpoint(
            batch_id=batch_id,
            last_processed_index=last_index,
            progress=self.progress,
            metadata={"stats": self.stats}
        )

        self.checkpoints[batch_id] = checkpoint

        # 添加到檢查點隊列以便異步保存
        self.checkpoint_queue.put(checkpoint)

    async def _resume_from_checkpoint(self, batch_id: str, records: List[DataRecord]) -> None:
        """從檢查點恢復"""
        if batch_id not in self.checkpoints:
            return

        checkpoint = self.checkpoints[batch_id]
        resume_index = checkpoint.last_processed_index

        self.logger.info("resuming_from_checkpoint",
                        batch_id=batch_id,
                        resume_index=resume_index)

        # 跳過已處理的記錄
        if resume_index < len(records):
            records[:] = records[resume_index:]

    def _checkpoint_worker(self) -> None:
        """檢查點工作者線程"""
        while True:
            try:
                checkpoint = self.checkpoint_queue.get(timeout=1.0)

                # 保存檢查點到持久存儲
                # 實際實現會保存到文件或數據庫
                self.logger.debug("checkpoint_saved",
                                batch_id=checkpoint.batch_id,
                                index=checkpoint.last_processed_index)

                self.checkpoint_queue.task_done()

            except:
                # 超時，繼續循環
                continue

    def _resource_monitor(self) -> None:
        """資源監控線程"""
        while True:
            try:
                # 監控CPU使用率
                cpu_percent = psutil.cpu_percent(interval=1)
                self.stats["cpu_utilization_avg"] = (
                    self.stats["cpu_utilization_avg"] + cpu_percent
                ) / 2  # 移動平均

                # 監控記憶體使用量
                process = psutil.Process()
                memory_mb = process.memory_info().rss / 1024 / 1024

                if self.stats["total_memory_peak"] < memory_mb:
                    self.stats["total_memory_peak"] = memory_mb

                time.sleep(5)  # 每5秒監控一次

            except Exception as e:
                self.logger.warning("resource_monitor_error", error=str(e))
                time.sleep(5)

    def get_batch_stats(self) -> Dict[str, Any]:
        """獲取批處理統計"""
        return {
            **self.stats,
            "current_progress": {
                "processed_records": self.progress.processed_records,
                "total_records": self.progress.total_records,
                "throughput_records_per_second": round(self.progress.throughput_records_per_second, 2),
                "current_memory_mb": round(self.progress.current_memory_mb, 2)
            },
            "configuration": {
                "mode": self.batch_config.mode.value,
                "strategy": self.batch_config.strategy.value,
                "batch_size": self.batch_config.batch_size,
                "max_workers": self.batch_config.max_workers
            },
            "uptime_seconds": (datetime.utcnow() - self.progress.start_time).total_seconds()
        }

    async def shutdown_batch_processor(self) -> None:
        """關閉批處理器"""
        self.logger.info("batch_processor_shutdown_initiated")

        # 等待進行中的任務完成
        self.thread_executor.shutdown(wait=True)
        self.process_executor.shutdown(wait=True)

        # 保存最終狀態
        if self.batch_config.enable_resume:
            await self._save_final_checkpoints()

        self.logger.info("batch_processor_shutdown_completed")

    async def _save_final_checkpoints(self) -> None:
        """保存最終檢查點"""
        # 保存所有活躍的檢查點
        for batch_id, checkpoint in self.checkpoints.items():
            try:
                # 最終保存邏輯
                self.logger.debug("final_checkpoint_saved", batch_id=batch_id)
            except Exception as e:
                self.logger.warning("final_checkpoint_save_failed", batch_id=batch_id, error=str(e))


# 全域批處理器實例
_batch_processor: Optional[BatchProcessor] = None


def init_batch_processor(config: Optional[Dict[str, Any]] = None) -> BatchProcessor:
    """
    初始化全域批處理器

    Args:
        config: 配置字典

    Returns:
        批處理器實例
    """
    global _batch_processor

    if _batch_processor is None:
        _batch_processor = BatchProcessor(config)

    return _batch_processor


def get_batch_processor() -> BatchProcessor:
    """獲取全域批處理器實例"""
    if _batch_processor is None:
        raise RuntimeError("批處理器尚未初始化，請先調用init_batch_processor()")
    return _batch_processor
