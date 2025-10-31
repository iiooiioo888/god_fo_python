**[← 返回第2章首頁](ch2-index.md)**

---

### 2.6 API詳細規範

#### 2.6.1 網站分析API

**分析網站 (POST /api/v1/analyze)**

*请求示例:*
```http
POST /api/v1/analyze HTTP/1.1
Host: wfe.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "url": "https://example.com",
  "options": {
    "follow_redirects": true,
    "advanced_analysis": true,
    "timeout": 30
  }
}
```

*成功響應示例:*
```json
{
  "url": "https://example.com",
  "tech_stack": {
    "server": [
      {
        "name": "Nginx",
        "version": "1.18.0",
        "confidence": 0.95
      }
    ]
  },
  "anti_crawling": {}
}
```

---

## 📑 相關章節

| 前序 | 當前 | 後續 |
|-----|------|------|
| [2.5 資料模型詳細定義](ch2-5-資料模型詳細定義.md) | **2.6 API詳細規範** | [2.7 效能優化策略](ch2-7-效能優化策略.md) |

**快速鏈接：**
- [← 返回第2章首頁](ch2-index.md)
- [2.5 資料模型詳細定義](ch2-5-資料模型詳細定義.md)
- [2.7 效能優化策略](ch2-7-效能優化策略.md)
