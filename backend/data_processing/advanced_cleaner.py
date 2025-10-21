"""
WebCrawler Commander - 高級數據清理器
先進的數據清理和規範化處理器

功能特色：
- AI輔助數據清理 (機器學習異常檢測)
- 語言檢測與多語言處理
- 統計異常值檢測與修復
- 數據去噪與平滑處理
- 模式學習與智能填充
- 高級編碼處理與Unicode規範化

作者: Jerry開發工作室
版本: v1.0.0
"""

import asyncio
import re
import json
import hashlib
import statistics
import unicodedata
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import math

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import chardet
import ftfy
import langdetect

from ..utils.config_manager import get_config_manager
from ..utils.logger_service import get_logger
from ..utils.error_handler import get_error_handler, with_error_handling, RecoveryStrategy, RecoveryConfig, ErrorContext
from ..utils.performance_monitor import get_performance_monitor, performance_monitor, benchmark_operation
from ..utils.audit_logger import get_audit_logger, audit_log, AuditLevel, AuditCategory

from .data_processor import DataRecord, DataQualityMetrics


class CleanStrategy(Enum):
    """清理策略枚舉"""
    CONSERVATIVE = "conservative"      # 保守策略 - 只處理明顯錯誤
    MODERATE = "moderate"            # 中等策略 - 平衡清理與保持
    AGGRESSIVE = "aggressive"        # 激進策略 - 大幅清理和規範化
    AI_ENHANCED = "ai_enhanced"      # AI增強 - 使用機器學習


class NoiseLevel(Enum):
    """噪聲等級枚舉"""
    LOW = "low"                      # 低噪聲
    MEDIUM = "medium"               # 中等噪聲
    HIGH = "high"                   # 高噪聲
    AUTO = "auto"                   # 自動檢測


@dataclass
class CleaningRule:
    """清理規則配置"""
    name: str
    rule_type: str
    priority: int = 1
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AdvancedCleaningMetrics:
    """高級清理指標"""
    ai_detections: int = 0
    language_corrections: int = 0
    statistical_outliers: int = 0
    encoding_fixes: int = 0
    pattern_learning: int = 0
    noise_reduction: float = 0.0
    confidence_scores: List[float] = field(default_factory=list)


