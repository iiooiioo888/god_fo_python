# CH1 代碼示例 - 1.6 API 端點詳細規範

## API 基礎信息

### 服務端點
```
生產環境: https://api.mirror.example.com/api/v1
開發環境: http://localhost:8080/api/v1
測試環境: https://staging-api.mirror.example.com/api/v1
```

### 認證方式
```
Bearer Token (JWT)
Header: Authorization: Bearer <your_jwt_token>
```

### 通用響應格式

#### 成功響應 (HTTP 200)
```json
{
  "code": 0,
  "message": "Success",
  "data": {
    // 實際數據
  },
  "timestamp": "2024-10-31T10:30:00Z",
  "request_id": "req_abc123def456"
}
```

#### 錯誤響應 (HTTP 4xx/5xx)
```json
{
  "code": 40001,
  "message": "Data source not found",
  "error": {
    "type": "NOT_FOUND",
    "details": "Data source with ID 'ds_001' does not exist",
    "error_code": "DATASOURCE_NOT_FOUND"
  },
  "timestamp": "2024-10-31T10:30:00Z",
  "request_id": "req_abc123def456"
}
```

---

## 資料源管理 API

### 1. 創建資料源

**請求**
```bash
POST /datasources
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "User Analytics Database",
  "url": "postgresql://db.prod.example.com:5432/analytics",
  "type": "postgresql",
  "description": "Main analytics database for user behavior analysis",
  "category": "database",
  "tags": ["production", "analytics", "postgresql"],
  "metadata": {
    "schema": "public",
    "table": "user_events",
    "update_frequency": "hourly"
  },
  "connection_config": {
    "host": "db.prod.example.com",
    "port": 5432,
    "database": "analytics",
    "ssl_mode": "require"
  }
}
```

**成功響應 (HTTP 201)**
```json
{
  "code": 0,
  "message": "Data source created successfully",
  "data": {
    "id": "ds_20241031_001",
    "name": "User Analytics Database",
    "url": "postgresql://db.prod.example.com:5432/analytics",
    "type": "postgresql",
    "status": "active",
    "category": "database",
    "tags": ["production", "analytics", "postgresql"],
    "created_at": "2024-10-31T10:30:00Z",
    "created_by": "user_123",
    "version_id": "v1.0.0"
  },
  "timestamp": "2024-10-31T10:30:00Z"
}
```

### 2. 獲取資料源詳情

**請求**
```bash
GET /datasources/{datasource_id}
Authorization: Bearer <token>

# 示例
GET /datasources/ds_20241031_001
```

**成功響應 (HTTP 200)**
```json
{
  "code": 0,
  "message": "Success",
  "data": {
    "id": "ds_20241031_001",
    "name": "User Analytics Database",
    "url": "postgresql://db.prod.example.com:5432/analytics",
    "type": "postgresql",
    "status": "active",
    "category": "database",
    "tags": ["production", "analytics"],
    "description": "Main analytics database",
    "owner_id": "user_123",
    "created_at": "2024-10-31T10:30:00Z",
    "updated_at": "2024-10-31T11:00:00Z",
    "access_count": 1542,
    "health": {
      "status": "healthy",
      "availability": 99.95,
      "last_check": "2024-10-31T11:25:00Z",
      "quality_score": 94.5
    },
    "version_id": "v1.0.0"
  }
}
```

### 3. 查詢資料源列表

**請求**
```bash
GET /datasources?page=1&size=20&type=postgresql&status=active&sort_by=created_at&sort_order=desc
Authorization: Bearer <token>
```

**請求參數**
| 參數 | 類型 | 必需 | 說明 |
|------|------|------|------|
| page | integer | 否 | 頁碼，默認 1 |
| size | integer | 否 | 每頁數量，默認 20，最大 100 |
| type | string | 否 | 資料源類型過濾 |
| status | string | 否 | 狀態過濾 (active, inactive, archived) |
| category | string | 否 | 分類過濾 |
| owner_id | string | 否 | 所有者過濾 |
| sort_by | string | 否 | 排序字段 (created_at, updated_at, name) |
| sort_order | string | 否 | 排序順序 (asc, desc) |

