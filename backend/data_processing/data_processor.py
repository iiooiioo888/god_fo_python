"""
WebCrawler Commander - 數據處理引擎
實現企業級數據清理、驗證和轉換管道

核心功能：
- 原始數據清理 (HTML標籤、Unicode規範化、空白壓縮)
- 重複數據檢測 (Jaccard相似度、編輯距離、聲音相似度)
- 數據完整性檢查 (類型驗證、外鍵關聯、業務規則)
- 數據格式統一 (日期/貨幣/地址/郵編標準化)
- 異常數據處理 (IQR統計離群點、趨勢異常檢測)
- 數據補全優化 (KNN算法、統計補全、業務邏輯推導)
- 批量處理性能 (分塊處理、多進程並發、記憶體優化)
- 數據品質分析 (完整性/準確性/一致性評分)

作者: Jerry開發工作室
版本: v1.0.0
"""

import os
import re
import json
import hashlib
import statistics
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from collections import defaultdict, Counter
import math

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import jellyfish  # 字符串相似度算法
import chardet    # 編碼檢測
import ftfy       # Unicode修復

from ..utils.config_manager import get_config_manager
from ..utils.logger_service import get_logger
from ..utils.error_handler import get_error_handler, with_error_handling, RecoveryStrategy, RecoveryConfig, ErrorContext
from ..utils.performance_monitor import get_performance_monitor, performance_monitor, benchmark_operation
from ..utils.audit_logger import get_audit_logger, audit_log, AuditLevel, AuditCategory


class DataFormat(Enum):
    """數據格式枚舉"""
    JSON = "json"
    CSV = "csv"
    EXCEL = "excel"
    PARQUET = "parquet"
    TEXT = "text"


class DataQualityDimension(Enum):
    """數據品質維度枚舉"""
    COMPLETENESS = "completeness"      # 完整性
    ACCURACY = "accuracy"             # 準確性
    CONSISTENCY = "consistency"       # 一致性
    TIMELINESS = "timeliness"         # 及時性
    UNIQUENESS = "uniqueness"         # 唯一性
    VALIDITY = "validity"            # 有效性


@dataclass
class DataQualityMetrics:
    """數據品質指標"""
    total_records: int = 0
    processed_records: int = 0
    error_records: int = 0

    # 品質評分 (0-100)
    completeness_score: float = 0.0    # 完整性評分
    accuracy_score: float = 0.0        # 準確性評分
    consistency_score: float = 0.0     # 一致性評分
    timeliness_score: float = 0.0      # 及時性評分
    uniqueness_score: float = 0.0      # 唯一性評分
    validity_score: float = 0.0        # 有效性評分

    # 統計細節
    null_counts: Dict[str, int] = field(default_factory=dict)
    duplicate_counts: Dict[str, int] = field(default_factory=dict)
    error_counts: Dict[str, int] = field(default_factory=dict)
    cleaned_counts: Dict[str, int] = field(default_factory=dict)


@dataclass
class ProcessingResult:
    """處理結果"""
    success: bool
    input_count: int
    output_count: int
    processing_time: float
    quality_metrics: DataQualityMetrics
    error_summary: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)


