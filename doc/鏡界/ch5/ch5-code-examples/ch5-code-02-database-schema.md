# CH5 代碼示例 - 5.5 數據庫架構定義

## 核心表結構

```sql
-- 媒體工作表
CREATE TABLE IF NOT EXISTS media_jobs (
    task_id VARCHAR(36) PRIMARY KEY,
    original_file VARCHAR(512) NOT NULL,
    processed_data JSONB,
    analysis_result JSONB,
    status VARCHAR(20) DEFAULT 'pending',
    quality_score FLOAT,
    created_by VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 處理任務表
CREATE TABLE IF NOT EXISTS processing_tasks (
    task_id VARCHAR(36),
    step VARCHAR(50),
    status VARCHAR(20),
    result JSONB,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    PRIMARY KEY (task_id, step),
    FOREIGN KEY (task_id) REFERENCES media_jobs(task_id)
);

-- 分析結果表
CREATE TABLE IF NOT EXISTS ai_results (
    result_id VARCHAR(36) PRIMARY KEY,
    task_id VARCHAR(36),
    model_name VARCHAR(100),
    result_data JSONB,
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES media_jobs(task_id)
);

-- 索引
CREATE INDEX idx_media_jobs_status ON media_jobs(status);
CREATE INDEX idx_media_jobs_created_by ON media_jobs(created_by);
CREATE INDEX idx_processing_tasks_status ON processing_tasks(status);
CREATE INDEX idx_ai_results_task_id ON ai_results(task_id);
```

---

## 相關文件引用

- **核心實現**: [代碼示例 - 媒體處理](ch5-code-01-media-processor.md)
- **API 示例**: [代碼示例 - API 端點](ch5-code-03-api-examples.md)
