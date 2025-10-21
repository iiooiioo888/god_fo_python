"""
WebCrawler Commander - 數據處理管道
企業級數據清理、驗證和轉換管道系統

作者: Jerry開發工作室
版本: v1.0.0
"""

from .data_processor import (
    DataProcessor, DataCleaner, DuplicateDetector, DataValidator,
    DataRecord, DataQualityMetrics, ProcessingResult,
    DataFormat, DataQualityDimension
)

from .pipeline_orchestrator import PipelineOrchestrator
from .advanced_cleaner import AdvancedDataCleaner
from .smart_validator import SmartDataValidator
from .data_enricher import DataEnricher
from .quality_gate import QualityGate
from .batch_processor import BatchProcessor

__all__ = [
    # 核心數據處理器
    'DataProcessor',
    'DataCleaner',
    'DuplicateDetector',
    'DataValidator',

    # 數據模型
    'DataRecord',
    'DataQualityMetrics',
    'ProcessingResult',
    'DataFormat',
    'DataQualityDimension',

    # 高級處理管道組件
    'PipelineOrchestrator',
    'AdvancedDataCleaner',
    'SmartDataValidator',
    'DataEnricher',
    'QualityGate',
    'BatchProcessor'
]

__version__ = "1.0.0"
