# CH8 代碼示例 - 8.6 API 端點詳細規範

## 節點註冊 API

```bash
POST /cluster/nodes/register
Authorization: Bearer <token>

{
  "node_id": "node-001",
  "cpu_cores": 8,
  "memory_gb": 16
}
```

**響應**
```json
{
  "code": 0,
  "data": {"node_id": "node-001", "status": "healthy"}
}
```

## 任務調度 API

```bash
POST /cluster/tasks/schedule
Authorization: Bearer <token>

{
  "definition": {"url": "http://example.com", "rules": {}},
  "priority": 7
}
```

**響應**
```json
{
  "code": 0,
  "data": {"task_id": "task-123", "status": "pending"}
}
```

---

## Python 客戶端

```python
class ClusterClient:
    def register_node(self, node_id: str, cpu_cores: int, memory_gb: int):
        response = requests.post(
            f'{self.base_url}/cluster/nodes/register',
            headers=self.headers,
            json={'node_id': node_id, 'cpu_cores': cpu_cores, 'memory_gb': memory_gb}
        )
        return response.json()['data']
    
    def schedule_task(self, definition: dict, priority: int = 5):
        response = requests.post(
            f'{self.base_url}/cluster/tasks/schedule',
            headers=self.headers,
            json={'definition': definition, 'priority': priority}
        )
        return response.json()['data']['task_id']
```

---

## 相關文件引用

- **核心實現**: [代碼示例 - 集群管理](ch8-code-01-cluster-manager.md)
- **數據庫**: [代碼示例 - 數據庫定義](ch8-code-02-database-schema.md)