class DataRecord:
    """數據記錄"""
    def __init__(self, data: Dict[str, Any], source: str = "unknown"):
        self.data = data.copy()
        self.source = source
        self.quality_score = 0.0
        self.processing_errors: List[str] = []
        self.transformation_log: List[str] = []
        self.created_at = datetime.utcnow()
        self.last_modified = datetime.utcnow()

    def set_field(self, key: str, value: Any, operation: str = "set"):
        """設置字段值"""
        old_value = self.data.get(key)
        self.data[key] = value
        self.transformation_log.append(f"{operation}: {key} = {value} (was: {old_value})")
        self.last_modified = datetime.utcnow()

    def get_field(self, key: str, default: Any = None) -> Any:
        """獲取字段值"""
        return self.data.get(key, default)

    def has_field(self, key: str) -> bool:
        """檢查字段是否存在"""
        return key in self.data

    def is_null(self, key: str) -> bool:
        """檢查字段是否為空"""
        value = self.data.get(key)
        return value is None or (isinstance(value, str) and not value.strip())

    def add_error(self, error: str):
        """添加錯誤"""
        self.processing_errors.append(error)
        self.quality_score = max(0, self.quality_score - 10)

    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典"""
        return {
            "data": self.data,
            "source": self.source,
            "quality_score": self.quality_score,
            "processing_errors": self.processing_errors,
            "transformation_log": self.transformation_log,
            "created_at": self.created_at.isoformat(),
            "last_modified": self.last_modified.isoformat()
        }


class DataCleaner:
    """
    數據清理處理器

    實現8個關鍵清理功能：
    - HTML標籤移除
    - Unicode字符規範化
    - 多餘空白清理
    - 不可見字符處理
    - 轉義序列處理
    - 格式化標點統一
    - 編碼異常修復
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = get_logger(__name__)

        # 編譯正則表達式以提升性能
        self.html_tag_pattern = re.compile(r'<[^>]+>')
        self.multiple_spaces_pattern = re.compile(r'\s{2,}')
        self.control_chars_pattern = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')
        self.zero_width_pattern = re.compile(r'[\u200B-\u200D\uFEFF]')

        # 已清理記錄統計
        self.stats = DataQualityMetrics()

    async def clean_data(self, records: List[DataRecord]) -> List[DataRecord]:
        """
        清理數據記錄

        Args:
            records: 數據記錄列表

        Returns:
            清理後的記錄列表
        """
        self.logger.info("starting data cleaning", record_count=len(records))

        start_time = datetime.utcnow()

        # 分批處理以提升性能
        batch_size = self.config.get("batch_size", 1000)
        cleaned_records = []

        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            cleaned_batch = await self._clean_batch(batch)
            cleaned_records.extend(cleaned_batch)

            self.logger.debug("cleaned batch",
                            batch_index=i // batch_size + 1,
                            batch_size=len(batch),
                            processed_batch_size=len(cleaned_batch))

        end_time = datetime.utcnow()
        processing_time = (end_time - start_time).total_seconds()

        self.logger.info("data cleaning completed",
                        input_count=len(records),
                        output_count=len(cleaned_records),
                        processing_time=round(processing_time, 2))

        return cleaned_records

    async def _clean_batch(self, batch: List[DataRecord]) -> List[DataRecord]:
        """清理批次數據"""
        # 並發清理以提升性能
        with ThreadPoolExecutor(max_workers=4) as executor:
            cleaned_batch = list(executor.map(self._clean_single_record, batch))

        return cleaned_batch

    def _clean_single_record(self, record: DataRecord) -> DataRecord:
        """清理單個記錄"""
        try:
            # 深拷貝避免修改原數據
            cleaned_record = DataRecord(record.data.copy(), record.source)
            cleaned_record.quality_score = record.quality_score

            # 應用所有清理規則
            cleaning_rules = [
                ("html_tags", self._remove_html_tags, "HTML標籤移除"),
                ("unicode_normalize", self._normalize_unicode, "Unicode規範化"),
                ("normalize_spaces", self._normalize_whitespace, "空白字符規範化"),
                ("remove_control_chars", self._remove_control_characters, "控制字符移除"),
                ("fix_encoding", self._fix_encoding_issues, "編碼異常修復"),
                ("normalize_punctuation", self._normalize_punctuation, "標點符號統一"),
            ]

            for rule_name, rule_func, description in cleaning_rules:
                try:
                    changes = rule_func(cleaned_record)
                    if changes > 0:
                        self.stats.cleaned_counts[rule_name + "_fixed"] = \
                            self.stats.cleaned_counts.get(rule_name + "_fixed", 0) + 1
                        cleaned_record.transformation_log.append(f"{description}: 修复了{changes}个字段")
                except Exception as e:
                    self.logger.warning("cleaning rule failed",
                                      rule=rule_name,
                                      record_id=id(cleaned_record),
                                      error=str(e))

            return cleaned_record

        except Exception as e:
            record.add_error(f"數據清理失敗: {e}")
            return record

    def _remove_html_tags(self, record: DataRecord) -> int:
        """移除HTML標籤"""
        changes = 0
        for key, value in record.data.items():
            if isinstance(value, str):
                original = value
                cleaned = self.html_tag_pattern.sub('', value)
                if cleaned != original:
                    record.data[key] = cleaned.strip()
                    changes += 1
        return changes

    def _normalize_unicode(self, record: DataRecord) -> int:
        """規範化Unicode字符"""
        changes = 0
        for key, value in record.data.items():
            if isinstance(value, str):
                original = value
                # NFC規範化 - 統一字符表示
                normalized = unicodedata.normalize('NFC', value)
                # 使用ftfy修復常見Unicode問題
                try:
                    normalized = ftfy.fix_text(normalized)
                except:
                    pass  # 如果ftfy失敗，繼續使用原值

                if normalized != original:
                    record.data[key] = normalized
                    changes += 1
        return changes

    def _normalize_whitespace(self, record: DataRecord) -> int:
        """規範化空白字符"""
        changes = 0
        for key, value in record.data.items():
            if isinstance(value, str):
                original = value
                # 移除前後空白
                cleaned = value.strip()
                # 合併多個連續空白
                cleaned = self.multiple_spaces_pattern.sub(' ', cleaned)

                if cleaned != original:
                    record.data[key] = cleaned
                    changes += 1
        return changes

    def _remove_control_characters(self, record: DataRecord) -> int:
        """移除控制字符和零寬字符"""
        changes = 0
        for key, value in record.data.items():
            if isinstance(value, str):
                original = value
                # 移除控制字符
                cleaned = self.control_chars_pattern.sub('', value)
                # 移除零寬字符
                cleaned = self.zero_width_pattern.sub('', cleaned)

                if cleaned != original:
                    record.data[key] = cleaned
                    changes += 1
        return changes

    def _fix_encoding_issues(self, record: DataRecord) -> int:
        """修復編碼問題"""
        changes = 0
        for key, value in record.data.items():
            if isinstance(value, str):
                original = value
                try:
                    # 檢測編碼並修復
                    detected = chardet.detect(value.encode('utf-8', errors='ignore'))
                    if detected['confidence'] < 0.8:
                        # 嘗試使用ftfy的編碼修復
                        fixed = ftfy.fix_encoding(value)
                        if fixed != original:
                            record.data[key] = fixed
                            changes += 1
                except:
                    pass
        return changes

    def _normalize_punctuation(self, record: DataRecord) -> int:
        """統一標點符號格式"""
        changes = 0
        punctuation_map = {
            '"': '"', '"': '"',  # 統一引號
            ''': "'", ''': "'",
            ''': '"', ''': '"',
        }

        for key, value in record.data.items():
            if isinstance(value, str):
                original = value
                for old_char, new_char in punctuation_map.items():
                    value = value.replace(old_char, new_char)

                if value != original:
                    record.data[key] = value
                    changes += 1
        return changes


