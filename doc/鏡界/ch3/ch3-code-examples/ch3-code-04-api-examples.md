# CH3 代碼示例 - 3.6 API 端點詳細規範

## 健康檢測 API

### 1. 執行健康檢測

**請求**
```bash
POST /health-checks/perform
Authorization: Bearer <token>

{
  "datasource_id": "ds_001"
}
```

**成功響應 (202)**
```json
{
  "code": 0,
  "data": {
    "check_id": "check_abc123",
    "datasource_id": "ds_001",
    "status": "in_progress",
    "started_at": "2024-10-31T12:00:00Z"
  }
}
```

### 2. 獲取檢測結果

**請求**
```bash
GET /health-checks/{check_id}
Authorization: Bearer <token>
```

**成功響應**
```json
{
  "code": 0,
  "data": {
    "check_id": "check_abc123",
    "datasource_id": "ds_001",
    "overall_status": "healthy",
    "checks": {
      "http_connection": {"success": true, "status_code": 200},
      "dns_resolution": {"success": true, "resolved_ips": ["192.168.1.1"]},
      "ssl_certificate": {"success": true, "days_remaining": 287},
      "response_time": {"avg_response_time_ms": 145}
    },
    "metrics": {
      "availability": 99.95,
      "response_time_ms": 145,
      "error_rate_percent": 0.05,
      "quality_score": 98.5
    },
    "check_time": "2024-10-31T12:00:30Z"
  }
}
```

### 3. 獲取健康歷史

**請求**
```bash
GET /datasources/{datasource_id}/health-history?days=7
Authorization: Bearer <token>
```

**成功響應**
```json
{
  "code": 0,
  "data": {
    "datasource_id": "ds_001",
    "period": "7d",
    "records": [
      {
        "check_time": "2024-10-31T12:00:00Z",
        "overall_status": "healthy",
        "availability": 99.95,
        "response_time_ms": 145
      }
    ]
  }
}
```

---

## 告警 API

### 1. 查詢告警

**請求**
```bash
GET /alerts?status=active&level=critical&page=1&size=20
Authorization: Bearer <token>
```

**成功響應**
```json
{
  "code": 0,
  "data": {
    "total": 5,
    "items": [
      {
        "alert_id": "alert_001",
        "datasource_id": "ds_001",
        "level": "critical",
        "message": "Data source is unavailable",
        "status": "active",
        "created_at": "2024-10-31T11:30:00Z"
      }
    ]
  }
}
```

### 2. 確認告警

**請求**
```bash
POST /alerts/{alert_id}/acknowledge
Authorization: Bearer <token>

{
  "comment": "Acknowledged, investigating..."
}
```

**成功響應**
```json
{
  "code": 0,
  "data": {
    "alert_id": "alert_001",
    "status": "acknowledged",
    "acknowledged_at": "2024-10-31T12:00:00Z"
  }
}
```

---

## Python 客戶端示例

```python
import requests
from typing import Dict, List

class HealthMonitorClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {token}'}
    
    def perform_health_check(self, datasource_id: str) -> Dict:
        """執行健康檢測"""
        response = requests.post(
            f'{self.base_url}/health-checks/perform',
            headers=self.headers,
            json={'datasource_id': datasource_id}
        )
        return response.json()
    
    def get_health_history(self, datasource_id: str, days: int = 7) -> Dict:
        """獲取健康歷史"""
        response = requests.get(
            f'{self.base_url}/datasources/{datasource_id}/health-history',
            headers=self.headers,
            params={'days': days}
        )
        return response.json()
    
    def get_alerts(self, status: str = 'active', level: str = None) -> Dict:
        """查詢告警"""
        params = {'status': status}
        if level:
            params['level'] = level
        
        response = requests.get(
            f'{self.base_url}/alerts',
            headers=self.headers,
            params=params
        )
        return response.json()
    
    def acknowledge_alert(self, alert_id: str, comment: str = '') -> Dict:
        """確認告警"""
        response = requests.post(
            f'{self.base_url}/alerts/{alert_id}/acknowledge',
            headers=self.headers,
            json={'comment': comment}
        )
        return response.json()

# 使用示例
client = HealthMonitorClient(
    'https://api.health-monitor.example.com/api/v1',
    'your_token_here'
)

# 執行檢測
result = client.perform_health_check('ds_001')

# 查詢告警
alerts = client.get_alerts(status='active')
```

---

## 相關文件引用

- **核心監測**: [代碼示例 - 健康監測](ch3-code-01-health-monitor.md)
- **告警系統**: [代碼示例 - 告警系統](ch3-code-02-alert-system.md)
- **數據庫**: [代碼示例 - 數據庫定義](ch3-code-03-database-schema.md)
