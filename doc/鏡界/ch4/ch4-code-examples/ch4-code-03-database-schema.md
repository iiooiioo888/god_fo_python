# CH4 代碼示例 - 4.5 數據庫架構定義

## 核心表結構

```sql
-- 工作流定義表
CREATE TABLE IF NOT EXISTS workflow_definitions (
    workflow_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    version VARCHAR(20) NOT NULL,
    definition_json JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_by VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, version)
);

-- 工作流執行表
CREATE TABLE IF NOT EXISTS workflow_executions (
    execution_id VARCHAR(36) PRIMARY KEY,
    workflow_id VARCHAR(36) NOT NULL,
    input_data JSONB,
    status VARCHAR(20) DEFAULT 'pending',
    error_message TEXT,
    created_by VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_workflow FOREIGN KEY (workflow_id)
        REFERENCES workflow_definitions(workflow_id)
);

-- 工作流狀態表
CREATE TABLE IF NOT EXISTS workflow_states (
    state_id VARCHAR(36) PRIMARY KEY,
    execution_id VARCHAR(36) NOT NULL,
    state_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_execution FOREIGN KEY (execution_id)
        REFERENCES workflow_executions(execution_id)
);

-- 任務執行表
CREATE TABLE IF NOT EXISTS task_executions (
    task_execution_id VARCHAR(36) PRIMARY KEY,
    execution_id VARCHAR(36) NOT NULL,
    task_id VARCHAR(36),
    status VARCHAR(20) DEFAULT 'pending',
    result JSONB,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_execution FOREIGN KEY (execution_id)
        REFERENCES workflow_executions(execution_id)
);

-- 創建索引
CREATE INDEX idx_we_workflow_id ON workflow_executions(workflow_id);
CREATE INDEX idx_we_status ON workflow_executions(status);
CREATE INDEX idx_ws_execution_id ON workflow_states(execution_id);
CREATE INDEX idx_te_execution_id ON task_executions(execution_id);
CREATE INDEX idx_te_status ON task_executions(status);
```

---

## 相關文件引用

- **核心引擎**: [代碼示例 - 工作流引擎](ch4-code-01-workflow-engine.md)
- **服務集成**: [代碼示例 - 服務集成](ch4-code-02-service-integration.md)
- **API 示例**: [代碼示例 - API 端點](ch4-code-04-api-examples.md)
