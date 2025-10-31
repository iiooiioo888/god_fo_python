# CH1 代碼示例 - 1.5 數據庫架構定義

## 數據庫設計概述

資料源註冊中心採用 PostgreSQL 作為主要存儲引擎，支持完整的 ACID 事務、豐富的數據類型和高性能索引。

---

## 核心表定義

### 1. data_sources - 資料源主表

```sql
-- 創建 data_sources 表
CREATE TABLE IF NOT EXISTS data_sources (
    id VARCHAR(36) PRIMARY KEY,
    project_id VARCHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    display_name VARCHAR(255),
    description TEXT,
    url VARCHAR(2048) NOT NULL,
    type VARCHAR(50) NOT NULL,  -- postgresql, mysql, mongodb, api, s3, etc.
    status VARCHAR(20) NOT NULL DEFAULT 'active',  -- active, inactive, archived, deleted
    
    -- 分類和標籤
    category VARCHAR(100),
    tags JSONB DEFAULT '[]'::jsonb,
    
    -- 元數據
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- 連接配置（加密存儲）
    connection_config JSONB,
    
    -- 版本控制
    version_id VARCHAR(36),
    current_version INTEGER DEFAULT 1,
    
    -- 健康狀態
    health_status VARCHAR(20) DEFAULT 'unknown',  -- healthy, warning, error, unknown
    quality_score DECIMAL(5,2) DEFAULT 0,
    last_health_check TIMESTAMP,
    
    -- 審計字段
    owner_id VARCHAR(36) NOT NULL,
    created_by VARCHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(36),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    
    -- 統計信息
    access_count INTEGER DEFAULT 0,
    last_accessed_at TIMESTAMP,
    
    CONSTRAINT fk_project_id FOREIGN KEY (project_id) REFERENCES projects(id),
    CONSTRAINT check_valid_type CHECK (type IN (
        'postgresql', 'mysql', 'mongodb', 'elasticsearch', 
        'api', 'http', 'ftp', 's3', 'azure_blob', 'gcs'
    )),
    CONSTRAINT check_valid_status CHECK (status IN (
        'active', 'inactive', 'archived', 'deleted'
    ))
);

-- 創建索引
CREATE INDEX idx_data_sources_project_id ON data_sources(project_id);
CREATE INDEX idx_data_sources_owner_id ON data_sources(owner_id);
CREATE INDEX idx_data_sources_type ON data_sources(type);
CREATE INDEX idx_data_sources_category ON data_sources(category);
CREATE INDEX idx_data_sources_status ON data_sources(status);
CREATE INDEX idx_data_sources_created_at ON data_sources(created_at);
CREATE INDEX idx_data_sources_updated_at ON data_sources(updated_at);

-- JSONB 索引用於標籤搜尋
CREATE INDEX idx_data_sources_tags ON data_sources USING GIN (tags);

-- 全文搜尋索引
CREATE INDEX idx_data_sources_name_tsvector ON data_sources 
    USING GIN (to_tsvector('chinese', name));
CREATE INDEX idx_data_sources_description_tsvector ON data_sources 
    USING GIN (to_tsvector('chinese', description));
```

### 2. data_source_versions - 版本歷史表

```sql
CREATE TABLE IF NOT EXISTS data_source_versions (
    version_id VARCHAR(36) PRIMARY KEY,
    data_source_id VARCHAR(36) NOT NULL,
    previous_version_id VARCHAR(36),
    
    -- 版本號
    version_number INTEGER NOT NULL,
    version_name VARCHAR(100),
    
    -- 變更信息
    changes JSONB NOT NULL,  -- 存儲前後對比
    change_summary TEXT,
    change_type VARCHAR(50) NOT NULL,  -- create, update, delete, archive
    
    -- 審批信息
    approval_status VARCHAR(20) DEFAULT 'pending',  -- pending, approved, rejected
    approved_by VARCHAR(36),
    approval_comment TEXT,
    
    -- 回滾信息
    can_rollback BOOLEAN DEFAULT TRUE,
    rollback_enabled_until TIMESTAMP,
    
    -- 審計
    created_by VARCHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_data_source_id FOREIGN KEY (data_source_id) 
        REFERENCES data_sources(id),
    CONSTRAINT fk_previous_version FOREIGN KEY (previous_version_id) 
        REFERENCES data_source_versions(version_id)
);

CREATE INDEX idx_versions_data_source_id ON data_source_versions(data_source_id);
CREATE INDEX idx_versions_created_at ON data_source_versions(created_at);
CREATE INDEX idx_versions_approval_status ON data_source_versions(approval_status);
```

### 3. data_source_categories - 分類表

