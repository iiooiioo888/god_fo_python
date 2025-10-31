# CH9 代碼示例 - 9.1 部署與運維管理實現

## 部署服務

```python
from typing import Dict, List, Any
from datetime import datetime
import logging
import asyncio

class DeploymentService:
    """部署服務"""
    
    def __init__(self, db: 'Database', config: Dict):
        self.db = db
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    async def deploy(
        self,
        service_name: str,
        version: str,
        config: Dict
    ) -> str:
        """部署服務版本"""
        deployment_id = f"deploy-{datetime.utcnow().timestamp()}"
        
        try:
            # 1. 驗證版本
            if not await self._validate_version(service_name, version):
                raise ValueError(f"Invalid version: {version}")
            
            # 2. 準備部署
            await self._prepare_deployment(deployment_id, service_name, version)
            
            # 3. 執行部署
            result = await self._execute_deployment(deployment_id, config)
            
            if result:
                status = "success"
            else:
                status = "failed"
            
            # 4. 記錄部署
            await self._record_deployment(
                deployment_id, service_name, version, status
            )
            
            return deployment_id
            
        except Exception as e:
            self.logger.error(f"Deployment failed: {str(e)}")
            await self._record_deployment(
                deployment_id, service_name, version, "failed"
            )
            raise
    
    async def _validate_version(self, service_name: str, version: str) -> bool:
        """驗證版本"""
        # 檢查版本格式和存在性
        return True
    
    async def _prepare_deployment(
        self,
        deployment_id: str,
        service_name: str,
        version: str
    ):
        """準備部署"""
        # 下載部署包
        # 準備配置文件
        # 驗證依賴
        pass
    
    async def _execute_deployment(
        self,
        deployment_id: str,
        config: Dict
    ) -> bool:
        """執行部署"""
        # 停止舊版本
        # 啟動新版本
        # 健康檢查
        return True
    
    async def _record_deployment(
        self,
        deployment_id: str,
        service_name: str,
        version: str,
        status: str
    ):
        """記錄部署"""
        sql = """
        INSERT INTO deployments (
            deployment_id, service_name, version, status, created_at
        ) VALUES (
            %(deployment_id)s, %(service_name)s, %(version)s,
            %(status)s, %(created_at)s
        )
        """
        
        self.db.execute(sql, {
            'deployment_id': deployment_id,
            'service_name': service_name,
            'version': version,
            'status': status,
            'created_at': datetime.utcnow().isoformat()
        })

class MonitoringService:
    """監控服務"""
    
    def __init__(self, db: 'Database', config: Dict):
        self.db = db
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    async def monitor_metrics(self):
        """監控系統指標"""
        while True:
            try:
                metrics = await self._collect_metrics()
                await self._store_metrics(metrics)
                await self._check_alerts(metrics)
            except Exception as e:
                self.logger.error(f"Monitoring error: {str(e)}")
            
            await asyncio.sleep(60)
    
    async def _collect_metrics(self) -> Dict:
        """收集指標"""
        return {
            'cpu_usage': 45.2,
            'memory_usage': 62.1,
            'disk_usage': 78.5,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def _store_metrics(self, metrics: Dict):
        """存儲指標"""
        sql = """
        INSERT INTO metrics (data, recorded_at)
        VALUES (%(data)s, %(recorded_at)s)
        """
        
        import json
        self.db.execute(sql, {
            'data': json.dumps(metrics),
            'recorded_at': metrics['timestamp']
        })
    
    async def _check_alerts(self, metrics: Dict):
        """檢查告警"""
        thresholds = {
            'cpu_usage': 80,
            'memory_usage': 85,
            'disk_usage': 90
        }
        
        for key, threshold in thresholds.items():
            if metrics.get(key, 0) > threshold:
                await self._trigger_alert(key, metrics[key], threshold)
    
    async def _trigger_alert(self, metric_name: str, value: float, threshold: float):
        """觸發告警"""
        self.logger.warning(
            f"Alert: {metric_name}={value}% exceeds threshold {threshold}%"
        )
```

---

## 相關文件引用

- **主文檔**: [9.2 詳細功能清單](../ch9-2-詳細功能清單.md)
- **數據庫**: [代碼示例 - 數據庫定義](ch9-code-02-database-schema.md)
- **API 示例**: [代碼示例 - API 端點](ch9-code-03-api-examples.md)
