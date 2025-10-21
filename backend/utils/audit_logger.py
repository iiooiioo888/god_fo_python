"""
WebCrawler Commander - 統一審計日誌系統
企業級合規審計與安全監控

功能特色：
- 全面操作審計
- 合規性報告生成
- 實時安全監控
- 數據訪問追蹤
- 多層次權限審計
"""

import os
import json
import hashlib
import threading
import asyncio
from typing import Dict, List, Optional, Any, Union, Callable, Type
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path
import uuid

from .logger_service import get_logger


class AuditLevel(Enum):
    """審計等級枚舉"""
    TRACE = "TRACE"             # 詳細追蹤
    ACCESS = "ACCESS"           # 資源訪問
    ACTION = "ACTION"           # 用戶操作
    SECURITY = "SECURITY"       # 安全事件
    COMPLIANCE = "COMPLIANCE"   # 合規事件
    EMERGENCY = "EMERGENCY"     # 緊急事件


class AuditCategory(Enum):
    """審計分類枚舉"""
    AUTHENTICATION = "AUTHENTICATION"   # 身份認證
    AUTHORIZATION = "AUTHORIZATION"     # 權限授權
    DATA_ACCESS = "DATA_ACCESS"         # 數據訪問
    SYSTEM_CONFIG = "SYSTEM_CONFIG"     # 系統配置
    BUSINESS_LOGIC = "BUSINESS_LOGIC"   # 業務邏輯
    SECURITY_EVENT = "SECURITY_EVENT"   # 安全事件
    COMPLIANCE_CHECK = "COMPLIANCE_CHECK" # 合規檢查
    SYSTEM_MAINTENANCE = "SYSTEM_MAINTENANCE" # 系統維護


