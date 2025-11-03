**[← 返回第9章首頁](ch9-index.md)**

---

### 9.6 API詳細規範

#### 9.6.1 基礎API規範

1. **服務管理API**
   ```
   GET    /api/v1/services              - 列出所有服務
   GET    /api/v1/services/{id}         - 獲取服務詳情
   POST   /api/v1/services              - 創建服務
   PUT    /api/v1/services/{id}         - 更新服務
   DELETE /api/v1/services/{id}         - 刪除服務
   ```

2. **健康檢查API**
   ```
   GET    /health                       - 系統整體健康檢查
   GET    /health/services              - 所有服務健康狀態
   GET    /health/services/{id}         - 特定服務健康狀態
   ```

3. **監控API**
   ```
   GET    /api/v1/metrics               - 獲取性能指標
   GET    /api/v1/metrics/{service}     - 獲取服務指標
   GET    /api/v1/alerts                - 獲取告警列表
   POST   /api/v1/alerts/{id}/acknowledge - 確認告警
   ```

#### 9.6.2 認證與授權

```
授權類型: OAuth2 / JWT
Bearer Token: Authorization: Bearer <token>

RBAC角色:
- admin     - 系統管理員
- operator  - 運維操作員
- developer - 開發人員
- viewer    - 只讀查看
```

#### 9.6.3 請求/響應格式

**成功響應 (200)**:
```json
{
  "code": 0,
  "message": "Success",
  "data": {
    "id": "service-001",
    "name": "data-source-registry",
    "status": "running"
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

**錯誤響應 (4xx/5xx)**:
```json
{
  "code": 1001,
  "message": "Service not found",
  "errors": [
    {
      "field": "id",
      "error": "Invalid service id format"
    }
  ],
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### 9.6.4 限流規則

| 端點 | 限制 | 說明 |
|------|------|------|
| GET /api/v1/* | 1000/min | 查詢操作 |
| POST /api/v1/* | 100/min | 寫入操作 |
| DELETE /api/v1/* | 50/min | 刪除操作 |
| 管理端點 | 500/min | 需要admin角色 |

#### 9.6.5 超時配置

```
連接超時:     5秒
讀取超時:     30秒
寫入超時:     30秒
批量操作超時:  60秒
```

---

## 📑 相關章節

|| 前序 | 當前 | 後續 |
||-----|------|------|
|| [9.5](ch9-5-資料模型詳細定義.md) | **9.6** | [9.7](ch9-7-效能優化策略.md) |

**快速鏈接：**
- [← 返回第9章首頁](ch9-index.md)
