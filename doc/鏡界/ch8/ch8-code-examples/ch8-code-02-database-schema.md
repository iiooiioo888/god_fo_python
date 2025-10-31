# CH8 代碼示例 - 8.5 數據庫架構定義

```sql
-- 集群節點表
CREATE TABLE IF NOT EXISTS cluster_nodes (
    node_id VARCHAR(36) PRIMARY KEY,
    status VARCHAR(20),
    cpu_cores INT,
    memory_gb INT,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 爬蟲任務表
CREATE TABLE IF NOT EXISTS crawler_tasks (
    task_id VARCHAR(36) PRIMARY KEY,
    node_id VARCHAR(36),
    definition JSONB,
    status VARCHAR(20),
    priority INT,
    result JSONB,
    created_at TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (node_id) REFERENCES cluster_nodes(node_id)
);

-- 資源使用記錄
CREATE TABLE IF NOT EXISTS resource_usage (
    usage_id VARCHAR(36) PRIMARY KEY,
    node_id VARCHAR(36),
    cpu_usage FLOAT,
    memory_usage FLOAT,
    recorded_at TIMESTAMP,
    FOREIGN KEY (node_id) REFERENCES cluster_nodes(node_id)
);

-- 索引
CREATE INDEX idx_cluster_nodes_status ON cluster_nodes(status);
CREATE INDEX idx_crawler_tasks_status ON crawler_tasks(status);
CREATE INDEX idx_resource_usage_node_id ON resource_usage(node_id);
```

---

## 相關文件引用

- **核心實現**: [代碼示例 - 集群管理](ch8-code-01-cluster-manager.md)
- **API 示例**: [代碼示例 - API 端點](ch8-code-03-api-examples.md)
