# CH7 代碼示例 - 7.5 數據庫架構定義

```sql
-- 合規性檢查記錄
CREATE TABLE IF NOT EXISTS compliance_records (
    record_id VARCHAR(36) PRIMARY KEY,
    data_source_id VARCHAR(36),
    check_results JSONB,
    passed BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 加密密鑰表
CREATE TABLE IF NOT EXISTS encryption_keys (
    key_id VARCHAR(36) PRIMARY KEY,
    key_type VARCHAR(50),
    encrypted_key TEXT,
    algorithm VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_at TIMESTAMP
);

-- 審計日志
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id VARCHAR(36) PRIMARY KEY,
    operator_id VARCHAR(36),
    action VARCHAR(100),
    resource_id VARCHAR(36),
    changes JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_compliance_passed ON compliance_records(passed);
CREATE INDEX idx_encryption_keys_expiry ON encryption_keys(expiry_at);
CREATE INDEX idx_audit_logs_operator ON audit_logs(operator_id);
```

---

## 相關文件引用

- **核心實現**: [代碼示例 - 合規引擎](ch7-code-01-compliance-engine.md)
- **API 示例**: [代碼示例 - API 端點](ch7-code-03-api-examples.md)
