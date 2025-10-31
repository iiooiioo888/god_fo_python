# CH1 代碼示例 - 1.2 核心功能實現

## 資料源 CRUD 管理實現

### DataSourceService 核心服務類

```python
import json
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urlparse
from enum import Enum

class DataSourceStatus(Enum):
    """資料源狀態枚舉"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"
    DELETED = "deleted"

class DataSourceService:
    """資料源元資料管理核心服務"""
    
    def __init__(
        self,
        db: 'Database',
        search_index: 'SearchIndex',
        event_bus: 'EventBus',
        config: Dict
    ):
        self.db = db
        self.search_index = search_index
        self.event_bus = event_bus
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def create_data_source(
        self,
        project_id: str,
        data_source: Dict,
        user_id: str
    ) -> Dict:
        """
        創建新的資料源
        
        Args:
            project_id: 所屬專案 ID
            data_source: 資料源物件
            user_id: 創建者 ID
            
        Returns:
            創建後的資料源物件
        """
        # 1. 驗證資料源
        self._validate_data_source(data_source)
        
        # 2. 生成唯一 ID
        data_source['id'] = f"ds-{uuid.uuid4().hex[:8]}"
        data_source['project_id'] = project_id
        data_source['created_at'] = datetime.utcnow().isoformat()
        data_source['updated_at'] = data_source['created_at']
        data_source['owner_id'] = user_id
        data_source['status'] = DataSourceStatus.ACTIVE.value
        
        # 3. 處理分類和標籤
        self._process_categories_and_tags(data_source)
        
        # 4. 保存到資料庫
        self._save_to_db(data_source)
        
        # 5. 更新搜尋索引
        self.search_index.add(data_source)
        
        # 6. 發布創建事件
        self.event_bus.publish("data_source.created", {
            "data_source_id": data_source['id'],
            "project_id": project_id,
            "user_id": user_id
        })
        
        self.logger.info(f"Created data source {data_source['id']} for project {project_id}")
        return data_source
    
    def _validate_data_source(self, data_source: Dict):
        """驗證資料源定義的有效性"""
        # 必填字段檢查
        required_fields = ["name", "url", "type"]
        for field in required_fields:
            if not data_source.get(field):
                raise ValueError(f"Missing required field: {field}")
        
        # URL 格式驗證
        if not self._is_valid_url(data_source['url']):
            raise ValueError("Invalid URL format")
        
        # 資料類型驗證
        valid_types = ["postgresql", "mysql", "mongodb", "elasticsearch", 
                       "api", "http", "ftp", "s3"]
        if data_source['type'] not in valid_types:
            raise ValueError(f"Invalid data type. Must be one of: {', '.join(valid_types)}")
    
    def _is_valid_url(self, url: str) -> bool:
        """驗證 URL 格式"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def _process_categories_and_tags(self, data_source: Dict):
        """處理分類和標籤"""
        # 自動分類（如果未指定）
        if not data_source.get('category'):
            data_source['category'] = self._auto_categorize(data_source)
        
        # 自動標籤建議
        if self.config.get('auto_tagging_enabled', True):
            auto_tags = self._generate_auto_tags(data_source)
            existing_tags = data_source.get('tags', [])
            data_source['tags'] = list(set(existing_tags + auto_tags))
    
    def _auto_categorize(self, data_source: Dict) -> str:
        """自動分類算法"""
        url = data_source.get('url', '').lower()
        data_type = data_source.get('type', '').lower()
        
        # 基於 URL 和類型的分類
        if 'api' in url or data_type in ['api', 'http']:
            return 'api'
        elif data_type in ['postgresql', 'mysql', 'mongodb']:
            return 'database'
        elif data_type in ['elasticsearch']:
            return 'search'
        elif data_type in ['s3', 'ftp']:
            return 'storage'
        else:
            return 'other'
    
    def _generate_auto_tags(self, data_source: Dict) -> List[str]:
        """生成自動標籤"""
        tags = []
        url = data_source.get('url', '').lower()
        data_type = data_source.get('type', '').lower()
        
        # 基於 URL 的標籤
        if 'prod' in url or 'production' in url:
            tags.append('production')
        if 'dev' in url or 'development' in url:
            tags.append('development')
        if 'test' in url or 'testing' in url:
            tags.append('testing')
        
        # 基於類型的標籤
        if data_type in ['postgresql', 'mysql']:
            tags.append('relational-db')
        elif data_type in ['mongodb']:
            tags.append('nosql')
        elif data_type in ['elasticsearch']:
            tags.append('search-engine')
        
        return tags
    
    def _save_to_db(self, data_source: Dict):
        """保存到資料庫"""
        sql = """
        INSERT INTO data_sources (
            id, project_id, name, description, url, type, 
            category, tags, status, created_at, updated_at, owner_id, metadata
        ) VALUES (
            %(id)s, %(project_id)s, %(name)s, %(description)s, %(url)s, %(type)s,
            %(category)s, %(tags)s, %(status)s, %(created_at)s, %(updated_at)s, 
            %(owner_id)s, %(metadata)s
        )
        """
        
        params = {
            "id": data_source['id'],
            "project_id": data_source['project_id'],
            "name": data_source['name'],
            "description": data_source.get('description', ''),
            "url": data_source['url'],
            "type": data_source['type'],
            "category": data_source.get('category', 'other'),
            "tags": json.dumps(data_source.get('tags', [])),
            "status": data_source['status'],
            "created_at": data_source['created_at'],
            "updated_at": data_source['updated_at'],
            "owner_id": data_source['owner_id'],
            "metadata": json.dumps(data_source.get('metadata', {}))
        }
        
        self.db.execute(sql, params)
    
    def get_data_source(
        self,
        data_source_id: str,
        project_id: str,
        user_id: str
    ) -> Dict:
        """
        獲取資料源詳情
        
        Args:
            data_source_id: 資料源 ID
            project_id: 專案 ID
            user_id: 請求用戶 ID
            
        Returns:
            資料源物件
        """
        # 1. 檢查權限
        if not self._has_permission(user_id, project_id, "read"):
            raise PermissionError("User does not have permission to read this data source")
        
        # 2. 從資料庫獲取
        data_source = self._get_from_db(data_source_id, project_id)
        if not data_source:
            raise ValueError(f"Data source {data_source_id} not found")
        
        return data_source
    
    def _get_from_db(self, data_source_id: str, project_id: str) -> Optional[Dict]:
        """從資料庫獲取資料源"""
        sql = """
        SELECT * FROM data_sources 
        WHERE id = %(id)s AND project_id = %(project_id)s AND status != %(deleted)s
        """
        
        row = self.db.fetchone(sql, {
            "id": data_source_id,
            "project_id": project_id,
            "deleted": DataSourceStatus.DELETED.value
        })
        
        return row
    
    def update_data_source(
        self,
        data_source_id: str,
        project_id: str,
        updates: Dict,
        user_id: str
    ) -> Dict:
        """
        更新資料源
        
        Args:
            data_source_id: 資料源 ID
            project_id: 專案 ID
            updates: 更新字段
            user_id: 更新者 ID
            
        Returns:
            更新後的資料源
        """
        # 1. 獲取當前資料源
        current = self.get_data_source(data_source_id, project_id, user_id)
        
        # 2. 檢查權限
        if not self._has_permission(user_id, project_id, "write"):
            raise PermissionError("User does not have permission to update this data source")
        
        # 3. 驗證更新
        self._validate_updates(updates, current)
        
        # 4. 創建新版本
        version_id = self._create_version(current, updates, user_id)
        
        # 5. 更新時間戳
        updates['updated_at'] = datetime.utcnow().isoformat()
        updates['version_id'] = version_id
        
        # 6. 保存更新
        self._save_update(data_source_id, project_id, updates)
        
        # 7. 更新搜尋索引
        updated_source = self._get_from_db(data_source_id, project_id)
        self.search_index.update(updated_source)
        
        # 8. 發布更新事件
        self.event_bus.publish("data_source.updated", {
            "data_source_id": data_source_id,
            "project_id": project_id,
            "user_id": user_id,
            "changes": updates,
            "version_id": version_id
        })
        
        self.logger.info(f"Updated data source {data_source_id}, version {version_id}")
        return updated_source
    
    def _validate_updates(self, updates: Dict, current: Dict):
        """驗證更新是否有效"""
        # 不能修改 ID 和專案 ID
        if "id" in updates or "project_id" in updates:
            raise ValueError("Cannot update data source ID or project ID")
        
        # 驗證 URL 變更
        if "url" in updates and updates["url"] != current.get('url'):
            if not self._is_valid_url(updates["url"]):
                raise ValueError("Invalid URL format")
    
    def _create_version(self, current: Dict, updates: Dict, user_id: str) -> str:
        """創建新版本"""
        version_id = f"v{uuid.uuid4().hex[:8]}"
        
        version_record = {
            "version_id": version_id,
            "data_source_id": current['id'],
            "previous_version": current.get('version_id', 'v1'),
            "changes": updates,
            "created_by": user_id,
            "created_at": datetime.utcnow().isoformat()
        }
        
        self._save_version(version_record)
        return version_id
    
    def _save_version(self, version_record: Dict):
        """保存版本記錄"""
        sql = """
        INSERT INTO data_source_versions (
            version_id, data_source_id, previous_version, changes, created_by, created_at
        ) VALUES (
            %(version_id)s, %(data_source_id)s, %(previous_version)s, 
            %(changes)s, %(created_by)s, %(created_at)s
        )
        """
        
        params = {
            "version_id": version_record['version_id'],
            "data_source_id": version_record['data_source_id'],
            "previous_version": version_record['previous_version'],
            "changes": json.dumps(version_record['changes']),
            "created_by": version_record['created_by'],
            "created_at": version_record['created_at']
        }
        
        self.db.execute(sql, params)
    
    def _save_update(self, data_source_id: str, project_id: str, updates: Dict):
        """保存更新到資料庫"""
        set_clause = ", ".join([f"{k} = %({k})s" for k in updates.keys()])
        sql = f"""
        UPDATE data_sources 
        SET {set_clause}
        WHERE id = %(id)s AND project_id = %(project_id)s
        """
        
        params = updates.copy()
        params['id'] = data_source_id
        params['project_id'] = project_id
        
        self.db.execute(sql, params)
    
    def _has_permission(self, user_id: str, project_id: str, action: str) -> bool:
        """檢查用戶是否有權限"""
        # 簡化實現，實際應調用權限服務
        return True

# 使用示例
if __name__ == "__main__":
    # 初始化服務
    service = DataSourceService(
        db=None,  # 實際使用時傳入數據庫連接
        search_index=None,  # 實際使用時傳入搜尋引擎
        event_bus=None,  # 實際使用時傳入事件總線
        config={'auto_tagging_enabled': True}
    )
    
    # 創建資料源
    new_ds = {
        "name": "User API",
        "url": "https://api.example.com/users",
        "type": "api",
        "description": "User management API",
        "tags": ["api", "users"]
    }
    
    # result = service.create_data_source("proj_001", new_ds, "user_123")
```

