# CH2 代碼示例 - 2.6 API 端點詳細規範

## API 基礎信息

```
基礎 URL: https://api.fingerprint.example.com/api/v1
認證: JWT Bearer Token
```

---

## 指紋分析 API

### 1. 提交網站分析

**請求**
```bash
POST /fingerprints/analyze
Authorization: Bearer <token>
Content-Type: application/json

{
  "url": "https://example.com",
  "response_data": {
    "status_code": 200,
    "headers": {
      "Server": "nginx/1.20.0",
      "X-Powered-By": "PHP/8.0"
    },
    "html": "<html>...</html>",
    "request_time": 0.345
  }
}
```

**成功響應 (201)**
```json
{
  "code": 0,
  "data": {
    "fingerprint_id": "fp-abc12345",
    "domain": "example.com",
    "tech_stack": {
      "servers": [{"name": "Nginx", "version": "1.20.0"}],
      "languages": [{"name": "PHP", "version": "8.0"}]
    },
    "anticrawl": {
      "level": 2,
      "mechanisms": ["user_agent_detection", "rate_limiting"]
    },
    "confidence_score": 0.92,
    "recommendations": [
      {
        "category": "rate_limit",
        "suggestion": "實施延遲和隨機化策略",
        "priority": "high"
      }
    ],
    "analysis_time": "2024-10-31T12:00:00Z"
  }
}
```

### 2. 獲取指紋詳情

**請求**
```bash
GET /fingerprints/{fingerprint_id}
Authorization: Bearer <token>
```

**成功響應**
```json
{
  "code": 0,
  "data": {
    "fingerprint_id": "fp-abc12345",
    "domain": "example.com",
    "url": "https://example.com",
    "tech_stack": {...},
    "anticrawl": {...},
    "confidence_score": 0.92,
    "created_at": "2024-10-31T10:00:00Z",
    "analysis_count": 5,
    "false_positive_count": 0
  }
}
```

### 3. 搜尋指紋

**請求**
```bash
GET /fingerprints/search?domain=example.com&tech_types=nginx&anticrawl_level=HIGH
Authorization: Bearer <token>
```

**成功響應**
```json
{
  "code": 0,
  "data": {
    "total": 42,
    "page": 1,
    "size": 20,
    "items": [
      {
        "fingerprint_id": "fp-abc12345",
        "domain": "example.com",
        "anticrawl_level": 2,
        "confidence_score": 0.92
      }
    ]
  }
}
```

---

## 指紋匹配 API

### 1. 尋找相似指紋

**請求**
```bash
GET /fingerprints/{fingerprint_id}/similar?threshold=0.7&limit=10
Authorization: Bearer <token>
```

**成功響應**
```json
{
  "code": 0,
  "data": {
    "query_fingerprint": "fp-abc12345",
    "similar_fingerprints": [
      {
        "fingerprint_id": "fp-xyz98765",
        "domain": "similar.com",
        "similarity_score": 0.89
      }
    ]
  }
}
```

### 2. 計算相似度

**請求**
```bash
POST /fingerprints/compare
Authorization: Bearer <token>

{
  "fingerprint_id1": "fp-abc12345",
  "fingerprint_id2": "fp-xyz98765"
}
```

**成功響應**
```json
{
  "code": 0,
  "data": {
    "similarity_score": 0.87,
    "tech_stack_similarity": 0.95,
    "anticrawl_similarity": 0.78
  }
}
```

---

## 爬蟲配置建議 API

### 1. 獲取爬蟲配置建議

**請求**
```bash
GET /fingerprints/{fingerprint_id}/crawler-config
Authorization: Bearer <token>
```

**成功響應**
```json
{
  "code": 0,
  "data": {
    "fingerprint_id": "fp-abc12345",
    "recommendations": [
      {
        "category": "headers",
        "priority": "critical",
        "config": {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
          "Referer": "https://google.com"
        }
      },
      {
        "category": "delays",
        "priority": "high",
        "config": {
          "min_delay": 2,
          "max_delay": 5,
          "random": true
        }
      },
      {
        "category": "strategy",
        "priority": "high",
        "config": {
          "use_proxy": true,
          "rotate_user_agent": true,
          "browser_rendering": false
        }
      }
    ]
  }
}
```