**成功響應 (HTTP 200)**
```json
{
  "code": 0,
  "message": "Success",
  "data": {
    "page": 1,
    "size": 20,
    "total": 156,
    "total_pages": 8,
    "items": [
      {
        "id": "ds_20241031_001",
        "name": "User Analytics Database",
        "type": "postgresql",
        "category": "database",
        "status": "active",
        "owner_id": "user_123",
        "created_at": "2024-10-31T10:30:00Z",
        "health_status": "healthy",
        "quality_score": 94.5
      },
      // ... 更多資料源
    ]
  }
}
```

### 4. 更新資料源

**請求**
```bash
PUT /datasources/{datasource_id}
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "User Analytics Database (Updated)",
  "description": "Updated description",
  "tags": ["production", "analytics", "postgresql", "v2"],
  "category": "database"
}
```

**成功響應 (HTTP 200)**
```json
{
  "code": 0,
  "message": "Data source updated successfully",
  "data": {
    "id": "ds_20241031_001",
    "name": "User Analytics Database (Updated)",
    "version_id": "v1.0.1",
    "updated_at": "2024-10-31T11:00:00Z",
    "change_log": {
      "name": "User Analytics Database -> User Analytics Database (Updated)",
      "tags": ["production", "analytics", "postgresql"] -> ["production", "analytics", "postgresql", "v2"]
    }
  }
}
```

### 5. 刪除資料源

**請求**
```bash
DELETE /datasources/{datasource_id}
Authorization: Bearer <token>

# 示例
DELETE /datasources/ds_20241031_001
```

**成功響應 (HTTP 200)**
```json
{
  "code": 0,
  "message": "Data source deleted successfully",
  "data": {
    "id": "ds_20241031_001",
    "deleted_at": "2024-10-31T11:05:00Z",
    "deletion_type": "soft_delete"
  }
}
```

---

## 搜尋 API

### 1. 全文搜尋

**請求**
```bash
GET /search?q=user&page=1&size=20&filters[type]=postgresql&filters[status]=active
Authorization: Bearer <token>

# 或使用 POST 進行複雜查詢
POST /search
Content-Type: application/json
Authorization: Bearer <token>

{
  "query": "user database",
  "page": 1,
  "size": 20,
  "filters": {
    "type": "postgresql",
    "status": "active",
    "category": ["database", "analytics"]
  },
  "sort_by": "relevance",
  "sort_order": "desc"
}
```

**成功響應 (HTTP 200)**
```json
{
  "code": 0,
  "message": "Success",
  "data": {
    "query": "user database",
    "total": 45,
    "page": 1,
    "size": 20,
    "results": [
      {
        "id": "ds_20241031_001",
        "name": "User Analytics Database",
        "type": "postgresql",
        "description": "Main analytics database for user behavior analysis",
        "score": 0.98,
        "health_status": "healthy",
        "quality_score": 94.5,
        "tags": ["production", "analytics"]
      },
      // ... 更多結果
    ],
    "suggestions": [
      "user behavior database",
      "user events table",
      "user profile database"
    ],
    "facets": {
      "type": [
        {"name": "postgresql", "count": 28},
        {"name": "mongodb", "count": 12},
        {"name": "api", "count": 5}
      ],
      "status": [
        {"name": "active", "count": 40},
        {"name": "inactive", "count": 5}
      ]
    },
    "search_time_ms": 145
  }
}
```

### 2. 高級搜尋

**請求**
```bash
POST /search/advanced
Content-Type: application/json
Authorization: Bearer <token>

{
  "conditions": [
    {
      "field": "name",
      "operator": "contains",
      "value": "user"
    },
    {
      "field": "type",
      "operator": "equals",
      "value": "postgresql"
    },
    {
      "field": "created_at",
      "operator": "range",
      "value": {
        "gte": "2024-01-01",
        "lte": "2024-12-31"
      }
    }
  ],
  "boolean_operator": "AND",
  "page": 1,
  "size": 20
}
```

