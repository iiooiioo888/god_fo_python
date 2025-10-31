# CH4 代碼示例 - 4.5 數據庫架構定義

## 資料處理工作流引擎核心表結構

```sql
-- ==================== 類型定義 ====================

-- 執行狀態枚舉（強制資料一致性）
CREATE TYPE execution_status AS ENUM (
    'pending', 'running', 'success', 'failed', 'cancelled', 'retry'
);

-- 任務狀態枚舉
CREATE TYPE task_status AS ENUM (
    'pending', 'running', 'success', 'failed', 'skipped', 'timeout'
);

-- ==================== 核心表定義 ====================

-- 工作流定義表
CREATE TABLE IF NOT EXISTS workflow_definitions (
    workflow_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    version VARCHAR(20) NOT NULL,
    definition_json JSONB NOT NULL COMMENT '工作流定義（YAML/JSON格式）',
    status VARCHAR(20) DEFAULT 'active',
    created_by VARCHAR(36),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT uq_workflow_name_version UNIQUE(name, version)
);

-- 工作流執行表
CREATE TABLE IF NOT EXISTS workflow_executions (
    execution_id VARCHAR(36) PRIMARY KEY,
    workflow_id VARCHAR(36) NOT NULL,
    
    -- 執行信息
    input_data JSONB,
    status execution_status NOT NULL DEFAULT 'pending',
    
    -- 時間追蹤（檢測時間 vs 寫入時間）
    start_time TIMESTAMP COMMENT '執行開始時間',
    end_time TIMESTAMP COMMENT '執行結束時間',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- 結構化錯誤訊息
    error_code VARCHAR(20),
    error_detail TEXT,
    
    -- 審計信息
    created_by VARCHAR(36),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_execution_workflow 
        FOREIGN KEY (workflow_id) REFERENCES workflow_definitions(workflow_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 工作流狀態表
CREATE TABLE IF NOT EXISTS workflow_states (
    state_id VARCHAR(36) PRIMARY KEY,
    execution_id VARCHAR(36) NOT NULL,
    state_data JSONB NOT NULL COMMENT '工作流執行狀態快照',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_state_execution 
        FOREIGN KEY (execution_id) REFERENCES workflow_executions(execution_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 任務執行表
CREATE TABLE IF NOT EXISTS task_executions (
    task_execution_id VARCHAR(36) PRIMARY KEY,
    execution_id VARCHAR(36) NOT NULL,
    task_id VARCHAR(36),
    
    -- 任務狀態
    status task_status NOT NULL DEFAULT 'pending',
    result JSONB,
    
    -- 時間追蹤
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 結構化錯誤
    error_code VARCHAR(20),
    error_detail TEXT,
    
    -- 重試信息
    retry_count INT DEFAULT 0,
    max_retries INT DEFAULT 3,
    
    CONSTRAINT fk_task_execution 
        FOREIGN KEY (execution_id) REFERENCES workflow_executions(execution_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ==================== 索引優化 ====================

-- 複合索引加速常見查詢場景
CREATE INDEX idx_we_workflow_status 
    ON workflow_executions(workflow_id, status, created_at DESC);

CREATE INDEX idx_we_created_time 
    ON workflow_executions(created_at DESC);

CREATE INDEX idx_ws_execution_id 
    ON workflow_states(execution_id);

CREATE INDEX idx_te_execution_status 
    ON task_executions(execution_id, status);

CREATE INDEX idx_te_created_time 
    ON task_executions(created_at DESC);

-- ==================== 性能最佳實踐 ====================

-- 執行統計表（加速儀表板查詢）
CREATE TABLE IF NOT EXISTS execution_statistics (
    stat_id VARCHAR(36) PRIMARY KEY,
    workflow_id VARCHAR(36) NOT NULL,
    
    stat_date DATE NOT NULL,
    stat_hour INT COMMENT 'NULL 表示日彙總',
    
    -- 統計指標
    total_executions INT DEFAULT 0,
    successful_executions INT DEFAULT 0,
    failed_executions INT DEFAULT 0,
    avg_duration_ms INT COMMENT '平均執行時間（毫秒）',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_stat_workflow 
        FOREIGN KEY (workflow_id) REFERENCES workflow_definitions(workflow_id),
    
    -- 唯一約束
    UNIQUE(workflow_id, stat_date, stat_hour)
);

CREATE INDEX idx_execution_stat_workflow_date 
    ON execution_statistics(workflow_id, stat_date DESC);
```

---

## 設計原則

✅ **類型安全**
- 使用 ENUM 強制狀態值一致性
- 編譯時檢查提升性能

✅ **時間追蹤**
- 分離 start_time 和 created_at
- 支援準確的性能分析

✅ **結構化錯誤**
- error_code + error_detail 分離
- 支援程式化錯誤處理和告警

✅ **外鍵約束**
- 防止孤立資料
- 支援級聯刪除

✅ **複合索引**
- 優化常見查詢模式
- 提升大規模執行記錄的查詢性能

---

## 相關文件引用

- **主文檔**: [4.5 資料模型詳細定義](../ch4-5-数据模型详细定义.md)
- **核心實現**: [代碼示例 - 工作流引擎](ch4-code-01-workflow-engine.md)
- **API 示例**: [代碼示例 - API 端點](ch4-code-04-api-examples.md)
