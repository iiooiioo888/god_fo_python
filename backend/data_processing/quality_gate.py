"""
WebCrawler Commander - 品質門檻檢查器
數據品質評估與放行控制

作者: Jerry開發工作室
版本: v1.0.0
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from ..utils.logger_service import get_logger
from .data_processor import DataRecord, DataQualityMetrics


@dataclass
class QualityThreshold:
    """品質門檻"""
    completeness_min: float = 80.0
    accuracy_min: float = 85.0
    consistency_min: float = 75.0
    timeliness_max_hours: float = 24.0


class QualityGate:
    """品質門檻"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = get_logger(__name__)
        self.threshold = QualityThreshold(**self.config.get("thresholds", {}))

    async def check_quality(self, records: List[DataRecord], metrics: DataQualityMetrics) -> Dict[str, Any]:
        """檢查品質"""
        self.logger.info("quality_gate_check_started", record_count=len(records))

        results = {
            "passed": True,
            "score": 0.0,
            "issues": [],
            "recommendations": []
        }

        # 檢查各種品質指標
        if metrics.completeness_score < self.threshold.completeness_min:
            results["issues"].append(f"完整性過低: {metrics.completeness_score}%")
            results["passed"] = False

        if metrics.validity_score < self.threshold.accuracy_min:
            results["issues"].append(f"有效性過低: {metrics.validity_score}%")
            results["passed"] = False

        # 計算總體評分
        results["score"] = (metrics.completeness_score + metrics.validity_score) / 2

        self.logger.info("quality_gate_check_completed", passed=results["passed"], score=results["score"])
        return results


def init_quality_gate(config: Optional[Dict[str, Any]] = None) -> QualityGate:
    return QualityGate(config)


def get_quality_gate() -> QualityGate:
    return QualityGate()
