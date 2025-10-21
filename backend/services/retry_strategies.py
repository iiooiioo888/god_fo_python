"""
WebCrawler Commander - 自適應重試機制模塊
實現智慧重試策略，提升爬蟲任務成功率和系統穩定性

核心功能：
- 指數退避策略 (Exponential Backoff) - 動態調整延遲時間
- 線性退避策略 (Linear Backoff) - 簡單線性增加延遲
- 指數抖動退避 (Exponential Jitter) - 添加隨機性避免同步請求
- HTTP狀態碼智慧重試 (Status Code Aware Retry) - 根據狀態碼決定重試策略
- 自適應延遲調整 (Adaptive Delay Tuning) - 根據響應模式調整策略

作者: Jerry開發工作室
版本: v1.0.0
"""

import asyncio
import random
import time
import math
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque

from ..utils.config_manager import get_config_manager
from ..utils.logger_service import get_logger


class RetryStrategy(Enum):
    """重試策略枚舉"""
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    LINEAR_BACKOFF = "linear_backoff"
    EXPONENTIAL_JITTER = "exponential_jitter"
    FIXED_DELAY = "fixed_delay"
    ADAPTIVE = "adaptive"


@dataclass
class RetryConfig:
    """重試配置數據類"""
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    max_attempts: int = 3
    initial_delay: float = 1.0  # 初始延遲秒數
    max_delay: float = 60.0     # 最大延遲秒數
    backoff_factor: float = 2.0 # 退避因子
    jitter_range: float = 0.1   # 抖動範圍 (相對於延遲的百分比)

    # HTTP狀態碼重試映射
    retry_on_status_codes: List[int] = field(default_factory=lambda: [500, 502, 503, 504, 408, 429])

    # 自適應參數
    enable_adaptive: bool = False
    learning_window: int = 10  # 學習窗口大小
    success_threshold: float = 0.8  # 成功率閾值


@dataclass
class RetryAttempt:
    """重試嘗試記錄數據類"""
    attempt_number: int
    delay_used: float
    start_time: datetime
    end_time: Optional[datetime] = None
    status_code: Optional[int] = None
    error_message: Optional[str] = None
    success: bool = False
    response_time: Optional[float] = None


@dataclass
class RetryResult:
    """重試結果數據類"""
    total_attempts: int
    final_success: bool
    total_time: float
    average_response_time: Optional[float] = None
    attempts: List[RetryAttempt] = field(default_factory=list)
    final_error: Optional[str] = None
    strategy_adapted: bool = False


class ExponentialBackoffStrategy:
    """
    指數退避策略
    實現標準的指數退避算法，適應網路不穩定情況
    """

    def __init__(self, config: RetryConfig):
        self.config = config
        self.logger = get_logger(__name__)

    async def should_retry(self, attempt: int, status_code: Optional[int],
                          error: Optional[Exception]) -> bool:
        """
        判斷是否應該重試

        Args:
            attempt: 當前嘗試次數 (0起始)
            status_code: HTTP狀態碼
            error: 異常對象

        Returns:
            是否重試
        """
        # 檢查最大嘗試次數
        if attempt >= self.config.max_attempts:
            return False

        # 檢查狀態碼
        if status_code and status_code in self.config.retry_on_status_codes:
            return True

        # 檢查異常類型
        if error:
            # 網路相關異常通常可以重試
            retryable_errors = (
                ConnectionError, TimeoutError,
                OSError  # 包括ConnectionResetError等
            )
            if isinstance(error, retryable_errors):
                return True

        return False

    async def get_delay(self, attempt: int) -> float:
        """
        計算延遲時間

        Args:
            attempt: 當前嘗試次數

        Returns:
            延遲秒數
        """
        # 指數退避計算: initial_delay * (backoff_factor ^ attempt)
        base_delay = self.config.initial_delay * (self.config.backoff_factor ** attempt)

        # 應用最大延遲限制
        delay = min(base_delay, self.config.max_delay)

        # 添加抖動 (根據策略配置)
        if self.config.strategy == RetryStrategy.EXPONENTIAL_JITTER:
            jitter = random.uniform(-self.config.jitter_range, self.config.jitter_range)
            delay *= (1.0 + jitter)

        # 確保最小延遲
        delay = max(delay, 0.1)

        self.logger.debug("calculated_retry_delay",
                         attempt=attempt,
                         delay=round(delay, 3),
                         strategy=self.config.strategy.value)

        return delay


