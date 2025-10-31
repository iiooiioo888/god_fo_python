# CH6 代碼示例 - 6.2 LLM 集成與代碼生成

## LLM 集成實現

```python
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

class LLMIntegration:
    """LLM 集成層"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.model_client = self._init_model_client()
    
    def _init_model_client(self):
        """初始化 LLM 客戶端"""
        provider = self.config.get('provider', 'openai')
        if provider == 'openai':
            import openai
            openai.api_key = self.config['api_key']
            return openai
        return None
    
    async def generate_code(
        self,
        requirement: str,
        language: str = 'python',
        context: Optional[Dict] = None
    ) -> str:
        """
        根據需求生成代碼
        
        Args:
            requirement: 需求描述
            language: 編程語言
            context: 上下文信息
            
        Returns:
            生成的代碼
        """
        prompt = self._build_prompt(requirement, language, context)
        
        response = await asyncio.to_thread(
            self.model_client.ChatCompletion.create,
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert code generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2048
        )
        
        generated_code = response.choices[0].message.content
        return generated_code
    
    async def analyze_error(
        self,
        error_message: str,
        code_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """分析錯誤並提供建議"""
        prompt = f"""
        分析以下錯誤並提供修複建議：
        
        錯誤信息：{error_message}
        
        {f'代碼上下文：{code_context}' if code_context else ''}
        
        請提供：
        1. 錯誤原因
        2. 修複步驟
        3. 修複代碼示例
        """
        
        response = await asyncio.to_thread(
            self.model_client.ChatCompletion.create,
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert Python debugger."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        analysis_text = response.choices[0].message.content
        
        return {
            'error_message': error_message,
            'analysis': analysis_text,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _build_prompt(
        self,
        requirement: str,
        language: str,
        context: Optional[Dict]
    ) -> str:
        """構建提示詞"""
        prompt = f"""
        請根據以下需求生成 {language} 代碼：
        
        需求：{requirement}
        """
        
        if context:
            prompt += f"\n\n上下文：{json.dumps(context, ensure_ascii=False)}"
        
        prompt += """
        
        要求：
        1. 代碼應該是可直接運行的
        2. 包含必要的錯誤處理
        3. 添加詳細的註釋
        4. 遵循編程最佳實踐
        """
        
        return prompt

class CodeGenerator:
    """專門的代碼生成器"""
    
    def __init__(self, llm: LLMIntegration, db: 'Database'):
        self.llm = llm
        self.db = db
        self.logger = logging.getLogger(__name__)
    
    async def generate_spider_code(
        self,
        target_url: str,
        requirements: Dict
    ) -> str:
        """生成爬蟲代碼"""
        requirement = f"""
        生成一個爬蟲，用於爬取 {target_url}
        
        功能需求：
        {json.dumps(requirements, ensure_ascii=False)}
        """
        
        code = await self.llm.generate_code(
            requirement, 'python',
            {'framework': 'requests', 'type': 'spider'}
        )
        
        # 保存生成的代碼
        await self._save_generated_code('spider', code, requirements)
        
        return code
    
    async def generate_test_code(
        self,
        source_code: str,
        test_type: str = 'unit'
    ) -> str:
        """生成測試代碼"""
        requirement = f"""
        為以下代碼生成 {test_type} 測試：
        
        {source_code}
        """
        
        return await self.llm.generate_code(requirement, 'python')
    
    async def _save_generated_code(
        self,
        code_type: str,
        code: str,
        metadata: Dict
    ):
        """保存生成的代碼"""
        sql = """
        INSERT INTO generated_code (
            code_type, content, metadata, created_at
        ) VALUES (
            %(code_type)s, %(content)s, %(metadata)s, %(created_at)s
        )
        """
        
        self.db.execute(sql, {
            'code_type': code_type,
            'content': code,
            'metadata': json.dumps(metadata),
            'created_at': datetime.utcnow().isoformat()
        })

class KnowledgeBase:
    """知識庫"""
    
    def __init__(self, db: 'Database'):
        self.db = db
    
    async def get_similar_articles(
        self,
        query: str,
        limit: int = 5
    ) -> List[Dict]:
        """查詢相似的知識文章"""
        sql = """
        SELECT * FROM knowledge_articles
        WHERE title LIKE %s OR content LIKE %s
        LIMIT %s
        """
        
        articles = self.db.fetchall(sql, (f'%{query}%', f'%{query}%', limit))
        return articles
```

---

## 相關文件引用

- **主文檔**: [6.2 詳細功能清單](../ch6-2-詳細功能清單.md)
- **數據庫**: [代碼示例 - 數據庫定義](ch6-code-02-database-schema.md)
- **API 示例**: [代碼示例 - API 端點](ch6-code-03-api-examples.md)
