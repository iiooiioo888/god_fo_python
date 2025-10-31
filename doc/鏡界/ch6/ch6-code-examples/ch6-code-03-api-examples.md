# CH6 代碼示例 - 6.6 API 端點詳細規範

## 代碼生成 API

### 生成爬蟲代碼

**請求**
```bash
POST /ai/generate-code
Authorization: Bearer <token>

{
  "requirement": "爬取例子網站的商品列表",
  "language": "python",
  "context": {"framework": "requests", "type": "spider"}
}
```

**成功響應**
```json
{
  "code": 0,
  "data": {
    "code": "import requests...",
    "quality_score": 92,
    "explanation": "生成的代碼說明"
  }
}
```

### 錯誤診斷 API

**請求**
```bash
POST /ai/diagnose-error
Authorization: Bearer <token>

{
  "error_message": "ConnectionError: ...",
  "code_context": "response = requests.get(url)"
}
```

**成功響應**
```json
{
  "code": 0,
  "data": {
    "analysis": "錯誤分析",
    "solutions": ["解決方案 1", "解決方案 2"],
    "fixed_code": "修複後的代碼"
  }
}
```

---

## Python 客戶端

```python
import requests

class AIClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {token}'}
    
    def generate_code(self, requirement: str, language: str = 'python') -> str:
        response = requests.post(
            f'{self.base_url}/ai/generate-code',
            headers=self.headers,
            json={'requirement': requirement, 'language': language}
        )
        return response.json()['data']['code']
    
    def diagnose_error(self, error: str, code: str) -> dict:
        response = requests.post(
            f'{self.base_url}/ai/diagnose-error',
            headers=self.headers,
            json={'error_message': error, 'code_context': code}
        )
        return response.json()['data']
```

---

## 相關文件引用

- **核心實現**: [代碼示例 - LLM 集成](ch6-code-01-llm-integration.md)
- **數據庫**: [代碼示例 - 數據庫定義](ch6-code-02-database-schema.md)
