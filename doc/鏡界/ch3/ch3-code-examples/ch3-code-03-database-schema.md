# CH3 代碼示例 - 3.5 數據庫架構定義

## 健康監測系統核心表結構

```sql
-- ==================== 類型定義 ====================

-- 健康檢測狀態枚舉（強制資料一致性）
CREATE TYPE health_status AS ENUM ('success', 'warning', 'error', 'timeout');

-- 告警嚴重性和狀態枚舉
CREATE TYPE alert_severity AS ENUM ('info', 'warning', 'critical');
CREATE TYPE alert_status AS ENUM ('triggered', 'acknowledged', 'resolved', 'closed');

-- 告警條件枚舉
CREATE TYPE alert_condition AS ENUM ('gt', 'gte', 'lt', 'lte', 'eq', 'ne', 'in');

-- ==================== 核心表定義 ====================

-- 健康檢測結果表（時序資料，帶分區）
CREATE TABLE health_check_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    data_source_id UUID NOT NULL,
    
    -- 時間欄位分離（檢測時間 vs 寫入時間）
    check_time TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- 檢測結果（使用 ENUM 強制一致性）
    status health_status NOT NULL,
    response_time INT COMMENT '響應時間（毫秒）',
    
    -- 結構化錯誤訊息（支援程式化告警）
    error_code VARCHAR(20),
    error_detail TEXT,
    
    -- SSL 檢測
    ssl_certificate_valid BOOLEAN,
    ssl_expiry_days INT,
    
    -- 內容追蹤
    content_hash VARCHAR(64),
    
    CONSTRAINT fk_health_check_datasource 
        FOREIGN KEY (data_source_id) REFERENCES data_sources(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) PARTITION BY RANGE (check_time);

-- 分區表（按月分區以優化查詢性能）
CREATE TABLE health_check_records_2024_10 PARTITION OF health_check_records
    FOR VALUES FROM ('2024-10-01') TO ('2024-11-01');
CREATE TABLE health_check_records_2024_11 PARTITION OF health_check_records
    FOR VALUES FROM ('2024-11-01') TO ('2024-12-01');

-- 複合索引優化監控查詢場景
CREATE INDEX idx_health_check_datasource_time 
    ON health_check_records(data_source_id, check_time DESC);
CREATE INDEX idx_health_check_created_time 
    ON health_check_records(created_at DESC);
CREATE INDEX idx_health_check_status 
    ON health_check_records(data_source_id, status, check_time DESC);

-- ==================== 告警表定義 ====================

-- 告警歷史表（完整生命週期追蹤）
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    data_source_id UUID NOT NULL,
    
    -- 告警基本信息
    alert_type VARCHAR(50) NOT NULL,
    severity alert_severity NOT NULL,
    status alert_status NOT NULL DEFAULT 'triggered',
    message TEXT NOT NULL,
    
    -- 生命週期時間戳
    triggered_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    acknowledged_at TIMESTAMPTZ,
    resolved_at TIMESTAMPTZ,
    closed_at TIMESTAMPTZ,
    
    -- 指標詳情
    metric_name VARCHAR(100),
    metric_value NUMERIC(10, 2),
    threshold NUMERIC(10, 2),
    
    -- 處理信息
    assigned_to UUID,
    notes TEXT,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_alert_datasource 
        FOREIGN KEY (data_source_id) REFERENCES data_sources(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 告警查詢索引
CREATE INDEX idx_alert_datasource_status 
    ON alerts(data_source_id, status, triggered_at DESC);
CREATE INDEX idx_alert_severity_triggered 
    ON alerts(severity, triggered_at DESC);
CREATE INDEX idx_alert_triggered_time 
    ON alerts(triggered_at DESC);

-- ==================== 聚合表定義 ====================

-- 健康檢測統計表（加速儀表板查詢）
CREATE TABLE health_check_summary (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    data_source_id UUID NOT NULL,
    
    -- 時間維度
    summary_date DATE NOT NULL,
    summary_hour INT,  -- NULL 表示日彙總
    
    -- 統計指標
    total_checks INT NOT NULL DEFAULT 0,
    successful_checks INT NOT NULL DEFAULT 0,
    failed_checks INT NOT NULL DEFAULT 0,
    warning_checks INT NOT NULL DEFAULT 0,
    
    -- 性能指標（毫秒）
    avg_response_time INT,
    max_response_time INT,
    min_response_time INT,
    p95_response_time INT,
    
    -- 可用性
    availability_percentage NUMERIC(5, 2),
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_summary_datasource 
        FOREIGN KEY (data_source_id) REFERENCES data_sources(id),
    
    -- 唯一約束（每個時間段一條記錄）
    UNIQUE(data_source_id, summary_date, summary_hour)
);

CREATE INDEX idx_summary_datasource_date 
    ON health_check_summary(data_source_id, summary_date DESC);

-- ==================== 告警規則表定義 ====================

-- 動態告警規則配置
CREATE TABLE alert_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- 規則信息
    rule_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    
    -- 適用範圍
    data_source_id UUID,  -- NULL 表示全局規則
    metric_name VARCHAR(100) NOT NULL,
    
    -- 條件配置
    condition alert_condition NOT NULL,
    threshold NUMERIC(10, 2) NOT NULL,
    evaluation_window INT NOT NULL DEFAULT 300,  -- 秒
    
    -- 告警配置
    alert_severity alert_severity NOT NULL,
    cooldown_seconds INT DEFAULT 300,
    
    -- 通知配置
    notify_channels VARCHAR(100)[],
    notify_users UUID[],
    
    -- 審計
    created_by UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by UUID,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_alert_rules_active 
    ON alert_rules(is_active, metric_name);

-- ==================== 觸發器定義 ====================

-- 自動更新 updated_at 時間戳的函數
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 應用觸發器到需要的表
CREATE TRIGGER update_alerts_updated_at
    BEFORE UPDATE ON alerts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_health_check_summary_updated_at
    BEFORE UPDATE ON health_check_summary
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ==================== 視圖定義 ====================

-- 待處理告警視圖（便於監控儀表板）
CREATE VIEW pending_alerts AS
SELECT 
    id,
    data_source_id,
    alert_type,
    severity,
    message,
    triggered_at,
    metric_name,
    metric_value,
    threshold
FROM alerts
WHERE status IN ('triggered', 'acknowledged')
ORDER BY severity DESC, triggered_at ASC;

-- 最新健康狀態視圖
CREATE VIEW latest_health_status AS
SELECT DISTINCT ON (data_source_id)
    data_source_id,
    status,
    response_time,
    check_time,
    ssl_certificate_valid
FROM health_check_records
ORDER BY data_source_id, check_time DESC;
```

