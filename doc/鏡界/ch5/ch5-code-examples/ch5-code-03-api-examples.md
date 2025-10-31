# CH5 代碼示例 - 5.6 API 端點詳細規範

## 媒體上傳與處理 API

### 上傳並處理媒體

**請求**
```bash
POST /media/process
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: @photo.jpg
processing_rules: {
  "enhancement_level": "high",
  "analyze_content": true
}
```

**成功響應**
```json
{
  "code": 0,
  "data": {
    "task_id": "task-123456",
    "status": "processing",
    "created_at": "2024-10-31T12:00:00Z"
  }
}
```

### 查詢處理結果

**請求**
```bash
GET /media/tasks/{task_id}
Authorization: Bearer <token>
```

**成功響應**
```json
{
  "code": 0,
  "data": {
    "task_id": "task-123456",
    "status": "success",
    "quality_score": 92.5,
    "analysis": {
      "objects": ["person", "car"],
      "scene": "street",
      "confidence": 0.95
    }
  }
}
```

---

## Python 客戶端

```python
import requests

class MediaClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {token}'}
    
    def process_media(self, file_path: str, rules: dict) -> str:
        """上傳並處理媒體"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'processing_rules': str(rules)}
            response = requests.post(
                f'{self.base_url}/media/process',
                headers=self.headers,
                files=files,
                data=data
            )
        return response.json()['data']['task_id']
```

---

## 相關文件引用

- **核心實現**: [代碼示例 - 媒體處理](ch5-code-01-media-processor.md)
- **數據庫**: [代碼示例 - 數據庫定義](ch5-code-02-database-schema.md)