class LinearBackoffStrategy:
    """
    線性退避策略
    簡單的線性增加延遲，適用於資源競爭情況
    """

    def __init__(self, config: RetryConfig):
        self.config = config
        self.logger = get_logger(__name__)

    async def should_retry(self, attempt: int, status_code: Optional[int],
                          error: Optional[Exception]) -> bool:
        """判斷是否應該重試"""
        # 使用相同的邏輯作為指數退避
        strategy = ExponentialBackoffStrategy(self.config)
        return await strategy.should_retry(attempt, status_code, error)

    async def get_delay(self, attempt: int) -> float:
        """計算線性延遲"""
        # 線性增加: initial_delay + (attempt * increment)
        increment = self.config.initial_delay * 0.5  # 每次增加初始延遲的一半
        delay = self.config.initial_delay + (attempt * increment)

        # 應用最大延遲限制
        delay = min(delay, self.config.max_delay)

        # 確保最小延遲
        delay = max(delay, 0.1)

        self.logger.debug("calculated_linear_retry_delay",
                         attempt=attempt,
                         delay=round(delay, 3))

        return delay


class AdaptiveRetryStrategy:
    """
    自適應重試策略
    基於歷史表現動態調整重試參數
    """

    def __init__(self, config: RetryConfig):
        self.config = config
        self.logger = get_logger(__name__)

        # 學習歷史
        self.success_history: deque = deque(maxlen=config.learning_window)
        self.response_times: deque = deque(maxlen=config.learning_window)
        self.strategy_performance: Dict[str, float] = defaultdict(float)

        # 自適應參數
        self.current_backoff_factor = config.backoff_factor
        self.current_initial_delay = config.initial_delay

    async def should_retry(self, attempt: int, status_code: Optional[int],
                          error: Optional[Exception]) -> bool:
        """基於學習的智能重試決策"""
        # 如果學習數據不足，使用保守策略
        if len(self.success_history) < 5:
            strategy = ExponentialBackoffStrategy(self.config)
            return await strategy.should_retry(attempt, status_code, error)

        # 計算當前成功率
        success_rate = sum(self.success_history) / len(self.success_history)

        # 如果成功率很低，減少重試次數
        if success_rate < 0.3:
            return attempt < min(self.config.max_attempts, 2)

        # 如果成功率很高，增加重試積極性
        elif success_rate > self.config.success_threshold:
            return attempt < self.config.max_attempts + 1

        return attempt < self.config.max_attempts

    async def get_delay(self, attempt: int) -> float:
        """自適應延遲計算"""
        if len(self.response_times) < 3:
            # 數據不足，使用默認指數退避
            strategy = ExponentialBackoffStrategy(self.config)
            return await strategy.get_delay(attempt)

        # 基於平均響應時間調整
        avg_response_time = statistics.mean(self.response_times)

        # 如果響應很慢，增加初始延遲
        if avg_response_time > 5.0:  # 5秒
            adaptive_delay = self.config.initial_delay * 2.0
        elif avg_response_time > 2.0:  # 2秒
            adaptive_delay = self.config.initial_delay * 1.5
        else:
            adaptive_delay = self.config.initial_delay

        # 指數退避
        base_delay = adaptive_delay * (self.current_backoff_factor ** attempt)
        delay = min(base_delay, self.config.max_delay)

        # 添加學習到的抖動
        if self.success_history:
            success_rate = sum(self.success_history) / len(self.success_history)
            # 成功率越高，抖動越小
            adaptive_jitter = self.config.jitter_range * (1.0 - success_rate)
            if adaptive_jitter > 0:
                jitter = random.uniform(-adaptive_jitter, adaptive_jitter)
                delay *= (1.0 + jitter)

        delay = max(delay, 0.1)

        self.logger.debug("adaptive_retry_delay",
                         attempt=attempt,
                         delay=round(delay, 3),
                         avg_response_time=round(avg_response_time, 3),
                         success_rate=round(success_rate, 3) if 'success_rate' in locals() else 0)

        return delay

    def record_attempt(self, success: bool, response_time: Optional[float]):
        """記錄重試嘗試結果，用於學習"""
        self.success_history.append(1 if success else 0)

        if response_time is not None:
            self.response_times.append(response_time)

        # 每10個樣本調整策略參數
        if len(self.success_history) % 10 == 0:
            self._adjust_strategy_parameters()

    def _adjust_strategy_parameters(self):
        """基於學習數據調整策略參數"""
        if len(self.success_history) < 10:
            return

        success_rate = sum(self.success_history) / len(self.success_history)
        avg_response_time = statistics.mean(self.response_times) if self.response_times else 0

        # 如果成功率很高，稍微增加退避因子以降低請求頻率
        if success_rate > 0.9:
            self.current_backoff_factor = min(self.current_backoff_factor * 1.1, 3.0)

        # 如果成功率很低，減少退避因子以加快重試
        elif success_rate < 0.5:
            self.current_backoff_factor = max(self.current_backoff_factor * 0.9, 1.5)

        # 如果響應時間很慢，增加初始延遲
        if avg_response_time > 3.0:
            self.current_initial_delay = min(self.current_initial_delay * 1.2, 5.0)

        # 如果響應時間很快，減少初始延遲
        elif avg_response_time < 1.0 and success_rate > 0.8:
            self.current_initial_delay = max(self.current_initial_delay * 0.8, 0.2)


