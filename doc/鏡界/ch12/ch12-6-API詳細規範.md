# 第12章：數據質量管理中心

## 12.6 API詳細規範

**[← 返回第12章首頁](ch12-index.md)**

---

## 🔌 API 概覽

Ch12 數據質量管理中心提供完整的 RESTful API 和 gRPC API，支持質量監控、數據清洗、異常檢測等全部功能。

### API 架構

```
┌────────────────────────────────────────────────────────┐
│                    API Gateway                          │
│  • 身份驗證                                             │
│  • 限流控制                                             │
│  • 請求路由                                             │
└────────────────────────────────────────────────────────┘
               ↓                      ↓
┌──────────────────────┐   ┌──────────────────────┐
│    RESTful API       │   │      gRPC API        │
│  (HTTP/JSON)         │   │   (Protocol Buffers) │
└──────────────────────┘   └──────────────────────┘
               ↓                      ↓
┌────────────────────────────────────────────────────────┐
│            Ch12 Quality Management Services             │
└────────────────────────────────────────────────────────┘
```

---

## 1️⃣ RESTful API

### 基礎配置

```yaml
# API 基礎配置
base_url: https://api.example.com/quality/v1
authentication: Bearer Token
content_type: application/json
rate_limit: 1000 requests/minute
timeout: 30s
```

### 通用響應格式

```json
{
    "success": true,
    "data": { ... },
    "message": "操作成功",
    "timestamp": "2025-10-31T10:00:00Z",
    "request_id": "uuid"
}
```

```json
// 錯誤響應
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input parameters",
        "details": { ... }
    },
    "timestamp": "2025-10-31T10:00:00Z",
    "request_id": "uuid"
}
```

---

## 2️⃣ 質量監控 API

### 2.1 執行質量檢查

```http
POST /quality/checks
Content-Type: application/json
Authorization: Bearer {token}

{
    "data_source": "ch8_crawler",
    "table_name": "products",
    "check_type": "full",  // full, incremental, sample
    "rules": [
        "completeness",
        "accuracy",
        "consistency"
    ],
    "config": {
        "sample_size": 10000,
        "parallel": true
    }
}
```

**響應**
```json
{
    "success": true,
    "data": {
        "check_id": "chk_abc123",
        "status": "running",
        "estimated_duration": 120,
        "progress_url": "/quality/checks/chk_abc123/progress"
    }
}
```

### 2.2 查詢檢查結果

```http
GET /quality/checks/{check_id}
Authorization: Bearer {token}
```

**響應**
```json
{
    "success": true,
    "data": {
        "check_id": "chk_abc123",
        "status": "completed",
        "data_source": "ch8_crawler",
        "table_name": "products",
        "started_at": "2025-10-31T10:00:00Z",
        "completed_at": "2025-10-31T10:02:15Z",
        "duration_seconds": 135,
        "results": {
            "total_records": 100000,
            "valid_records": 95000,
            "invalid_records": 5000,
            "quality_score": 95.2,
            "dimension_scores": {
                "completeness": 98.0,
                "accuracy": 96.0,
                "consistency": 94.0,
                "timeliness": 92.0,
                "uniqueness": 97.0
            },
            "issues": [
                {
                    "rule_name": "email_format",
                    "severity": "error",
                    "affected_records": 1500,
                    "sample_records": [...]
                }
            ]
        }
    }
}
```

### 2.3 獲取質量指標

```http
GET /quality/metrics?source={data_source}&start={start_time}&end={end_time}&granularity={1h|1d|1w}
Authorization: Bearer {token}
```

**響應**
```json
{
    "success": true,
    "data": {
        "data_source": "ch8_crawler",
        "period": {
            "start": "2025-10-01T00:00:00Z",
            "end": "2025-10-31T23:59:59Z"
        },
        "metrics": [
            {
                "timestamp": "2025-10-31T10:00:00Z",
                "quality_score": 95.2,
                "total_records": 100000,
                "error_rate": 0.05
            },
            // ... more data points
        ],
        "summary": {
            "avg_quality_score": 94.5,
            "min_quality_score": 88.0,
            "max_quality_score": 98.5,
            "trend": "improving"
        }
    }
}
```

### 2.4 設置質量告警

```http
POST /quality/alerts
Content-Type: application/json
Authorization: Bearer {token}

{
    "name": "quality_drop_alert",
    "data_sources": ["ch8_crawler", "ch1_api"],
    "conditions": [
        {
            "metric": "quality_score",
            "operator": "<",
            "threshold": 80,
            "duration": "5m"
        }
    ],
    "severity": "critical",
    "channels": ["email", "slack"],
    "recipients": ["team@example.com"],
    "enabled": true
}
```

---

## 3️⃣ 數據清洗 API