```sql
CREATE TABLE IF NOT EXISTS data_source_categories (
    category_id VARCHAR(36) PRIMARY KEY,
    project_id VARCHAR(36) NOT NULL,
    
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    
    -- 分類層級
    parent_category_id VARCHAR(36),
    level INTEGER DEFAULT 0,
    sort_order INTEGER DEFAULT 0,
    
    -- 統計
    datasource_count INTEGER DEFAULT 0,
    
    -- 審計
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_project_id FOREIGN KEY (project_id) REFERENCES projects(id),
    CONSTRAINT fk_parent_category FOREIGN KEY (parent_category_id) 
        REFERENCES data_source_categories(category_id),
    UNIQUE(project_id, name, parent_category_id)
);

CREATE INDEX idx_categories_project_id ON data_source_categories(project_id);
CREATE INDEX idx_categories_parent_id ON data_source_categories(parent_category_id);
```

### 4. data_source_permissions - 權限管理表

```sql
CREATE TABLE IF NOT EXISTS data_source_permissions (
    permission_id VARCHAR(36) PRIMARY KEY,
    data_source_id VARCHAR(36) NOT NULL,
    
    -- 被授予者
    grantee_type VARCHAR(20) NOT NULL,  -- user, team, role, project
    grantee_id VARCHAR(36) NOT NULL,
    
    -- 權限級別
    access_level VARCHAR(20) NOT NULL,  -- read, read_write, admin
    
    -- 時間限制
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    
    -- 授權信息
    granted_by VARCHAR(36) NOT NULL,
    revoked_at TIMESTAMP,
    revocation_reason TEXT,
    
    CONSTRAINT fk_data_source_id FOREIGN KEY (data_source_id) 
        REFERENCES data_sources(id),
    UNIQUE(data_source_id, grantee_type, grantee_id)
);

CREATE INDEX idx_permissions_data_source_id ON data_source_permissions(data_source_id);
CREATE INDEX idx_permissions_grantee ON data_source_permissions(grantee_type, grantee_id);
CREATE INDEX idx_permissions_expires_at ON data_source_permissions(expires_at);
```

### 5. data_source_health - 健康監控表

```sql
CREATE TABLE IF NOT EXISTS data_source_health (
    health_id VARCHAR(36) PRIMARY KEY,
    data_source_id VARCHAR(36) NOT NULL,
    
    -- 健康指標
    status VARCHAR(20) NOT NULL,  -- healthy, warning, error, unknown
    availability_rate DECIMAL(5,2),  -- 可用率百分比
    response_time_ms INTEGER,
    error_rate DECIMAL(5,2),  -- 錯誤率百分比
    
    -- 質量評分
    quality_score DECIMAL(5,2),
    completeness_score DECIMAL(5,2),
    freshness_score DECIMAL(5,2),
    accuracy_score DECIMAL(5,2),
    
    -- 檢測詳情
    check_details JSONB DEFAULT '{}'::jsonb,
    error_messages TEXT,
    
    -- 時間戳
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_data_source_id FOREIGN KEY (data_source_id) 
        REFERENCES data_sources(id),
    CONSTRAINT check_valid_status CHECK (status IN (
        'healthy', 'warning', 'error', 'unknown'
    ))
);

CREATE INDEX idx_health_data_source_id ON data_source_health(data_source_id);
CREATE INDEX idx_health_checked_at ON data_source_health(checked_at);
CREATE INDEX idx_health_status ON data_source_health(status);

-- 分區表（按日期，用於大規模時序數據）
CREATE TABLE data_source_health_2024_10 PARTITION OF data_source_health
    FOR VALUES FROM ('2024-10-01') TO ('2024-11-01');
```

### 6. data_source_access_log - 訪問日志表

```sql
CREATE TABLE IF NOT EXISTS data_source_access_log (
    log_id VARCHAR(36) PRIMARY KEY,
    data_source_id VARCHAR(36) NOT NULL,
    
    -- 訪問者信息
    user_id VARCHAR(36) NOT NULL,
    project_id VARCHAR(36),
    
    -- 操作信息
    operation VARCHAR(50) NOT NULL,  -- read, write, delete, export
    access_type VARCHAR(50),  -- api, ui, sdk
    
    -- 結果
    status VARCHAR(20),  -- success, failure
    error_message TEXT,
    
    -- 性能指標
    duration_ms INTEGER,
    data_size_bytes BIGINT,
    
    -- 時間戳
    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_data_source_id FOREIGN KEY (data_source_id) 
        REFERENCES data_sources(id)
);

CREATE INDEX idx_access_log_data_source_id ON data_source_access_log(data_source_id);
CREATE INDEX idx_access_log_user_id ON data_source_access_log(user_id);
CREATE INDEX idx_access_log_accessed_at ON data_source_access_log(accessed_at);
CREATE INDEX idx_access_log_operation ON data_source_access_log(operation);
```

### 7. data_source_tags - 標籤管理表

```sql
CREATE TABLE IF NOT EXISTS data_source_tags (
    tag_id VARCHAR(36) PRIMARY KEY,
    project_id VARCHAR(36) NOT NULL,
    
    tag_name VARCHAR(100) NOT NULL,
    tag_type VARCHAR(50),  -- system, custom, business, technical
    color VARCHAR(7),  -- 十六進制顏色代碼
    
    -- 統計
    usage_count INTEGER DEFAULT 0,
    
    -- 審計
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_project_id FOREIGN KEY (project_id) REFERENCES projects(id),
    UNIQUE(project_id, tag_name)
);

CREATE INDEX idx_tags_project_id ON data_source_tags(project_id);
```