class FailurePatternAnalyzer:
    """
    失敗模式分析器
    識別常見的失敗模式並建議改進策略
    """

    def __init__(self):
        self.failure_patterns: Dict[str, int] = defaultdict(int)
        self.error_code_patterns: Dict[int, int] = defaultdict(int)
        self.time_based_failures: Dict[str, int] = defaultdict(int)

    def analyze_failure(self, error: Exception, status_code: Optional[int],
                       timestamp: datetime) -> str:
        """
        分析失敗模式

        Args:
            error: 異常對象
            status_code: HTTP狀態碼
            timestamp: 發生時間

        Returns:
            失敗模式描述
        """
        pattern = "unknown"

        # 分析異常類型
        if isinstance(error, ConnectionError):
            pattern = "connection_error"
        elif isinstance(error, TimeoutError):
            pattern = "timeout_error"
        elif isinstance(error, OSError):
            if "Connection reset" in str(error):
                pattern = "connection_reset"
            elif "Connection refused" in str(error):
                pattern = "connection_refused"
            else:
                pattern = "os_error"

        # 分析狀態碼
        if status_code:
            if status_code == 429:
                pattern = "rate_limited"
            elif status_code == 503:
                pattern = "service_unavailable"
            elif status_code == 502:
                pattern = "bad_gateway"
            elif status_code >= 500:
                pattern = "server_error"
            elif status_code >= 400:
                pattern = "client_error"

        # 分析時間模式
        hour = timestamp.hour
        if 2 <= hour <= 5:  # 維護時間
            pattern += "_maintenance_window"
        elif 9 <= hour <= 17:  # 工作時間，高負載
            pattern += "_peak_hours"

        # 記錄模式
        self.failure_patterns[pattern] += 1
        if status_code:
            self.error_code_patterns[status_code] += 1

        self.time_based_failures[f"{timestamp.date()}_{hour}"] += 1

        return pattern

    def get_pattern_insights(self) -> Dict[str, Any]:
        """獲取失敗模式分析結果"""
        insights = {
            "most_common_pattern": max(self.failure_patterns, key=self.failure_patterns.get, default="none"),
            "most_common_error_code": max(self.error_code_patterns, key=self.error_code_patterns.get, default=None),
            "pattern_distribution": dict(self.failure_patterns),
            "error_code_distribution": dict(self.error_code_patterns),
            "recommendations": []
        }

        # 生成改進建議
        total_failures = sum(self.failure_patterns.values())

        if total_failures > 10:
            # 分析常見模式
            if self.failure_patterns.get("timeout_error", 0) > total_failures * 0.3:
                insights["recommendations"].append("增加請求超時時間或減少並發請求")

            if self.failure_patterns.get("rate_limited", 0) > total_failures * 0.2:
                insights["recommendations"].append("降低請求頻率，增加延遲間隔")

            if self.failure_patterns.get("connection_reset", 0) > total_failures * 0.2:
                insights["recommendations"].append("檢查網路穩定性，使用代理IP輪換")

            if any(pattern.endswith("_maintenance_window") for pattern in self.failure_patterns):
                insights["recommendations"].append("避免在維護時間窗口(2-5點)執行爬蟲任務")

        return insights