### 3.1 執行數據清洗

```http
POST /cleaning/execute
Content-Type: application/json
Authorization: Bearer {token}

{
    "data_source": "ch8_crawler",
    "table_name": "products",
    "pipeline_id": "pipeline_001",  // 可選，使用預定義管道
    "operations": [  // 或自定義操作
        {
            "type": "deduplication",
            "config": {
                "key_columns": ["url", "title"],
                "keep": "first"
            }
        },
        {
            "type": "format_normalization",
            "config": {
                "columns": {
                    "email": "lowercase",
                    "price": "number"
                }
            }
        }
    ],
    "options": {
        "dry_run": false,
        "backup": true,
        "validate_after": true
    }
}
```

**響應**
```json
{
    "success": true,
    "data": {
        "execution_id": "exec_xyz789",
        "status": "running",
        "estimated_duration": 300,
        "progress_url": "/cleaning/executions/exec_xyz789"
    }
}
```

### 3.2 查詢清洗結果

```http
GET /cleaning/executions/{execution_id}
Authorization: Bearer {token}
```

**響應**
```json
{
    "success": true,
    "data": {
        "execution_id": "exec_xyz789",
        "status": "completed",
        "started_at": "2025-10-31T10:00:00Z",
        "completed_at": "2025-10-31T10:05:00Z",
        "duration_seconds": 300,
        "results": {
            "original_count": 100000,
            "cleaned_count": 95000,
            "removed_count": 5000,
            "modified_count": 15000,
            "operations_executed": [
                {
                    "operation": "deduplication",
                    "records_affected": 5000,
                    "duration_ms": 45000
                },
                {
                    "operation": "format_normalization",
                    "records_affected": 15000,
                    "duration_ms": 60000
                }
            ]
        },
        "validation": {
            "quality_score_before": 85.2,
            "quality_score_after": 95.1,
            "improvement": 9.9
        }
    }
}
```

### 3.3 創建清洗管道

```http
POST /cleaning/pipelines
Content-Type: application/json
Authorization: Bearer {token}

{
    "name": "product_cleaning_pipeline",
    "description": "標準產品數據清洗流程",
    "stages": [
        {
            "order": 1,
            "operation": "deduplication",
            "config": {
                "key_columns": ["url"],
                "keep": "latest"
            }
        },
        {
            "order": 2,
            "operation": "format_normalization",
            "config": {
                "columns": {
                    "price": "number",
                    "date": "iso8601"
                }
            }
        },
        {
            "order": 3,
            "operation": "missing_value",
            "config": {
                "strategies": {
                    "category": {"method": "mode"},
                    "price": {"method": "median"}
                }
            }
        }
    ],
    "data_sources": ["ch8_crawler"],
    "enabled": true
}
```

---

## 4️⃣ 規則管理 API

### 4.1 創建質量規則

```http
POST /rules
Content-Type: application/json
Authorization: Bearer {token}

{
    "name": "email_validation",
    "description": "驗證郵箱格式",
    "rule_type": "field",
    "category": "accuracy",
    "rule_definition": {
        "field": "email",
        "check_type": "regex",
        "params": {
            "pattern": "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"
        }
    },
    "severity": "error",
    "data_sources": ["ch8_crawler", "ch1_api"],
    "on_failure": "reject",
    "enabled": true
}
```

**響應**
```json
{
    "success": true,
    "data": {
        "rule_id": 101,
        "name": "email_validation",
        "status": "active"
    }
}
```

### 4.2 查詢規則列表

```http
GET /rules?category={category}&enabled={true|false}&page={page}&size={size}
Authorization: Bearer {token}
```

**響應**
```json
{
    "success": true,
    "data": {
        "rules": [
            {
                "rule_id": 101,
                "name": "email_validation",
                "rule_type": "field",
                "category": "accuracy",
                "severity": "error",
                "enabled": true,
                "execution_count": 15000,
                "success_rate": 0.98
            },
            // ... more rules
        ],
        "pagination": {
            "page": 1,
            "size": 20,
            "total": 150,
            "total_pages": 8
        }
    }
}
```

### 4.3 更新規則

```http
PUT /rules/{rule_id}
Content-Type: application/json
Authorization: Bearer {token}

{
    "enabled": false,
    "severity": "warning",
    "rule_definition": {
        // updated definition
    }
}
```

### 4.4 刪除規則

```http
DELETE /rules/{rule_id}
Authorization: Bearer {token}
```

---

## 5️⃣ 異常檢測 API

### 5.1 執行異常檢測