@dataclass
class AuditEvent:
    """審計事件"""
    event_id: str                           # 事件唯一標識
    timestamp: datetime                     # 事件時間
    level: AuditLevel                       # 事件等級
    category: AuditCategory                 # 事件分類
    action: str                             # 操作類型
    actor: str                              # 操作主體（用戶ID或系統組件）
    target: str                             # 操作目標（資源ID）
    result: str                             # 操作結果
    details: Dict[str, Any] = field(default_factory=dict)      # 詳細信息
    ip_address: Optional[str] = None        # IP地址
    user_agent: Optional[str] = None        # 用戶代理
    session_id: Optional[str] = None        # 會話ID
    request_id: Optional[str] = None        # 請求ID
    location: Optional[str] = None          # 地理位置
    device_info: Dict[str, Any] = field(default_factory=dict)  # 設備信息
    compliance_info: Dict[str, Any] = field(default_factory=dict)  # 合規信息
    hash: Optional[str] = None              # 事件哈希（防止篡改）

    def __post_init__(self):
        """自動生成事件哈希"""
        if not self.event_id:
            self.event_id = str(uuid.uuid4())

        # 計算事件哈希用於完整性驗證
        event_data = {
            "event_id": self.event_id,
            "timestamp": self.timestamp.isoformat(),
            "level": self.level.value,
            "category": self.category.value,
            "action": self.action,
            "actor": self.actor,
            "target": self.target,
            "result": self.result,
            "details": json.dumps(self.details, sort_keys=True)
        }

        content = json.dumps(event_data, sort_keys=True)
        self.hash = hashlib.sha256(content.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典"""
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp.isoformat(),
            "level": self.level.value,
            "category": self.category.value,
            "action": self.action,
            "actor": self.actor,
            "target": self.target,
            "result": self.result,
            "details": self.details,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "session_id": self.session_id,
            "request_id": self.request_id,
            "location": self.location,
            "device_info": self.device_info,
            "compliance_info": self.compliance_info,
            "hash": self.hash
        }


@dataclass
class ComplianceReport:
    """合規報告"""
    report_id: str
    generation_date: datetime
    compliance_standard: str
    assessment_period: tuple[datetime, datetime]
    overall_compliance_score: float
    critical_findings: List[str]
    compliance_details: Dict[str, Any] = field(default_factory=dict)
    remediation_actions: List[str] = field(default_factory=list)


class AuditLogger:
    """
    審計日誌記錄器

    提供企業級審計日誌管理：
    - 結構化事件記錄
    - 位置化敏感數據處理
    - 合規性報告生成
    - 實時監控與告警
    """

    def __init__(self, retention_days: int = 2555):  # 7年保留期
        self.logger = get_logger("audit_logger")

        # 配置
        self.retention_days = retention_days
        self.max_daily_logs = 100000  # 每日最大日誌數量

        # 審計事件存儲
        self.audit_events: List[AuditEvent] = []
        self.archive_path = Path("logs/audit_archive")

        # 統計信息
        self.daily_stats = {
            "events_logged": 0,
            "security_events": 0,
            "compliance_checks": 0,
            "unauthorized_access": 0
        }

        # 敏感數據處理
        self.sensitive_fields = {
            "password", "token", "api_key", "secret", "ssn",
            "credit_card", "bank_account", "email"
        }

        # 數據完整性驗證
        self.integrity_check_enabled = True
        self.last_integrity_check = datetime.utcnow()

        # 鎖用於線程安全
        self._lock = threading.Lock()

        # 確保歸檔目錄存在
        self.archive_path.mkdir(parents=True, exist_ok=True)

        self.logger.info("audit_logger_initialized", retention_days=retention_days)

    def log_audit_event(self, level: Union[str, AuditLevel],
                       category: Union[str, AuditCategory],
                       action: str, actor: str, target: str,
                       result: str, **kwargs) -> AuditEvent:
        """
        記錄審計事件

        Args:
            level: 事件等級
            category: 事件分類
            action: 操作類型
            actor: 操作主體
            target: 操作目標
            result: 操作結果
            **kwargs: 附加信息

        Returns:
            記錄的審計事件對象
        """
        # 轉換枚舉類型
        if isinstance(level, str):
            level = AuditLevel(level)
        if isinstance(category, str):
            category = AuditCategory(category)

        # 從上下文獲取信息
        details = kwargs.pop("details", {})
        ip_address = kwargs.pop("ip_address", None)
        user_agent = kwargs.pop("user_agent", None)
        session_id = kwargs.pop("session_id", None)
        request_id = kwargs.pop("request_id", None)
        location = kwargs.pop("location", None)
        device_info = kwargs.pop("device_info", {})
        compliance_info = kwargs.pop("compliance_info", {})

        # 處理敏感數據遮罩
        details = self._sanitize_sensitive_data(details)

        # 創建審計事件
        event = AuditEvent(
            event_id="",  # 自動生成
            timestamp=datetime.utcnow(),
            level=level,
            category=category,
            action=action,
            actor=actor,
            target=target,
            result=result,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id,
            request_id=request_id,
            location=location,
            device_info=device_info,
            compliance_info=compliance_info
        )

        # 添加到存儲
        with self._lock:
            self.audit_events.append(event)
            self._update_stats(event)

            # 檢查日誌數量限制
            if len(self.audit_events) > self.max_daily_logs:
                self._archive_old_events()

        # 寫入專門的審計日誌文件
        self._write_to_audit_log(event)

        # 實時監控關鍵事件
        self._monitor_critical_events(event)

        return event

    def _sanitize_sensitive_data(self, data: Any) -> Any:
        """處理敏感數據遮罩"""
        if isinstance(data, dict):
            sanitized = {}
            for key, value in data.items():
                if key.lower() in self.sensitive_fields:
                    sanitized[key] = self._mask_sensitive_value(str(value))
                else:
                    sanitized[key] = self._sanitize_sensitive_data(value)
            return sanitized
        elif isinstance(data, list):
            return [self._sanitize_sensitive_data(item) for item in data]
        elif isinstance(data, str) and len(data) > 50:  # 長字符串可能包含敏感信息
            # 簡單的敏感數據檢測（生產環境應該更複雜）
            sensitive_keywords = ["password", "token", "key", "secret"]
            for keyword in sensitive_keywords:
                if keyword in data.lower():
                    return self._mask_sensitive_value(data)
        return data

    def _mask_sensitive_value(self, value: str) -> str:
        """遮罩敏感值"""
        if len(value) <= 4:
            return "*" * len(value)
        return value[:2] + "*" * (len(value) - 4) + value[-2:]

    def _update_stats(self, event: AuditEvent):
        """更新統計信息"""
        self.daily_stats["events_logged"] += 1

        if event.category == AuditCategory.SECURITY_EVENT:
            self.daily_stats["security_events"] += 1
        elif event.category == AuditCategory.COMPLIANCE_CHECK:
            self.daily_stats["compliance_checks"] += 1

        # 檢查未授權訪問
        if event.result == "DENIED" or "unauthorized" in event.result.lower():
            self.daily_stats["unauthorized_access"] += 1

    def _write_to_audit_log(self, event: AuditEvent):
        """寫入專門的審計日誌文件"""
        log_line = json.dumps(event.to_dict(), ensure_ascii=False)

        # 按日期分文件
        today = event.timestamp.date()
        log_file = self.archive_path / f"audit_{today}.log"

        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_line + '\n')
        except Exception as e:
            self.logger.error("failed_to_write_audit_log", error=str(e), event_id=event.event_id)

    def _monitor_critical_events(self, event: AuditEvent):
        """監控關鍵事件並發出告警"""
        alert_triggers = {
            AuditLevel.SECURITY: lambda e: e.category == AuditCategory.SECURITY_EVENT,
            AuditLevel.EMERGENCY: lambda e: True,  # 所有緊急事件
            AuditLevel.COMPLIANCE: lambda e: e.result in ["FAILED", "VIOLATION"]
        }

        for level, condition in alert_triggers.items():
            if event.level == level and condition(event):
                self._send_security_alert(event)
                break

    def _send_security_alert(self, event: AuditEvent):
        """發送安全告警"""
        alert_data = {
            "alert_type": "security_event",
            "severity": event.level.value,
            "event_id": event.event_id,
            "category": event.category.value,
            "action": event.action,
            "actor": event.actor,
            "result": event.result,
            "timestamp": event.timestamp.isoformat()
        }

        self.logger.critical("security_alert_triggered", **alert_data)

        # 這裡可以集成其他告警系統（如郵件、Slack等）
        # send_email_alert(alert_data)
        # send_slack_alert(alert_data)

    def generate_compliance_report(self, standard: str = "GDPR",
                                 start_date: Optional[datetime] = None,
                                 end_date: Optional[datetime] = None) -> ComplianceReport:
        """
        生成合規報告

        Args:
            standard: 合規標準 (GDPR/HIPAA/PCI_DSS)
            start_date: 報告開始日期
            end_date: 報告結束日期

        Returns:
            合規報告對象
        """
        if start_date is None:
            start_date = datetime.utcnow() - timedelta(days=90)
        if end_date is None:
            end_date = datetime.utcnow()

        # 過濾相關事件
        relevant_events = [
            event for event in self.audit_events
            if start_date <= event.timestamp <= end_date
            and event.category in [AuditCategory.DATA_ACCESS,
                                 AuditCategory.COMPLIANCE_CHECK,
                                 AuditCategory.SECURITY_EVENT]
        ]

        # 計算合規評分
        compliance_score = self._calculate_compliance_score(relevant_events, standard)

        # 識別關鍵發現
        critical_findings = self._identify_critical_findings(relevant_events, standard)

        # 生成修復建議
        remediation_actions = self._generate_remediation_actions(critical_findings, standard)

        report = ComplianceReport(
            report_id=str(uuid.uuid4()),
            generation_date=datetime.utcnow(),
            compliance_standard=standard,
            assessment_period=(start_date, end_date),
            overall_compliance_score=compliance_score,
            critical_findings=critical_findings,
            compliance_details=self._generate_compliance_details(relevant_events, standard),
            remediation_actions=remediation_actions
        )

        self.logger.info("compliance_report_generated",
                        report_id=report.report_id,
                        standard=standard,
                        score=round(compliance_score, 2),
                        findings_count=len(critical_findings))

        return report

    def _calculate_compliance_score(self, events: List[AuditEvent], standard: str) -> float:
        """計算合規評分"""
        if not events:
            return 100.0  # 沒有事件意味著沒有違規

        score = 100.0
        penalties = {
            "GDPR": {
                "unauthorized_data_access": 10,
                "missing_audit_log": 5,
                "data_breach": 25,
                "failed_compliance_check": 15
            },
            "HIPAA": {
                "unauthorized_medical_data_access": 20,
                "missing_encryption": 15,
                "audit_violation": 10
            },
            "PCI_DSS": {
                "card_data_exposure": 30,
                "failed_security_scan": 10,
                "weak_encryption": 20
            }
        }

        standard_penalties = penalties.get(standard, {})

        for event in events:
            if event.result in ["DENIED", "FAILED", "VIOLATION"]:
                # 基於事件細節確定具體懲罰
                if "data_access" in event.action.lower() and "unauthorized" in str(event.details).lower():
                    score -= standard_penalties.get("unauthorized_data_access", 5)
                elif "encryption" in str(event.details).lower():
                    score -= standard_penalties.get("missing_encryption", 5)
                else:
                    score -= standard_penalties.get("failed_compliance_check", 2)

        return max(0.0, score)

    def _identify_critical_findings(self, events: List[AuditEvent], standard: str) -> List[str]:
        """識別關鍵發現"""
        findings = []
        critical_patterns = {
            "GDPR": [
                "大量個人數據未經授權訪問",
                "數據處理缺乏正當性依據",
                "用戶刪除權未正確執行"
            ],
            "HIPAA": [
                "醫療數據未加密存儲",
                "未經授權訪問PHI數據",
                "缺少業務關聯協議"
            ],
            "PCI_DSS": [
                "持卡人數據暴露風險",
                "安全掃描失敗",
                "弱加密算法使用"
            ]
        }

        standard_patterns = critical_patterns.get(standard, [])

        for pattern in standard_patterns:
            # 檢查是否存在相關事件的模式
            if any(pattern.lower() in str(event.details).lower() for event in events):
                findings.append(pattern)

        # 動態分析其他風險
        failed_events = [e for e in events if e.result in ["FAILED", "VIOLATION"]]
        unauthorized_events = [e for e in events if "unauthorized" in str(e.details).lower()]

        if len(failed_events) > len(events) * 0.1:  # 失敗率超過10%
            findings.append("高比例操作失敗，可能存在系統性問題")

        if len(unauthorized_events) > 0:
            findings.append(f"發現{len(unauthorized_events)}起未經授權訪問事件")

        return findings

    def _generate_remediation_actions(self, findings: List[str], standard: str) -> List[str]:
        """生成修復建議"""
        remediation_map = {
            "GDPR": {
                "大量個人數據未經授權訪問": [
                    "實施更嚴格的存取控制",
                    "增加多因素身份驗證",
                    "定期進行安全意識培訓"
                ],
                "數據處理缺乏正當性依據": [
                    "審查數據處理的法律依據",
                    "記錄所有數據處理目的",
                    "實現自動合規檢查"
                ],
                "高比例操作失敗": [
                    "優化系統性能",
                    "增加錯誤處理能力",
                    "實施更好的監控機制"
                ]
            }
        }

        actions = []
        standard_remediations = remediation_map.get(standard, {})

        for finding in findings:
            if finding in standard_remediations:
                actions.extend(standard_remediations[finding])
            else:
                actions.append(f"針對 '{finding}' 進行專項安全評估")

        return list(set(actions))  # 去重

    def _generate_compliance_details(self, events: List[AuditEvent], standard: str) -> Dict[str, Any]:
        """生成合規詳細信息"""
        details = {
            "total_events_reviewed": len(events),
            "event_distribution": {},
            "timeline_analysis": {},
            "risk_assessment": {}
        }

        # 事件分佈統計
        category_counts = {}
        for event in events:
            category_counts[event.category.value] = category_counts.get(event.category.value, 0) + 1

        details["event_distribution"] = category_counts

        # 時間線分析
        daily_events = {}
        for event in events:
            day = event.timestamp.date()
            daily_events[str(day)] = daily_events.get(str(day), 0) + 1

        details["timeline_analysis"] = daily_events

        # 風險評估
        risk_score = 100.0
        high_risk_events = [e for e in events if e.level in [AuditLevel.EMERGENCY, AuditLevel.SECURITY]]
        risk_score -= len(high_risk_events) * 5

        details["risk_assessment"] = {
            "overall_risk_score": max(0.0, risk_score),
            "high_risk_events": len(high_risk_events),
            "risk_level": "high" if risk_score < 70 else "medium" if risk_score < 85 else "low"
        }

        return details

    def query_audit_events(self, filters: Dict[str, Any],
                          start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None,
                          limit: int = 1000) -> List[AuditEvent]:
        """
        查詢審計事件

        Args:
            filters: 查詢篩選條件
            start_date: 開始日期
            end_date: 結束日期
            limit: 返回記錄數量限制

        Returns:
            匹配的審計事件列表
        """
        filtered_events = self.audit_events.copy()

        # 時間範圍過濾
        if start_date or end_date:
            filtered_events = [
                event for event in filtered_events
                if (not start_date or event.timestamp >= start_date) and
                   (not end_date or event.timestamp <= end_date)
            ]

        # 應用其他篩選條件
        for key, value in filters.items():
            if hasattr(AuditEvent, key):
                filtered_events = [
                    event for event in filtered_events
                    if getattr(event, key) == value
                ]

        # 按時間降序排序並限制數量
        filtered_events.sort(key=lambda e: e.timestamp, reverse=True)
        return filtered_events[:limit]

    def search_security_events(self, keywords: List[str],
                             hours_back: int = 24) -> List[AuditEvent]:
        """
        搜索安全相關事件

        Args:
            keywords: 搜索關鍵詞
            hours_back: 查詢時間範圍（小時）

        Returns:
            匹配的安全事件
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)

        security_events = [
            event for event in self.audit_events
            if event.timestamp >= cutoff_time and
            event.category in [AuditCategory.SECURITY_EVENT, AuditCategory.AUTHENTICATION] and
            event.level in [AuditLevel.SECURITY, AuditLevel.EMERGENCY]
        ]

        # 關鍵詞過濾
        if keywords:
            filtered_events = []
            for event in security_events:
                event_text = json.dumps(event.to_dict(), ensure_ascii=False)
                if any(keyword.lower() in event_text.lower() for keyword in keywords):
                    filtered_events.append(event)
            security_events = filtered_events

        return sorted(security_events, key=lambda e: e.timestamp, reverse=True)

    def get_audit_stats(self) -> Dict[str, Any]:
        """獲取審計統計信息"""
        with self._lock:
            stats = self.daily_stats.copy()

        # 計算更多統計指標
        if self.audit_events:
            latest_event = max(self.audit_events, key=lambda e: e.timestamp)
            oldest_event = min(self.audit_events, key=lambda e: e.timestamp)

            stats.update({
                "total_events_stored": len(self.audit_events),
                "date_range": {
                    "oldest": oldest_event.timestamp.isoformat(),
                    "latest": latest_event.timestamp.isoformat()
                },
                "retention_days": self.retention_days,
                "average_events_per_day": len(self.audit_events) / max(1, (datetime.utcnow() - oldest_event.timestamp).days),
                "integrity_last_checked": self.last_integrity_check.isoformat(),
                "achive_location": str(self.archive_path)
            })

        return stats

    def _archive_old_events(self, force: bool = False):
        """歸檔舊事件"""
        cutoff_date = datetime.utcnow() - timedelta(days=self.retention_days)

        old_events = [event for event in self.audit_events if event.timestamp < cutoff_date]

        if old_events and (force or len(old_events) > 1000):  # 批量歸檔閾值
            # 按月份分組歸檔
            archives = {}
            for event in old_events:
                month_key = event.timestamp.strftime("%Y-%m")
                if month_key not in archives:
                    archives[month_key] = []
                archives[month_key].append(event)

            # 寫入歸檔文件
            for month, events in archives.items():
                archive_file = self.archive_path / f"audit_{month}.archive"

                try:
                    with open(archive_file, 'w', encoding='utf-8') as f:
                        for event in events:
                            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + '\n')
                except Exception as e:
                    self.logger.error("failed_to_archive_events", month=month, error=str(e))

            # 從內存中移除已歸檔的事件
            self.audit_events = [
                event for event in self.audit_events
                if event.timestamp >= cutoff_date
            ]

            self.logger.info("audit_events_archived",
                           archived_count=len(old_events),
                           retained_count=len(self.audit_events),
                           archive_files=len(archives))

    def export_audit_report(self, format: str = "JSON",
                          start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None) -> str:
        """導出審計報告"""
        if start_date or end_date:
            events = self.query_audit_events({}, start_date, end_date, limit=50000)
        else:
            events = self.audit_events

        if format.upper() == "JSON":
            report = {
                "export_timestamp": datetime.utcnow().isoformat(),
                "total_events": len(events),
                "date_range": {
                    "start": min(events, key=lambda e: e.timestamp).timestamp.isoformat() if events else None,
                    "end": max(events, key=lambda e: e.timestamp).timestamp.isoformat() if events else None
                },
                "events": [event.to_dict() for event in events]
            }
            return json.dumps(report, indent=2, ensure_ascii=False)

        return "Unsupported format"

    def verify_integrity(self) -> bool:
        """
        驗證審計日誌完整性

        Returns:
            完整性是否通過
        """
        self.last_integrity_check = datetime.utcnow()
        integrity_issues = []

        for event in self.audit_events:
            # 重新計算哈希進行驗證
            original_hash = event.hash

            # 創建一個臨時事件來計算新哈希
            temp_event = AuditEvent(
                event_id=event.event_id,
                timestamp=event.timestamp,
                level=event.level,
                category=event.category,
                action=event.action,
                actor=event.actor,
                target=event.target,
                result=event.result,
                details=event.details
            )

            if original_hash != temp_event.hash:
                integrity_issues.append(event.event_id)

        if integrity_issues:
            self.logger.warning("audit_integrity_check_failed",
                              corrupted_events=len(integrity_issues),
                              event_ids=integrity_issues[:10])  # 只記錄前10個

            return False

        self.logger.info("audit_integrity_check_passed",
                        events_checked=len(self.audit_events))

        return True


