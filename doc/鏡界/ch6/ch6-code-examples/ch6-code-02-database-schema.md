# CH6 代碼示例 - 6.5 數據庫架構定義

## 核心表結構

```sql
-- AI 對話表
CREATE TABLE IF NOT EXISTS ai_conversations (
    conversation_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    title VARCHAR(255),
    status VARCHAR(20),
    messages JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 生成的代碼表
CREATE TABLE IF NOT EXISTS generated_code (
    code_id VARCHAR(36) PRIMARY KEY,
    code_type VARCHAR(50),
    content TEXT,
    metadata JSONB,
    quality_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 知識文章表
CREATE TABLE IF NOT EXISTS knowledge_articles (
    article_id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    category VARCHAR(100),
    tags VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_conversations_user_id ON ai_conversations(user_id);
CREATE INDEX idx_generated_code_type ON generated_code(code_type);
CREATE INDEX idx_knowledge_articles_category ON knowledge_articles(category);
```

---

## 相關文件引用

- **核心實現**: [代碼示例 - LLM 集成](ch6-code-01-llm-integration.md)
- **API 示例**: [代碼示例 - API 端點](ch6-code-03-api-examples.md)