```http
POST /anomaly/detect
Content-Type: application/json
Authorization: Bearer {token}

{
    "data_source": "ch8_crawler",
    "table_name": "products",
    "columns": ["price", "quantity"],
    "detection_methods": [
        {
            "method": "isolation_forest",
            "params": {
                "contamination": 0.1
            }
        },
        {
            "method": "zscore",
            "params": {
                "threshold": 3.0
            }
        }
    ],
    "ensemble": {
        "enabled": true,
        "threshold": 0.7
    }
}
```

**響應**
```json
{
    "success": true,
    "data": {
        "detection_id": "det_456",
        "status": "completed",
        "anomalies_found": 127,
        "results": [
            {
                "record_id": "rec_001",
                "anomaly_score": 0.85,
                "confidence": 0.92,
                "affected_fields": ["price"],
                "details": {
                    "expected_range": [10, 1000],
                    "actual_value": 9999
                }
            },
            // ... more anomalies
        ]
    }
}
```

### 5.2 查詢異常記錄

```http
GET /anomaly/records?source={data_source}&severity={severity}&status={status}&start={start_date}&end={end_date}
Authorization: Bearer {token}
```

**響應**
```json
{
    "success": true,
    "data": {
        "anomalies": [
            {
                "anomaly_id": "anom_001",
                "data_source": "ch8_crawler",
                "table_name": "products",
                "anomaly_type": "outlier",
                "detection_method": "isolation_forest",
                "anomaly_score": 0.85,
                "severity": "high",
                "detected_at": "2025-10-31T10:00:00Z",
                "status": "pending",
                "affected_fields": ["price"],
                "original_data": {...}
            },
            // ... more records
        ],
        "pagination": {...}
    }
}
```

### 5.3 更新異常狀態

```http
PATCH /anomaly/records/{anomaly_id}
Content-Type: application/json
Authorization: Bearer {token}

{
    "status": "resolved",
    "resolution": "價格已修正為正確值",
    "reviewed_by": "admin@example.com"
}
```

---

## 6️⃣ 數據血緣 API

### 6.1 查詢數據血緣

```http
GET /lineage/entities/{entity_id}?direction={upstream|downstream}&depth={depth}
Authorization: Bearer {token}
```

**響應**
```json
{
    "success": true,
    "data": {
        "entity": {
            "entity_id": "ent_001",
            "name": "dw_products",
            "type": "table",
            "qualified_name": "warehouse.public.products"
        },
        "lineage": {
            "upstream": [
                {
                    "entity_id": "ent_002",
                    "name": "raw_products",
                    "type": "table",
                    "relation_type": "derived",
                    "transformation": "product_cleaning"
                }
            ],
            "downstream": [
                {
                    "entity_id": "ent_003",
                    "name": "product_analytics",
                    "type": "view",
                    "relation_type": "aggregated"
                }
            ]
        }
    }
}
```

### 6.2 影響分析

```http
POST /lineage/impact-analysis
Content-Type: application/json
Authorization: Bearer {token}

{
    "entity_id": "ent_001",
    "change_type": "schema_change",
    "affected_fields": ["price", "quantity"]
}
```

**響應**
```json
{
    "success": true,
    "data": {
        "impact_summary": {
            "direct_impact": 5,
            "indirect_impact": 12,
            "severity": "high"
        },
        "affected_entities": [
            {
                "entity_id": "ent_003",
                "name": "product_analytics",
                "impact_level": "direct",
                "affected_operations": ["aggregation", "reporting"]
            },
            // ... more entities
        ],
        "recommendations": [
            "更新下游視圖 product_analytics 的 schema",
            "通知相關團隊檢查依賴的報表"
        ]
    }
}
```

### 6.3 創建血緣關係

```http
POST /lineage/relations
Content-Type: application/json
Authorization: Bearer {token}

{
    "source_entity_id": "ent_001",
    "target_entity_id": "ent_002",
    "relation_type": "derived",
    "transformation_id": "trans_001",
    "field_mapping": {
        "mapping": [
            {"source": "user_id", "target": "customer_id"},
            {"source": "email", "target": "contact_email"}
        ]
    }
}
```

---

## 7️⃣ 質量報告 API

### 7.1 生成質量報告

```http
POST /reports/generate
Content-Type: application/json
Authorization: Bearer {token}

{
    "report_type": "daily",
    "period_start": "2025-10-01",
    "period_end": "2025-10-31",
    "data_sources": ["ch8_crawler", "ch1_api"],
    "sections": [
        "quality_overview",
        "dimension_scores",
        "top_issues",
        "trend_analysis",
        "recommendations"
    ],
    "format": "pdf",
    "delivery": {
        "channels": ["email"],
        "recipients": ["team@example.com"]
    }
}
```

**響應**
```json
{
    "success": true,
    "data": {
        "report_id": "rpt_789",
        "status": "generating",
        "estimated_duration": 60,
        "progress_url": "/reports/rpt_789/progress"
    }
}
```

