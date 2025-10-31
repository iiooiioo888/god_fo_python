# CH7 代碼示例 - 7.6 API 端點詳細規範

## 合規性檢查 API

```bash
POST /compliance/check
Authorization: Bearer <token>

{
  "data_source_id": "ds_001",
  "check_types": ["gdpr", "ccpa", "pii"]
}
```

**響應**
```json
{
  "code": 0,
  "data": {
    "passed": true,
    "results": {
      "gdpr": {"passed": true},
      "ccpa": {"passed": true},
      "pii": {"passed": true, "findings": []}
    }
  }
}
```

---

## Python 客戶端

```python
class ComplianceClient:
    def check_compliance(self, data_source_id: str, check_types: list):
        response = requests.post(
            f'{self.base_url}/compliance/check',
            headers=self.headers,
            json={'data_source_id': data_source_id, 'check_types': check_types}
        )
        return response.json()['data']
```

---

## 相關文件引用

- **核心實現**: [代碼示例 - 合規引擎](ch7-code-01-compliance-engine.md)
- **數據庫**: [代碼示例 - 數據庫定義](ch7-code-02-database-schema.md)