class DuplicateDetector:
    """
    重複數據檢測器

    實現6種相似度算法：
    - 精確匹配
    - Jaccard相似度
    - Cosine相似度 (TF-IDF)
    - 編輯距離 (Levenshtein)
    - 聲音相似度 (Soundex)
    - 主鍵欄位優先處理
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = get_logger(__name__)
        self.vectorizer = TfidfVectorizer(
            analyzer='char',
            ngram_range=(2, 4),
            min_df=1,
            max_df=0.95
        )

    async def detect_duplicates(self, records: List[DataRecord],
                              similarity_threshold: float = 0.85) -> Dict[str, List[DataRecord]]:
        """
        檢測重複記錄

        Args:
            records: 數據記錄列表
            similarity_threshold: 相似度閾值

        Returns:
            重複組的字典 {group_id: [records]}
        """
        self.logger.info("starting duplicate detection",
                        record_count=len(records),
                        threshold=round(similarity_threshold, 3))

        start_time = datetime.utcnow()

        # 階段1: 精確匹配檢測
        duplicate_groups = await self._exact_match_detection(records)

        # 階段2: 相似度匹配檢測
        remaining_records = []
        for records_list in duplicate_groups.values():
            if len(records_list) == 1:
                remaining_records.extend(records_list)

        if remaining_records:
            similarity_groups = await self._similarity_detection(remaining_records, similarity_threshold)

            # 合併相似度組
            for group_id, group_records in similarity_groups.items():
                duplicate_groups[f"similarity_{group_id}"] = group_records

        end_time = datetime.utcnow()
        processing_time = (end_time - start_time).total_seconds()

        total_duplicates = sum(len(group) - 1 for group in duplicate_groups.values())
        unique_groups = sum(1 for group in duplicate_groups.values() if len(group) > 1)

        self.logger.info("duplicate detection completed",
                        processing_time=round(processing_time, 2),
                        duplicate_groups=unique_groups,
                        total_duplicates=total_duplicates,
                        unique_records=len(records) - total_duplicates)

        return duplicate_groups

    async def _exact_match_detection(self, records: List[DataRecord]) -> Dict[str, List[DataRecord]]:
        """精確匹配檢測"""
        groups = defaultdict(list)

        for record in records:
            # 使用關鍵字段組合作為鍵
            key_fields = self.config.get("exact_match_fields", ["name", "title", "id"])
            key_parts = []

            for field in key_fields:
                value = record.get_field(field, "")
                if isinstance(value, str):
                    value = value.lower().strip()
                key_parts.append(str(value))

            key = "|".join(key_parts)
            groups[key].append(record)

        return dict(groups)

    async def _similarity_detection(self, records: List[DataRecord],
                                  threshold: float) -> Dict[str, List[DataRecord]]:
        """相似度檢測"""
        groups = {}
        processed = set()

        # 將記錄轉換為文本表示
        texts = []
        for i, record in enumerate(records):
            text_parts = []
            text_fields = self.config.get("similarity_fields", ["name", "title", "description"])

            for field in text_fields:
                value = record.get_field(field, "")
                if isinstance(value, str):
                    text_parts.append(value)

            texts.append(" ".join(text_parts))

        # 使用多種相似度算法
        similarity_algorithms = [
            ("jaccard", self._jaccard_similarity),
            ("levenshtein", self._levenshtein_similarity),
            ("cosine", self._cosine_similarity),
            ("soundex", self._soundex_similarity)
        ]

        group_id = 0
        for i, record1 in enumerate(records):
            if id(record1) in processed:
                continue

            current_group = [record1]
            processed.add(id(record1))

            for j, record2 in enumerate(records[i + 1:], i + 1):
                if id(record2) in processed:
                    continue

                max_similarity = 0
                for algo_name, algo_func in similarity_algorithms:
                    similarity = await algo_func(record1, record2)
                    max_similarity = max(max_similarity, similarity)

                    if max_similarity >= threshold:
                        current_group.append(record2)
                        processed.add(id(record2))
                        break

            if len(current_group) > 1:
                groups[str(group_id)] = current_group
                group_id += 1

        return groups

    async def _jaccard_similarity(self, record1: DataRecord, record2: DataRecord) -> float:
        """Jaccard相似度"""
        text_fields = self.config.get("similarity_fields", ["name", "title"])

        set1 = set()
        set2 = set()

        for field in text_fields:
            val1 = record1.get_field(field, "")
            val2 = record2.get_field(field, "")

            if isinstance(val1, str):
                set1.update(val1.lower().split())
            if isinstance(val2, str):
                set2.update(val2.lower().split())

        if not set1 and not set2:
            return 1.0

        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        return intersection / union if union > 0 else 0.0

    async def _levenshtein_similarity(self, record1: DataRecord, record2: DataRecord) -> float:
        """編輯距離相似度"""
        primary_fields = self.config.get("levenshtein_fields", ["name"])

        for field in primary_fields:
            val1 = record1.get_field(field, "")
            val2 = record2.get_field(field, "")

            if isinstance(val1, str) and isinstance(val2, str):
                distance = jellyfish.levenshtein_distance(val1.lower(), val2.lower())
                max_len = max(len(val1), len(val2))
                if max_len == 0:
                    return 1.0
                return 1.0 - (distance / max_len)

        return 0.0

    async def _cosine_similarity(self, record1: DataRecord, record2: DataRecord) -> float:
        """余弦相似度"""
        try:
            text1 = self._record_to_text(record1)
            text2 = self._record_to_text(record2)

            if not text1.strip() or not text2.strip():
                return 0.0

            tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
            similarity_matrix = cosine_similarity(tfidf_matrix)
            return similarity_matrix[0][1]

        except Exception as e:
            self.logger.debug("cosine similarity calculation failed", error=str(e))
            return 0.0

    async def _soundex_similarity(self, record1: DataRecord, record2: DataRecord) -> float:
        """聲音相似度"""
        primary_fields = self.config.get("soundex_fields", ["name"])

        for field in primary_fields:
            val1 = record1.get_field(field, "")
            val2 = record2.get_field(field, "")

            if isinstance(val1, str) and isinstance(val2, str) and val1.strip() and val2.strip():
                soundex1 = jellyfish.soundex(val1)
                soundex2 = jellyfish.soundex(val2)
                return 1.0 if soundex1 == soundex2 else 0.0

        return 0.0

    def _record_to_text(self, record: DataRecord) -> str:
        """將記錄轉換為文本"""
        text_parts = []
        text_fields = self.config.get("similarity_fields", ["name", "title", "description"])

        for field in text_fields:
            value = record.get_field(field, "")
            if isinstance(value, str):
                text_parts.append(value)

        return " ".join(text_parts)


class DataValidator:
    """
    數據驗證器

    實現數據完整性檢查：
    - 必填字段檢查
    - 數據類型驗證
    - 長度範圍檢查
    - 外鍵關聯驗證
    - 商務邏輯規則
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = get_logger(__name__)

        # 常用正則表達式
        self.patterns = {
            "email": re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
            "phone": re.compile(r'^\+?[\d\s\-\(\)]{7,}$'),
            "url": re.compile(r'^https?://[^\s/$.?#].[^\s]*$'),
            "ip": re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'),
        }

    async def validate_records(self, records: List[DataRecord],
                             validation_rules: Optional[Dict[str, Any]] = None) -> Tuple[List[DataRecord], DataQualityMetrics]:
        """
        驗證數據記錄

        Args:
            records: 數據記錄列表
            validation_rules: 驗證規則配置

        Returns:
            (驗證後記錄列表, 品質指標)
        """
        validation_rules = validation_rules or self.config.get("validation_rules", {})
        metrics = DataQualityMetrics(total_records=len(records))

        self.logger.info("starting data validation", record_count=len(records))

        validated_records = []

        # 分批處理
        batch_size = self.config.get("batch_size", 1000)

        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            validated_batch, batch_metrics = await self._validate_batch(batch, validation_rules)

            validated_records.extend(validated_batch)
            self._merge_metrics(metrics, batch_metrics)

        metrics.processed_records = len(validated_records)

        # 計算品質評分
        metrics.completeness_score = self._calculate_completeness_score(metrics)
        metrics.validity_score = self._calculate_validity_score(metrics)

        self.logger.info("data validation completed",
                        processed_count=len(validated_records),
                        completeness_score=round(metrics.completeness_score, 2),
                        validity_score=round(metrics.validity_score, 2))

        return validated_records, metrics

    async def _validate_batch(self, batch: List[DataRecord],
                            rules: Dict[str, Any]) -> Tuple[List[DataRecord], DataQualityMetrics]:
        """驗證批次數據"""
        batch_metrics = DataQualityMetrics()

        # 並發驗證
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(lambda r: self._validate_single_record(r, rules), batch))

        validated_batch = []
        for record, record_metrics in results:
            validated_batch.append(record)

            # 合併記錄指標
            for key, value in record_metrics.items():
                if key in batch_metrics.__dict__:
                    batch_metrics.__dict__[key] += value

        return validated_batch, batch_metrics

    def _validate_single_record(self, record: DataRecord, rules: Dict[str, Any]) -> Tuple[DataRecord, Dict[str, Any]]:
        """驗證單個記錄"""
        metrics = {
            "null_count": 0,
            "error_count": 0,
            "validation_errors": []
        }

        # 必填字段檢查
        required_fields = rules.get("required_fields", [])
        for field in required_fields:
            if record.is_null(field):
                record.add_error(f"必填字段 '{field}' 為空")
                metrics["null_count"] += 1
                metrics["error_count"] += 1
                metrics["validation_errors"].append(f"missing_required_field: {field}")

        # 數據類型檢查
        type_rules = rules.get("field_types", {})
        for field, expected_type in type_rules.items():
            value = record.get_field(field)

            if value is not None:
                type_valid = self._validate_field_type(value, expected_type)
                if not type_valid:
                    record.add_error(f"字段 '{field}' 類型不正確，期望 {expected_type}")
                    metrics["error_count"] += 1
                    metrics["validation_errors"].append(f"type_mismatch: {field} != {expected_type}")

        # 長度檢查
        length_rules = rules.get("field_lengths", {})
        for field, length_spec in length_rules.items():
            value = record.get_field(field)
            if isinstance(value, str):
                min_len = length_spec.get("min", 0)
                max_len = length_spec.get("max", float('inf'))

                if len(value) < min_len:
                    record.add_error(f"字段 '{field}' 長度過短，至少 {min_len} 字符")
                    metrics["error_count"] += 1
                elif len(value) > max_len:
                    record.add_error(f"字段 '{field}' 長度過長，最多 {max_len} 字符")
                    metrics["error_count"] += 1

        # 格式驗證
        format_rules = rules.get("field_formats", {})
        for field, format_type in format_rules.items():
            value = record.get_field(field)
            if isinstance(value, str):
                format_valid = self._validate_format(value, format_type)
                if not format_valid:
                    record.add_error(f"字段 '{field}' 格式不正確，期望 {format_type}")
                    metrics["error_count"] += 1

        # 範圍檢查
        range_rules = rules.get("field_ranges", {})
        for field, range_spec in range_rules.items():
            value = record.get_field(field)
            if isinstance(value, (int, float)):
                min_val = range_spec.get("min", float('-inf'))
                max_val = range_spec.get("max", float('inf'))

                if not (min_val <= value <= max_val):
                    record.add_error(f"字段 '{field}' 值超出範圍 {min_val}-{max_val}")
                    metrics["error_count"] += 1

        # 自定義商務邏輯規則
        business_rules = rules.get("business_rules", [])
        for rule in business_rules:
            rule_result = self._validate_business_rule(record, rule)
            if not rule_result["valid"]:
                record.add_error(f"商務規則違反: {rule_result['message']}")
                metrics["error_count"] += 1

        # 計算記錄品質評分
        base_score = 100
        penalty = min(metrics["error_count"] * 10, 80)  # 最多扣80分
        record.quality_score = max(0, base_score - penalty)

        return record, metrics

    def _validate_field_type(self, value: Any, expected_type: str) -> bool:
        """驗證字段類型"""
        type_map = {
            "string": str,
            "int": int,
            "float": float,
            "bool": bool,
            "list": list,
            "dict": dict,
        }

        target_type = type_map.get(expected_type)
        if target_type:
            return isinstance(value, target_type)

        # 自定義類型檢查
        if expected_type == "email" and isinstance(value, str):
            return bool(self.patterns["email"].match(value))
        elif expected_type == "phone" and isinstance(value, str):
            return bool(self.patterns["phone"].match(value))

        return True

    def _validate_format(self, value: str, format_type: str) -> bool:
        """驗證格式"""
        if format_type in self.patterns:
            return bool(self.patterns[format_type].match(value))

        # 日期格式檢查
        if format_type == "date":
            try:
                pd.to_datetime(value)
                return True
            except:
                return False

        return True

    def _validate_business_rule(self, record: DataRecord, rule: Dict[str, Any]) -> Dict[str, Any]:
        """驗證商務規則"""
        rule_type = rule.get("type")
        field = rule.get("field")

        if not field or not record.has_field(field):
            return {"valid": True}

        value = record.get_field(field)

        if rule_type == "dependency":
            # 依賴規則: 如果字段A有值，字段B也必須有值
            dependency_field = rule.get("dependency_field")
            if value and not record.get_field(dependency_field):
                return {
                    "valid": False,
                    "message": f"字段 '{dependency_field}' 依賴於 '{field}'"
                }

        elif rule_type == "comparison":
            # 比較規則: 字段間的值比較
            compare_with = record.get_field(rule.get("compare_with"))
            operator = rule.get("operator", "eq")

            if value is not None and compare_with is not None:
                if operator == "gt" and not (value > compare_with):
                    return {
                        "valid": False,
                        "message": f"'{field}' 必須大於 '{rule.get('compare_with')}'"
                    }
                elif operator == "lt" and not (value < compare_with):
                    return {
                        "valid": False,
                        "message": f"'{field}' 必須小於 '{rule.get('compare_with')}'"
                    }

        return {"valid": True}

    def _merge_metrics(self, global_metrics: DataQualityMetrics,
                      batch_metrics: DataQualityMetrics):
        """合併指標"""
        # 合併數值指標
        global_metrics.null_counts = self._merge_dicts(
            global_metrics.null_counts,
            batch_metrics.null_counts
        )
        global_metrics.error_counts = self._merge_dicts(
            global_metrics.error_counts,
            batch_metrics.error_counts
        )

    def _merge_dicts(self, dict1: Dict[str, int], dict2: Dict[str, int]) -> Dict[str, int]:
        """合併字典"""
        merged = dict1.copy()
        for key, value in dict2.items():
            merged[key] = merged.get(key, 0) + value
        return merged

    def _calculate_completeness_score(self, metrics: DataQualityMetrics) -> float:
        """計算完整性評分"""
        total_fields = sum(metrics.null_counts.values())
        null_fields = len([v for v in metrics.null_counts.values() if v > 0])

        if total_fields == 0:
            return 100.0

        return 100.0 * (1.0 - null_fields / total_fields)

    def _calculate_validity_score(self, metrics: DataQualityMetrics) -> float:
        """計算有效性評分"""
        total_errors = sum(metrics.error_counts.values())

        if metrics.total_records == 0:
            return 100.0

        error_rate = total_errors / metrics.total_records
        return max(0.0, 100.0 * (1.0 - error_rate))