**成功響應 (HTTP 200)**
```json
{
  "code": 0,
  "message": "Success",
  "data": {
    "conditions": [
      {"field": "name", "operator": "contains", "value": "user"},
      {"field": "type", "operator": "equals", "value": "postgresql"},
      {"field": "created_at", "operator": "range", "value": {"gte": "2024-01-01", "lte": "2024-12-31"}}
    ],
    "boolean_operator": "AND",
    "total": 18,
    "page": 1,
    "size": 20,
    "results": [
      {
        "id": "ds_20241031_001",
        "name": "User Analytics Database",
        "type": "postgresql",
        "created_at": "2024-10-31T10:30:00Z"
      }
      // ... 更多結果
    ]
  }
}
```

---

## 版本管理 API

### 1. 查看版本歷史

**請求**
```bash
GET /datasources/{datasource_id}/versions?page=1&size=20
Authorization: Bearer <token>
```

**成功響應 (HTTP 200)**
```json
{
  "code": 0,
  "message": "Success",
  "data": {
    "datasource_id": "ds_20241031_001",
    "total": 5,
    "page": 1,
    "versions": [
      {
        "version_id": "v1.0.1",
        "version_number": 1,
        "changes": {
          "name": {"old": "User Analytics Database", "new": "User Analytics Database (Updated)"},
          "tags": {"old": ["production"], "new": ["production", "v2"]}
        },
        "change_type": "update",
        "created_at": "2024-10-31T11:00:00Z",
        "created_by": "user_123"
      },
      {
        "version_id": "v1.0.0",
        "version_number": 0,
        "change_type": "create",
        "created_at": "2024-10-31T10:30:00Z",
        "created_by": "user_123"
      }
    ]
  }
}
```

### 2. 版本對比

**請求**
```bash
GET /datasources/{datasource_id}/versions/compare?from_version=v1.0.0&to_version=v1.0.1
Authorization: Bearer <token>
```

**成功響應 (HTTP 200)**
```json
{
  "code": 0,
  "message": "Success",
  "data": {
    "datasource_id": "ds_20241031_001",
    "from_version": "v1.0.0",
    "to_version": "v1.0.1",
    "differences": [
      {
        "field": "name",
        "old_value": "User Analytics Database",
        "new_value": "User Analytics Database (Updated)",
        "change_type": "modified"
      },
      {
        "field": "tags",
        "old_value": ["production", "analytics"],
        "new_value": ["production", "analytics", "v2"],
        "change_type": "modified"
      }
    ]
  }
}
```

### 3. 版本回溯

**請求**
```bash
POST /datasources/{datasource_id}/rollback
Content-Type: application/json
Authorization: Bearer <token>

{
  "target_version": "v1.0.0",
  "reason": "Revert to stable version"
}
```

**成功響應 (HTTP 200)**
```json
{
  "code": 0,
  "message": "Data source rolled back successfully",
  "data": {
    "datasource_id": "ds_20241031_001",
    "from_version": "v1.0.1",
    "to_version": "v1.0.0",
    "rolled_back_at": "2024-10-31T11:10:00Z",
    "rollback_version": "v1.0.2"
  }
}
```

---

## 權限管理 API

### 1. 授予訪問權限

**請求**
```bash
POST /datasources/{datasource_id}/permissions
Content-Type: application/json
Authorization: Bearer <token>

{
  "grantee": "analytics_team",
  "grantee_type": "team",
  "access_level": "read_write",
  "expires_at": "2025-12-31T23:59:59Z"
}
```

**成功響應 (HTTP 201)**
```json
{
  "code": 0,
  "message": "Permission granted successfully",
  "data": {
    "permission_id": "perm_20241031_001",
    "datasource_id": "ds_20241031_001",
    "grantee": "analytics_team",
    "grantee_type": "team",
    "access_level": "read_write",
    "created_at": "2024-10-31T11:15:00Z",
    "expires_at": "2025-12-31T23:59:59Z"
  }
}
```

### 2. 查看權限列表