---

## 設計亮點

✅ **類型安全**
- 使用 ENUM 類型強制有效值，防止資料不一致
- PostgreSQL 的編譯時類型檢查提升性能

✅ **時序資料優化**
- 表分區支援百萬級檢測記錄存儲
- 複合索引加速時間序列查詢

✅ **完整性約束**
- 外鍵關聯防止孤立資料
- 唯一約束確保統計表的唯一性

✅ **程式化告警**
- 結構化 error_code / error_detail 支援自動化規則
- ENUM 條件類型支援動態規則評估

✅ **生命週期追蹤**
- 四個時間戳（triggered/acknowledged/resolved/closed）完整記錄告警狀態
- 自動 updated_at 更新支援審計追蹤

---

## 相關文件引用

- **主文檔**: [3.5 資料模型詳細定義](../ch3-5-数据模型详细定义.md)
- **核心實現**: [代碼示例 - 健康監測](ch3-code-01-health-monitor.md)
- **API 示例**: [代碼示例 - API 端點](ch3-code-04-api-examples.md)

---

## 📋 生產級數據庫設計補充指南

### 響應時間監控設計

**問題**: 模糊的時間單位導致查詢、告警和 SLA 對標困難

**最佳實踐**:
```sql
-- ✅ 推薦做法：明確標註單位
response_time INT COMMENT '響應時間（毫秒 ms）'

-- 配套查詢示例
SELECT 
    data_source_id,
    AVG(response_time) as avg_response_ms,
    MAX(response_time) as max_response_ms,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY response_time) as p95_response_ms
FROM health_check_records
WHERE check_time > NOW() - INTERVAL '24 hours'
GROUP BY data_source_id;

-- SLA 對標示例
SELECT 
    data_source_id,
    COUNT(*) as total_checks,
    SUM(CASE WHEN response_time <= 1000 THEN 1 ELSE 0 END) as sla_compliant,
    ROUND(100.0 * SUM(CASE WHEN response_time <= 1000 THEN 1 ELSE 0 END) / COUNT(*), 2) as sla_compliance_pct
FROM health_check_records
WHERE check_time > NOW() - INTERVAL '7 days'
GROUP BY data_source_id;
```

