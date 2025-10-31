# CH3 代碼示例 - 3.5 數據庫架構定義

## 核心表結構

### 1. health_check_records - 健康檢測記錄表

```sql
CREATE TABLE IF NOT EXISTS health_check_records (
    record_id VARCHAR(36) PRIMARY KEY,
    datasource_id VARCHAR(36) NOT NULL,
    check_time TIMESTAMP NOT NULL,
    
    -- 檢測結果
    overall_status VARCHAR(20) NOT NULL,  -- healthy, warning, error, critical
    metrics JSONB NOT NULL,  -- {availability, response_time_ms, error_rate_percent, quality_score}
    check_details JSONB NOT NULL,  -- 詳細檢測結果
    
    -- 審計
    created_by VARCHAR(36) DEFAULT 'system',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_datasource FOREIGN KEY (datasource_id)
        REFERENCES data_sources(id)
);

CREATE INDEX idx_hcr_datasource_id ON health_check_records(datasource_id);
CREATE INDEX idx_hcr_check_time ON health_check_records(check_time);
CREATE INDEX idx_hcr_overall_status ON health_check_records(overall_status);

-- 分區表（按月）
CREATE TABLE health_check_records_2024_10
PARTITION OF health_check_records
FOR VALUES FROM ('2024-10-01') TO ('2024-11-01');
```

### 2. alerts - 告警表

```sql
CREATE TABLE IF NOT EXISTS alerts (
    alert_id VARCHAR(36) PRIMARY KEY,
    datasource_id VARCHAR(36) NOT NULL,
    
    level VARCHAR(20) NOT NULL,  -- info, warning, error, critical
    message TEXT NOT NULL,
    metrics JSONB DEFAULT '{}',
    
    status VARCHAR(20) DEFAULT 'active',  -- active, acknowledged, resolved
    acknowledged_by VARCHAR(36),
    acknowledged_at TIMESTAMP,
    resolved_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_datasource FOREIGN KEY (datasource_id)
        REFERENCES data_sources(id)
);

CREATE INDEX idx_alerts_datasource_id ON alerts(datasource_id);
CREATE INDEX idx_alerts_level ON alerts(level);
CREATE INDEX idx_alerts_status ON alerts(status);
CREATE INDEX idx_alerts_created_at ON alerts(created_at);
```

### 3. alert_rules - 告警規則表

```sql
CREATE TABLE IF NOT EXISTS alert_rules (
    rule_id VARCHAR(36) PRIMARY KEY,
    datasource_id VARCHAR(36),
    
    name VARCHAR(100) NOT NULL,
    level VARCHAR(20) NOT NULL,  -- info, warning, error, critical
    condition JSONB NOT NULL,
    
    -- 通知渠道
    email_enabled BOOLEAN DEFAULT TRUE,
    slack_enabled BOOLEAN DEFAULT TRUE,
    dingtalk_enabled BOOLEAN DEFAULT FALSE,
    
    enabled BOOLEAN DEFAULT TRUE,
    created_by VARCHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_datasource FOREIGN KEY (datasource_id)
        REFERENCES data_sources(id)
);

CREATE INDEX idx_ar_datasource_id ON alert_rules(datasource_id);
CREATE INDEX idx_ar_enabled ON alert_rules(enabled);
```

### 4. health_trends - 健康趨勢分析表

```sql
CREATE TABLE IF NOT EXISTS health_trends (
    trend_id VARCHAR(36) PRIMARY KEY,
    datasource_id VARCHAR(36) NOT NULL,
    
    -- 時間區間
    period_start TIMESTAMP NOT NULL,
    period_end TIMESTAMP NOT NULL,
    period_type VARCHAR(20) NOT NULL,  -- hourly, daily, weekly, monthly
    
    -- 統計數據
    avg_availability DECIMAL(5,2),
    min_availability DECIMAL(5,2),
    max_availability DECIMAL(5,2),
    
    avg_response_time_ms INTEGER,
    min_response_time_ms INTEGER,
    max_response_time_ms INTEGER,
    
    error_count INTEGER DEFAULT 0,
    alert_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_datasource FOREIGN KEY (datasource_id)
        REFERENCES data_sources(id)
);

CREATE INDEX idx_ht_datasource_id ON health_trends(datasource_id);
CREATE INDEX idx_ht_period ON health_trends(period_start, period_end);
```

---

## 相關文件引用

- **核心監測**: [代碼示例 - 健康監測](ch3-code-01-health-monitor.md)
- **告警系統**: [代碼示例 - 告警系統](ch3-code-02-alert-system.md)
- **API 示例**: [代碼示例 - API 端點](ch3-code-04-api-examples.md)
