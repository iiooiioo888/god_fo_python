# 第7章：資料合規與安全中心 (Data Compliance and Security Center)

## 7.6 API詳細規範

**[← 返回第7章首頁](ch7-index.md)**

---

#### 7.6.1 合規性检查API

**检查資料源合規性 (POST /api/v1/compliance/check)**

*请求示例:*
```http
POST /api/v1/compliance/check HTTP/1.1
Host: dcsc.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "data_source_id": "ds-7a8b9c0d",
  "include_content": true
}
```

*成功響應示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data_source_id": "ds-7a8b9c0d",
  "project_id": "proj-123",
  "status": "warning",
  "total_rules": 15,
  "passed_rules": 12,
  "failed_rules": 2,
  "not_applicable_rules": 1,
  "critical_issues": 0,
  "results": [
    {
      "rule_id": "rule-gdpr-001",
      "rule_name": "個人資料標识检查",
      "applicable": true,
      "passed": false,
      "message": "檢測到潜在的個人身份資訊",
      "details": {
        "findings": [
          {
            "pattern_id": "pattern-email",
            "pattern_name": "电子邮件地址",
            "data_category": "personal",
            "start": 125,
            "end": 150,
            "value": "user@example.com",
            "context": "联系資訊: user@example.com"
          }
        ]
      }
    },
    {
      "rule_id": "rule-gdpr-002",
      "rule_name": "資料最小化检查",
      "applicable": true,
      "passed": true,
      "message": "规则通過: 資料最小化要求已满足"
    }
  ],
  "suggestions": [
    "必須解决: 個人資料標识检查 - 檢測到潜在的個人身份資訊",
    "建議改进: 檢測到 2 個可優化的合規性问题"
  ],
  "timestamp": "2023-06-15T10:30:45Z"
}
```

#### 7.6.2 敏感資料檢測API

**檢測敏感資料 (POST /api/v1/data:detect-sensitive)**

*请求示例:*
```http
POST /api/v1/data:detect-sensitive HTTP/1.1
Host: dcsc.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "data": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-123-4567",
    "address": "123 Main St, Anytown, USA"
  },
  "context": {
    "categories": ["contact", "personal"],
    "regions": ["us"]
  }
}
```

*成功響應示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data_hash": "d41d8cd98f00b204e9800998ecf8427e",
  "total_patterns": 8,
  "findings": [
    {
      "pattern_id": "pattern-name",
      "pattern_name": "個人姓名",
      "data_category": "personal",
      "value": "John Doe",
      "context": "name: John Doe",
      "path": "name",
      "type": "value"
    },
    {
      "pattern_id": "pattern-email",
      "pattern_name": "电子邮件地址",
      "data_category": "personal",
      "value": "john.doe@example.com",
      "context": "email: john.doe@example.com",
      "path": "email",
      "type": "value"
    },
    {
      "pattern_id": "pattern-phone",
      "pattern_name": "电话號码",
      "data_category": "personal",
      "value": "+1-555-123-4567",
      "context": "phone: +1-555-123-4567",
      "path": "phone",
      "type": "value"
    }
  ],
  "context": {
    "categories": ["contact", "personal"],
    "regions": ["us"]
  },
  "severity": "high",
  "timestamp": "2023-06-15T10:35:20Z"
}
```

#### 7.6.3 用戶同意管理API

**記錄用戶同意 (POST /api/v1/consents)**

*请求示例:*
```http
POST /api/v1/consents HTTP/1.1
Host: dcsc.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "user_id": "user-123",
  "data_source_id": "ds-7a8b9c0d",
  "consent_type": "data_processing",
  "consent_value": true,
  "consent_details": {
    "purpose": "資料採集與處理",
    "data_types": ["personal", "contact"],
    "retention_period": "2 years"
  }
}
```

*成功響應示例:*
```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/consents/consent-1a2b3c4d

{
  "id": "consent-1a2b3c4d",
  "user_id": "user-123",
  "data_source_id": "ds-7a8b9c0d",
  "project_id": "proj-123",
  "consent_type": "data_processing",
  "consent_value": true,
  "consent_details": {
    "purpose": "資料採集與處理",
    "data_types": ["personal", "contact"],
    "retention_period": "2 years"
  },
  "consent_timestamp": "2023-06-15T10:30:45Z",
  "revoked": false
}
```

**獲取用戶同意記錄 (GET /api/v1/consents/{user_id})**

*请求示例:*
```http
GET /api/v1/consents/user-123?data_source_id=ds-7a8b9c0d HTTP/1.1
Host: dcsc.mirror-realm.com
Authorization: Bearer <access_token>
```

*成功響應示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "items": [
    {
      "id": "consent-1a2b3c4d",
      "user_id": "user-123",
      "data_source_id": "ds-7a8b9c0d",
      "project_id": "proj-123",
      "consent_type": "data_processing",
      "consent_value": true,
      "consent_details": {
        "purpose": "資料採集與處理",
        "data_types": ["personal", "contact"],
        "retention_period": "2 years"
      },
      "consent_timestamp": "2023-06-15T10:30:45Z",
      "revoked": false
    },
    {
      "id": "consent-5e6f7g8h",
      "user_id": "user-123",
      "data_source_id": "ds-7a8b9c0d",
      "project_id": "proj-123",
      "consent_type": "data_sharing",
      "consent_value": false,
      "consent_details": {
        "purpose": "與第三方共享資料",
        "data_types": ["personal"],
        "retention_period": "1 year"
      },
      "consent_timestamp": "2023-06-10T08:15:30Z",
      "revoked": true,
      "revoked_at": "2023-06-12T14:20:15Z"
    }
  ],
  "total": 2
}
```

---

## 📑 相關章節

| 前序 | 當前 | 後續 |
|-----|------|------|
| [7.5 資料模型詳細定義](ch7-5-資料模型詳細定義.md) | **7.6 API詳細規範** | [7.7 效能優化策略](ch7-7-效能優化策略.md) |

**快速鏈接：**
- [7.5 資料模型詳細定義](ch7-5-資料模型詳細定義.md)
- [7.7 效能優化策略](ch7-7-效能優化策略.md)
- [← 返回第7章首頁](ch7-index.md)