**應用場景**:
- CH1 (DSR): response_time 用於搜尋索引效率監控
- CH4 (Workflow): avg_duration_ms 用於工作流性能追蹤
- CH5 (Media): processing_time_ms 用於媒體處理性能分析

---

### 時間戳完整性設計

**問題**: 單一 created_at 無法區分「事件發生時間」和「資料寫入時間」

**最佳實踐**:
```sql
-- ✅ 時間戳分離
check_time TIMESTAMPTZ NOT NULL COMMENT '檢測執行時間（事件時間）',
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW() COMMENT '資料寫入時間（記錄時間）'

-- 索引策略
CREATE INDEX idx_check_time ON health_check_records(check_time DESC);  -- 時序查詢
CREATE INDEX idx_created_at ON health_check_records(created_at DESC);  -- 審計追蹤

-- 查詢示例：找出 1 小時內遲到的檢測（監控網路延遲）
SELECT 
    data_source_id,
    check_time,
    created_at,
    EXTRACT(EPOCH FROM (created_at - check_time))/1000 as delay_seconds
FROM health_check_records
WHERE created_at - check_time > INTERVAL '5 minutes'
ORDER BY delay_seconds DESC;
```

**應用場景**:
- CH3 (DSHM): 檢測時間 vs 記錄時間（監測網路延遲）
- CH9 (Deployment): 部署開始時間 vs 部署完成時間

**複合索引優化**:
```sql
-- 常見查詢模式
CREATE INDEX idx_health_check_datasource_time 
    ON health_check_records(data_source_id, check_time DESC);  -- 查詢特定源的最新檢測

CREATE INDEX idx_health_check_status_time 
    ON health_check_records(data_source_id, status, check_time DESC);  -- 查詢故障歷史
```

---

### 狀態欄位規範化設計

**問題**: VARCHAR 允許任意值，導致資料不一致和查詢低效

**最佳實踐**:
```sql
-- ✅ 使用 ENUM 型別強制一致性
CREATE TYPE health_status AS ENUM ('success', 'warning', 'error', 'timeout');

CREATE TABLE health_check_records (
    status health_status NOT NULL
);

-- 效能對比
-- VARCHAR(20): 存儲 3-20 字節，無驗證
-- ENUM:        固定 4 字節，編譯時驗證，查詢更快

-- 應用層驗證示例
def insert_health_check(data_source_id, status):
    valid_statuses = ['success', 'warning', 'error', 'timeout']
    if status not in valid_statuses:
        raise ValueError(f"Invalid status: {status}")
    # ... insert to DB
```

**應用場景**:
- 所有狀態欄位：execution_status, task_status, alert_severity, alert_status
- 條件欄位：alert_condition ('gt', 'gte', 'lt', 'lte', 'eq', 'ne')

---

### 告警狀態追蹤設計

**問題**: 缺少完整的告警生命週期記錄

**最佳實踐**:
```sql
-- ✅ 完整的生命週期時間戳
CREATE TYPE alert_status AS ENUM ('triggered', 'acknowledged', 'resolved', 'closed');

CREATE TABLE alerts (
    -- 生命週期狀態
    status alert_status NOT NULL DEFAULT 'triggered',
    
    -- 時間戳完整追蹤
    triggered_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),    -- 告警觸發
    acknowledged_at TIMESTAMPTZ,                        -- 人工確認
    resolved_at TIMESTAMPTZ,                            -- 問題解決
    closed_at TIMESTAMPTZ,                              -- 告警關閉
    
    -- 人工干預追蹤
    assigned_to UUID,
    notes TEXT
);

-- 告警生命週期查詢
SELECT 
    id,
    alert_type,
    EXTRACT(EPOCH FROM (triggered_at - NOW()))/60 as minutes_since_triggered,
    CASE 
        WHEN status = 'triggered' THEN '未確認'
        WHEN acknowledged_at IS NOT NULL AND resolved_at IS NULL THEN '已確認,待解決'
        WHEN resolved_at IS NOT NULL AND closed_at IS NULL THEN '已解決,待關閉'
        ELSE '已關閉'
    END as lifecycle_stage,
    EXTRACT(EPOCH FROM COALESCE(closed_at, NOW()) - triggered_at)/60 as total_lifetime_minutes
FROM alerts
ORDER BY triggered_at DESC;

-- 告警響應時間統計
SELECT 
    alert_type,
    COUNT(*) as total_alerts,
    AVG(EXTRACT(EPOCH FROM (acknowledged_at - triggered_at))/60) as avg_ack_time_minutes,
    AVG(EXTRACT(EPOCH FROM (resolved_at - triggered_at))/3600) as avg_resolve_time_hours
FROM alerts
WHERE triggered_at > NOW() - INTERVAL '30 days'
GROUP BY alert_type;
```

