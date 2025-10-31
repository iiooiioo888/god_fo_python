# CH4 代碼示例 - 4.6 API 端點詳細規範

## 工作流執行 API

### 1. 創建並執行工作流

**請求**
```bash
POST /workflows/execute
Authorization: Bearer <token>

{
  "workflow_id": "wf_001",
  "input_data": {
    "source": "ds_001",
    "target": "storage_001"
  }
}
```

**成功響應 (202)**
```json
{
  "code": 0,
  "data": {
    "execution_id": "exec-abc123",
    "workflow_id": "wf_001",
    "status": "running",
    "created_at": "2024-10-31T12:00:00Z"
  }
}
```

### 2. 查詢執行狀態

**請求**
```bash
GET /workflows/executions/{execution_id}
Authorization: Bearer <token>
```

**成功響應**
```json
{
  "code": 0,
  "data": {
    "execution_id": "exec-abc123",
    "status": "running",
    "progress": 45.5,
    "tasks": [
      {
        "task_id": "task_extract",
        "status": "success",
        "result": {"rows": 1000}
      }
    ]
  }
}
```

---

## Python 客戶端示例

```python
import requests

class WorkflowClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {token}'}
    
    def execute_workflow(self, workflow_id: str, input_data: dict) -> str:
        """執行工作流"""
        response = requests.post(
            f'{self.base_url}/workflows/execute',
            headers=self.headers,
            json={'workflow_id': workflow_id, 'input_data': input_data}
        )
        return response.json()['data']['execution_id']
    
    def get_execution_status(self, execution_id: str) -> dict:
        """獲取執行狀態"""
        response = requests.get(
            f'{self.base_url}/workflows/executions/{execution_id}',
            headers=self.headers
        )
        return response.json()['data']
```

---

## 相關文件引用

- **核心引擎**: [代碼示例 - 工作流引擎](ch4-code-01-workflow-engine.md)
- **服務集成**: [代碼示例 - 服務集成](ch4-code-02-service-integration.md)
- **數據庫**: [代碼示例 - 數據庫定義](ch4-code-03-database-schema.md)
