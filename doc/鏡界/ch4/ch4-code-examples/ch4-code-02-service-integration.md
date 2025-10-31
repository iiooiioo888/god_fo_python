# CH4 代碼示例 - 4.3 服務集成與監控

## 任務註冊表實現

```python
from typing import Dict, Callable, Any
import logging

class TaskRegistry:
    """任務處理器註冊表"""
    
    def __init__(self):
        self.handlers: Dict[str, Callable] = {}
        self.logger = logging.getLogger(__name__)
    
    def register(self, task_type: str, handler: Callable):
        """註冊任務處理器"""
        self.handlers[task_type] = handler
        self.logger.info(f"Task handler registered: {task_type}")
    
    def get_handler(self, task_type: str) -> Callable:
        """獲取任務處理器"""
        return self.handlers.get(task_type)
    
    def register_builtin_handlers(self):
        """註冊內置任務處理器"""
        # 資料提取任務
        self.register("data_extract", DataExtractHandler)
        
        # 資料轉換任務
        self.register("data_transform", DataTransformHandler)
        
        # 資料驗證任務
        self.register("data_validate", DataValidateHandler)
        
        # 資料存儲任務
        self.register("data_store", DataStoreHandler)

class DataExtractHandler:
    """資料提取任務處理器"""
    
    async def __call__(self, params: Dict[str, Any], execution_id: str) -> Dict:
        """
        提取資料
        
        params:
            - source: 資料源
            - query: 查詢語句
            - format: 格式 (json, csv, xml)
        """
        source = params.get('source')
        query = params.get('query')
        
        # 連接資料源並執行查詢
        result = {
            'status': 'success',
            'rows_extracted': 1000,
            'data': []  # 實際數據
        }
        
        return result

class DataTransformHandler:
    """資料轉換任務處理器"""
    
    async def __call__(self, params: Dict[str, Any], execution_id: str) -> Dict:
        """轉換資料"""
        transformation_rules = params.get('rules', [])
        input_data = params.get('data_extract', {})
        
        result = {
            'status': 'success',
            'rows_transformed': 1000
        }
        
        return result

class DataValidateHandler:
    """資料驗證任務處理器"""
    
    async def __call__(self, params: Dict[str, Any], execution_id: str) -> Dict:
        """驗證資料"""
        validation_rules = params.get('rules', [])
        
        result = {
            'status': 'success',
            'valid_rows': 980,
            'invalid_rows': 20
        }
        
        return result

class DataStoreHandler:
    """資料存儲任務處理器"""
    
    async def __call__(self, params: Dict[str, Any], execution_id: str) -> Dict:
        """存儲資料"""
        target = params.get('target')
        
        result = {
            'status': 'success',
            'rows_stored': 980
        }
        
        return result

class WorkflowMonitor:
    """工作流監控服務"""
    
    def __init__(self, db: 'Database', config: Dict):
        self.db = db
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    async def get_execution_status(self, execution_id: str) -> Dict:
        """獲取執行狀態"""
        sql = """
        SELECT * FROM workflow_executions
        WHERE execution_id = %s
        """
        
        execution = self.db.fetchone(sql, (execution_id,))
        
        if not execution:
            raise ValueError(f"Execution not found: {execution_id}")
        
        # 獲取任務狀態
        task_sql = """
        SELECT * FROM task_executions
        WHERE task_execution_id LIKE %s
        ORDER BY created_at
        """
        
        tasks = self.db.fetchall(task_sql, (f"{execution_id}_%",))
        
        return {
            'execution_id': execution_id,
            'status': execution.get('status'),
            'progress': self._calculate_progress(tasks),
            'tasks': tasks,
            'created_at': execution.get('created_at'),
            'updated_at': execution.get('updated_at')
        }
    
    def _calculate_progress(self, tasks: List[Dict]) -> float:
        """計算進度百分比"""
        if not tasks:
            return 0.0
        
        completed = sum(1 for t in tasks if t.get('status') == 'success')
        return (completed / len(tasks)) * 100
```

---

## 相關文件引用

- **核心引擎**: [代碼示例 - 工作流引擎](ch4-code-01-workflow-engine.md)
- **數據庫架構**: [代碼示例 - 數據庫定義](ch4-code-03-database-schema.md)
- **API 示例**: [代碼示例 - API 端點](ch4-code-04-api-examples.md)