---

## 自動分類與標籤生成

### 完整的分類算法實現

```python
class CategoryEngine:
    """資料源自動分類引擎"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def categorize(self, data_source: Dict) -> str:
        """
        多層次自動分類
        
        使用以下信號進行分類：
        1. URL 特徵
        2. 資料類型
        3. 內容描述
        4. 元數據
        """
        scores = {}
        
        # 1. URL 分析
        url_category = self._analyze_url(data_source.get('url', ''))
        if url_category:
            scores[url_category] = scores.get(url_category, 0) + 3
        
        # 2. 類型分析
        type_category = self._analyze_type(data_source.get('type', ''))
        if type_category:
            scores[type_category] = scores.get(type_category, 0) + 2
        
        # 3. 描述分析
        desc_category = self._analyze_description(data_source.get('description', ''))
        if desc_category:
            scores[desc_category] = scores.get(desc_category, 0) + 1
        
        # 返回得分最高的分類
        if scores:
            best_category = max(scores, key=scores.get)
            return best_category
        
        return 'uncategorized'
    
    def _analyze_url(self, url: str) -> Optional[str]:
        """URL 特徵分析"""
        url_lower = url.lower()
        
        patterns = {
            'social': ['facebook', 'twitter', 'instagram', 'linkedin', 'tiktok'],
            'news': ['bbc', 'cnn', 'reuters', 'apnews', 'news'],
            'ecommerce': ['amazon', 'ebay', 'aliexpress', 'shopify', 'woocommerce'],
            'api': ['api.', '/api/', 'api-', 'swagger', 'openapi'],
            'storage': ['s3', 'blob', 'storage', 'cdn'],
            'database': ['postgresql', 'mysql', 'mongodb', 'redis']
        }
        
        for category, keywords in patterns.items():
            if any(kw in url_lower for kw in keywords):
                return category
        
        return None
    
    def _analyze_type(self, data_type: str) -> Optional[str]:
        """資料類型分析"""
        type_mapping = {
            'postgresql': 'database',
            'mysql': 'database',
            'mongodb': 'database',
            'elasticsearch': 'search',
            'api': 'api',
            'http': 'api',
            's3': 'storage',
            'ftp': 'storage'
        }
        
        return type_mapping.get(data_type.lower())
    
    def _analyze_description(self, description: str) -> Optional[str]:
        """描述文本分析"""
        keywords = {
            'social': ['social', 'media', 'user', 'post', 'follow'],
            'news': ['news', 'article', 'publish', 'content'],
            'ecommerce': ['product', 'order', 'cart', 'purchase', 'price'],
            'analytics': ['analytics', 'metric', 'dashboard', 'report'],
            'payment': ['payment', 'invoice', 'billing', 'transaction']
        }
        
        desc_lower = description.lower()
        for category, words in keywords.items():
            if any(word in desc_lower for word in words):
                return category
        
        return None
```

