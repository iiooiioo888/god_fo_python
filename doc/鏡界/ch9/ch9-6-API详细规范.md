**[← 返回第9章首頁](ch9-index.md)**

---

### 9.6 效能测试方案

#### 9.6.1 基準测试場景

1. **資料源註冊中心效能测试**
   ```python
   # dsr_load_test.py
   import os
   import time
   import json
   import random
   from locust import HttpUser, task, between, events
   from locust.runners import MasterRunner
   
   # 测试配置
   TEST_DATA_SOURCES = [
       {
           "name": f"test-source-{i}",
           "display_name": f"Test Source {i}",
           "url": f"https://example.com/data/{i}",
           "category": random.choice(["web", "api", "social"]),
           "data_type": random.choice(["html", "json", "xml"]),
           "tags": ["test", "performance"]
       } for i in range(1000)
   ]
   
   @events.test_start.add_listener
   def on_test_start(environment, **kwargs):
       """测试開始前的准備工作"""
       if not isinstance(environment.runner, MasterRunner):
           print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting DSR performance test")
           print(f"  * Test data sources: {len(TEST_DATA_SOURCES)}")
           print(f"  * Target RPS: {environment.parsed_options.spawn_rate}")
   
   class DataSourcesUser(HttpUser):
       wait_time = between(0.1, 0.5)
       
       def on_start(self):
           """用戶启動時的初始化"""
           self.auth_token = self._get_auth_token()
           self.headers = {
               "Authorization": f"Bearer {self.auth_token}",
               "Content-Type": "application/json"
           }
       
       def _get_auth_token(self):
           """獲取認證令牌"""
           response = self.client.post(
               "/api/v1/auth/token",
               json={
                   "client_id": "performance-test",
                   "client_secret": "perf-test-secret",
                   "grant_type": "client_credentials"
               }
           )
           return response.json()["access_token"]
       
       @task(5)
       def list_data_sources(self):
           """列出資料源"""
           self.client.get(
               "/api/v1/data-sources",
               headers=self.headers,
               name="/api/v1/data-sources"
           )
       
       @task(3)
       def get_data_source(self):
           """獲取单個資料源"""
           source_id = f"ds-{random.randint(1, 1000):04d}"
           self.client.get(
               f"/api/v1/data-sources/{source_id}",
               headers=self.headers,
               name="/api/v1/data-sources/{id}"
           )
       
       @task(2)
       def create_data_source(self):
           """创建資料源"""
           source = random.choice(TEST_DATA_SOURCES)
           self.client.post(
               "/api/v1/data-sources",
               json=source,
               headers=self.headers,
               name="/api/v1/data-sources"
           )
       
       @task(1)
       def search_data_sources(self):
           """搜尋資料源"""
           query = random.choice(["test", "example", "api", "web"])
           self.client.get(
               f"/api/v1/data-sources?search={query}",
               headers=self.headers,
               name="/api/v1/data-sources:search"
           )
   ```

2. **分布式爬蟲集群效能测试**
   ```python
   # crawler_cluster_load_test.py
   import os
   import time
   import json
   import random
   from locust import HttpUser, task, between, events
   from locust.runners import MasterRunner
   
   # 测试配置
   TEST_TASKS = [
       {
           "task_type": "web_crawl",
           "parameters": {
               "url": f"https://example.com/page/{i}",
               "depth": random.randint(1, 3)
           },
           "priority": random.randint(1, 10),
           "min_resources": {
               "memory_mb": random.choice([512, 1024, 2048]),
               "cpu_cores": random.uniform(0.5, 2.0)
           }
       } for i in range(10000)
   ]
   
   class CrawlerUser(HttpUser):
       wait_time = between(0.01, 0.1)
       
       def on_start(self):
           """用戶启動時的初始化"""
           self.auth_token = self._get_auth_token()
           self.headers = {
               "Authorization": f"Bearer {self.auth_token}",
               "Content-Type": "application/json"
           }
       
       def _get_auth_token(self):
           """獲取認證令牌"""
           response = self.client.post(
               "/api/v1/auth/token",
               json={
                   "client_id": "crawler-test",
                   "client_secret": "crawler-test-secret",
                   "grant_type": "client_credentials"
               }
           )
           return response.json()["access_token"]
       
       @task(10)
       def create_task(self):
           """创建爬蟲任務"""
           task = random.choice(TEST_TASKS)
           response = self.client.post(
               "/api/v1/tasks",
               json=task,
               headers=self.headers,
               name="/api/v1/tasks"
           )
           
           if response.status_code == 201:
               task_id = response.json()["id"]
               # 轮询任務狀態
               for _ in range(10):
                   time.sleep(0.1)
                   status_response = self.client.get(
                       f"/api/v1/tasks/{task_id}",
                       headers=self.headers,
                       name="/api/v1/tasks/{id}"
                   )
                   
                   if status_response.status_code == 200:
                       status = status_response.json()["status"]
                       if status in ["completed", "failed"]:
                           break
   ```

#### 9.6.2 效能指標阈值

1. **API效能指標阈值**
   | 指標 | 95分位 | 99分位 | 错误率 | 資源使用 |
   |------|--------|--------|--------|----------|
   | **資料源註冊中心** | | | | |
   | 列建資料源 | <200ms | <500ms | <0.1% | CPU<50%, Mem<70% |
   | 獲取資料源列表 | <100ms | <300ms | <0.1% | CPU<40%, Mem<60% |
   | 搜尋資料源 | <150ms | <400ms | <0.1% | CPU<45%, Mem<65% |
   | **分布式爬蟲集群** | | | | |
   | 创建爬蟲任務 | <100ms | <300ms | <0.1% | CPU<50%, Mem<70% |
   | 任務狀態查詢 | <50ms | <200ms | <0.1% | CPU<30%, Mem<50% |
   | 節点心跳 | <20ms | <100ms | <0.01% | CPU<20%, Mem<40% |

2. **系統容量规划**
   | 服務 | 单例配置 | 单例數量 | 支援QPS | 每日任務量 | 儲存需求 |
   |------|----------|----------|---------|------------|----------|
   | 資料源註冊中心 | 2vCPU, 4GB | 3 | 1,000 | - | 50GB |
   | 網站指紋分析引擎 | 4vCPU, 8GB | 5 | 500 | - | 200GB |
   | 資料源健康监测系統 | 2vCPU, 4GB | 3 | 2,000 | - | 100GB |
   | 資料處理工作流引擎 | 4vCPU, 8GB | 5 | 1,500 | - | 150GB |
   | 自動化媒體處理管道 | 8vCPU, 16GB, 1GPU | 10 | 100 | 10,000 | 10TB |
   | AI輔助開发系統 | 4vCPU, 8GB | 3 | 300 | - | 50GB |
   | 資料合規與安全中心 | 2vCPU, 4GB | 3 | 500 | - | 75GB |
   | 分布式爬蟲集群管理系統 | 4vCPU, 8GB | 5 | 2,000 | 1,000,000 | 200GB |

---

## 📑 相關章節

| 前序 | 當前 | 後續 |
|-----|------|------|
| [9.5](ch9-5-資料模型詳細定義.md) | **9.6** | [9.7](ch9-7-效能優化策略.md) |

**快速鏈接：**
- [← 返回第9章首頁](ch9-index.md)
