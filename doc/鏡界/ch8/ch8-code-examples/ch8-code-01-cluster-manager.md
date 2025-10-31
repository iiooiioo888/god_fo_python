# CH8 代碼示例 - 8.2 分布式爬蟲集群管理實現

## 集群管理器

```python
import asyncio
from typing import Dict, List, Any
from datetime import datetime
from enum import Enum
import logging

class NodeStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    OFFLINE = "offline"

class ClusterManager:
    """爬蟲集群管理器"""
    
    def __init__(self, db: 'Database', config: Dict):
        self.db = db
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.nodes: Dict[str, Any] = {}
        self.task_scheduler = TaskScheduler(db)
    
    async def register_node(
        self,
        node_id: str,
        node_info: Dict
    ) -> bool:
        """註冊爬蟲節點"""
        try:
            node_data = {
                'node_id': node_id,
                'status': NodeStatus.HEALTHY.value,
                'cpu_cores': node_info.get('cpu_cores', 4),
                'memory_gb': node_info.get('memory_gb', 8),
                'registered_at': datetime.utcnow().isoformat()
            }
            
            sql = """
            INSERT INTO cluster_nodes (
                node_id, status, cpu_cores, memory_gb, registered_at
            ) VALUES (
                %(node_id)s, %(status)s, %(cpu_cores)s, %(memory_gb)s, %(registered_at)s
            )
            ON CONFLICT (node_id) DO UPDATE SET
                status = %(status)s
            """
            
            self.db.execute(sql, node_data)
            self.nodes[node_id] = node_data
            
            self.logger.info(f"Node {node_id} registered successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register node: {str(e)}")
            return False
    
    async def schedule_task(
        self,
        task_definition: Dict,
        priority: int = 5
    ) -> str:
        """調度任務"""
        task_id = f"task-{datetime.utcnow().timestamp()}"
        
        # 1. 選擇最佳節點
        best_node = self._select_best_node()
        
        if not best_node:
            raise RuntimeError("No available nodes")
        
        # 2. 創建任務記錄
        task_data = {
            'task_id': task_id,
            'node_id': best_node['node_id'],
            'definition': task_definition,
            'status': 'pending',
            'priority': priority,
            'created_at': datetime.utcnow().isoformat()
        }
        
        sql = """
        INSERT INTO crawler_tasks (
            task_id, node_id, definition, status, priority, created_at
        ) VALUES (
            %(task_id)s, %(node_id)s, %(definition)s,
            %(status)s, %(priority)s, %(created_at)s
        )
        """
        
        self.db.execute(sql, task_data)
        
        return task_id
    
    def _select_best_node(self) -> Dict:
        """選擇最佳節點"""
        healthy_nodes = [
            n for n in self.nodes.values()
            if n['status'] == NodeStatus.HEALTHY.value
        ]
        
        if not healthy_nodes:
            return None
        
        # 按 CPU 和內存選擇
        return max(healthy_nodes, key=lambda n: n['cpu_cores'] + n['memory_gb'])
    
    async def monitor_nodes(self):
        """監控節點健康狀態"""
        while True:
            for node_id, node in self.nodes.items():
                try:
                    health_check = await self._health_check(node_id)
                    
                    if health_check:
                        status = NodeStatus.HEALTHY.value
                    else:
                        status = NodeStatus.UNHEALTHY.value
                    
                    self._update_node_status(node_id, status)
                    
                except Exception as e:
                    self.logger.error(f"Health check failed for {node_id}: {str(e)}")
                    self._update_node_status(node_id, NodeStatus.OFFLINE.value)
            
            await asyncio.sleep(60)  # 每 60 秒檢查一次
    
    async def _health_check(self, node_id: str) -> bool:
        """健康檢查"""
        # 實現實際的健康檢查邏輯
        return True
    
    def _update_node_status(self, node_id: str, status: str):
        """更新節點狀態"""
        sql = "UPDATE cluster_nodes SET status = %s WHERE node_id = %s"
        self.db.execute(sql, (status, node_id))
        self.nodes[node_id]['status'] = status

class TaskScheduler:
    """任務調度器"""
    
    def __init__(self, db: 'Database'):
        self.db = db
    
    async def get_next_task(self, node_id: str) -> Dict:
        """獲取下一個待執行的任務"""
        sql = """
        SELECT * FROM crawler_tasks
        WHERE status = 'pending' AND node_id = %s
        ORDER BY priority DESC, created_at ASC
        LIMIT 1
        """
        
        task = self.db.fetchone(sql, (node_id,))
        return task
    
    async def update_task_status(
        self,
        task_id: str,
        status: str,
        result: Dict = None
    ):
        """更新任務狀態"""
        sql = """
        UPDATE crawler_tasks
        SET status = %s, result = %s, completed_at = %s
        WHERE task_id = %s
        """
        
        import json
        self.db.execute(sql, (
            status,
            json.dumps(result) if result else None,
            datetime.utcnow().isoformat() if status == 'success' else None,
            task_id
        ))
```

---

## 相關文件引用

- **主文檔**: [8.2 詳細功能清單](../ch8-2-詳細功能清單.md)
- **數據庫**: [代碼示例 - 數據庫定義](ch8-code-02-database-schema.md)
- **API 示例**: [代碼示例 - API 端點](ch8-code-03-api-examples.md)
