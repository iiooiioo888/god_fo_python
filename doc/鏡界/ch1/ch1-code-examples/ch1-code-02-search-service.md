# CH1 代碼示例 - 1.3 搜尋服務實現

## 搜尋服務核心實現

### SearchService 類

```python
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum

class QueryType(Enum):
    """查詢類型枚舉"""
    FULLTEXT = "fulltext"
    FILTER = "filter"
    RANGE = "range"
    BOOLEAN = "boolean"
    ADVANCED = "advanced"

class SortOrder(Enum):
    """排序順序"""
    ASC = "asc"
    DESC = "desc"

class SearchService:
    """資料源搜尋服務"""
    
    def __init__(
        self,
        search_engine: 'SearchEngine',
        db: 'Database',
        config: Dict
    ):
        self.search_engine = search_engine
        self.db = db
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 默認搜尋配置
        self.default_page_size = config.get('default_page_size', 20)
        self.max_page_size = config.get('max_page_size', 100)
        self.enable_fuzzy_match = config.get('enable_fuzzy_match', True)
        self.enable_suggestions = config.get('enable_suggestions', True)
    
    def search(
        self,
        query: str,
        project_id: str,
        user_id: str,
        filters: Optional[Dict] = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: Optional[str] = None,
        sort_order: str = "desc"
    ) -> Dict:
        """
        執行全文搜尋
        
        Args:
            query: 搜尋關鍵詞
            project_id: 專案 ID
            user_id: 用戶 ID（用於權限檢查）
            filters: 篩選條件
            page: 頁碼
            page_size: 每頁數量
            sort_by: 排序字段
            sort_order: 排序順序 (asc/desc)
            
        Returns:
            搜尋結果
        """
        # 1. 驗證參數
        page_size = min(page_size, self.max_page_size)
        offset = (page - 1) * page_size
        
        # 2. 構建搜尋查詢
        search_query = self._build_search_query(query, filters, sort_by, sort_order)
        
        # 3. 執行搜尋
        search_results = self.search_engine.search(
            query=search_query,
            offset=offset,
            limit=page_size
        )
        
        # 4. 檢查權限並過濾結果
        filtered_results = self._apply_permissions(
            search_results['hits'],
            user_id,
            project_id
        )
        
        # 5. 組裝結果
        result = {
            'query': query,
            'total': search_results['total'],
            'page': page,
            'page_size': page_size,
            'total_pages': (search_results['total'] + page_size - 1) // page_size,
            'results': filtered_results,
            'aggregations': search_results.get('aggregations', {}),
            'search_time_ms': search_results.get('search_time_ms', 0)
        }
        
        # 6. 添加搜尋建議（如果啟用）
        if self.enable_suggestions and len(filtered_results) == 0:
            result['suggestions'] = self._generate_suggestions(query)
        
        self.logger.info(
            f"Search completed: query='{query}', "
            f"results={len(filtered_results)}, "
            f"total={search_results['total']}"
        )
        
        return result
    
    def advanced_search(
        self,
        conditions: List[Dict],
        boolean_operator: str = "AND",
        project_id: str = None,
        user_id: str = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict:
        """
        執行高級搜尋（複雜條件）
        
        Args:
            conditions: 搜尋條件列表
                [
                    {'field': 'name', 'operator': 'contains', 'value': 'user'},
                    {'field': 'type', 'operator': 'equals', 'value': 'api'},
                    {'field': 'created_at', 'operator': 'range', 'value': {'gte': '2024-01-01'}}
                ]
            boolean_operator: AND/OR/NOT
            project_id: 專案 ID
            user_id: 用戶 ID
            page: 頁碼
            page_size: 每頁數量
            
        Returns:
            搜尋結果
        """
        # 1. 驗證條件
        self._validate_conditions(conditions)
        
        # 2. 構建複雜查詢
        search_query = self._build_advanced_query(conditions, boolean_operator)
        
        # 3. 執行搜尋
        offset = (page - 1) * page_size
        search_results = self.search_engine.search(
            query=search_query,
            offset=offset,
            limit=page_size
        )
        
        # 4. 應用權限過濾
        filtered_results = self._apply_permissions(
            search_results['hits'],
            user_id,
            project_id
        )
        
        return {
            'conditions': conditions,
            'boolean_operator': boolean_operator,
            'total': search_results['total'],
            'page': page,
            'page_size': page_size,
            'results': filtered_results
        }
    
    def _build_search_query(
        self,
        query: str,
        filters: Optional[Dict] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "desc"
    ) -> Dict:
        """構建搜尋查詢"""
        es_query = {
            'bool': {
                'must': [
                    {
                        'multi_match': {
                            'query': query,
                            'fields': [
                                'name^3',          # 名稱權重最高
                                'description^2',  # 描述次之
                                'url^1',
                                'tags^2'
                            ],
                            'fuzziness': 'AUTO' if self.enable_fuzzy_match else 0,
                            'operator': 'or'
                        }
                    }
                ],
                'filter': []
            }
        }
        
        # 添加過濾條件
        if filters:
            for field, value in filters.items():
                if isinstance(value, list):
                    # 多值過濾（OR）
                    es_query['bool']['filter'].append({
                        'terms': {field: value}
                    })
                elif isinstance(value, dict):
                    # 範圍查詢
                    es_query['bool']['filter'].append({
                        'range': {field: value}
                    })
                else:
                    # 單值過濾
                    es_query['bool']['filter'].append({
                        'term': {field: value}
                    })
        
        # 添加排序
        sort = []
        if sort_by:
            sort.append({sort_by: {'order': sort_order}})
        # 默認按相關度排序
        sort.append({'_score': {'order': 'desc'}})
        
        return {
            'query': es_query,
            'sort': sort
        }
    
    def _build_advanced_query(
        self,
        conditions: List[Dict],
        boolean_operator: str = "AND"
    ) -> Dict:
        """構建高級複雜查詢"""
        query_clauses = []
        
        for condition in conditions:
            field = condition['field']
            operator = condition['operator']
            value = condition['value']
            
            if operator == 'contains':
                query_clauses.append({
                    'match': {field: {'query': value, 'operator': 'or'}}
                })
            elif operator == 'equals':
                query_clauses.append({'term': {field: value}})
            elif operator == 'range':
                query_clauses.append({'range': {field: value}})
            elif operator == 'prefix':
                query_clauses.append({'prefix': {field: value}})
            elif operator == 'regex':
                query_clauses.append({'regexp': {field: value}})
            elif operator == 'in':
                query_clauses.append({'terms': {field: value}})
        
        # 根據 boolean_operator 組合查詢
        if boolean_operator.upper() == "AND":
            es_query = {'bool': {'must': query_clauses}}
        elif boolean_operator.upper() == "OR":
            es_query = {'bool': {'should': query_clauses, 'minimum_should_match': 1}}
        elif boolean_operator.upper() == "NOT":
            es_query = {'bool': {'must_not': query_clauses}}
        else:
            es_query = {'bool': {'must': query_clauses}}
        
        return {'query': es_query}
    
    def _apply_permissions(
        self,
        results: List[Dict],
        user_id: str,
        project_id: str
    ) -> List[Dict]:
        """應用權限過濾"""
        # 簡化實現，實際應查詢權限服務
        filtered = []
        for result in results:
            # 檢查用戶是否有權限訪問此資料源
            has_permission = self._check_permission(
                result['_source'].get('id'),
                user_id,
                project_id,
                'read'
            )
            
            if has_permission:
                filtered.append({
                    'id': result['_source'].get('id'),
                    'name': result['_source'].get('name'),
                    'type': result['_source'].get('type'),
                    'description': result['_source'].get('description'),
                    'url': result['_source'].get('url'),
                    'category': result['_source'].get('category'),
                    'tags': result['_source'].get('tags'),
                    'score': result.get('_score'),
                    'created_at': result['_source'].get('created_at')
                })
        
        return filtered
    
    def _check_permission(
        self,
        resource_id: str,
        user_id: str,
        project_id: str,
        action: str
    ) -> bool:
        """檢查用戶權限"""
        # 簡化實現
        return True
    
    def _validate_conditions(self, conditions: List[Dict]):
        """驗證搜尋條件"""
        valid_operators = [
            'contains', 'equals', 'range', 'prefix', 
            'regex', 'in', 'gt', 'gte', 'lt', 'lte'
        ]
        
        for condition in conditions:
            if 'field' not in condition or 'operator' not in condition:
                raise ValueError("Missing required fields: field, operator")
            
            if condition['operator'] not in valid_operators:
                raise ValueError(f"Invalid operator: {condition['operator']}")
    
    def _generate_suggestions(self, query: str) -> List[str]:
        """生成搜尋建議"""
        suggestions = []
        
        # 1. 檢查拼寫建議
        spell_suggestions = self.search_engine.get_spell_suggestions(query)
        suggestions.extend(spell_suggestions)
        
        # 2. 相關搜尋建議
        related = self.search_engine.get_related_terms(query)
        suggestions.extend(related)
        
        return suggestions[:5]  # 返回前 5 個建議
    
    def get_facets(
        self,
        query: Optional[str] = None,
        filters: Optional[Dict] = None,
        facet_fields: List[str] = None
    ) -> Dict:
        """
        獲取搜尋結果的分面統計
        
        用於生成篩選選項（如類型、標籤等）
        """
        if facet_fields is None:
            facet_fields = ['type', 'category', 'tags', 'owner_id']
        
        # 構建搜尋查詢
        search_query = self._build_search_query(query or '*', filters)
        
        # 添加分面聚合
        aggregations = {}
        for field in facet_fields:
            aggregations[field] = {
                'terms': {'field': field, 'size': 50}
            }
        
        search_query['aggs'] = aggregations
        search_query['size'] = 0  # 只獲取聚合，不要文檔
        
        # 執行聚合查詢
        results = self.search_engine.search(query=search_query)
        
        facets = {}
        for field, agg_result in results.get('aggregations', {}).items():
            facets[field] = [
                {'name': bucket['key'], 'count': bucket['doc_count']}
                for bucket in agg_result['buckets']
            ]
        
        return facets
```