---

## 標籤生成引擎

```python
class TagEngine:
    """資料源自動標籤生成引擎"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def generate_tags(self, data_source: Dict) -> List[str]:
        """
        生成自動標籤
        
        標籤維度：
        - 環境標籤（production, development, testing）
        - 技術標籤（api, database, nosql 等）
        - 業務標籤（user, product, order 等）
        """
        tags = set()
        
        # 1. 環境標籤
        env_tags = self._extract_environment_tags(data_source.get('url', ''))
        tags.update(env_tags)
        
        # 2. 技術標籤
        tech_tags = self._extract_technical_tags(data_source.get('type', ''))
        tags.update(tech_tags)
        
        # 3. 業務標籤
        business_tags = self._extract_business_tags(
            data_source.get('description', ''),
            data_source.get('name', '')
        )
        tags.update(business_tags)
        
        # 4. 質量標籤
        quality_tags = self._extract_quality_tags(data_source)
        tags.update(quality_tags)
        
        return list(tags)
    
    def _extract_environment_tags(self, url: str) -> List[str]:
        """提取環境標籤"""
        tags = []
        url_lower = url.lower()
        
        if any(x in url_lower for x in ['prod', 'production', 'live']):
            tags.append('production')
        if any(x in url_lower for x in ['dev', 'development', 'staging']):
            tags.append('development')
        if any(x in url_lower for x in ['test', 'testing', 'qa']):
            tags.append('testing')
        
        return tags
    
    def _extract_technical_tags(self, data_type: str) -> List[str]:
        """提取技術標籤"""
        tags = []
        data_type_lower = data_type.lower()
        
        if any(x in data_type_lower for x in ['postgresql', 'mysql', 'oracle']):
            tags.extend(['sql', 'relational-db'])
        if any(x in data_type_lower for x in ['mongodb', 'nosql']):
            tags.extend(['nosql', 'document-db'])
        if 'elasticsearch' in data_type_lower:
            tags.extend(['search', 'elasticsearch'])
        if any(x in data_type_lower for x in ['api', 'http']):
            tags.append('rest-api')
        if any(x in data_type_lower for x in ['s3', 'ftp']):
            tags.append('external-storage')
        
        return tags
    
    def _extract_business_tags(self, description: str, name: str) -> List[str]:
        """提取業務標籤"""
        tags = []
        text = (description + " " + name).lower()
        
        business_keywords = {
            'user': ['user', 'account', 'profile', 'identity'],
            'product': ['product', 'catalog', 'inventory', 'sku'],
            'order': ['order', 'purchase', 'transaction', 'checkout'],
            'payment': ['payment', 'billing', 'invoice', 'charge'],
            'analytics': ['analytics', 'metric', 'report', 'dashboard'],
            'content': ['content', 'article', 'media', 'asset']
        }
        
        for tag, keywords in business_keywords.items():
            if any(kw in text for kw in keywords):
                tags.append(tag)
        
        return tags
    
    def _extract_quality_tags(self, data_source: Dict) -> List[str]:
        """提取質量標籤"""
        tags = []
        
        # 基於完整性的標籤
        if data_source.get('description'):
            tags.append('documented')
        
        # 基於類型多樣性的標籤
        if data_source.get('tags'):
            tags.append('tagged')
        
        # 基於元數據豐富度的標籤
        if data_source.get('metadata', {}).get('schema'):
            tags.append('schema-defined')
        
        return tags
```

---

## 相關文件引用

- **主文檔**: [1.2 詳細功能清單](../ch1-2-詳細功能清單.md)
- **API 示例**: [代碼示例 - API 調用](ch1-code-02-api-examples.md)
- **數據庫架構**: [代碼示例 - 數據庫定義](ch1-code-03-database-schema.md)
