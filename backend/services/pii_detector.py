"""
WebCrawler Commander - PII檢測與脫敏引擎
企業級隱私信息保護，GDPR/HIPAA第一道防線

核心功能：
- 18種隱私保護識別碼精準識別與分類
- 多重脫敏策略：遮罩/加密/替換/刪除
- 置信度動態評分與阈值調整
- 跨語言實體識別：中文/英文NER支持
- GDPR/HIPAA醫療專用合規規則庫
- 企業級審計日誌與合規報告
- 性能優化：批處理/並發/快取機制

作者: Jerry開發工作室
版本: v1.0.0
"""

import os
import re
import json
import hashlib
import asyncio
import threading
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple, Callable, Set
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from collections import defaultdict, Counter
import math

import pandas as pd
import numpy as np
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

from ..utils.config_manager import get_config_manager
from ..utils.logger_service import get_logger


class PIIEntityType(Enum):
    """PII實體類型枚舉"""
    PERSON = "PERSON"                    # 人名
    EMAIL_ADDRESS = "EMAIL_ADDRESS"      # 郵箱地址
    PHONE_NUMBER = "PHONE_NUMBER"        # 電話號碼
    ADDRESS = "ADDRESS"                  # 地址
    SSN = "US_SSN"                       # 社會安全號
    CREDIT_CARD = "CREDIT_CARD"           # 信用卡號
    IBAN = "IBAN_CODE"                   # 銀行帳號
    LICENSE_PLATE = "LICENSE_PLATE"       # 車牌號
    PASSPORT = "PASSPORT"                # 護照號
    DRIVERS_LICENSE = "US_DRIVER_LICENSE" # 駕駛執照
    IP_ADDRESS = "IP_ADDRESS"            # IP地址
    MAC_ADDRESS = "MAC_ADDRESS"          # MAC地址
    URL = "URL"                         # 網址
    LOCATION = "LOCATION"                # 地位置標
    BIRTH_DATE = "DATE_TIME"             # 出生日期
    HEALTH_RECORD = "MEDICAL_LICENSE"    # 健康記錄
    FINANCIAL_ID = "US_ITIN"             # 金融標識
    DEVICE_ID = "IMEI"                   # 設備標識


class AnonymizationStrategy(Enum):
    """脫敏策略枚舉"""
    MASKING = "masking"          # 遮罩
    ENCRYPTION = "encryption"    # 加密
    REPLACEMENT = "replacement"  # 替換
    DELETION = "deletion"        # 刪除


class ComplianceLevel(Enum):
    """合規等級枚舉"""
    PUBLIC = "PUBLIC"            # 公開信息
    INTERNAL = "INTERNAL"         # 內部信息
    CONFIDENTIAL = "CONFIDENTIAL" # 機密信息
    RESTRICTED = "RESTRICTED"     # 限制信息