**請求**
```bash
GET /datasources/{datasource_id}/permissions
Authorization: Bearer <token>
```

**成功響應 (HTTP 200)**
```json
{
  "code": 0,
  "message": "Success",
  "data": {
    "datasource_id": "ds_20241031_001",
    "total": 3,
    "permissions": [
      {
        "permission_id": "perm_20241031_001",
        "grantee": "analytics_team",
        "grantee_type": "team",
        "access_level": "read_write",
        "created_at": "2024-10-31T11:15:00Z",
        "expires_at": "2025-12-31T23:59:59Z"
      },
      {
        "permission_id": "perm_20241031_002",
        "grantee": "user_456",
        "grantee_type": "user",
        "access_level": "read",
        "created_at": "2024-10-30T10:00:00Z"
      }
    ]
  }
}
```

### 3. 撤銷訪問權限

**請求**
```bash
DELETE /datasources/{datasource_id}/permissions/{permission_id}
Authorization: Bearer <token>

# 示例
DELETE /datasources/ds_20241031_001/permissions/perm_20241031_001
```

**成功響應 (HTTP 200)**
```json
{
  "code": 0,
  "message": "Permission revoked successfully",
  "data": {
    "permission_id": "perm_20241031_001",
    "datasource_id": "ds_20241031_001",
    "revoked_at": "2024-10-31T11:20:00Z"
  }
}
```

---

## 健康監控 API

### 1. 獲取健康狀態

**請求**
```bash
GET /datasources/{datasource_id}/health
Authorization: Bearer <token>
```

**成功響應 (HTTP 200)**
```json
{
  "code": 0,
  "message": "Success",
  "data": {
    "datasource_id": "ds_20241031_001",
    "health_status": "healthy",
    "availability": 99.95,
    "response_time_ms": 45,
    "error_rate": 0.05,
    "quality_score": 94.5,
    "completeness_score": 96.0,
    "freshness_score": 92.0,
    "accuracy_score": 95.5,
    "last_check": "2024-10-31T11:25:00Z",
    "next_check": "2024-10-31T12:25:00Z",
    "check_details": {
      "connection_status": "connected",
      "data_freshness": "updated 2 hours ago",
      "error_messages": []
    }
  }
}
```

### 2. 手動觸發健康檢測

**請求**
```bash
POST /datasources/{datasource_id}/health/check
Authorization: Bearer <token>
```

**成功響應 (HTTP 200)**
```json
{
  "code": 0,
  "message": "Health check triggered successfully",
  "data": {
    "datasource_id": "ds_20241031_001",
    "check_id": "check_20241031_001",
    "status": "checking",
    "started_at": "2024-10-31T11:30:00Z"
  }
}
```

---

## 錯誤處理

### 常見錯誤碼

| 狀態碼 | 錯誤碼 | 說明 | 示例 |
|-------|--------|------|------|
| 400 | INVALID_REQUEST | 請求參數無效 | 缺少必需字段 |
| 401 | UNAUTHORIZED | 未授權 | Token 過期或無效 |
| 403 | FORBIDDEN | 無權限 | 用戶沒有訪問權限 |
| 404 | NOT_FOUND | 資源不存在 | 資料源不存在 |
| 409 | CONFLICT | 資源衝突 | 重複的資源名稱 |
| 429 | RATE_LIMIT | 超過速率限制 | 請求過於頻繁 |
| 500 | INTERNAL_ERROR | 服務器內部錯誤 | 未預期的錯誤 |

### 錯誤響應示例

```json
{
  "code": 40004,
  "message": "Data source not found",
  "error": {
    "type": "NOT_FOUND",
    "details": "Data source with ID 'ds_invalid' does not exist",
    "error_code": "DATASOURCE_NOT_FOUND",
    "request_id": "req_20241031_001"
  },
  "timestamp": "2024-10-31T11:30:00Z"
}
```

---

## Python 調用示例

### 使用 requests 庫

