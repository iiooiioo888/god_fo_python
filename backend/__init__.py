"""
WebCrawler Commander Backend

企業級爬蟲管理系統後端服務

模組結構:
├── services/          - 核心業務服務
├── data_processing/   - 數據處理服務
├── security/          - 安全與合規服務
├── monitoring/        - 監控與分析服務
├── api/               - API接口服務
├── task_management/   - 任務管理服務
├── deployment/        - 部署與運維服務
├── testing/           - 測試套件
├── utils/             - 工具與實用程式
└── config/            - 配置文件

作者: Jerry開發工作室
版本: v1.0.0
"""

__version__ = "1.0.0"
__author__ = "Jerry開發工作室"
__description__ = "企業級爬蟲管理與數據分析系統"

# 導出主要服務
from .main import create_application

__all__ = [
    "create_application",
]