### 8. data_source_dependencies - 依賴關係表

```sql
CREATE TABLE IF NOT EXISTS data_source_dependencies (
    dependency_id VARCHAR(36) PRIMARY KEY,
    
    source_id VARCHAR(36) NOT NULL,      -- 被依賴的資料源
    dependent_id VARCHAR(36) NOT NULL,   -- 依賴的資料源
    
    dependency_type VARCHAR(50) NOT NULL,  -- direct, indirect, manual
    strength VARCHAR(20),  -- critical, high, medium, low
    
    -- 發現方式
    discovered_by VARCHAR(50),  -- manual, auto_analysis, workflow
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_source_id FOREIGN KEY (source_id) 
        REFERENCES data_sources(id),
    CONSTRAINT fk_dependent_id FOREIGN KEY (dependent_id) 
        REFERENCES data_sources(id),
    CONSTRAINT check_no_self_dependency CHECK (source_id != dependent_id),
    UNIQUE(source_id, dependent_id)
);

CREATE INDEX idx_dependencies_source_id ON data_source_dependencies(source_id);
CREATE INDEX idx_dependencies_dependent_id ON data_source_dependencies(dependent_id);
```

---

## 視圖定義

### 資料源概覽視圖

```sql
CREATE OR REPLACE VIEW v_datasource_overview AS
SELECT 
    ds.id,
    ds.name,
    ds.type,
    ds.category,
    ds.status,
    ds.owner_id,
    ds.created_at,
    ds.updated_at,
    ds.access_count,
    ds.quality_score,
    dsh.status as health_status,
    dsh.availability_rate,
    COUNT(DISTINCT dsp.permission_id) as permission_count,
    ARRAY_AGG(DISTINCT dh.tag_name) as tags
FROM data_sources ds
LEFT JOIN data_source_health dsh ON ds.id = dsh.data_source_id
LEFT JOIN data_source_permissions dsp ON ds.id = dsp.data_source_id
LEFT JOIN data_source_tags dh ON ds.tags::text LIKE CONCAT('%', dh.tag_name, '%')
WHERE ds.status != 'deleted'
GROUP BY ds.id, dsh.id;
```

### 權限聚合視圖

```sql
CREATE OR REPLACE VIEW v_datasource_permissions_summary AS
SELECT 
    ds.id,
    ds.name,
    COUNT(CASE WHEN dsp.access_level = 'read' THEN 1 END) as read_access_count,
    COUNT(CASE WHEN dsp.access_level = 'read_write' THEN 1 END) as write_access_count,
    COUNT(CASE WHEN dsp.access_level = 'admin' THEN 1 END) as admin_access_count,
    ARRAY_AGG(DISTINCT dsp.grantee_id) FILTER (WHERE dsp.revoked_at IS NULL) as active_grantees
FROM data_sources ds
LEFT JOIN data_source_permissions dsp ON ds.id = dsp.data_source_id
GROUP BY ds.id;
```

---

## 觸發器和存儲過程

### 自動更新 updated_at 觸發器

```sql
CREATE OR REPLACE FUNCTION update_updated_at_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_datasources_update_timestamp
BEFORE UPDATE ON data_sources
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_timestamp();

CREATE TRIGGER tr_categories_update_timestamp
BEFORE UPDATE ON data_source_categories
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_timestamp();
```

### 記錄變更歷史觸發器

```sql
CREATE OR REPLACE FUNCTION log_datasource_changes()
RETURNS TRIGGER AS $$
DECLARE
    v_changes JSONB;
BEGIN
    IF TG_OP = 'UPDATE' THEN
        v_changes := jsonb_object_agg(
            key,
            json_build_object('old', OLD.*, 'new', NEW.*)
        ) FROM jsonb_object_keys(to_jsonb(NEW)) AS key;
    ELSIF TG_OP = 'DELETE' THEN
        v_changes := to_jsonb(OLD);
    ELSE
        v_changes := to_jsonb(NEW);
    END IF;
    
    INSERT INTO data_source_versions (
        version_id, data_source_id, changes, 
        change_type, created_by, created_at
    )
    VALUES (
        gen_random_uuid()::text,
        NEW.id,
        v_changes,
        TG_OP::text,
        COALESCE(NEW.updated_by, NEW.created_by),
        CURRENT_TIMESTAMP
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_datasource_audit_log
AFTER INSERT OR UPDATE OR DELETE ON data_sources
FOR EACH ROW
EXECUTE FUNCTION log_datasource_changes();
```

---

## 相關文件引用

- **主文檔**: [1.5 數據模型詳細定義](../ch1-5-數據模型詳細定義.md)
- **核心組件**: [代碼示例 - 核心功能](ch1-code-01-core-functions.md)
- **搜尋服務**: [代碼示例 - 搜尋服務](ch1-code-02-search-service.md)
- **API 示例**: [代碼示例 - API 端點](ch1-code-04-api-examples.md)