**應用場景**:
- CH3 (DSHM): 完整的告警管理流程
- CH8 (Cluster): 任務失敗告警追蹤
- CH9 (Deployment): 部署失敗告警處理

---

### 嚴重性分級標準化設計

**問題**: 不同系統使用不同的嚴重性定義（4 級、5 級、10 級混亂）

**最佳實踐**:
```sql
-- ✅ 統一的嚴重性分級
CREATE TYPE alert_severity AS ENUM ('info', 'warning', 'critical');

-- 全局嚴重性定義表（支援跨系統一致性）
CREATE TABLE severity_levels (
    level severity_enum PRIMARY KEY,
    numeric_value INT NOT NULL,  -- info=1, warning=2, critical=3
    description TEXT,
    sla_response_minutes INT,
    escalation_enabled BOOLEAN
);

INSERT INTO severity_levels VALUES
    ('info', 1, '信息性消息', NULL, FALSE),
    ('warning', 2, '需要關注但不影響服務', 60, TRUE),
    ('critical', 3, '影響生產服務', 15, TRUE);

-- 應用層對應
SEVERITY_MAP = {
    'info': 1,
    'warning': 2,
    'critical': 3
}
```

---

### 外鍵約束強化設計

**問題**: 允許孤立資料，導致資料完整性問題

**最佳實踐**:
```sql
-- ✅ 完整的外鍵約束與級聯操作
CONSTRAINT fk_alert_datasource 
    FOREIGN KEY (data_source_id) 
    REFERENCES data_sources(id) 
    ON DELETE CASCADE      -- 刪除源時自動刪除相關告警
    ON UPDATE CASCADE      -- 更新源ID時自動更新告警

-- 避免孤立資料查詢
SELECT 
    a.id, a.data_source_id
FROM alerts a
WHERE NOT EXISTS (
    SELECT 1 FROM data_sources ds WHERE ds.id = a.data_source_id
);

-- 定期清理孤立資料（備用）
DELETE FROM alerts 
WHERE data_source_id NOT IN (SELECT id FROM data_sources);
```

---

### 複合索引策略設計

**問題**: 單欄索引無法優化常見的多條件查詢

**最佳實踐**:
```sql
-- ✅ 根據查詢模式設計複合索引

-- 查詢模式 1: 查詢特定源的最新健康檢測
-- SELECT * FROM health_check_records 
-- WHERE data_source_id = ? ORDER BY check_time DESC LIMIT 1
CREATE INDEX idx_health_check_datasource_time 
    ON health_check_records(data_source_id, check_time DESC);

-- 查詢模式 2: 查詢某源某時間範圍內的錯誤檢測
-- SELECT * FROM health_check_records 
-- WHERE data_source_id = ? AND status = 'error' AND check_time > ?
CREATE INDEX idx_health_check_status_time 
    ON health_check_records(data_source_id, status, check_time DESC);

-- 查詢模式 3: 審計日志查詢
-- SELECT * FROM alerts 
-- WHERE severity = 'critical' ORDER BY triggered_at DESC
CREATE INDEX idx_alert_severity_triggered 
    ON alerts(severity, triggered_at DESC);

-- 索引使用情況監控
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as total_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_returned
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

---

### UUID vs BIGSERIAL 選擇設計

**問題**: 分散式系統需要 UUID，但某些查詢場景需要序列值

**最佳實踐**:
```sql
-- ✅ 混合策略：主鍵用 UUID，高頻查詢欄位用序列
CREATE TABLE health_check_records (
    -- 主鍵用 UUID（分散式友善）
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- 內部序列用於高效分頁查詢
    seq_id BIGSERIAL UNIQUE,
    
    data_source_id UUID NOT NULL,
    check_time TIMESTAMPTZ NOT NULL,
    -- ... other fields
);