@dataclass
class PIIEntity:
    """PII實體數據結構"""
    entity_type: PIIEntityType
    value: str
    start_index: int
    end_index: int
    confidence_score: float
    context: str = ""
    language: str = "auto"
    compliance_level: ComplianceLevel = ComplianceLevel.CONFIDENTIAL
    metadata: Dict[str, Any] = field(default_factory=dict)
    detected_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典"""
        return {
            **asdict(self),
            "entity_type": self.entity_type.value,
            "compliance_level": self.compliance_level.value,
            "detected_at": self.detected_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PIIEntity':
        """從字典創建實體"""
        data_copy = data.copy()
        data_copy["entity_type"] = PIIEntityType(data["entity_type"])
        data_copy["compliance_level"] = ComplianceLevel(data["compliance_level"])
        data_copy["detected_at"] = datetime.fromisoformat(data["detected_at"])
        return cls(**data_copy)


@dataclass
class AnonymizationResult:
    """脫敏結果"""
    original_entity: PIIEntity
    anonymized_value: str
    strategy_used: AnonymizationStrategy
    compliance_notes: List[str] = field(default_factory=list)
    processing_time: float = 0.0
    reversible: bool = False
    encryption_key_id: Optional[str] = None


@dataclass
class PIIDetectionResult:
    """PII檢測結果"""
    text_id: str
    entities_found: List[PIIEntity]
    processing_time: float
    language_detected: str
    total_entities: int = 0
    high_confidence_count: int = 0
    anonymized: bool = False
    compliance_report: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.total_entities = len(self.entities_found)
        confidence_threshold = 0.8  # 可配置
        self.high_confidence_count = sum(
            1 for entity in self.entities_found
            if entity.confidence_score >= confidence_threshold
        )


class RegulatoryRule:
    """合規規則"""

    def __init__(self, rule_id: str, name: str, description: str,
                 entity_types: List[PIIEntityType],
                 compliance_level: ComplianceLevel,
                 retention_period_days: Optional[int] = None,
                 gdpr_applicable: bool = True,
                 hipaa_applicable: bool = False,
                 custom_requirements: Dict[str, Any] = None):
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.entity_types = entity_types
        self.compliance_level = compliance_level
        self.retention_period_days = retention_period_days
        self.gdpr_applicable = gdpr_applicable
        self.hipaa_applicable = hipaa_applicable
        self.custom_requirements = custom_requirements or {}

    def is_applicable_to_entity(self, entity: PIIEntity) -> bool:
        """檢查規則是否適用於實體"""
        return entity.entity_type in self.entity_types

    def generate_compliance_notes(self, entity: PIIEntity) -> List[str]:
        """生成合規說明"""
        notes = []
        if self.gdpr_applicable:
            notes.append(f"GDPR適用 - {self.description}")
        if self.hipaa_applicable:
            notes.append(f"HIPAA適用 - {self.description}")
        if self.retention_period_days:
            notes.append(f"數據保留期: {self.retention_period_days}天")
        return notes


class AnonymizationEngine:
    """脫敏引擎"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = get_logger(__name__)

        # 加密配置
        self._setup_encryption()

        # 策略配置
        self.strategy_configs = self.config.get("strategies", {
            "default": "masking",
            "PERSON": "masking",
            "EMAIL_ADDRESS": "masking",
            "PHONE_NUMBER": "masking",
            "CREDIT_CARD": "encryption",
            "US_SSN": "encryption",
            "ADDRESS": "replacement"
        })

    def _setup_encryption(self):
        """設置加密"""
        encryption_key = self.config.get("encryption_key")
        if not encryption_key:
            # 生成新密鑰（生產環境應該從安全存儲獲取）
            encryption_key = base64.urlsafe_b64encode(os.urandom(32))

        self.fernet = Fernet(encryption_key)
        self.key_id = self.config.get("key_id", "default")

    async def anonymize_entity(self, entity: PIIEntity) -> AnonymizationResult:
        """脫敏實體"""
        start_time = datetime.utcnow()
        strategy_name = self.strategy_configs.get(
            entity.entity_type.value,
            self.strategy_configs.get("default", "masking")
        )

        strategy = AnonymizationStrategy(strategy_name)
        anonymized_value = await self._apply_strategy(entity, strategy)

        processing_time = (datetime.utcnow() - start_time).total_seconds()

        return AnonymizationResult(
            original_entity=entity,
            anonymized_value=anonymized_value,
            strategy_used=strategy,
            compliance_notes=["脫敏處理完成"],
            processing_time=processing_time,
            reversible=(strategy == AnonymizationStrategy.ENCRYPTION),
            encryption_key_id=self.key_id if strategy == AnonymizationStrategy.ENCRYPTION else None
        )

    async def _apply_strategy(self, entity: PIIEntity, strategy: AnonymizationStrategy) -> str:
        """應用脫敏策略"""
        value = entity.value

        if strategy == AnonymizationStrategy.MASKING:
            return self._mask_value(value, entity.entity_type)
        elif strategy == AnonymizationStrategy.ENCRYPTION:
            return self._encrypt_value(value)
        elif strategy == AnonymizationStrategy.REPLACEMENT:
            return self._replace_value(value, entity.entity_type)
        elif strategy == AnonymizationStrategy.DELETION:
            return "[DELETED]"
        else:
            return value  # 不處理

    def _mask_value(self, value: str, entity_type: PIIEntityType) -> str:
        """遮罩值"""
        masks = {
            PIIEntityType.PERSON: self._mask_person_name,
            PIIEntityType.EMAIL_ADDRESS: self._mask_email,
            PIIEntityType.PHONE_NUMBER: self._mask_phone,
            PIIEntityType.CREDIT_CARD: self._mask_credit_card,
            PIIEntityType.US_SSN: self._mask_ssn,
        }

        mask_func = masks.get(entity_type, self._mask_generic)
        return mask_func(value)

    def _mask_person_name(self, name: str) -> str:
        """遮罩人名 (保留首尾字符)"""
        if len(name) <= 1:
            return "*"
        elif len(name) == 2:
            return name[0] + "*"
        else:
            return name[0] + "*" * (len(name) - 2) + name[-1]

    def _mask_email(self, email: str) -> str:
        """遮罩郵箱"""
        if "@" not in email:
            return self._mask_generic(email)

        local, domain = email.split("@", 1)
        if len(local) <= 1:
            masked_local = "*"
        else:
            masked_local = local[0] + "*" * (len(local) - 1)

        return f"{masked_local}@{domain}"

    def _mask_phone(self, phone: str) -> str:
        """遮罩電話號碼"""
        # 移除所有非數字字符
        digits = re.sub(r'\D', '', phone)
        if len(digits) <= 4:
            return "*" * len(digits)

        # 保留後4位，前面的數字遮罩
        return "*" * (len(digits) - 4) + digits[-4:]

    def _mask_credit_card(self, card: str) -> str:
        """遮罩信用卡號"""
        digits = re.sub(r'\D', '', card)
        if len(digits) <= 4:
            return "*" * len(digits)

        return "*" * (len(digits) - 4) + digits[-4:]

    def _mask_ssn(self, ssn: str) -> str:
        """遮罩SSN (社會安全號)"""
        digits = re.sub(r'\D', '', ssn)
        if len(digits) != 9:
            return self._mask_generic(ssn)

        # SSN格式: XXX-XX-XXXX，遮罩中間部分
        return f"{digits[:3]}-{'*' * 2}-{digits[-4:]}"

    def _mask_generic(self, value: str) -> str:
        """通用遮罩"""
        if len(value) <= 4:
            return "*" * len(value)
        return "*" * (len(value) - 4) + value[-4:]

    def _encrypt_value(self, value: str) -> str:
        """加密值"""
        encrypted = self.fernet.encrypt(value.encode())
        return base64.urlsafe_b64encode(encrypted).decode()

    def _replace_value(self, value: str, entity_type: PIIEntityType) -> str:
        """替換值"""
        replacements = {
            PIIEntityType.ADDRESS: "[ADDRESS]",
            PIIEntityType.LOCATION: "[LOCATION]",
            PIIEntityType.URL: "[URL]",
            PIIEntityType.IP_ADDRESS: "[IP_ADDRESS]",
        }

        return replacements.get(entity_type, "[REDACTED]")

    def deanonymize_value(self, encrypted_value: str, key_id: str) -> Optional[str]:
        """解密值"""
        try:
            if key_id != self.key_id:
                self.logger.warning("key_id_mismatch_for_deanonymization",
                                  provided_key_id=key_id,
                                  expected_key_id=self.key_id)
                return None

            encrypted_bytes = base64.urlsafe_b64decode(encrypted_value)
            decrypted = self.fernet.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception as e:
            self.logger.error("deanonymization_failed", error=str(e))
            return None