class AdvancedDataCleaner:
    """
    高級數據清理器

    提供AI增強的數據清理功能：
    - 機器學習異常檢測
    - 多語言處理與規範化
    - 統計分析與異常值處理
    - 智能編碼檢測與修復
    - 模式學習與預測填充
    - 數據去噪與優化
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = get_logger(__name__)

        # 初始化統一框架組件
        self.error_handler = get_error_handler(__name__)
        self.performance_monitor = get_performance_monitor(__name__)
        self.audit_logger = get_audit_logger()

        # 清理策略
        self.clean_strategy = CleanStrategy(self.config.get("clean_strategy", "moderate"))

        # 噪聲檢測等級
        self.noise_level = NoiseLevel(self.config.get("noise_level", "auto"))

        # AI模型
        self.isolation_forest = None
        self.scaler = StandardScaler()

        # 語言檢測快取
        self.language_cache: Dict[str, str] = {}
        self.encoding_cache: Dict[str, str] = {}

        # 清理指標
        self.metrics = AdvancedCleaningMetrics()

        # 清理規則
        self.cleaning_rules: List[CleaningRule] = self._init_cleaning_rules()

        # 正則表達式模式
        self._compile_patterns()

        # 設置錯誤恢復
        self._setup_error_recovery()

        # 設置性能基準
        self._setup_performance_benchmarks()

        self.logger.info("advanced_data_cleaner_initialized", strategy=self.clean_strategy.value)

    def _init_cleaning_rules(self) -> List[CleaningRule]:
        """初始化清理規則"""
        rules = [
            CleaningRule(
                name="ai_anomaly_detection",
                rule_type="ai",
                priority=1,
                enabled=self.clean_strategy == CleanStrategy.AI_ENHANCED,
                config={"contamination": 0.1}
            ),
            CleaningRule(
                name="language_detection",
                rule_type="language",
                priority=2,
                enabled=True,
                config={"confidence_threshold": 0.7}
            ),
            CleaningRule(
                name="encoding_normalization",
                rule_type="encoding",
                priority=3,
                enabled=True,
                config={"fallback_encoding": "utf-8"}
            ),
            CleaningRule(
                name="statistical_outlier_removal",
                rule_type="statistics",
                priority=4,
                enabled=self.clean_strategy in [CleanStrategy.MODERATE, CleanStrategy.AGGRESSIVE, CleanStrategy.AI_ENHANCED],
                config={"method": "iqr", "multiplier": 1.5}
            ),
            CleaningRule(
                name="pattern_learning_fill",
                rule_type="pattern",
                priority=5,
                enabled=self.clean_strategy == CleanStrategy.AI_ENHANCED,
                config={"min_samples": 100}
            ),
            CleaningRule(
                name="noise_reduction",
                rule_type="noise",
                priority=6,
                enabled=True,
                config={"reduction_factor": 0.1}
            )
        ]

        return rules

    def _compile_patterns(self) -> None:
        """編譯正則表達式模式"""
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'\b\+?[\d\s\-\(\)]{7,}\b')
        self.url_pattern = re.compile(r'https?://[^\s<>"\']+' , re.I)
        self.currency_pattern = re.compile(r'\b[$€£¥]\s*\d+(?:[,.]\d+)*\b')
        self.date_pattern = re.compile(r'\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b')

        # 噪聲字符模式
        self.noise_chars = re.compile(r'[\u200B-\u200D\uFEFF\u00A0\u00AD\u2000-\u200A\u2028-\u2029\u0080-\u00BF]+')

    def _setup_error_recovery(self):
        """設置錯誤恢復配置"""
        # AI清理錯誤恢復
        ai_error_config = RecoveryConfig(
            strategy=RecoveryStrategy.SKIP,
            max_retries=1
        )
        self.error_handler.register_recovery_config("ai_cleaning_error", ai_error_config)

        # 編碼錯誤恢復
        encoding_error_config = RecoveryConfig(
            strategy=RecoveryStrategy.FALLBACK,
            fallback_function=self._fallback_encoding,
            max_retries=2
        )
        self.error_handler.register_recovery_config("encoding_error", encoding_error_config)

    def _setup_performance_benchmarks(self):
        """設置性能基準"""
        # 清理速度基準
        self.performance_monitor.set_benchmark(
            "advanced_cleaning_speed_records_per_second",
            500.0,  # 500記錄/秒
            tolerance_percent=30,
            environment="production"
        )

        # 記憶體使用基準
        self.performance_monitor.set_benchmark(
            "advanced_cleaning_memory_mb",
            1024.0,  # 1GB記憶體限制
            tolerance_percent=25,
            environment="production"
        )

    async def _fallback_encoding(self, error_details) -> None:
        """編碼錯誤備用策略"""
        self.logger.warning("using_fallback_encoding_strategy",
                           original_error=error_details.message)

    @performance_monitor
    @benchmark_operation("advanced_cleaning", expected_max_time_ms=300000)  # 5分鐘
    @with_audit_trail("advanced_data_cleaning")
    @with_error_handling("data_processing")
    async def clean_data_advanced(self, records: List[DataRecord],
                                custom_rules: Optional[List[Dict[str, Any]]] = None) -> List[DataRecord]:
        """
        高級數據清理

        Args:
            records: 數據記錄列表
            custom_rules: 自定義清理規則

        Returns:
            清理後的記錄列表
        """
        start_time = datetime.utcnow()
        self.logger.info("starting_advanced_cleaning", record_count=len(records))

        # 初始化AI模型
        await self._initialize_ai_models(records)

        # 應用自定義規則
        if custom_rules:
            await self._apply_custom_rules(custom_rules)

        # 按優先級執行清理規則
        sorted_rules = sorted(self.cleaning_rules, key=lambda r: r.priority)

        processed_records = records.copy()

        for rule in sorted_rules:
            if rule.enabled:
                try:
                    self.logger.debug("applying_cleaning_rule", rule=rule.name)

                    rule_start = datetime.utcnow()
                    processed_records = await self._apply_cleaning_rule(rule, processed_records)
                    rule_time = (datetime.utcnow() - rule_start).total_seconds()

                    self.logger.debug("rule_applied",
                                    rule=rule.name,
                                    processing_time=round(rule_time, 2))

                except Exception as e:
                    self.logger.warning("cleaning_rule_failed",
                                      rule=rule.name,
                                      error=str(e))

                    # 繼續處理其他規則
                    continue

        # 最終數據修復和驗證
        final_records = await self._final_data_repair(processed_records)

        # 更新指標
        self.metrics.confidence_scores = [r.quality_score for r in final_records if r.quality_score > 0]

        processing_time = (datetime.utcnow() - start_time).total_seconds()

        # 記錄審計事件
        audit_log(
            level=AuditLevel.ACCESS,
            category=AuditCategory.DATA_ACCESS,
            action="advanced_cleaning_completed",
            actor="advanced_data_cleaner",
            target="data_records",
            result="SUCCESS",
            details={
                "record_count": len(records),
                "processed_count": len(final_records),
                "processing_time_seconds": round(processing_time, 2),
                "ai_detections": self.metrics.ai_detections,
                "quality_improvement": self._calculate_quality_improvement(records, final_records)
            }
        )

        self.logger.info("advanced_cleaning_completed",
                        input_count=len(records),
                        output_count=len(final_records),
                        processing_time=round(processing_time, 2),
                        ai_detections=self.metrics.ai_detections)

        return final_records

    async def _initialize_ai_models(self, records: List[DataRecord]) -> None:
        """初始化AI模型"""
        if self.clean_strategy != CleanStrategy.AI_ENHANCED:
            return

        try:
            # 準備數據用於機器學習
            numerical_data = []
            text_data = []

            for record in records:
                # 提取數值特徵
                numerical_features = []
                for field, value in record.data.items():
                    if isinstance(value, (int, float)):
                        numerical_features.append(float(value))
                    elif isinstance(value, str) and value.replace('.', '').isdigit():
                        try:
                            numerical_features.append(float(value))
                        except:
                            continue

                if len(numerical_features) >= 3:  # 最少3個數值特徵
                    numerical_data.append(numerical_features)

                # 提取文本特徵
                text_features = []
                for field, value in record.data.items():
                    if isinstance(value, str):
                        text_features.append(value)

                if text_features:
                    text_data.append(' '.join(text_features[:3]))  # 使用前3個文本字段

            # 訓練隔離森林
            if len(numerical_data) >= 50:
                numerical_array = np.array(numerical_data)
                scaled_data = self.scaler.fit_transform(numerical_array)

                self.isolation_forest = IsolationForest(
                    contamination=0.1,
                    random_state=42,
                    n_estimators=100
                )
                self.isolation_forest.fit(scaled_data)

                self.logger.info("ai_models_initialized",
                               numerical_samples=len(numerical_data),
                               text_samples=len(text_data))

        except Exception as e:
            self.logger.warning("ai_model_initialization_failed", error=str(e))

    async def _apply_custom_rules(self, custom_rules: List[Dict[str, Any]]) -> None:
        """應用自定義規則"""
        for rule_dict in custom_rules:
            rule = CleaningRule(
                name=rule_dict.get("name", f"custom_rule_{len(self.cleaning_rules)}"),
                rule_type=rule_dict.get("type", "custom"),
                priority=rule_dict.get("priority", 10),
                enabled=rule_dict.get("enabled", True),
                config=rule_dict.get("config", {})
            )
            self.cleaning_rules.append(rule)

        self.logger.debug("custom_rules_applied", count=len(custom_rules))

    async def _apply_cleaning_rule(self, rule: CleaningRule,
                                 records: List[DataRecord]) -> List[DataRecord]:
        """應用單個清理規則"""
        if rule.rule_type == "ai":
            return await self._apply_ai_detection(rule, records)
        elif rule.rule_type == "language":
            return await self._apply_language_processing(rule, records)
        elif rule.rule_type == "encoding":
            return await self._apply_encoding_normalization(rule, records)
        elif rule.rule_type == "statistics":
            return await self._apply_statistical_outlier_removal(rule, records)
        elif rule.rule_type == "pattern":
            return await self._apply_pattern_learning(rule, records)
        elif rule.rule_type == "noise":
            return await self._apply_noise_reduction(rule, records)
        else:
            self.logger.warning("unknown_rule_type", rule_type=rule.rule_type)
            return records

    async def _apply_ai_detection(self, rule: CleaningRule,
                                records: List[DataRecord]) -> List[DataRecord]:
        """應用AI異常檢測"""
        if not self.isolation_forest:
            return records

        try:
            processed_records = []

            for record in records:
                # 提取數值特徵
                numerical_features = []
                feature_fields = []

                for field, value in record.data.items():
                    if isinstance(value, (int, float)):
                        numerical_features.append(float(value))
                        feature_fields.append(field)
                    elif isinstance(value, str) and value.replace('.', '').isdigit():
                        try:
                            numerical_features.append(float(value))
                            feature_fields.append(field)
                        except:
                            continue

                if len(numerical_features) >= 3:
                    # AI異常檢測
                    features_array = np.array([numerical_features])
                    scaled_features = self.scaler.transform(features_array)

                    anomaly_score = self.isolation_forest.decision_function(scaled_features)[0]
                    prediction = self.isolation_forest.predict(scaled_features)[0]

                    if prediction == -1:  # 異常記錄
                        # 修復異常值
                        for i, field in enumerate(feature_fields):
                            original_value = numerical_features[i]
                            # 使用中位數替換異常值
                            median_value = await self._calculate_field_median(records, field)

                            if median_value is not None:
                                record.set_field(field, median_value,
                                               f"ai_anomaly_replacement_{original_value}")
                                record.add_error(f"字段 '{field}' 檢測到異常值，已替換為中位數 {median_value}")
                                self.metrics.ai_detections += 1

                processed_records.append(record)

            return processed_records

        except Exception as e:
            self.logger.error("ai_detection_failed", error=str(e))
            return records

    async def _calculate_field_median(self, records: List[DataRecord], field: str) -> Optional[float]:
        """計算字段的中位數"""
        values = []
        for record in records:
            value = record.get_field(field)
            if isinstance(value, (int, float)):
                values.append(float(value))
            elif isinstance(value, str) and value.replace('.', '').isdigit():
                try:
                    values.append(float(value))
                except:
                    continue

        if values:
            return statistics.median(values)
        return None

    async def _apply_language_processing(self, rule: CleaningRule,
                                       records: List[DataRecord]) -> List[DataRecord]:
        """應用語言處理和規範化"""
        confidence_threshold = rule.config.get("confidence_threshold", 0.7)

        processed_records = []

        for record in records:
            processed_record = DataRecord(record.data.copy(), record.source)

            for field, value in record.data.items():
                if isinstance(value, str) and len(value.strip()) > 10:
                    try:
                        # 檢測語言
                        cache_key = hashlib.md5(value.encode()).hexdigest()[:8]
                        if cache_key not in self.language_cache:
                            detected = langdetect.detect_langs(value)
                            if detected and detected[0].prob >= confidence_threshold:
                                self.language_cache[cache_key] = detected[0].lang
                            else:
                                self.language_cache[cache_key] = None

                        language = self.language_cache[cache_key]

                        if language:
                            # 根據語言進行規範化處理
                            if language in ['zh', 'zh-cn', 'zh-tw']:
                                # 中文處理
                                normalized = self._normalize_chinese_text(value)
                            elif language in ['ja', 'ko']:
                                # 日韓文處理
                                normalized = self._normalize_cjk_text(value)
                            else:
                                # 其他語言的基礎處理
                                normalized = unicodedata.normalize('NFC', value)

                            if normalized != value:
                                processed_record.set_field(field, normalized,
                                                         f"language_normalization_{language}")
                                self.metrics.language_corrections += 1

                    except Exception as e:
                        # 語言檢測失敗，跳過
                        processed_record.set_field(field, value)

                else:
                    processed_record.set_field(field, value)

            # 複製其他屬性
            processed_record.quality_score = record.quality_score
            processed_record.processing_errors = record.processing_errors.copy()
            processed_record.transformation_log = record.transformation_log.copy()

            processed_records.append(processed_record)

        return processed_records

    def _normalize_chinese_text(self, text: str) -> str:
        """規範化中文文本"""
        # 將全角字符轉換為半角
        normalized = text.translate(str.maketrans({
            '０': '0', '１': '1', '２': '2', '３': '3', '４': '4',
            '５': '5', '６': '6', '７': '7', '８': '8', '９': '9',
            'Ａ': 'A', 'Ｂ': 'B', 'Ｃ': 'C', 'Ｄ': 'D', 'Ｅ': 'E',
            '．': '.', '，': ',', '；': ';', '：': ':', '！': '!',
            '？': '?', '（': '(', '）': ')', '【': '[', '】': ']'
        }))

        # Unicode規範化
        normalized = unicodedata.normalize('NFC', normalized)

        return normalized

    def _normalize_cjk_text(self, text: str) -> str:
        """規範化中日韓文本"""
        # NFC規範化
        normalized = unicodedata.normalize('NFC', text)

        # 移除不必要的零寬字符
        normalized = self.noise_chars.sub('', normalized)

        return normalized

    async def _apply_encoding_normalization(self, rule: CleaningRule,
                                          records: List[DataRecord]) -> List[DataRecord]:
        """應用編碼規範化和修復"""
        fallback_encoding = rule.config.get("fallback_encoding", "utf-8")

        processed_records = []

        for record in records:
            processed_record = DataRecord(record.data.copy(), record.source)

            for field, value in record.data.items():
                if isinstance(value, str):
                    original_value = value

                    try:
                        # 編碼檢測和修復
                        cache_key = hashlib.md5(value.encode('utf-8', errors='ignore')).hexdigest()[:8]

                        if cache_key not in self.encoding_cache:
                            detected = chardet.detect(value.encode('utf-8', errors='ignore'))
                            if detected['confidence'] > 0.8:
                                self.encoding_cache[cache_key] = detected['encoding']

                        detected_encoding = self.encoding_cache.get(cache_key)

                        if detected_encoding and detected_encoding.lower() != 'utf-8':
                            # 嘗試解碼並重新編碼
                            try:
                                decoded = value.encode(detected_encoding).decode('utf-8')
                                processed_record.set_field(field, decoded,
                                                         f"encoding_fix_{detected_encoding}")
                                self.metrics.encoding_fixes += 1
                            except:
                                # 編碼修復失敗，使用ftfy
                                fixed = ftfy.fix_encoding(value)
                                if fixed != value:
                                    processed_record.set_field(field, fixed,
                                                             f"encoding_fix_ftfy")
                                    self.metrics.encoding_fixes += 1

                        else:
                            # 使用ftfy進行通用修復
                            fixed = ftfy.fix_text(value)
                            if fixed != value:
                                processed_record.set_field(field, fixed, "encoding_fix_ftfy")
                                self.metrics.encoding_fixes += 1

                    except Exception as e:
                        self.logger.debug("encoding_fix_failed",
                                        field=field,
                                        error=str(e))
                        processed_record.set_field(field, original_value)

            # 複製其他屬性
            processed_record.quality_score = record.quality_score
            processed_record.processing_errors = record.processing_errors.copy()
            processed_record.transformation_log = record.transformation_log.copy()

            processed_records.append(processed_record)

        return processed_records

    async def _apply_statistical_outlier_removal(self, rule: CleaningRule,
                                               records: List[DataRecord]) -> List[DataRecord]:
        """應用統計異常值移除"""
        method = rule.config.get("method", "iqr")
        multiplier = rule.config.get("multiplier", 1.5)

        processed_records = []

        for record in records:
            processed_record = DataRecord(record.data.copy(), record.source)

            for field, value in record.data.items():
                if isinstance(value, (int, float)):
                    # 檢查是否為異常值
                    is_outlier = False

                    if method == "iqr":
                        is_outlier = await self._is_outlier_iqr(records, field, value, multiplier)
                    elif method == "zscore":
                        is_outlier = await self._is_outlier_zscore(records, field, value, multiplier)

                    if is_outlier:
                        # 替換為中位數
                        median_value = await self._calculate_field_median(records, field)
                        if median_value is not None:
                            processed_record.set_field(field, median_value,
                                                     f"outlier_replacement_{value}")
                            processed_record.add_error(f"字段 '{field}' 的異常值 {value} 已替換為中位數 {median_value}")
                            self.metrics.statistical_outliers += 1

            # 複製其他屬性
            processed_record.quality_score = record.quality_score
            processed_record.processing_errors = record.processing_errors.copy()
            processed_record.transformation_log = record.transformation_log.copy()

            processed_records.append(processed_record)

        return processed_records

    async def _is_outlier_iqr(self, records: List[DataRecord], field: str,
                            value: float, multiplier: float) -> bool:
        """基於IQR的異常值檢測"""
        values = []
        for record in records:
            field_value = record.get_field(field)
            if isinstance(field_value, (int, float)):
                values.append(float(field_value))

        if len(values) < 4:  # 需要足夠的樣本
            return False

        values.sort()
        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        iqr = q3 - q1

        lower_bound = q1 - multiplier * iqr
        upper_bound = q3 + multiplier * iqr

        return value < lower_bound or value > upper_bound

    async def _is_outlier_zscore(self, records: List[DataRecord], field: str,
                               value: float, threshold: float) -> bool:
        """基於Z-score的異常值檢測"""
        values = []
        for record in records:
            field_value = record.get_field(field)
            if isinstance(field_value, (int, float)):
                values.append(float(field_value))

        if len(values) < 2:
            return False

        mean_val = statistics.mean(values)
        stdev = statistics.stdev(values) if len(values) > 1 else 0

        if stdev == 0:
            return False

        z_score = abs(value - mean_val) / stdev
        return z_score > threshold

    async def _apply_pattern_learning(self, rule: CleaningRule,
                                    records: List[DataRecord]) -> List[DataRecord]:
        """應用模式學習和預測填充"""
        min_samples = rule.config.get("min_samples", 100)

        if len(records) < min_samples:
            return records

        # 學習字段間的模式
        patterns = await self._learn_field_patterns(records)

        processed_records = []

        for record in records:
            processed_record = DataRecord(record.data.copy(), record.source)

            # 使用學習到的模式進行填充
            for field in record.data.keys():
                if record.is_null(field):
                    predicted_value = await self._predict_missing_value(record, field, patterns)
                    if predicted_value is not None:
                        processed_record.set_field(field, predicted_value, "pattern_prediction")
                        self.metrics.pattern_learning += 1

            # 複製其他屬性
            processed_record.quality_score = record.quality_score
            processed_record.processing_errors = record.processing_errors.copy()
            processed_record.transformation_log = record.transformation_log.copy()

            processed_records.append(processed_record)

        return processed_records

    async def _learn_field_patterns(self, records: List[DataRecord]) -> Dict[str, Dict[str, Any]]:
        """學習字段間的模式"""
        patterns = {}

        # 簡化的模式學習實現
        # 實際實現會使用更複雜的機器學習算法

        for record in records:
            for field, value in record.data.items():
                if field not in patterns:
                    patterns[field] = {
                        "type": type(value).__name__ if value is not None else None,
                        "null_count": 0,
                        "value_counts": {},
                        "correlations": {}
                    }

                if value is None:
                    patterns[field]["null_count"] += 1
                else:
                    value_str = str(value)
                    patterns[field]["value_counts"][value_str] = \
                        patterns[field]["value_counts"].get(value_str, 0) + 1

        # 計算相關性（簡化版本）
        for field1 in patterns:
            for field2 in patterns:
                if field1 != field2:
                    correlation = await self._calculate_field_correlation(records, field1, field2)
                    patterns[field1]["correlations"][field2] = correlation

        return patterns

    async def _calculate_field_correlation(self, records: List[DataRecord],
                                         field1: str, field2: str) -> float:
        """計算字段間的相關性"""
        # 簡化的相關性計算
        pairs = 0
        matches = 0

        for record in records:
            val1 = record.get_field(field1)
            val2 = record.get_field(field2)

            if val1 is not None and val2 is not None:
                pairs += 1
                if val1 == val2:  # 完全匹配
                    matches += 1

        return matches / pairs if pairs > 0 else 0.0

    async def _predict_missing_value(self, record: DataRecord, field: str,
                                   patterns: Dict[str, Dict[str, Any]]) -> Optional[Any]:
        """預測缺失值"""
        if field not in patterns:
            return None

        pattern = patterns[field]

        # 基於相關字段進行預測
        best_correlation = 0.0
        best_related_field = None

        for related_field, correlation in pattern["correlations"].items():
            if correlation > best_correlation and not record.is_null(related_field):
                best_correlation = correlation
                best_related_field = related_field

        if best_related_field and best_correlation > 0.3:
            # 使用相關字段的值
            return record.get_field(best_related_field)

        # 使用最常見的值
        if pattern["value_counts"]:
            most_common = max(pattern["value_counts"].items(), key=lambda x: x[1])[0]
            return most_common

        return None

    async def _apply_noise_reduction(self, rule: CleaningRule,
                                   records: List[DataRecord]) -> List[DataRecord]:
        """應用噪聲減少"""
        reduction_factor = rule.config.get("reduction_factor", 0.1)

        processed_records = []

        for record in records:
            processed_record = DataRecord(record.data.copy(), record.source)

            for field, value in record.data.items():
                if isinstance(value, str):
                    # 移除噪聲字符
                    cleaned = self.noise_chars.sub('', value)

                    # 縮短過長的序列
                    if len(cleaned) > len(value) * (1 - reduction_factor):
                        # 識別並移除重複模式
                        cleaned = await self._reduce_text_noise(cleaned, reduction_factor)

                    if cleaned != value:
                        processed_record.set_field(field, cleaned, "noise_reduction")
                        self.metrics.noise_reduction += len(value) - len(cleaned)

            # 複製其他屬性
            processed_record.quality_score = record.quality_score
            processed_record.processing_errors = record.processing_errors.copy()
            processed_record.transformation_log = record.transformation_log.copy()

            processed_records.append(processed_record)

        return processed_records

    async def _reduce_text_noise(self, text: str, reduction_factor: float) -> str:
        """減少文本噪聲"""
        # 簡化的噪聲減少實現
        # 實際實現會使用更複雜的算法

        # 移除連續的重複字符
        import re
        cleaned = re.sub(r'(.)\1{3,}', r'\1\1', text)  # 將4個或更多重複字符縮減為2個

        return cleaned

    async def _final_data_repair(self, records: List[DataRecord]) -> List[DataRecord]:
        """最終數據修復和驗證"""
        # 最終的數據一致性檢查和修復
        final_records = []

        for record in records:
            # 確保必要的清理
            final_record = DataRecord(record.data.copy(), record.source)

            # 最後的Unicode規範化
            for field, value in record.data.items():
                if isinstance(value, str):
                    normalized = unicodedata.normalize('NFC', value)
                    if normalized != value:
                        final_record.set_field(field, normalized, "final_unicode_normalization")

            # 更新品質評分
            final_record.quality_score = min(100, record.quality_score + 10)  # 清理完成後獎勵10分

            # 複製其他屬性
            final_record.processing_errors = record.processing_errors.copy()
            final_record.transformation_log = record.transformation_log.copy()

            final_records.append(final_record)

        return final_records

    def _calculate_quality_improvement(self, original: List[DataRecord],
                                     cleaned: List[DataRecord]) -> float:
        """計算品質改善度"""
        if len(original) != len(cleaned):
            return 0.0

        total_improvement = 0.0
        count = 0

        for orig, clean in zip(original, cleaned):
            if orig.quality_score != clean.quality_score:
                improvement = clean.quality_score - orig.quality_score
                total_improvement += improvement
                count += 1

        return total_improvement / count if count > 0 else 0.0

    def get_cleaning_metrics(self) -> Dict[str, Any]:
        """獲取清理指標"""
        return {
            "ai_detections": self.metrics.ai_detections,
            "language_corrections": self.metrics.language_corrections,
            "statistical_outliers": self.metrics.statistical_outliers,
            "encoding_fixes": self.metrics.encoding_fixes,
            "pattern_learning": self.metrics.pattern_learning,
            "noise_reduction_bytes": self.metrics.noise_reduction,
            "avg_confidence_score": statistics.mean(self.metrics.confidence_scores) if self.metrics.confidence_scores else 0.0,
            "strategy": self.clean_strategy.value,
            "enabled_rules": len([r for r in self.cleaning_rules if r.enabled])
        }


# 全域高級清理器實例
_advanced_cleaner: Optional[AdvancedDataCleaner] = None


def init_advanced_cleaner(config: Optional[Dict[str, Any]] = None) -> AdvancedDataCleaner:
    """
    初始化全域高級數據清理器

    Args:
        config: 配置字典

    Returns:
        高級數據清理器實例
    """
    global _advanced_cleaner

    if _advanced_cleaner is None:
        _advanced_cleaner = AdvancedDataCleaner(config)

    return _advanced_cleaner


def get_advanced_cleaner() -> AdvancedDataCleaner:
    """獲取全域高級清理器實例"""
    if _advanced_cleaner is None:
        raise RuntimeError("高級清理器尚未初始化，請先調用init_advanced_cleaner()")
    return _advanced_cleaner