```python
import requests
import json
from datetime import datetime, timedelta

class DSRClient:
    """資料源註冊中心 API 客戶端"""
    
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    
    def create_datasource(self, name: str, url: str, ds_type: str, **kwargs) -> dict:
        """創建資料源"""
        data = {
            'name': name,
            'url': url,
            'type': ds_type,
            **kwargs
        }
        response = requests.post(
            f'{self.base_url}/datasources',
            headers=self.headers,
            json=data
        )
        return response.json()
    
    def get_datasource(self, datasource_id: str) -> dict:
        """獲取資料源詳情"""
        response = requests.get(
            f'{self.base_url}/datasources/{datasource_id}',
            headers=self.headers
        )
        return response.json()
    
    def search(self, query: str, filters: dict = None, page: int = 1, size: int = 20) -> dict:
        """搜尋資料源"""
        params = {
            'q': query,
            'page': page,
            'size': size
        }
        if filters:
            for key, value in filters.items():
                params[f'filters[{key}]'] = value
        
        response = requests.get(
            f'{self.base_url}/search',
            headers=self.headers,
            params=params
        )
        return response.json()
    
    def grant_permission(self, datasource_id: str, grantee: str, grantee_type: str, 
                        access_level: str, expires_at: datetime = None) -> dict:
        """授予訪問權限"""
        data = {
            'grantee': grantee,
            'grantee_type': grantee_type,
            'access_level': access_level
        }
        if expires_at:
            data['expires_at'] = expires_at.isoformat() + 'Z'
        
        response = requests.post(
            f'{self.base_url}/datasources/{datasource_id}/permissions',
            headers=self.headers,
            json=data
        )
        return response.json()
    
    def get_health(self, datasource_id: str) -> dict:
        """獲取資料源健康狀態"""
        response = requests.get(
            f'{self.base_url}/datasources/{datasource_id}/health',
            headers=self.headers
        )
        return response.json()

# 使用示例
if __name__ == '__main__':
    client = DSRClient(
        base_url='https://api.mirror.example.com/api/v1',
        token='your_jwt_token_here'
    )
    
    # 創建資料源
    result = client.create_datasource(
        name='User Database',
        url='postgresql://db.example.com:5432/users',
        ds_type='postgresql',
        description='Main user database',
        tags=['production', 'users']
    )
    print(f"Created datasource: {result['data']['id']}")
    
    # 搜尋資料源
    search_result = client.search(
        query='user',
        filters={'type': 'postgresql', 'status': 'active'},
        page=1,
        size=10
    )
    print(f"Found {search_result['data']['total']} datasources")
    
    # 授予權限
    perm_result = client.grant_permission(
        datasource_id=result['data']['id'],
        grantee='analytics_team',
        grantee_type='team',
        access_level='read_write',
        expires_at=datetime.now() + timedelta(days=365)
    )
    print(f"Permission granted: {perm_result['data']['permission_id']}")
    
    # 獲取健康狀態
    health = client.get_health(result['data']['id'])
    print(f"Health status: {health['data']['health_status']}")
```

---

## Curl 調用示例

### 創建資料源

```bash
curl -X POST https://api.mirror.example.com/api/v1/datasources \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Analytics DB",
    "url": "postgresql://db.example.com/analytics",
    "type": "postgresql",
    "description": "Main analytics database",
    "tags": ["production", "analytics"]
  }'
```

### 搜尋資料源

```bash
curl -X GET "https://api.mirror.example.com/api/v1/search?q=user&type=postgresql" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 授予權限

```bash
curl -X POST https://api.mirror.example.com/api/v1/datasources/ds_001/permissions \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "grantee": "analytics_team",
    "grantee_type": "team",
    "access_level": "read_write"
  }'
```

---

## 相關文件引用

- **主文檔**: [1.6 API 詳細規範](../ch1-6-API詳細規範.md)
- **核心功能**: [代碼示例 - 核心功能](ch1-code-01-core-functions.md)
- **搜尋服務**: [代碼示例 - 搜尋服務](ch1-code-02-search-service.md)
- **數據庫**: [代碼示例 - 數據庫定義](ch1-code-03-database-schema.md)
