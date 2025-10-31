# CH9 代碼示例 - 9.5 數據庫架構定義

```sql
-- 部署記錄表
CREATE TABLE IF NOT EXISTS deployments (
    deployment_id VARCHAR(36) PRIMARY KEY,
    service_name VARCHAR(100),
    version VARCHAR(50),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 配置表
CREATE TABLE IF NOT EXISTS configurations (
    config_id VARCHAR(36) PRIMARY KEY,
    service_name VARCHAR(100),
    config_data JSONB,
    version INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 系統指標表
CREATE TABLE IF NOT EXISTS metrics (
    metric_id VARCHAR(36) PRIMARY KEY,
    data JSONB,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_deployments_service ON deployments(service_name);
CREATE INDEX idx_configurations_service ON configurations(service_name);
CREATE INDEX idx_metrics_recorded_at ON metrics(recorded_at);
```

---

## 相關文件引用

- **核心實現**: [代碼示例 - 部署服務](ch9-code-01-deployment-service.md)
- **API 示例**: [代碼示例 - API 端點](ch9-code-03-api-examples.md)