class RetryManager:
    """
    重試管理器主類
    整合各種重試策略，提供統一的介面
    """

    def __init__(self, config: Optional[RetryConfig] = None):
        self.config = config or RetryConfig()
        self.logger = get_logger(__name__)

        # 初始化策略
        self.strategies = {
            RetryStrategy.EXPONENTIAL_BACKOFF: ExponentialBackoffStrategy(self.config),
            RetryStrategy.LINEAR_BACKOFF: LinearBackoffStrategy(self.config),
            RetryStrategy.EXPONENTIAL_JITTER: ExponentialBackoffStrategy(self.config),
            RetryStrategy.FIXED_DELAY: ExponentialBackoffStrategy(self.config),  # 使用指數邏輯但固定因子
            RetryStrategy.ADAPTIVE: AdaptiveRetryStrategy(self.config)
        }

        # 統計和監控
        self.failure_analyzer = FailurePatternAnalyzer()
        self.retry_statistics: Dict[str, Any] = {
            "total_retries": 0,
            "successful_retries": 0,
            "failed_retries": 0,
            "average_retry_delay": 0.0,
            "retry_patterns": defaultdict(int)
        }

    async def execute_with_retry(self, func: Callable, *args, **kwargs) -> Tuple[Any, RetryResult]:
        """
        使用重試機制執行函數

        Args:
            func: 要執行的函數
            *args: 位置參數
            **kwargs: 關鍵字參數

        Returns:
            (最終結果, 重試結果統計)
        """
        strategy = self.strategies.get(self.config.strategy)
        if not strategy:
            raise ValueError(f"未知的重試策略: {self.config.strategy}")

        attempts = []
        start_time = datetime.utcnow()

        for attempt in range(self.config.max_attempts + 1):
            attempt_start = datetime.utcnow()

            try:
                result = await func(*args, **kwargs)
                response_time = (datetime.utcnow() - attempt_start).total_seconds()

                # 記錄成功嘗試
                attempt_record = RetryAttempt(
                    attempt_number=attempt,
                    delay_used=0.0,  # 第一個嘗試沒有延遲
                    start_time=attempt_start,
                    end_time=datetime.utcnow(),
                    success=True,
                    response_time=response_time
                )
                attempts.append(attempt_record)

                # 如果啟用自適應學習，記錄成功
                if self.config.enable_adaptive and isinstance(strategy, AdaptiveRetryStrategy):
                    strategy.record_attempt(True, response_time)

                # 統計更新
                self.retry_statistics["successful_retries"] += 1

                retry_result = RetryResult(
                    total_attempts=len(attempts),
                    final_success=True,
                    total_time=(datetime.utcnow() - start_time).total_seconds(),
                    attempts=attempts,
                    average_response_time=statistics.mean([a.response_time for a in attempts if a.response_time])
                )

                self.logger.info("retry_execution_successful",
                               total_attempts=len(attempts),
                               final_response_time=response_time)

                return result, retry_result

            except Exception as e:
                response_time = (datetime.utcnow() - attempt_start).total_seconds()

                # 分析失敗模式
                pattern = self.failure_analyzer.analyze_failure(e, None, attempt_start)

                # 記錄失敗嘗試
                attempt_record = RetryAttempt(
                    attempt_number=attempt,
                    delay_used=0.0,
                    start_time=attempt_start,
                    end_time=datetime.utcnow(),
                    success=False,
                    error_message=str(e),
                    response_time=response_time
                )
                attempts.append(attempt_record)

                self.retry_statistics["failed_retries"] += 1
                self.retry_statistics["retry_patterns"][pattern] += 1

                # 如果啟用自適應學習，記錄失敗
                if self.config.enable_adaptive and isinstance(strategy, AdaptiveRetryStrategy):
                    strategy.record_attempt(False, response_time)

                # 檢查是否應該重試
                should_retry = await strategy.should_retry(attempt, None, e)

                if not should_retry or attempt >= self.config.max_attempts:
                    # 最終失敗
                    retry_result = RetryResult(
                        total_attempts=len(attempts),
                        final_success=False,
                        total_time=(datetime.utcnow() - start_time).total_seconds(),
                        attempts=attempts,
                        final_error=str(e),
                        average_response_time=statistics.mean([a.response_time for a in attempts if a.response_time]) if any(a.response_time for a in attempts) else None
                    )

                    self.logger.warning("retry_execution_failed",
                                      total_attempts=len(attempts),
                                      final_error=str(e),
                                      most_common_pattern=pattern)

                    raise e

                # 計算延遲時間
                delay = await strategy.get_delay(attempt)

                # 更新嘗試記錄的延遲
                attempt_record.delay_used = delay

                self.retry_statistics["total_retries"] += 1

                # 記錄延遲統計
                if self.retry_statistics["average_retry_delay"] == 0:
                    self.retry_statistics["average_retry_delay"] = delay
                else:
                    self.retry_statistics["average_retry_delay"] = (
                        (self.retry_statistics["average_retry_delay"] * (self.retry_statistics["total_retries"] - 1)) + delay
                    ) / self.retry_statistics["total_retries"]

                self.logger.debug("retry_attempt_failed_waiting",
                                attempt=attempt + 1,
                                max_attempts=self.config.max_attempts + 1,
                                delay=round(delay, 3),
                                error=str(e))

                # 等待延遲
                await asyncio.sleep(delay)

        # 不應該到達這裡，但為了完整性
        raise RuntimeError("重試邏輯錯誤")

    def get_retry_statistics(self) -> Dict[str, Any]:
        """獲取重試統計信息"""
        stats = self.retry_statistics.copy()
        stats["failure_analysis"] = self.failure_analyzer.get_pattern_insights()
        return stats

    def update_config(self, new_config: RetryConfig):
        """更新重試配置"""
        self.config = new_config

        # 重新初始化策略
        self.strategies = {
            RetryStrategy.EXPONENTIAL_BACKOFF: ExponentialBackoffStrategy(self.config),
            RetryStrategy.LINEAR_BACKOFF: LinearBackoffStrategy(self.config),
            RetryStrategy.EXPONENTIAL_JITTER: ExponentialBackoffStrategy(self.config),
            RetryStrategy.FIXED_DELAY: ExponentialBackoffStrategy(self.config),
            RetryStrategy.ADAPTIVE: AdaptiveRetryStrategy(self.config)
        }

        self.logger.info("retry_config_updated", strategy=self.config.strategy.value)


# 全域重試管理器實例
_retry_manager: Optional[RetryManager] = None


def init_retry_manager(config: Optional[RetryConfig] = None) -> RetryManager:
    """
    初始化全域重試管理器

    Args:
        config: 重試配置

    Returns:
        重試管理器實例
    """
    global _retry_manager

    if _retry_manager is None:
        _retry_manager = RetryManager(config)

    return _retry_manager


def get_retry_manager() -> RetryManager:
    """獲取全域重試管理器實例"""
    if _retry_manager is None:
        raise RuntimeError("重試管理器尚未初始化，請先調用init_retry_manager()")
    return _retry_manager


# 便捷函數
async def execute_with_retry(func: Callable, config: Optional[RetryConfig] = None, *args, **kwargs) -> Tuple[Any, RetryResult]:
    """
    便捷的重試執行函數

    Args:
        func: 要執行的函數
        config: 重試配置（可選）
        *args: 位置參數
        **kwargs: 關鍵字參數

    Returns:
        (函數結果, 重試統計)
    """
    manager = get_retry_manager() if _retry_manager else RetryManager(config or RetryConfig())
    return await manager.execute_with_retry(func, *args, **kwargs)
