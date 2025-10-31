# CH4 代碼示例 - 4.2 資料處理工作流引擎實現

## 工作流引擎核心實現

```python
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
import uuid

class ExecutionStatus(Enum):
    """執行狀態"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRY = "retry"

class TaskStatus(Enum):
    """任務狀態"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class TaskDefinition:
    """任務定義"""
    id: str
    name: str
    type: str
    handler: str
    params: Dict[str, Any] = field(default_factory=dict)
    retry_policy: Dict = field(default_factory=lambda: {"max_retries": 3, "backoff": "exponential"})
    timeout: int = 300
    dependencies: List[str] = field(default_factory=list)

@dataclass
class WorkflowDefinition:
    """工作流定義"""
    id: str
    name: str
    version: str
    tasks: List[TaskDefinition]
    triggers: Dict = field(default_factory=dict)
    variables: Dict = field(default_factory=dict)
    enable_parallel: bool = True

class WorkflowEngine:
    """資料處理工作流引擎"""
    
    def __init__(self, db: 'Database', task_registry: 'TaskRegistry', config: Dict):
        self.db = db
        self.task_registry = task_registry
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.state_manager = StateManager(db)
        self.executor = TaskExecutor(task_registry, config)
    
    async def execute_workflow(
        self,
        workflow_def: WorkflowDefinition,
        input_data: Dict[str, Any],
        user_id: str
    ) -> str:
        """
        執行工作流
        
        Args:
            workflow_def: 工作流定義
            input_data: 輸入數據
            user_id: 用戶 ID
            
        Returns:
            執行 ID
        """
        try:
            # 1. 創建執行記錄
            execution_id = self._create_execution_record(
                workflow_def, input_data, user_id
            )
            
            # 2. 初始化工作流狀態
            await self.state_manager.initialize(execution_id, workflow_def, input_data)
            
            # 3. 執行工作流
            await self._execute_tasks(execution_id, workflow_def)
            
            # 4. 更新執行狀態
            await self.state_manager.update_status(
                execution_id, ExecutionStatus.SUCCESS.value
            )
            
            self.logger.info(f"Workflow {workflow_def.id} executed successfully")
            return execution_id
            
        except Exception as e:
            self.logger.error(f"Workflow execution failed: {str(e)}")
            await self.state_manager.update_status(
                execution_id, ExecutionStatus.FAILED.value, str(e)
            )
            raise
    
    async def _execute_tasks(self, execution_id: str, workflow_def: WorkflowDefinition):
        """執行工作流中的任務"""
        completed_tasks = set()
        pending_tasks = {t.id: t for t in workflow_def.tasks}
        
        while pending_tasks:
            # 找出可執行的任務（依賴都已完成）
            runnable_tasks = [
                t for t in pending_tasks.values()
                if all(dep in completed_tasks for dep in t.dependencies)
            ]
            
            if not runnable_tasks:
                if pending_tasks:
                    raise RuntimeError("Circular dependency detected")
                break
            
            # 執行任務
            if workflow_def.enable_parallel:
                # 並行執行
                tasks = [
                    self._execute_task(execution_id, task)
                    for task in runnable_tasks
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)
            else:
                # 順序執行
                results = []
                for task in runnable_tasks:
                    result = await self._execute_task(execution_id, task)
                    results.append(result)
            
            # 標記完成
            for i, task in enumerate(runnable_tasks):
                result = results[i]
                if isinstance(result, Exception):
                    raise result
                completed_tasks.add(task.id)
                del pending_tasks[task.id]
    
    async def _execute_task(
        self,
        execution_id: str,
        task: TaskDefinition
    ) -> Dict[str, Any]:
        """執行單個任務"""
        task_execution_id = f"{execution_id}_{task.id}"
        
        try:
            # 更新任務狀態為運行中
            await self.state_manager.update_task_status(
                task_execution_id, TaskStatus.RUNNING.value
            )
            
            # 獲取任務輸入數據
            input_data = await self.state_manager.get_task_input(execution_id, task)
            
            # 執行任務
            result = await self.executor.execute(
                task, input_data, execution_id
            )
            
            # 保存任務結果
            await self.state_manager.save_task_result(task_execution_id, result)
            
            # 更新任務狀態為成功
            await self.state_manager.update_task_status(
                task_execution_id, TaskStatus.SUCCESS.value
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Task {task.id} failed: {str(e)}")
            
            # 重試邏輯
            max_retries = task.retry_policy.get("max_retries", 3)
            backoff = task.retry_policy.get("backoff", "exponential")
            
            for attempt in range(max_retries):
                try:
                    wait_time = self._calculate_backoff(backoff, attempt)
                    await asyncio.sleep(wait_time)
                    
                    result = await self.executor.execute(
                        task, input_data, execution_id
                    )
                    
                    await self.state_manager.update_task_status(
                        task_execution_id, TaskStatus.SUCCESS.value
                    )
                    
                    return result
                    
                except Exception as retry_error:
                    if attempt == max_retries - 1:
                        await self.state_manager.update_task_status(
                            task_execution_id, TaskStatus.FAILED.value, str(retry_error)
                        )
                        raise
            
    def _calculate_backoff(self, strategy: str, attempt: int) -> float:
        """計算退避時間"""
        if strategy == "exponential":
            return min(2 ** attempt, 60)  # 最多 60 秒
        elif strategy == "linear":
            return attempt * 5
        else:
            return 1
    
    def _create_execution_record(
        self,
        workflow_def: WorkflowDefinition,
        input_data: Dict,
        user_id: str
    ) -> str:
        """創建執行記錄"""
        execution_id = f"exec-{uuid.uuid4().hex[:12]}"
        
        sql = """
        INSERT INTO workflow_executions (
            execution_id, workflow_id, input_data, status, 
            created_by, created_at
        ) VALUES (
            %(execution_id)s, %(workflow_id)s, %(input_data)s,
            %(status)s, %(user_id)s, %(created_at)s
        )
        """
        
        self.db.execute(sql, {
            'execution_id': execution_id,
            'workflow_id': workflow_def.id,
            'input_data': json.dumps(input_data),
            'status': ExecutionStatus.PENDING.value,
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat()
        })
        
        return execution_id

class TaskExecutor:
    """任務執行器"""
    
    def __init__(self, task_registry: 'TaskRegistry', config: Dict):
        self.task_registry = task_registry
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    async def execute(
        self,
        task: TaskDefinition,
        input_data: Dict[str, Any],
        execution_id: str
    ) -> Dict[str, Any]:
        """執行任務"""
        # 1. 獲取任務處理器
        handler = self.task_registry.get_handler(task.handler)
        
        if not handler:
            raise ValueError(f"Handler not found: {task.handler}")
        
        # 2. 驗證輸入
        validated_input = self._validate_input(task, input_data)
        
        # 3. 執行任務（帶超時控制）
        try:
            result = await asyncio.wait_for(
                handler(validated_input, execution_id),
                timeout=task.timeout
            )
            return result
        except asyncio.TimeoutError:
            raise RuntimeError(f"Task {task.id} timeout after {task.timeout}s")
    
    def _validate_input(
        self,
        task: TaskDefinition,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """驗證並融合輸入數據"""
        merged_input = task.params.copy()
        merged_input.update(input_data)
        return merged_input

class StateManager:
    """工作流狀態管理器"""
    
    def __init__(self, db: 'Database'):
        self.db = db
        self.logger = logging.getLogger(__name__)
    
    async def initialize(
        self,
        execution_id: str,
        workflow_def: WorkflowDefinition,
        input_data: Dict
    ):
        """初始化工作流狀態"""
        # 初始化全局變量
        state = {
            'variables': workflow_def.variables.copy(),
            'input': input_data,
            'tasks': {}
        }
        
        sql = """
        INSERT INTO workflow_states (
            execution_id, state_data, created_at
        ) VALUES (%(execution_id)s, %(state_data)s, %(created_at)s)
        """
        
        self.db.execute(sql, {
            'execution_id': execution_id,
            'state_data': json.dumps(state),
            'created_at': datetime.utcnow().isoformat()
        })
    
    async def update_status(
        self,
        execution_id: str,
        status: str,
        error_message: Optional[str] = None
    ):
        """更新執行狀態"""
        sql = """
        UPDATE workflow_executions 
        SET status = %(status)s, error_message = %(error_message)s,
            updated_at = %(updated_at)s
        WHERE execution_id = %(execution_id)s
        """
        
        self.db.execute(sql, {
            'execution_id': execution_id,
            'status': status,
            'error_message': error_message,
            'updated_at': datetime.utcnow().isoformat()
        })
    
    async def update_task_status(
        self,
        task_execution_id: str,
        status: str,
        error_message: Optional[str] = None
    ):
        """更新任務狀態"""
        sql = """
        INSERT INTO task_executions (
            task_execution_id, status, error_message, created_at
        ) VALUES (
            %(task_execution_id)s, %(status)s, %(error_message)s, %(created_at)s
        )
        """
        
        self.db.execute(sql, {
            'task_execution_id': task_execution_id,
            'status': status,
            'error_message': error_message,
            'created_at': datetime.utcnow().isoformat()
        })
    
    async def save_task_result(
        self,
        task_execution_id: str,
        result: Dict[str, Any]
    ):
        """保存任務結果"""
        sql = """
        UPDATE task_executions 
        SET result = %(result)s
        WHERE task_execution_id = %(task_execution_id)s
        """
        
        self.db.execute(sql, {
            'task_execution_id': task_execution_id,
            'result': json.dumps(result)
        })
    
    async def get_task_input(
        self,
        execution_id: str,
        task: TaskDefinition
    ) -> Dict[str, Any]:
        """獲取任務輸入數據"""
        # 從狀態中獲取輸入和依賴任務的結果
        state_sql = "SELECT state_data FROM workflow_states WHERE execution_id = %s"
        state_row = self.db.fetchone(state_sql, (execution_id,))
        
        if state_row:
            state = json.loads(state_row['state_data'])
            input_data = state.get('input', {}).copy()
            
            # 合併依賴任務的結果
            for dep_id in task.dependencies:
                result_sql = """
                SELECT result FROM task_executions 
                WHERE task_execution_id = %s
                """
                result_row = self.db.fetchone(result_sql, (f"{execution_id}_{dep_id}",))
                if result_row and result_row['result']:
                    dep_result = json.loads(result_row['result'])
                    input_data[dep_id] = dep_result
            
            return input_data
        
        return {}
```

---

## 相關文件引用

- **主文檔**: [4.2 詳細功能清單](../ch4-2-詳細功能清單.md)
- **服務集成**: [代碼示例 - 服務集成](ch4-code-02-service-integration.md)
- **數據庫架構**: [代碼示例 - 數據庫定義](ch4-code-03-database-schema.md)
- **API 示例**: [代碼示例 - API 端點](ch4-code-04-api-examples.md)