# 全域審計日誌器實例
_audit_logger: Optional[AuditLogger] = None


def get_audit_logger() -> AuditLogger:
    """獲取全域審計日誌器實例"""
    global _audit_logger

    if _audit_logger is None:
        _audit_logger = AuditLogger()

    return _audit_logger


def audit_log(level: Union[str, AuditLevel], category: Union[str, AuditCategory],
              action: str, actor: str, target: str, result: str, **kwargs):
    """便捷的審計日誌記錄函數"""
    logger = get_audit_logger()
    return logger.log_audit_event(level, category, action, actor, target, result, **kwargs)


def with_audit_trail(operation: str, actor_field: str = "user_id"):
    """審計追蹤裝飾器"""
    def decorator(func: Callable):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # 提取操作主體
            actor = "system"  # 默認系統操作
            if actor_field in kwargs:
                actor = kwargs[actor_field]
            elif len(args) > 0 and hasattr(args[0], actor_field):
                actor = getattr(args[0], actor_field, "system")

            target = f"{func.__module__}.{func.__name__}"

            try:
                result = await func(*args, **kwargs)

                # 記錄成功的操作
                audit_log(
                    level=AuditLevel.ACCESS,
                    category=AuditCategory.BUSINESS_LOGIC,
                    action=operation,
                    actor=str(actor),
                    target=target,
                    result="SUCCESS",
                    details={"operation": operation, "target": target}
                )

                return result

            except Exception as e:
                # 記錄失敗的操作
                audit_log(
                    level=AuditLevel.SECURITY,
                    category=AuditCategory.SECURITY_EVENT,
                    action=operation,
                    actor=str(actor),
                    target=target,
                    result="FAILED",
                    details={
                        "operation": operation,
                        "error": str(e),
                        "error_type": type(e).__name__
                    }
                )

                raise e

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            # 提取操作主體
            actor = "system"
            if actor_field in kwargs:
                actor = kwargs[actor_field]
            elif len(args) > 0 and hasattr(args[0], actor_field):
                actor = getattr(args[0], actor_field, "system")

            target = f"{func.__module__}.{func.__name__}"

            try:
                result = func(*args, **kwargs)

                audit_log(
                    level=AuditLevel.ACCESS,
                    category=AuditCategory.BUSINESS_LOGIC,
                    action=operation,
                    actor=str(actor),
                    target=target,
                    result="SUCCESS",
                    details={"operation": operation}
                )

                return result

            except Exception as e:
                audit_log(
                    level=AuditLevel.SECURITY,
                    category=AuditCategory.SECURITY_EVENT,
                    action=operation,
                    actor=str(actor),
                    target=target,
                    result="FAILED",
                    details={
                        "operation": operation,
                        "error": str(e),
                        "error_type": type(e).__name__
                    }
                )

                raise e

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