-- 高效的分頁查詢（基於 seq_id）
SELECT * FROM health_check_records
WHERE seq_id > last_seq_id
ORDER BY seq_id
LIMIT 100;

-- 優勢對比
-- UUID:       16 字節，分散式原生支援，但分頁查詢較慢
-- BIGSERIAL:  8 字節，本地分頁最快，但分散式需要協調
-- 混合策略:   兩者結合，兼得之利
```

---

### 結構化錯誤訊息設計

**問題**: 非結構化的 error_message 難以程式化處理

**最佳實踐**:
```sql
-- ✅ 分離錯誤代碼和詳情
error_code VARCHAR(20) COMMENT '標準化錯誤代碼（如：CONNECTION_TIMEOUT）',
error_detail TEXT COMMENT '詳細錯誤信息'

-- 全局錯誤代碼定義
CREATE TABLE error_codes (
    code VARCHAR(20) PRIMARY KEY,
    description TEXT,
    category VARCHAR(50),  -- network, timeout, auth, etc
    is_retryable BOOLEAN,
    severity alert_severity
);

INSERT INTO error_codes VALUES
    ('CONNECTION_TIMEOUT', '連接超時', 'network', TRUE, 'warning'),
    ('DNS_FAIL', 'DNS 解析失敗', 'network', TRUE, 'warning'),
    ('SSL_CERT_INVALID', 'SSL 證書無效', 'security', FALSE, 'critical'),
    ('AUTH_FAILED', '認證失敗', 'auth', FALSE, 'warning');

-- 應用層使用
def handle_error(error_code: str):
    error_def = ERROR_CODES.get(error_code)
    if error_def and error_def['is_retryable']:
        retry_with_backoff()
    if error_def and error_def['severity'] == 'critical':
        trigger_alert()
```

---

### 分區策略設計

**問題**: 時序資料無限增長，查詢性能下降

**最佳實踐**:
```sql
-- ✅ 按時間分區（時序資料最佳實踐）
CREATE TABLE health_check_records (
    id UUID,
    data_source_id UUID,
    check_time TIMESTAMPTZ,
    -- ... other fields
) PARTITION BY RANGE (check_time);

-- 按月分區
CREATE TABLE health_check_records_2024_10 PARTITION OF health_check_records
    FOR VALUES FROM ('2024-10-01') TO ('2024-11-01');

CREATE TABLE health_check_records_2024_11 PARTITION OF health_check_records
    FOR VALUES FROM ('2024-11-01') TO ('2024-12-01');

-- 自動化分區維護
-- 創建新月份分區（每月執行一次）
CREATE TABLE health_check_records_2024_12 PARTITION OF health_check_records
    FOR VALUES FROM ('2024-12-01') TO ('2025-01-01');

-- 分區的效能優勢
-- 1. 查詢只掃描相關分區（顯著加快查詢）
-- 2. 刪除舊資料時直接 DROP 分區（比 DELETE 快 1000 倍）
-- 3. 索引維護更有效率

-- 查詢性能對比
-- SELECT AVG(response_time) FROM health_check_records 
-- WHERE check_time > NOW() - INTERVAL '7 days'
-- 分區表: 只掃描 7 個分區，比無分區快 10-100 倍
```

---

## 📊 設計決策矩陣

| 設計決策 | 問題 | 推薦方案 | 適用場景 |
|---------|------|---------|---------|
| 時間單位 | 模糊性 | 在註釋中明確標註（ms/s/μs） | 所有性能指標 |
| 時間戳 | 區分不清 | 分離 check_time 和 created_at | 所有時序表 |
| 狀態欄位 | 不一致 | 使用 ENUM 類型 | 所有狀態欄位 |
| 告警生命週期 | 不完整 | 記錄 4 個時間戳 | 告警管理表 |
| 嚴重性分級 | 混亂 | 建立全局定義表 | 所有告警系統 |
| 外鍵約束 | 孤立資料 | 加上級聯刪除/更新 | 所有從表 |
| 索引 | 查詢慢 | 根據查詢模式設計複合索引 | 高頻查詢表 |
| 主鍵 | 分散式 | UUID 主鍵 + BIGSERIAL 序列 | 高可用系統 |
| 錯誤訊息 | 難以程式化 | 分離 error_code 和 error_detail | 所有錯誤處理 |
| 時序資料 | 性能下降 | 按月分區 | 監控/審計表 |
