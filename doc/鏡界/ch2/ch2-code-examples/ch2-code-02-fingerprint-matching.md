# CH2 代碼示例 - 2.3 指紋匹配和搜尋服務

## 指紋匹配引擎

```python
import logging
from typing import Dict, List, Tuple, Optional
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class FingerprintMatcher:
    """指紋匹配和相似度計算服務"""
    
    def __init__(self, fingerprint_db: 'FingerprintDatabase', config: Dict):
        self.fingerprint_db = fingerprint_db
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def find_similar_fingerprints(
        self,
        fingerprint_id: str,
        threshold: float = 0.7,
        limit: int = 10
    ) -> List[Tuple[str, float]]:
        """
        尋找相似的指紋記錄
        
        Args:
            fingerprint_id: 查詢指紋 ID
            threshold: 相似度閾值
            limit: 返回結果數量限制
            
        Returns:
            [(相似指紋ID, 相似度分數)]
        """
        # 獲取查詢指紋
        query_fp = self.fingerprint_db.get_fingerprint(fingerprint_id)
        if not query_fp:
            raise ValueError(f"Fingerprint {fingerprint_id} not found")
        
        # 轉換為特徵向量
        query_vector = self._fingerprint_to_vector(query_fp)
        
        # 獲取所有指紋
        all_fingerprints = self.fingerprint_db.get_all_fingerprints()
        
        similarities = []
        for fp in all_fingerprints:
            if fp['fingerprint_id'] == fingerprint_id:
                continue
                
            fp_vector = self._fingerprint_to_vector(fp)
            similarity = cosine_similarity([query_vector], [fp_vector])[0][0]
            
            if similarity >= threshold:
                similarities.append((fp['fingerprint_id'], float(similarity)))
        
        # 按相似度排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:limit]
    
    def _fingerprint_to_vector(self, fingerprint: Dict) -> np.ndarray:
        """將指紋轉換為特徵向量"""
        features = []
        
        # 技術棧特徵
        tech_stack = fingerprint.get('tech_stack', {})
        features.extend([
            len(tech_stack.get('servers', [])),
            len(tech_stack.get('languages', [])),
            len(tech_stack.get('frameworks', [])),
            len(tech_stack.get('cms', [])),
            len(tech_stack.get('cdns', []))
        ])
        
        # 反爬機制特徵
        anticrawl = fingerprint.get('anticrawl_mechanisms', [])
        features.append(len(anticrawl))
        
        # 置信度特徵
        features.append(fingerprint.get('confidence_score', 0.5))
        
        return np.array(features)
    
    def batch_match(
        self,
        fingerprint_ids: List[str],
        threshold: float = 0.7
    ) -> Dict[str, List[Tuple[str, float]]]:
        """批量匹配相似指紋"""
        results = {}
        for fp_id in fingerprint_ids:
            try:
                results[fp_id] = self.find_similar_fingerprints(
                    fp_id, threshold
                )
            except Exception as e:
                self.logger.error(f"Matching failed for {fp_id}: {str(e)}")
                results[fp_id] = []
        
        return results
    
    def calculate_similarity(
        self,
        fingerprint_id1: str,
        fingerprint_id2: str
    ) -> float:
        """計算兩個指紋的相似度"""
        fp1 = self.fingerprint_db.get_fingerprint(fingerprint_id1)
        fp2 = self.fingerprint_db.get_fingerprint(fingerprint_id2)
        
        if not fp1 or not fp2:
            return 0.0
        
        vector1 = self._fingerprint_to_vector(fp1)
        vector2 = self._fingerprint_to_vector(fp2)
        
        return float(cosine_similarity([vector1], [vector2])[0][0])
```

## 指紋搜尋服務

```python
class FingerprintSearchService:
    """指紋搜尋和過濾服務"""
    
    def __init__(self, fingerprint_db: 'FingerprintDatabase', config: Dict):
        self.fingerprint_db = fingerprint_db
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def search(
        self,
        query: str,
        filters: Optional[Dict] = None,
        page: int = 1,
        size: int = 20
    ) -> Dict:
        """
        搜尋指紋記錄
        
        Args:
            query: 搜尋關鍵詞（域名、技術等）
            filters: 篩選條件
                {
                    'tech_types': ['Apache', 'PHP'],
                    'anticrawl_level': 'HIGH',
                    'confidence_min': 0.8
                }
            page: 頁碼
            size: 每頁數量
        """
        # 基礎搜尋
        results = self.fingerprint_db.search_by_domain(query)
        
        # 應用過濾
        if filters:
            results = self._apply_filters(results, filters)
        
        # 分頁
        total = len(results)
        offset = (page - 1) * size
        items = results[offset:offset + size]
        
        return {
            'query': query,
            'filters': filters,
            'page': page,
            'size': size,
            'total': total,
            'items': items
        }
    
    def _apply_filters(self, fingerprints: List[Dict], filters: Dict) -> List[Dict]:
        """應用篩選條件"""
        filtered = fingerprints
        
        # 技術類型篩選
        if 'tech_types' in filters:
            tech_types = set(filters['tech_types'])
            filtered = [
                fp for fp in filtered
                if any(
                    tech_types & set(fp.get('tech_stack', {}).get(key, []))
                    for key in ['servers', 'languages', 'frameworks']
                )
            ]
        
        # 反爬級別篩選
        if 'anticrawl_level' in filters:
            level_map = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3, 'EXTREME': 4}
            min_level = level_map.get(filters['anticrawl_level'], 0)
            filtered = [
                fp for fp in filtered
                if len(fp.get('anticrawl_mechanisms', [])) >= min_level
            ]
        
        # 置信度篩選
        if 'confidence_min' in filters:
            min_confidence = filters['confidence_min']
            filtered = [
                fp for fp in filtered
                if fp.get('confidence_score', 0) >= min_confidence
            ]
        
        return filtered
    
    def get_tech_statistics(self, fingerprints: List[Dict]) -> Dict:
        """統計技術棧信息"""
        stats = {
            'servers': {},
            'languages': {},
            'frameworks': {},
            'cms': {}
        }
        
        for fp in fingerprints:
            tech_stack = fp.get('tech_stack', {})
            
            for server in tech_stack.get('servers', []):
                name = server.get('name', 'unknown')
                stats['servers'][name] = stats['servers'].get(name, 0) + 1
            
            for lang in tech_stack.get('languages', []):
                name = lang.get('name', 'unknown')
                stats['languages'][name] = stats['languages'].get(name, 0) + 1
            
            for fw in tech_stack.get('frameworks', []):
                name = fw.get('name', 'unknown')
                stats['frameworks'][name] = stats['frameworks'].get(name, 0) + 1
            
            for cms in tech_stack.get('cms', []):
                name = cms.get('name', 'unknown')
                stats['cms'][name] = stats['cms'].get(name, 0) + 1
        
        return stats
```

---

## 相關文件引用

- **核心功能**: [代碼示例 - 核心實現](ch2-code-01-core-fingerprint.md)
- **數據庫架構**: [代碼示例 - 數據庫定義](ch2-code-03-database-schema.md)
- **API 示例**: [代碼示例 - API 端點](ch2-code-04-api-examples.md)