---

## Elasticsearch 適配器實現

```python
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ElasticsearchException
from typing import Dict, List

class ElasticsearchAdapter:
    """Elasticsearch 搜尋引擎適配器"""
    
    def __init__(self, config: Dict):
        """
        初始化 Elasticsearch 連接
        
        Args:
            config: 配置字典
                {
                    'hosts': ['localhost:9200'],
                    'index': 'data_sources',
                    'timeout': 30,
                    'max_retries': 3
                }
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 創建 Elasticsearch 客戶端
        self.es = Elasticsearch(
            hosts=config.get('hosts', ['localhost:9200']),
            timeout=config.get('timeout', 30),
            max_retries=config.get('max_retries', 3)
        )
        
        self.index = config.get('index', 'data_sources')
    
    def create_index(self):
        """創建索引和映射"""
        settings = {
            'settings': {
                'number_of_shards': 5,
                'number_of_replicas': 2,
                'analysis': {
                    'tokenizer': {
                        'my_tokenizer': {
                            'type': 'standard'
                        }
                    },
                    'analyzer': {
                        'my_analyzer': {
                            'type': 'custom',
                            'tokenizer': 'my_tokenizer',
                            'filter': ['lowercase', 'stop']
                        }
                    }
                }
            },
            'mappings': {
                'properties': {
                    'id': {'type': 'keyword'},
                    'name': {
                        'type': 'text',
                        'analyzer': 'my_analyzer',
                        'fields': {'keyword': {'type': 'keyword'}}
                    },
                    'description': {
                        'type': 'text',
                        'analyzer': 'my_analyzer'
                    },
                    'url': {'type': 'keyword'},
                    'type': {'type': 'keyword'},
                    'category': {'type': 'keyword'},
                    'tags': {'type': 'keyword'},
                    'status': {'type': 'keyword'},
                    'owner_id': {'type': 'keyword'},
                    'created_at': {'type': 'date'},
                    'updated_at': {'type': 'date'},
                    'project_id': {'type': 'keyword'}
                }
            }
        }
        
        try:
            if self.es.indices.exists(index=self.index):
                self.es.indices.delete(index=self.index)
            
            self.es.indices.create(index=self.index, body=settings)
            self.logger.info(f"Index '{self.index}' created successfully")
        except ElasticsearchException as e:
            self.logger.error(f"Failed to create index: {str(e)}")
            raise
    
    def add_document(self, doc_id: str, document: Dict):
        """添加文檔到索引"""
        try:
            self.es.index(
                index=self.index,
                id=doc_id,
                body=document
            )
            self.logger.debug(f"Document {doc_id} added to index")
        except ElasticsearchException as e:
            self.logger.error(f"Failed to add document: {str(e)}")
            raise
    
    def search(
        self,
        query: Dict,
        offset: int = 0,
        limit: int = 20
    ) -> Dict:
        """執行搜尋查詢"""
        try:
            search_body = {
                'query': query.get('query', {'match_all': {}}),
                'sort': query.get('sort', []),
                'from': offset,
                'size': limit
            }
            
            # 添加聚合（如果有）
            if 'aggs' in query:
                search_body['aggs'] = query['aggs']
            
            # 如果只查聚合，不需要文檔
            if query.get('size') == 0:
                search_body['size'] = 0
            
            start_time = datetime.utcnow()
            response = self.es.search(index=self.index, body=search_body)
            search_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            return {
                'total': response['hits']['total']['value'],
                'hits': response['hits']['hits'],
                'aggregations': response.get('aggregations', {}),
                'search_time_ms': search_time
            }
        except ElasticsearchException as e:
            self.logger.error(f"Search failed: {str(e)}")
            raise
    
    def get_spell_suggestions(self, query: str) -> List[str]:
        """獲取拼寫糾正建議"""
        try:
            suggestion_query = {
                'suggest': {
                    'spell-check': {
                        'text': query,
                        'term': {'field': 'name'}
                    }
                }
            }
            
            response = self.es.search(
                index=self.index,
                body=suggestion_query
            )
            
            suggestions = []
            for suggestion in response.get('suggest', {}).get('spell-check', []):
                if suggestion['options']:
                    suggestions.append(suggestion['options'][0]['text'])
            
            return suggestions
        except Exception as e:
            self.logger.warning(f"Failed to get spell suggestions: {str(e)}")
            return []
    
    def get_related_terms(self, query: str) -> List[str]:
        """獲取相關搜尋詞"""
        try:
            related_query = {
                'query': {
                    'more_like_this': {
                        'fields': ['name', 'description'],
                        'like': query,
                        'min_term_freq': 1,
                        'max_query_terms': 5
                    }
                },
                'size': 5
            }
            
            response = self.es.search(index=self.index, body=related_query)
            
            related = []
            for hit in response['hits']['hits']:
                related.append(hit['_source']['name'])
            
            return related
        except Exception as e:
            self.logger.warning(f"Failed to get related terms: {str(e)}")
            return []
    
    def delete_document(self, doc_id: str):
        """刪除文檔"""
        try:
            self.es.delete(index=self.index, id=doc_id)
        except ElasticsearchException as e:
            self.logger.error(f"Failed to delete document: {str(e)}")
            raise
    
    def bulk_index(self, documents: List[Tuple[str, Dict]]):
        """批量索引文檔"""
        from elasticsearch.helpers import bulk
        
        try:
            actions = [
                {
                    '_index': self.index,
                    '_id': doc_id,
                    '_source': doc
                }
                for doc_id, doc in documents
            ]
            
            bulk(self.es, actions)
            self.logger.info(f"Bulk indexed {len(documents)} documents")
        except ElasticsearchException as e:
            self.logger.error(f"Bulk indexing failed: {str(e)}")
            raise
```

---

## 相關文件引用

- **主文檔**: [1.3 技術架構](../ch1-3-技術架構.md)
- **搜尋 API**: [API 示例 - 搜尋端點](ch1-code-04-api-examples.md#搜尋端點)
- **配置建議**: [最佳實踐 - 搜尋優化](../ch1-10-最佳實踐指南.md#搜尋優化)
