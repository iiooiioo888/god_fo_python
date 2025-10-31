# 第8章：分布式爬蟲集群管理系統 (Distributed Crawler Cluster Management System)

## 8.6 API詳細規範

**[← 返回第8章首頁](ch8-index.md)**

---

#### 8.6.1 節点管理API

**註冊爬蟲節点 (POST /api/v1/nodes:register)**

*请求示例:*
```http
POST /api/v1/nodes:register HTTP/1.1
Host: dccms.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "crawler-node-01",
  "description": "Main crawler node in US East region",
  "ip_address": "192.168.1.101",
  "port": 8000,
  "node_type": "standard",
  "capabilities": {
    "content_types": ["html", "json", "xml"],
    "technologies": ["react", "angular", "wordpress"],
    "anti_crawling_bypass": ["user-agent", "proxy"]
  },
  "resources": {
    "cpu": 8,
    "memory_mb": 16384,
    "gpu": 1,
    "network_bandwidth_mbps": 1000
  }
}
```

*成功響應示例:*
```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/nodes/node-1a2b3c4d

{
  "node_id": "node-1a2b3c4d",
  "registration_time": 1686825045.123,
  "initial_status": "online"
}
```

**发送節点心跳 (POST /api/v1/nodes/{node_id}:heartbeat)**

*请求示例:*
```http
POST /api/v1/nodes/node-1a2b3c4d:heartbeat HTTP/1.1
Host: dccms.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "resources": {
    "cpu_usage": 0.65,
    "memory_usage": 0.75,
    "gpu_usage": 0.45
  },
  "load": 0.8,
  "active_tasks": ["task-123", "task-456"]
}
```

*成功響應示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "node_id": "node-1a2b3c4d",
  "timestamp": 1686825045.123,
  "status": "online"
}
```

#### 8.6.2 任務管理API

**创建爬蟲任務 (POST /api/v1/tasks)**

*请求示例:*
```http
POST /api/v1/tasks HTTP/1.1
Host: dccms.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "project_id": "proj-123",
  "workflow_id": "inst-1a2b3c4d5e6f",
  "task_type": "web_crawl",
  "parameters": {
    "url": "https://example.com/products",
    "depth": 2,
    "selectors": {
      "product": "div.product",
      "title": "h2.title",
      "price": "span.price"
    }
  },
  "priority": 7,
  "min_resources": {
    "memory_mb": 4096,
    "cpu_cores": 2
  },
  "capabilities": {
    "javascript_rendering": 1,
    "proxy_rotation": 1
  },
  "schedule_strategy": "least_loaded",
  "target_region": "us",
  "content_features": {
    "content_type": "html",
    "technology": "react"
  }
}
```

*成功響應示例:*
```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/tasks/task-123

{
  "id": "task-123",
  "status": "pending",
  "created_at": "2023-06-15T10:30:45Z",
  "priority": 7
}
```

**獲取任務狀態 (GET /api/v1/tasks/{task_id})**

*请求示例:*
```http
GET /api/v1/tasks/task-123 HTTP/1.1
Host: dccms.mirror-realm.com
Authorization: Bearer <access_token>
```

*成功響應示例 (處理中):*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "task-123",
  "project_id": "proj-123",
  "workflow_id": "inst-1a2b3c4d5e6f",
  "task_type": "web_crawl",
  "parameters": {
    "url": "https://example.com/products",
    "depth": 2,
    "selectors": {
      "product": "div.product",
      "title": "h2.title",
      "price": "span.price"
    }
  },
  "priority": 7,
  "min_resources": {
    "memory_mb": 4096,
    "cpu_cores": 2
  },
  "capabilities": {
    "javascript_rendering": 1,
    "proxy_rotation": 1
  },
  "schedule_strategy": "least_loaded",
  "target_region": "us",
  "content_features": {
    "content_type": "html",
    "technology": "react"
  },
  "status": "processing",
  "created_at": "2023-06-15T10:30:45Z",
  "updated_at": "2023-06-15T10:31:10Z",
  "assigned_node": "node-1a2b3c4d",
  "assigned_at": "2023-06-15T10:31:10Z",
  "retry_count": 0,
  "max_retries": 3
}
```

*成功響應示例 (已完成):*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "task-123",
  "project_id": "proj-123",
  "workflow_id": "inst-1a2b3c4d5e6f",
  "task_type": "web_crawl",
  "parameters": {
    "url": "https://example.com/products",
    "depth": 2,
    "selectors": {
      "product": "div.product",
      "title": "h2.title",
      "price": "span.price"
    }
  },
  "priority": 7,
  "min_resources": {
    "memory_mb": 4096,
    "cpu_cores": 2
  },
  "capabilities": {
    "javascript_rendering": 1,
    "proxy_rotation": 1
  },
  "schedule_strategy": "least_loaded",
  "target_region": "us",
  "content_features": {
    "content_type": "html",
    "technology": "react"
  },
  "status": "completed",
  "created_at": "2023-06-15T10:30:45Z",
  "updated_at": "2023-06-15T10:35:20Z",
  "assigned_node": "node-1a2b3c4d",
  "assigned_at": "2023-06-15T10:31:10Z",
  "completed_at": "2023-06-15T10:35:20Z",
  "result": {
    "success": true,
    "data": {
      "products": [
        {
          "title": "Product 1",
          "price": "$19.99",
          "url": "/products/1"
        },
        {
          "title": "Product 2",
          "price": "$29.99",
          "url": "/products/2"
        }
      ]
    },
    "metrics": {
      "pages_crawled": 15,
      "processing_time": 125.4,
      "data_size": 4294967
    },
    "timestamp": "2023-06-15T10:35:20Z"
  },
  "retry_count": 0,
  "max_retries": 3
}
```

---

## 📑 相關章節

| 前序 | 當前 | 後續 |
|-----|------|------|
| [8.5 資料模型詳細定義](ch8-5-資料模型詳細定義.md) | **8.6 API詳細規範** | [8.7 效能優化策略](ch8-7-效能優化策略.md) |

**快速鏈接：**
- [8.5 資料模型詳細定義](ch8-5-資料模型詳細定義.md)
- [8.7 效能優化策略](ch8-7-效能優化策略.md)
- [← 返回第8章首頁](ch8-index.md)