---

## 網站變更監測 API

### 1. 檢測網站變更

**請求**
```bash
POST /fingerprints/{fingerprint_id}/detect-changes
Authorization: Bearer <token>

{
  "current_response": {
    "status_code": 200,
    "headers": {...},
    "html": "..."
  }
}
```

**成功響應**
```json
{
  "code": 0,
  "data": {
    "fingerprint_id": "fp-abc12345",
    "changes_detected": true,
    "changes": [
      {
        "change_type": "tech_stack_change",
        "severity": "medium",
        "previous": {"server": "Apache 2.4"},
        "current": {"server": "Nginx 1.20"},
        "detected_at": "2024-10-31T12:30:00Z"
      }
    ]
  }
}
```

---

## Python 客戶端示例

```python
import requests
from typing import Dict, List

class FingerprintClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {token}'}
    
    def analyze_website(self, url: str, response_data: Dict) -> Dict:
        """分析網站指紋"""
        response = requests.post(
            f'{self.base_url}/fingerprints/analyze',
            headers=self.headers,
            json={'url': url, 'response_data': response_data}
        )
        return response.json()
    
    def get_fingerprint(self, fingerprint_id: str) -> Dict:
        """獲取指紋詳情"""
        response = requests.get(
            f'{self.base_url}/fingerprints/{fingerprint_id}',
            headers=self.headers
        )
        return response.json()
    
    def search_fingerprints(
        self,
        domain: str,
        tech_types: List[str] = None,
        anticrawl_level: str = None
    ) -> Dict:
        """搜尋指紋"""
        params = {'domain': domain}
        if tech_types:
            params['tech_types'] = ','.join(tech_types)
        if anticrawl_level:
            params['anticrawl_level'] = anticrawl_level
        
        response = requests.get(
            f'{self.base_url}/fingerprints/search',
            headers=self.headers,
            params=params
        )
        return response.json()
    
    def find_similar(self, fingerprint_id: str, threshold: float = 0.7) -> Dict:
        """尋找相似指紋"""
        response = requests.get(
            f'{self.base_url}/fingerprints/{fingerprint_id}/similar',
            headers=self.headers,
            params={'threshold': threshold}
        )
        return response.json()
    
    def get_crawler_config(self, fingerprint_id: str) -> Dict:
        """獲取爬蟲配置建議"""
        response = requests.get(
            f'{self.base_url}/fingerprints/{fingerprint_id}/crawler-config',
            headers=self.headers
        )
        return response.json()
    
    def detect_changes(self, fingerprint_id: str, current_response: Dict) -> Dict:
        """檢測網站變更"""
        response = requests.post(
            f'{self.base_url}/fingerprints/{fingerprint_id}/detect-changes',
            headers=self.headers,
            json={'current_response': current_response}
        )
        return response.json()

# 使用示例
client = FingerprintClient(
    'https://api.fingerprint.example.com/api/v1',
    'your_token_here'
)

# 分析網站
result = client.analyze_website(
    'https://example.com',
    {
        'status_code': 200,
        'headers': {'Server': 'nginx'},
        'html': '<html>...</html>'
    }
)

fp_id = result['data']['fingerprint_id']

# 獲取爬蟲配置
config = client.get_crawler_config(fp_id)
print(f"Crawler config: {config}")

# 尋找相似指紋
similar = client.find_similar(fp_id)
print(f"Similar fingerprints: {similar}")
```

---

## 相關文件引用

- **核心功能**: [代碼示例 - 核心實現](ch2-code-01-core-fingerprint.md)
- **搜尋服務**: [代碼示例 - 匹配和搜尋](ch2-code-02-fingerprint-matching.md)
- **數據庫**: [代碼示例 - 數據庫定義](ch2-code-03-database-schema.md)
