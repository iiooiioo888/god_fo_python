# CH9 代碼示例 - 9.6 API 端點詳細規範

## 部署 API

```bash
POST /deployment/deploy
Authorization: Bearer <token>

{
  "service_name": "crawler-service",
  "version": "v2.1.0",
  "config": {"replicas": 3}
}
```

**響應**
```json
{
  "code": 0,
  "data": {"deployment_id": "deploy-123", "status": "in_progress"}
}
```

## 系統指標 API

```bash
GET /monitoring/metrics?time_range=1h
Authorization: Bearer <token>
```

**響應**
```json
{
  "code": 0,
  "data": {
    "cpu_usage": [{"timestamp": "...", "value": 45.2}],
    "memory_usage": [{"timestamp": "...", "value": 62.1}]
  }
}
```

---

## Python 客戶端

```python
class DeploymentClient:
    def deploy(self, service_name: str, version: str):
        response = requests.post(
            f'{self.base_url}/deployment/deploy',
            headers=self.headers,
            json={'service_name': service_name, 'version': version}
        )
        return response.json()['data']['deployment_id']
```

---

## 相關文件引用

- **核心實現**: [代碼示例 - 部署服務](ch9-code-01-deployment-service.md)
- **數據庫**: [代碼示例 - 數據庫定義](ch9-code-02-database-schema.md)
