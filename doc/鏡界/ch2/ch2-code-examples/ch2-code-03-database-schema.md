# CH2 代碼示例 - 2.5 數據庫架構定義

## 核心表結構

### 1. website_fingerprints - 網站指紋主表

```sql
CREATE TABLE IF NOT EXISTS website_fingerprints (
    fingerprint_id VARCHAR(36) PRIMARY KEY,
    domain VARCHAR(255) NOT NULL,
    url VARCHAR(2048) NOT NULL,
    
    -- 技術棧信息
    tech_stack JSONB NOT NULL DEFAULT '{}',
    
    -- 反爬機制
    anticrawl_mechanisms JSONB DEFAULT '[]',
    anticrawl_level INTEGER DEFAULT 0,
    
    -- 指紋特徵
    fingerprint_signature VARCHAR(256) NOT NULL,
    content_features JSONB DEFAULT '{}',
    
    -- 質量評分
    confidence_score DECIMAL(5,2) DEFAULT 0,
    quality_status VARCHAR(20) DEFAULT 'pending',
    
    -- 爬蟲建議
    crawler_recommendations JSONB DEFAULT '[]',
    
    -- 審計字段
    created_by VARCHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_analyzed_at TIMESTAMP,
    
    -- 統計
    analysis_count INTEGER DEFAULT 0,
    false_positive_count INTEGER DEFAULT 0,
    false_negative_count INTEGER DEFAULT 0
);

CREATE INDEX idx_fp_domain ON website_fingerprints(domain);
CREATE INDEX idx_fp_signature ON website_fingerprints(fingerprint_signature);
CREATE INDEX idx_fp_confidence ON website_fingerprints(confidence_score);
CREATE INDEX idx_fp_anticrawl_level ON website_fingerprints(anticrawl_level);
CREATE INDEX idx_fp_created_at ON website_fingerprints(created_at);
```

### 2. fingerprint_tech_stack - 技術棧明細表

```sql
CREATE TABLE IF NOT EXISTS fingerprint_tech_stack (
    tech_stack_id VARCHAR(36) PRIMARY KEY,
    fingerprint_id VARCHAR(36) NOT NULL,
    
    tech_type VARCHAR(50) NOT NULL,  -- server, language, framework, cms, cdn
    tech_name VARCHAR(100) NOT NULL,
    tech_version VARCHAR(50),
    confidence DECIMAL(3,2) DEFAULT 0.9,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_fingerprint FOREIGN KEY (fingerprint_id) 
        REFERENCES website_fingerprints(fingerprint_id),
    CONSTRAINT check_valid_type CHECK (tech_type IN (
        'server', 'language', 'framework', 'cms', 'database', 'cdn', 'analytics'
    ))
);

CREATE INDEX idx_ts_fingerprint_id ON fingerprint_tech_stack(fingerprint_id);
CREATE INDEX idx_ts_tech_type ON fingerprint_tech_stack(tech_type);
CREATE INDEX idx_ts_tech_name ON fingerprint_tech_stack(tech_name);
```

### 3. anticrawl_mechanisms - 反爬機制詳情表

```sql
CREATE TABLE IF NOT EXISTS anticrawl_mechanisms (
    mechanism_id VARCHAR(36) PRIMARY KEY,
    fingerprint_id VARCHAR(36) NOT NULL,
    
    mechanism_type VARCHAR(50) NOT NULL,  -- js_challenge, captcha, rate_limit 等
    severity_level INTEGER DEFAULT 1,  -- 1-4, 越高越嚴格
    
    detection_method VARCHAR(100),
    evasion_strategies JSONB DEFAULT '[]',
    
    last_detected_at TIMESTAMP,
    
    CONSTRAINT fk_fingerprint FOREIGN KEY (fingerprint_id)
        REFERENCES website_fingerprints(fingerprint_id)
);

CREATE INDEX idx_acm_fingerprint_id ON anticrawl_mechanisms(fingerprint_id);
CREATE INDEX idx_acm_mechanism_type ON anticrawl_mechanisms(mechanism_type);
```

### 4. crawler_configurations - 爬蟲配置建議表

```sql
CREATE TABLE IF NOT EXISTS crawler_configurations (
    config_id VARCHAR(36) PRIMARY KEY,
    fingerprint_id VARCHAR(36) NOT NULL,
    
    config_type VARCHAR(50) NOT NULL,  -- headers, delays, strategy
    config_data JSONB NOT NULL,
    
    priority VARCHAR(20) DEFAULT 'medium',  -- critical, high, medium, low
    success_rate DECIMAL(5,2) DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_fingerprint FOREIGN KEY (fingerprint_id)
        REFERENCES website_fingerprints(fingerprint_id)
);

CREATE INDEX idx_cc_fingerprint_id ON crawler_configurations(fingerprint_id);
```

### 5. website_changes - 網站變更監測表

```sql
CREATE TABLE IF NOT EXISTS website_changes (
    change_id VARCHAR(36) PRIMARY KEY,
    fingerprint_id VARCHAR(36) NOT NULL,
    
    change_type VARCHAR(50) NOT NULL,  -- tech_stack_change, anticrawl_update
    previous_state JSONB,
    current_state JSONB,
    
    severity VARCHAR(20) DEFAULT 'medium',
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notified_at TIMESTAMP,
    
    CONSTRAINT fk_fingerprint FOREIGN KEY (fingerprint_id)
        REFERENCES website_fingerprints(fingerprint_id)
);

CREATE INDEX idx_wc_fingerprint_id ON website_changes(fingerprint_id);
CREATE INDEX idx_wc_detected_at ON website_changes(detected_at);
```

---

## 相關文件引用

- **核心功能**: [代碼示例 - 核心實現](ch2-code-01-core-fingerprint.md)
- **搜尋服務**: [代碼示例 - 匹配和搜尋](ch2-code-02-fingerprint-matching.md)
- **API 示例**: [代碼示例 - API 端點](ch2-code-04-api-examples.md)