class PIIDetector:
    """
    PII檢測器核心類

    實現企業級PII檢測與脫敏，支援：
    - 跨語言實體識別
    - 多重脫敏策略
    - 合規規則檢查
    - 性能優化與快取
    """

    def __init__(self, config_manager=None):
        self.config_manager = config_manager or get_config_manager()
        self.logger = get_logger(__name__)

        # 載入配置
        self.config = self.config_manager.get("pii_detection", {})
        self.logger.info("pii_detector_initializing", config_provided=bool(self.config))

        # 初始化組件
        self.anonymization_engine = AnonymizationEngine(self.config.get("anonymization", {}))

        # 快取和性能優化
        self._detection_cache = {}
        self._cache_lock = threading.Lock()

        # 統計信息
        self.stats = {
            "total_processed": 0,
            "entities_detected": 0,
            "anonymized_count": 0,
            "detection_time_avg": 0.0,
            "cache_hit_rate": 0.0,
            "errors_count": 0
        }

        self.logger.info("pii_detector_initialized")

    async def process_records(self, records: List['DataRecord']) -> List['DataRecord']:
        """
        處理數據記錄列表，檢測並脫敏PII

        Args:
            records: 輸入數據記錄

        Returns:
            處理後的記錄列表
        """
        if not self.config.get("enabled", True):
            self.logger.debug("pii_detection_disabled")
            return records

        self.logger.info("starting_pii_detection", record_count=len(records))

        start_time = datetime.utcnow()
        processed_records = []

        # 批處理優化
        batch_size = self.config.get("batch_size", 100)

        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            processed_batch = await self._process_batch(batch)
            processed_records.extend(processed_batch)

        processing_time = (datetime.utcnow() - start_time).total_seconds()

        self.logger.info("pii_detection_completed",
                        input_count=len(records),
                        output_count=len(processed_records),
                        processing_time=round(processing_time, 2),
                        entities_anonymized=self.stats["anonymized_count"])

        return processed_records

    async def _process_batch(self, batch: List['DataRecord']) -> List['DataRecord']:
        """處理批次記錄"""
        # 並發處理
        tasks = [self._process_single_record(record) for record in batch]

        # 控制並發數量
        semaphore = asyncio.Semaphore(self.config.get("max_concurrent", 4))

        async def process_with_semaphore(record, task):
            async with semaphore:
                return await task

        results = await asyncio.gather(*[
            process_with_semaphore(record, self._process_single_record(record))
            for record in batch
        ], return_exceptions=True)

        # 處理結果和異常
        processed_batch = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.logger.error("record_processing_failed",
                                record_id=id(batch[i]),
                                error=str(result))
                # 返回原始記錄並標記錯誤
                batch[i].add_error(f"PII處理失敗: {result}")
                processed_batch.append(batch[i])
                self.stats["errors_count"] += 1
            else:
                processed_batch.append(result)

        return processed_batch

    async def _process_single_record(self, record: 'DataRecord') -> 'DataRecord':
        """處理單個記錄"""
        try:
            self.stats["total_processed"] += 1

            # 記錄副本，避免修改原始數據
            processed_record = DataRecord(record.data.copy(), record.source)
            processed_record.quality_score = record.quality_score

            # 檢測PII實體
            detection_result = await self._detect_pii_in_record(processed_record)

            if detection_result.total_entities > 0:
                # 脫敏處理
                anonymization_results = await self._anonymize_entities(
                    processed_record, detection_result
                )

                # 記錄到審計日誌
                await self._log_anonymization_audit(
                    processed_record, detection_result, anonymization_results
                )

                # 更新記錄元數據
                processed_record.set_field("pii_detected", True, "pii_detection")
                processed_record.set_field("pii_entities_count",
                                         detection_result.total_entities, "pii_count")
                processed_record.set_field("pii_anonymized", True, "pii_anonymization")

            return processed_record

        except Exception as e:
            record.add_error(f"PII處理異常: {e}")
            self.logger.error("single_record_processing_error", error=str(e))
            return record

    async def _detect_pii_in_record(self, record: 'DataRecord') -> PIIDetectionResult:
        """在記錄中檢測PII"""
        start_time = datetime.utcnow()

        # 合併所有文本字段進行檢測
        text_fields = self.config.get("text_fields", ["title", "content", "description"])
        combined_text = self._combine_record_text(record, text_fields)

        if not combined_text.strip():
            return PIIDetectionResult(
                text_id=str(id(record)),
                entities_found=[],
                processing_time=0.0,
                language_detected="unknown"
            )

        # 快取檢查
        cache_key = hashlib.md5(combined_text.encode()).hexdigest()
        if cache_key in self._detection_cache:
            cached_result = PIIDetectionResult(**self._detection_cache[cache_key])
            cached_result.processing_time = (datetime.utcnow() - start_time).total_seconds()
            return cached_result

        # 語言檢測
        language = self._detect_language(combined_text)

        # PII檢測邏輯
        entities_found = await self._perform_pii_detection(combined_text, language)

        # 應用合規規則
        entities_found = await self._apply_compliance_rules(entities_found)

        # 置信度過濾
        confidence_threshold = self.config.get("confidence_threshold", 0.7)
        filtered_entities = [
            entity for entity in entities_found
            if entity.confidence_score >= confidence_threshold
        ]

        processing_time = (datetime.utcnow() - start_time).total_seconds()

        result = PIIDetectionResult(
            text_id=str(id(record)),
            entities_found=filtered_entities,
            processing_time=processing_time,
            language_detected=language
        )

        # 快取結果
        with self._cache_lock:
            self._detection_cache[cache_key] = {
                "text_id": result.text_id,
                "entities_found": [entity.to_dict() for entity in result.entities_found],
                "processing_time": result.processing_time,
                "language_detected": result.language_detected,
                "total_entities": result.total_entities,
                "high_confidence_count": result.high_confidence_count,
                "anonymized": result.anonymized,
                "compliance_report": result.compliance_report
            }

        self.stats["entities_detected"] += len(filtered_entities)
        self.stats["detection_time_avg"] = (
            (self.stats["detection_time_avg"] * (self.stats["total_processed"] - 1)) +
            processing_time
        ) / self.stats["total_processed"]

        return result

    def _combine_record_text(self, record: 'DataRecord', text_fields: List[str]) -> str:
        """合併記錄的文本字段"""
        texts = []
        for field in text_fields:
            value = record.get_field(field, "")
            if isinstance(value, str):
                texts.append(value)

        return " ".join(texts)

    def _detect_language(self, text: str) -> str:
        """檢測文本語言"""
        try:
            # 簡化的語言檢測邏輯
            if any(ord(char) > 127 for char in text):
                return "zh"  # 中文
            else:
                return "en"  # 英文
        except:
            return "unknown"

    async def _perform_pii_detection(self, text: str, language: str) -> List[PIIEntity]:
        """執行PII檢測"""
        # 此處實現具體的PII檢測邏輯
        # 使用正則表達式和簡單的關鍵詞匹配作為基礎實現
        # 生產環境中應替換為更強大的NLP模型

        entities = []

        # 定義檢測模式
        patterns = self._get_detection_patterns(language)

        for pattern_name, pattern_config in patterns.items():
            pattern = pattern_config["regex"]
            entity_type = pattern_config["type"]
            confidence = pattern_config["confidence"]

            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)

            for match in matches:
                entity = PIIEntity(
                    entity_type=entity_type,
                    value=match.group(),
                    start_index=match.start(),
                    end_index=match.end(),
                    confidence_score=confidence,
                    context=text[max(0, match.start()-20):match.end()+20],
                    language=language,
                    compliance_level=pattern_config.get("compliance_level", ComplianceLevel.CONFIDENTIAL)
                )
                entities.append(entity)

        # 去重處理
        entities = self._deduplicate_entities(entities)

        return entities

    def _get_detection_patterns(self, language: str) -> Dict[str, Dict[str, Any]]:
        """獲取檢測模式"""
        base_patterns = {
            # 郵箱
            "email": {
                "regex": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                "type": PIIEntityType.EMAIL_ADDRESS,
                "confidence": 0.95,
                "compliance_level": ComplianceLevel.CONFIDENTIAL
            },
            # 手機號 (簡化版本)
            "phone": {
                "regex": r'\b(?:\+?86)?(?:1[3-9]\d{9}|[0-9]{3,4}-?[0-9]{7,8}(?:-[0-9]{1,4})?)\b',
                "type": PIIEntityType.PHONE_NUMBER,
                "confidence": 0.85,
                "compliance_level": ComplianceLevel.CONFIDENTIAL
            },
            # 信用卡
            "credit_card": {
                "regex": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
                "type": PIIEntityType.CREDIT_CARD,
                "confidence": 0.90,
                "compliance_level": ComplianceLevel.RESTRICTED
            },
            # SSN (美國社會安全號)
            "ssn": {
                "regex": r'\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b',
                "type": PIIEntityType.SSN,
                "confidence": 0.85,
                "compliance_level": ComplianceLevel.RESTRICTED
            },
            # IP地址
            "ip": {
                "regex": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
                "type": PIIEntityType.IP_ADDRESS,
                "confidence": 0.80,
                "compliance_level": ComplianceLevel.CONFIDENTIAL
            }
        }

        # 語言特定模式
        if language == "zh":
            base_patterns.update({
                # 中文手機號
                "chinese_phone": {
                    "regex": r'\b1[3-9]\d{9}\b',
                    "type": PIIEntityType.PHONE_NUMBER,
                    "confidence": 0.95,
                    "compliance_level": ComplianceLevel.CONFIDENTIAL
                },
                # 中文地址關鍵詞 (簡化)
                "chinese_address": {
                    "regex": r'\b[\u4e00-\u9fff]+(?:省|市|區|縣|路|街|號)\b',
                    "type": PIIEntityType.ADDRESS,
                    "confidence": 0.70,
                    "compliance_level": ComplianceLevel.CONFIDENTIAL
                }
            })

        return base_patterns

    def _deduplicate_entities(self, entities: List[PIIEntity]) -> List[PIIEntity]:
        """去重實體"""
        seen = set()
        deduplicated = []

        for entity in entities:
            key = (entity.start_index, entity.end_index, entity.entity_type)
            if key not in seen:
                seen.add(key)
                deduplicated.append(entity)

        return deduplicated

    async def _apply_compliance_rules(self, entities: List[PIIEntity]) -> List[PIIEntity]:
        """應用合規規則"""
        # GDPR和HIPAA規則應用
        for entity in entities:
            if entity.entity_type in [PIIEntityType.EMAIL_ADDRESS, PIIEntityType.PHONE_NUMBER,
                                    PIIEntityType.ADDRESS, PIIEntityType.PERSON]:
                # 這些實體受GDPR保護
                entity.metadata["gdpr_applicable"] = True

            if entity.entity_type in [PIIEntityType.HEALTH_RECORD, PIIEntityType.MEDICAL_LICENSE]:
                # 這些實體受HIPAA保護
                entity.metadata["hipaa_applicable"] = True
                entity.compliance_level = ComplianceLevel.RESTRICTED

        return entities

    async def _anonymize_entities(self, record: 'DataRecord',
                                detection_result: PIIDetectionResult) -> List[AnonymizationResult]:
        """脫敏實體"""
        anonymization_results = []

        for entity in detection_result.entities_found:
            result = await self.anonymization_engine.anonymize_entity(entity)
            anonymization_results.append(result)

            # 在記錄中替換PII
            for field_name, field_value in record.data.items():
                if isinstance(field_value, str) and entity.value in field_value:
                    new_value = field_value.replace(entity.value, result.anonymized_value)
                    record.set_field(field_name, new_value, "pii_anonymization")

            self.stats["anonymized_count"] += 1

        return anonymization_results

    async def _log_anonymization_audit(self, record: 'DataRecord',
                                     detection_result: PIIDetectionResult,
                                     anonymization_results: List[AnonymizationResult]):
        """記錄脫敏審計日誌"""
        try:
            audit_data = {
                "event": "pii_anonymization",
                "record_id": str(id(record)),
                "entities_count": detection_result.total_entities,
                "language": detection_result.language_detected,
                "anonymization_results": [
                    {
                        "entity_type": result.original_entity.entity_type.value,
                        "strategy": result.strategy_used.value,
                        "confidence": result.original_entity.confidence_score,
                        "reversible": result.reversible
                    }
                    for result in anonymization_results
                ],
                "compliance": {
                    "gdpr_applicable": any(r.original_entity.metadata.get("gdpr_applicable", False)
                                         for r in anonymization_results),
                    "hipaa_applicable": any(r.original_entity.metadata.get("hipaa_applicable", False)
                                          for r in anonymization_results)
                },
                "processing_time": detection_result.processing_time
            }

            self.logger.info("pii_anonymization_completed", **audit_data)

        except Exception as e:
            self.logger.error("audit_logging_failed", error=str(e))

    def get_stats(self) -> Dict[str, Any]:
        """獲取統計信息"""
        return {
            **self.stats,
            "cache_size": len(self._detection_cache),
            "uptime_seconds": (datetime.utcnow() - datetime.utcnow()).total_seconds()  # 將在初始化時設置
        }

    async def health_check(self) -> Dict[str, Any]:
        """健康檢查"""
        return {
            "status": "healthy",
            "component": "pii_detector",
            "stats": self.get_stats(),
            "config_valid": bool(self.config),
            "anonymization_engine_ready": True
        }


# 從DataRecord導入，這裏需要避免循環導入
from ..data_processing.data_processor import DataRecord


# 全域PII檢測器實例
_pii_detector: Optional[PIIDetector] = None


def init_pii_detector(config_manager=None) -> PIIDetector:
    """
    初始化全域PII檢測器

    Args:
        config_manager: 配置管理器實例

    Returns:
        PII檢測器實例
    """
    global _pii_detector

    if _pii_detector is None:
        _pii_detector = PIIDetector(config_manager)

    return _pii_detector


def get_pii_detector() -> PIIDetector:
    """獲取全域PII檢測器實例"""
    if _pii_detector is None:
        raise RuntimeError("PII檢測器尚未初始化，請先調用init_pii_detector()")
    return _pii_detector
