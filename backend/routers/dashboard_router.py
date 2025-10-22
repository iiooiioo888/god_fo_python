#!/usr/bin/env python3
"""
儀表板API路由器
提供前端儀表板所需的數據接口
"""

import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..utils.logger_service import get_logger

# 創建路由器
router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


class SystemStats(BaseModel):
    """系統統計數據"""
    active_crawlers: int
    today_tasks: int
    scraped_data: int
    error_reports: int
    cpu_usage: float


class ResourceStats(BaseModel):
    """系統資源統計"""
    cpu: Dict[str, Any]
    memory: Dict[str, Any]
    disk: Dict[str, Any]
    network: Dict[str, Any]


class CrawlerItem(BaseModel):
    """爬蟲項目"""
    id: str
    name: str
    status: str
    type: str
    schedule: str
    records: int


# 模擬數據存儲（實際應用中應該從數據庫獲取）
_mock_crawlers = [
    {
        "id": "crawler_001",
        "name": "電商產品抓取",
        "description": "京東、淘寶商品信息采集",
        "status": "running",
        "type": "Python",
        "schedule": "每日執行",
        "records": 1254
    },
    {
        "id": "crawler_002",
        "name": "新聞資訊采集",
        "description": "新浪、騰訊新聞自動抓取",
        "status": "running",
        "type": "NodeJS",
        "schedule": "每小時",
        "records": 3876
    },
    {
        "id": "crawler_003",
        "name": "社交媒體監控",
        "description": "微博、微信輿情分析",
        "status": "paused",
        "type": "Python",
        "schedule": "實時",
        "records": 2341
    }
]


@router.get("/stats", response_model=SystemStats)
async def get_system_stats():
    """獲取系統統計數據"""
    logger = get_logger(__name__)

    try:
        # 模擬動態數據（實際應用中從服務獲取）
        stats = {
            "active_crawlers": len([c for c in _mock_crawlers if c["status"] == "running"]),
            "today_tasks": sum(c["records"] for c in _mock_crawlers) // 10,  # 模擬今日任務數
            "scraped_data": sum(c["records"] for c in _mock_crawlers),
            "error_reports": random.randint(0, 10),  # 隨機錯誤數
            "cpu_usage": random.uniform(30, 80)  # 隨機CPU使用率
        }

        logger.debug("system_stats_retrieved", stats=stats)
        return stats

    except Exception as e:
        logger.error("get_system_stats_error", error=str(e))
        raise HTTPException(status_code=500, detail="獲取系統統計失敗")


@router.get("/resources", response_model=ResourceStats)
async def get_resource_stats():
    """獲取系統資源統計"""
    logger = get_logger(__name__)

    try:
        # 模擬系統資源數據
        resources = {
            "cpu": {
                "usage": random.uniform(40, 70),
                "details": "64%"
            },
            "memory": {
                "usage": 40,
                "details": "3.2/8 GB"
            },
            "disk": {
                "usage": 24,
                "details": "120/500 GB"
            },
            "network": {
                "usage": random.uniform(60, 85),
                "details": f"{random.uniform(1, 1.5):.1f} MB/s"
            }
        }

        logger.debug("resource_stats_retrieved", resources=resources)
        return resources

    except Exception as e:
        logger.error("get_resource_stats_error", error=str(e))
        raise HTTPException(status_code=500, detail="獲取資源統計失敗")


@router.get("/crawlers", response_model=List[CrawlerItem])
async def get_crawlers():
    """獲取爬蟲列表"""
    logger = get_logger(__name__)

    try:
        crawlers = []
        for crawler in _mock_crawlers:
            crawlers.append({
                "id": crawler["id"],
                "name": crawler["name"],
                "status": crawler["status"],
                "type": crawler["type"],
                "schedule": crawler["schedule"],
                "records": crawler["records"]
            })

        logger.debug("crawlers_list_retrieved", count=len(crawlers))
        return crawlers

    except Exception as e:
        logger.error("get_crawlers_error", error=str(e))
        raise HTTPException(status_code=500, detail="獲取爬蟲列表失敗")


@router.get("/data-preview")
async def get_data_preview():
    """獲取數據預覽"""
    logger = get_logger(__name__)

    try:
        # 模擬產品數據
        mock_products = [
            {
                "name": "Apple iPhone 13 Pro Max",
                "platform": "京東自營旗艦店",
                "price": 9999.00,
                "sales": "月銷 5萬+",
                "image": "https://static.photos/retail/200x200/1"
            },
            {
                "name": "小米12 Pro",
                "platform": "小米官方旗艦店",
                "price": 4699.00,
                "sales": "月銷 10萬+",
                "image": "https://static.photos/retail/200x200/2"
            },
            {
                "name": "華為Mate 50 Pro",
                "platform": "華為官方旗艦店",
                "price": 6799.00,
                "sales": "月銷 8萬+",
                "image": "https://static.photos/retail/200x200/3"
            },
            {
                "name": "OPPO Find X5 Pro",
                "platform": "OPPO官方旗艦店",
                "price": 5999.00,
                "sales": "月銷 3萬+",
                "image": "https://static.photos/retail/200x200/4"
            }
        ]

        logger.debug("data_preview_retrieved", record_count=len(mock_products))
        return {
            "products": mock_products,
            "total_records": len(mock_products),
            "last_updated": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error("get_data_preview_error", error=str(e))
        raise HTTPException(status_code=500, detail="獲取數據預覽失敗")


@router.get("/system-status")
async def get_system_status():
    """獲取系統整體狀態"""
    logger = get_logger(__name__)

    try:
        status = {
            "overall_status": "running",
            "services": {
                "backend": {"status": "healthy", "response_time": "45ms"},
                "database": {"status": "healthy", "connections": 5},
                "queue": {"status": "healthy", "pending_tasks": 0},
                "monitoring": {"status": "healthy", "alerts": 0}
            },
            "performance": {
                "avg_response_time": "125ms",
                "throughput": "120 req/min",
                "error_rate": "0.1%"
            },
            "last_check": datetime.utcnow().isoformat()
        }

        logger.debug("system_status_retrieved")
        return status

    except Exception as e:
        logger.error("get_system_status_error", error=str(e))
        raise HTTPException(status_code=500, detail="獲取系統狀態失敗")