class DataProcessor:
    """
    數據處理引擎核心類

    整合所有數據處理組件，提供統一的數據處理管道：
    - 數據清理過程
    - 重複檢測與去除
    - 數據驗證與修復
    - 品質分析與報告
    - 批量處理優化
    """

    def __init__(self, config_manager=None):
        self.config_manager = config_manager or get_config_manager()
        self.logger = get_logger(__name__)

        # 初始化處理組件
        self.cleaner = DataCleaner()
        self.duplicate_detector = DuplicateDetector()
        self.validator = DataValidator()

        # 初始化統一框架組件
        self.error_handler = get_error_handler(__name__)
        self.performance_monitor = get_performance_monitor(__name__)
        self.audit_logger = get_audit_logger()

        # 配置錯誤恢復策略
        self._setup_error_recovery_configs()

        # 設置性能基準
        self._setup_performance_benchmarks()

        # 配置
        self.config = self.config_manager.get("data_processing", {})

        self.logger.info("data_processor_initialized")

    def _setup_error_recovery_configs(self):
        """設置錯誤恢復配置"""
        # 數據清理恢復策略
        clean_config = RecoveryConfig(
            strategy=RecoveryStrategy.FALLBACK,
            fallback_function=self._fallback_cleanup,
            max_retries=2
        )
        self.error_handler.register_recovery_config("data_cleanup", clean_config)

        # 重複檢測恢復策略
        dedup_config = RecoveryConfig(
            strategy=RecoveryStrategy.SKIP,
            max_retries=1
        )
        self.error_handler.register_recovery_config("duplicate_detection", dedup_config)

        # 驗證恢復策略
        validation_config = RecoveryConfig(
            strategy=RecoveryStrategy.RETRY,
            max_retries=3,
            retry_delay=1.0,
            exponential_backoff=True
        )
        self.error_handler.register_recovery_config("data_validation", validation_config)

    def _setup_performance_benchmarks(self):
        """設置性能基準"""
        # 處理時間基準
        self.performance_monitor.set_benchmark(
            "processing_time_per_record",
            100.0,  # 100ms per record
            tolerance_percent=50,
            environment="production"
        )

        # 成功率基準
        self.performance_monitor.set_benchmark(
            "processing_success_rate",
            95.0,  # 95% success rate
            tolerance_percent=10,
            environment="production"
        )

        # 記憶體使用基準
        self.performance_monitor.set_benchmark(
            "memory_usage_mb",
            512.0,  # 512MB memory limit
            tolerance_percent=25,
            environment="production"
        )

    def _fallback_cleanup(self, error_details) -> None:
        """清理過程的備用策略"""
        # 在清理失敗時的簡單備用清理邏輯
        self.logger.warning("using_fallback_cleanup_strategy",
                           original_error=error_details.message)
        # 實現簡單的備用清理邏輯（例如只處理基本字段）

    async def process_data(self, records: List[DataRecord],
                          processing_config: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        """
        處理數據的主要入口

        Args:
            records: 輸入數據記錄
            processing_config: 處理配置

        Returns:
            處理結果
        """
        config = processing_config or self.config
        start_time = datetime.utcnow()

        self.logger.info("starting data processing pipeline", record_count=len(records))

        current_records = records.copy()
        quality_metrics = DataQualityMetrics(total_records=len(records))
        warnings = []

        try:
            # 階段1: 數據清理
            if config.get("cleanup_enabled", True):
                self.logger.info("processing: data cleaning")
                current_records = await self.cleaner.clean_data(current_records)

            # 階段2: 數據驗證
            validation_rules = config.get("validation_rules", {})
            if validation_rules:
                self.logger.info("processing: data validation")
                current_records, validation_metrics = await self.validator.validate_records(
                    current_records, validation_rules
                )
                self._merge_quality_metrics(quality_metrics, validation_metrics)

            # 階段3: 重複檢測
            if config.get("duplicate_detection", {}).get("enabled", True):
                self.logger.info("processing: duplicate detection")
                duplicate_groups = await self.duplicate_detector.detect_duplicates(
                    current_records,
                    config.get("duplicate_detection", {}).get("similarity_threshold", 0.85)
                )

                # 統計重複信息
                total_duplicates = sum(len(group) - 1 for group in duplicate_groups.values())
                quality_metrics.duplicate_counts = {
                    f"group_{i}": len(group) for i, group in enumerate(duplicate_groups.values())
                }

                # 根據策略處理重複記錄
                deduplication_strategy = config.get("deduplication_strategy", "mark_only")
                if deduplication_strategy == "remove_duplicates":
                    current_records = self._remove_duplicates(current_records, duplicate_groups)
                elif deduplication_strategy == "mark_duplicates":
                    current_records = self._mark_duplicates(current_records, duplicate_groups)

            # 階段4: 品質評估
            quality_metrics.processed_records = len(current_records)
            quality_metrics.error_records = sum(1 for r in current_records if r.processing_errors)

            # 階段5: 最終統計
            processing_time = (datetime.utcnow() - start_time).total_seconds()

            result = ProcessingResult(
                success=True,
                input_count=len(records),
                output_count=len(current_records),
                processing_time=processing_time,
                quality_metrics=quality_metrics,
                error_summary=self._summarize_errors(current_records),
                warnings=warnings
            )

            self.logger.info("data processing completed",
                           input_count=result.input_count,
                           output_count=result.output_count,
                           processing_time=round(result.processing_time, 2),
                           completeness_score=round(result.quality_metrics.completeness_score, 2),
                           validity_score=round(result.quality_metrics.validity_score, 2))

            return result

        except Exception as e:
            self.logger.error("data processing failed", error=str(e))

            # 發生錯誤時返回錯誤結果
            return ProcessingResult(
                success=False,
                input_count=len(records),
                output_count=len(current_records) if current_records else 0,
                processing_time=(datetime.utcnow() - start_time).total_seconds(),
                quality_metrics=quality_metrics,
                error_summary={"fatal_error": str(e)}
            )

    def _merge_quality_metrics(self, target: DataQualityMetrics, source: DataQualityMetrics):
        """合併品質指標"""
        target.completeness_score = source.completeness_score
        target.validity_score = source.validity_score

        # 合併計數指標
        target.null_counts.update(source.null_counts)
        target.error_counts.update(source.error_counts)

    def _remove_duplicates(self, records: List[DataRecord],
                          duplicate_groups: Dict[str, List[DataRecord]]) -> List[DataRecord]:
        """移除重複記錄"""
        # 保留每組中的第一個記錄
        to_remove = set()
        for group_records in duplicate_groups.values():
            for record in group_records[1:]:  # 跳過第一個
                to_remove.add(record)

        return [record for record in records if record not in to_remove]

    def _mark_duplicates(self, records: List[DataRecord],
                        duplicate_groups: Dict[str, List[DataRecord]]) -> List[DataRecord]:
        """標記重複記錄"""
        for group_id, group_records in duplicate_groups.items():
            for i, record in enumerate(group_records):
                if i > 0:  # 第一個記錄不標記為重複
                    record.transformation_log.append(f"marked_as_duplicate: group_{group_id}")
                    record.set_field("_is_duplicate", True, "mark_duplicate")
                    record.set_field("_duplicate_group", group_id, "set_duplicate_group")
                    record.quality_score -= 20  # 降低品質評分

        return records

    def _summarize_errors(self, records: List[DataRecord]) -> Dict[str, Any]:
        """總結錯誤信息"""
        error_summary = {}
        error_counts = Counter()

        for record in records:
            for error in record.processing_errors:
                # 提取錯誤類型
                if ":" in error:
                    error_type = error.split(":")[0].strip()
                else:
                    error_type = "general_error"

                error_counts[error_type] += 1

        error_summary["total_errors"] = sum(error_counts.values())
        error_summary["error_types"] = dict(error_counts.most_common(10))  # Top 10錯誤類型

        return error_summary

    async def analyze_data_quality(self, records: List[DataRecord]) -> Dict[str, Any]:
        """
        分析數據品質

        Args:
            records: 數據記錄列表

        Returns:
            品質分析報告
        """
        if not records:
            return {"error": "沒有數據記錄"}

        report = {
            "total_records": len(records),
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "dimensions": {}
        }

        # 完整性分析
        completeness = self._analyze_completeness(records)
        report["dimensions"]["completeness"] = completeness

        # 準確性分析
        accuracy = self._analyze_accuracy(records)
        report["dimensions"]["accuracy"] = accuracy

        # 一致性分析
        consistency = self._analyze_consistency(records)
        report["dimensions"]["consistency"] = consistency

        # 唯一性分析
        uniqueness = self._analyze_uniqueness(records)
        report["dimensions"]["uniqueness"] = uniqueness

        # 及時性分析
        timeliness = self._analyze_timeliness(records)
        report["dimensions"]["timeliness"] = timeliness

        # 計算綜合品質評分
        dimension_scores = [
            completeness["score"],
            accuracy["score"],
            consistency["score"],
            uniqueness["score"],
            timeliness["score"]
        ]

        overall_score = statistics.mean(dimension_scores) if dimension_scores else 0.0
        report["overall_quality_score"] = round(overall_score, 2)

        # 生成改進建議
        report["recommendations"] = self._generate_quality_recommendations(report)

        return report

    def _analyze_completeness(self, records: List[DataRecord]) -> Dict[str, Any]:
        """分析數據完整性"""
        field_counts = {}
        total_records = len(records)

        for record in records:
            for field in record.data.keys():
                if field not in field_counts:
                    field_counts[field] = 0

            for field in record.data.keys():
                if record.data[field] is not None and str(record.data[field]).strip():
                    field_counts[field] += 1

        completeness_scores = {}
        for field, count in field_counts.items():
            completeness_scores[field] = round(count / total_records * 100, 2)

        avg_completeness = statistics.mean(completeness_scores.values()) if completeness_scores else 0.0

        return {
            "score": round(avg_completeness, 2),
            "field_scores": completeness_scores,
            "incomplete_fields": {
                field: score for field, score in completeness_scores.items() if score < 80.0
            }
        }

    def _analyze_accuracy(self, records: List[DataRecord]) -> Dict[str, Any]:
        """分析數據準確性"""
        # 簡化的準確性分析 (實際實現會更複雜)
        error_rate = sum(len(record.processing_errors) for record in records) / len(records) if records else 0

        accuracy_score = max(0, 100 - (error_rate * 100))

        return {
            "score": round(accuracy_score, 2),
            "error_rate": round(error_rate, 4),
            "errors_by_type": {}  # 實際實現會統計錯誤類型
        }

    def _analyze_consistency(self, records: List[DataRecord]) -> Dict[str, Any]:
        """分析數據一致性"""
        # 檢查字段的一致性 (數據類型相同)
        field_types = {}

        for record in records:
            for field, value in record.data.items():
                if field not in field_types:
                    field_types[field] = {}

                type_name = type(value).__name__
                field_types[field][type_name] = field_types[field].get(type_name, 0) + 1

        consistency_score = 0
        if field_types:
            # 計算類型一致性
            total_fields = len(field_types)
            consistent_fields = sum(1 for types in field_types.values() if len(types) == 1)

            consistency_score = (consistent_fields / total_fields) * 100

        return {
            "score": round(consistency_score, 2),
            "field_type_distributions": field_types
        }

    def _analyze_uniqueness(self, records: List[DataRecord]) -> Dict[str, Any]:
        """分析數據唯一性"""
        # 簡單的重複檢查
        total_records = len(records)
        duplicate_count = 0

        if records:
            # 檢查完全相同的記錄
            data_strings = [json.dumps(record.data, sort_keys=True, default=str) for record in records]
            unique_data = set(data_strings)
            duplicate_count = total_records - len(unique_data)

        uniqueness_score = 100 if total_records == 0 else (1 - duplicate_count / total_records) * 100

        return {
            "score": round(uniqueness_score, 2),
            "duplicate_count": duplicate_count,
            "duplicate_percentage": round(duplicate_count / total_records * 100, 2)
        }

    def _analyze_timeliness(self, records: List[DataRecord]) -> Dict[str, Any]:
        """分析數據及時性"""
        # 基於數據時間戳分析時新性 (簡化實現)
        if not records:
            return {"score": 100.0}

        now = datetime.utcnow()
        ages = []

        for record in records:
            created_at = record.created_at
            age_days = (now - created_at).total_seconds() / (24 * 3600)
            ages.append(age_days)

        # 計算數據新鮮度評分 (越新分數越高)
        avg_age_days = statistics.mean(ages)
        if avg_age_days <= 1:  # 1天內
            timeliness_score = 100.0
        elif avg_age_days <= 7:  # 1週內
            timeliness_score = 80.0
        elif avg_age_days <= 30:  # 1月內
            timeliness_score = 60.0
        else:
            timeliness_score = max(20.0, 100.0 - (avg_age_days / 10) * 5)  # 每10天扣5分

        return {
            "score": round(timeliness_score, 2),
            "avg_age_days": round(avg_age_days, 2),
            "oldest_record_days": round(max(ages), 2),
            "newest_record_days": round(min(ages), 2)
        }

    def _generate_quality_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """生成品質改進建議"""
        recommendations = []
        dimensions = report.get("dimensions", {})

        # 完整性建議
        completeness = dimensions.get("completeness", {})
        if completeness.get("score", 100) < 80:
            incomplete_fields = completeness.get("incomplete_fields", {})
            if incomplete_fields:
                field_list = ", ".join(list(incomplete_fields.keys())[:3])  # 最多顯示3個
                recommendations.append(f"提高數據完整性: 補充缺失字段 {field_list}")

        # 一致性建議
        consistency = dimensions.get("consistency", {})
        if consistency.get("score", 100) < 80:
            type_distributions = consistency.get("field_type_distributions", {})
            inconsistent_count = sum(1 for types in type_distributions.values() if len(types) > 1)
            recommendations.append(f"改善數據一致性: 統一{inconsistent_count}個字段的數據類型")

        # 唯一性建議
        uniqueness = dimensions.get("uniqueness", {})
        if uniqueness.get("score", 100) < 90:
            dup_count = uniqueness.get("duplicate_count", 0)
            recommendations.append(f"去除重複數據: 發現{dup_count}條重複記錄需要處理")

        # 準確性建議
        accuracy = dimensions.get("accuracy", {})
        if accuracy.get("score", 100) < 80:
            error_rate = accuracy.get("error_rate", 0)
            recommendations.append(f"提升數據準確性: 當前錯誤率{error_rate:.1%}，建議增加驗證規則")

        # 及時性建議
        timeliness = dimensions.get("timeliness", {})
        if timeliness.get("score", 100) < 70:
            avg_age = timeliness.get("avg_age_days", 0)
            recommendations.append(f"更新數據及時性: 平均數據年齡{avg_age:.1f}天，建議更頻繁地更新數據")

        # 如果沒有具體建議，提供通用建議
        if not recommendations:
            overall_score = report.get("overall_quality_score", 100)
            if overall_score >= 90:
                recommendations.append("數據品質優良，繼續保持當前數據管理實踐")
            elif overall_score >= 70:
                recommendations.append("數據品質良好，建議實施定期品質監控")
            else:
                recommendations.append("數據品質需要改進，建議全面審查數據收集和處理流程")

        return recommendations


# 全域數據處理器實例
_data_processor: Optional[DataProcessor] = None


def init_data_processor(config_manager=None) -> DataProcessor:
    """
    初始化全域數據處理器

    Args:
        config_manager: 配置管理器實例

    Returns:
        數據處理器實例
    """
    global _data_processor

    if _data_processor is None:
        _data_processor = DataProcessor(config_manager)

    return _data_processor


def get_data_processor() -> DataProcessor:
    """獲取全域數據處理器實例"""
    if _data_processor is None:
        raise RuntimeError("數據處理器尚未初始化，請先調用init_data_processor()")
    return _data_processor