### 7.2 查詢報告

```http
GET /reports/{report_id}
Authorization: Bearer {token}
```

**響應**
```json
{
    "success": true,
    "data": {
        "report_id": "rpt_789",
        "title": "數據質量日報 - 2025-10-31",
        "report_type": "daily",
        "status": "completed",
        "generated_at": "2025-10-31T23:00:00Z",
        "report_url": "https://storage.example.com/reports/rpt_789.pdf",
        "summary": {
            "overall_score": 95.2,
            "total_records": 10000000,
            "quality_improvement": 2.3
        }
    }
}
```

### 7.3 下載報告

```http
GET /reports/{report_id}/download
Authorization: Bearer {token}
```

**響應**
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="quality_report_2025-10-31.pdf"

[PDF binary content]
```

---

## 8️⃣ 批量操作 API

### 8.1 批量質量檢查

```http
POST /quality/checks/batch
Content-Type: application/json
Authorization: Bearer {token}

{
    "checks": [
        {
            "data_source": "ch8_crawler",
            "table_name": "products"
        },
        {
            "data_source": "ch1_api",
            "table_name": "users"
        }
    ],
    "parallel": true,
    "max_concurrency": 5
}
```

### 8.2 批量數據清洗

```http
POST /cleaning/batch
Content-Type: application/json
Authorization: Bearer {token}

{
    "pipeline_id": "pipeline_001",
    "targets": [
        {
            "data_source": "ch8_crawler",
            "table_name": "products"
        },
        {
            "data_source": "ch8_crawler",
            "table_name": "reviews"
        }
    ]
}
```

---

## 9️⃣ WebSocket API (實時推送)

### 9.1 連接 WebSocket

```javascript
const ws = new WebSocket('wss://api.example.com/quality/ws');
ws.onopen = () => {
    // 訂閱質量事件
    ws.send(JSON.stringify({
        action: 'subscribe',
        channels: ['quality_alerts', 'quality_metrics'],
        filters: {
            data_sources: ['ch8_crawler']
        }
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};
```

### 9.2 事件格式

```json
{
    "event_type": "quality_alert",
    "timestamp": "2025-10-31T10:00:00Z",
    "data": {
        "alert_id": "alert_001",
        "severity": "critical",
        "data_source": "ch8_crawler",
        "quality_score": 65.2,
        "threshold": 80,
        "message": "質量分數低於閾值"
    }
}
```

---

## 🔟 gRPC API

### 10.1 Protocol Buffers 定義

```protobuf
// quality_service.proto

syntax = "proto3";

package quality.v1;

service QualityService {
    // 執行質量檢查
    rpc ExecuteCheck(CheckRequest) returns (CheckResponse);
    
    // 獲取質量指標
    rpc GetMetrics(MetricsRequest) returns (MetricsResponse);
    
    // 執行數據清洗
    rpc ExecuteCleaning(CleaningRequest) returns (CleaningResponse);
    
    // 流式接收質量事件
    rpc StreamQualityEvents(EventSubscription) returns (stream QualityEvent);
}

message CheckRequest {
    string data_source = 1;
    string table_name = 2;
    string check_type = 3;
    repeated string rules = 4;
    map<string, string> config = 5;
}

message CheckResponse {
    string check_id = 1;
    string status = 2;
    int32 estimated_duration = 3;
}

message QualityEvent {
    string event_type = 1;
    string timestamp = 2;
    bytes data = 3;
}
```

### 10.2 使用示例 (Python)

```python
import grpc
from quality_pb2 import CheckRequest
from quality_pb2_grpc import QualityServiceStub

# 創建 gRPC 通道
channel = grpc.insecure_channel('localhost:50051')
stub = QualityServiceStub(channel)

# 執行質量檢查
request = CheckRequest(
    data_source='ch8_crawler',
    table_name='products',
    check_type='full',
    rules=['completeness', 'accuracy']
)

response = stub.ExecuteCheck(request)
print(f"Check ID: {response.check_id}")
print(f"Status: {response.status}")
```

---

## 📑 相關章節

| 前序 | 當前 | 後續 |
|-----|------|------|
| [12.5 資料模型詳細定義](ch12-5-資料模型詳細定義.md) | **12.6 API詳細規範** | [12.7 效能優化策略](ch12-7-效能優化策略.md) |

**快速鏈接：**
- [12.1 模組概述](ch12-1-模組概述.md)
- [12.5 資料模型詳細定義](ch12-5-資料模型詳細定義.md)
- [12.7 效能優化策略](ch12-7-效能優化策略.md)
- [← 返回第12章首頁](ch12-index.md)

---

**最後更新**: 2025-10-31  
**版本**: 1.0

