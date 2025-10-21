"""
WebCrawler Commander - AI驅動爬蟲生成器
使用自然語言處理和機器學習自動生成爬蟲配置

核心功能：
- 自然語言描述轉爬蟲配置 (NLP理解用戶意圖)
- 智能網站結構分析 (自動識別數據字段和選擇器)
- 自適應爬取策略生成 (基於網站類型智能決策)
- 配置優化建議 (性能調優和錯誤處理建議)
- 多輪對話式優化 (用戶反饋驅動的持續改進)
- 模板推薦系統 (基於相似度匹配的智能推薦)

作者: Jerry開發工作室
版本: v1.0.0
"""

import re
import json
import asyncio
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import math

from ..utils.config_manager import get_config_manager
from ..utils.logger_service import get_logger


@dataclass
class CrawlerIntent:
    """爬蟲意圖數據類"""
    description: str
    website_type: str = "generic"
    data_targets: List[str] = field(default_factory=list)
    extraction_patterns: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    confidence_score: float = 0.0
    parsed_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class GeneratedCrawlerConfig:
    """生成的爬蟲配置"""
    name: str
    description: str
    target_url: str
    selectors: Dict[str, str]
    data_mapping: Dict[str, Any]
    navigation_strategy: str
    retry_config: Dict[str, Any]
    rate_limits: Dict[str, Any]
    validation_rules: List[Dict[str, Any]]
    quality_checks: List[str]
    generated_at: datetime = field(default_factory=datetime.utcnow)
    confidence_level: float = 0.0
    suggestions: List[str] = field(default_factory=list)


@dataclass
class WebsiteAnalysis:
    """網站分析結果"""
    url: str
    title: str = ""
    meta_description: str = ""
    cms_type: str = ""
    has_pagination: bool = False
    has_search: bool = False
    estimated_data_size: str = ""
    page_structure: Dict[str, Any] = field(default_factory=dict)
    recommended_selectors: Dict[str, str] = field(default_factory=dict)
    analysis_timestamp: datetime = field(default_factory=datetime.utcnow)


class NaturalLanguageProcessor:
    """
    自然語言處理器
    解析用戶的自然語言描述，提取爬蟲配置意圖
    """

    def __init__(self):
        self.logger = get_logger(__name__)

        # 關鍵詞映射
        self.website_keywords = {
            "新聞": ["news", "article", "新聞", "報導", "資訊"],
            "電商": ["product", "商品", "價格", "購物", "商店", "商城"],
            "社交媒體": ["post", "貼文", "用戶", "社交", "timeline"],
            "招聘": ["job", "職缺", "招聘", "工作", "徵才"],
            "評論": ["review", "評論", "評價", "用戶評價"],
            "圖片": ["image", "圖片", "相片", "媒體庫"],
            "視頻": ["video", "視頻", "影片"],
            "聯繫人": ["contact", "聯繫", "聯絡人", "客服"]
        }

        self.action_keywords = {
            "提取": ["extract", "抓取", "提取", "獲取", "收集"],
            "監控": ["monitor", "監控", "追蹤", "監測"],
            "搜尋": ["search", "搜尋", "查找", "過濾"],
            "下載": ["download", "下載", "保存"]
        }

        self.constraint_patterns = [
            (r'每\s*(\d+)\s*分鐘', 'frequency_minutes'),
            (r'每天\s*(\d+)\s*次', 'daily_limit'),
            (r'最多\s*(\d+)\s*頁', 'max_pages'),
            (r'只取\s*(\d+)\s*年', 'year_limit')
        ]

    async def parse_description(self, description: str, url: Optional[str] = None) -> CrawlerIntent:
        """
        解析自然語言描述

        Args:
            description: 用戶描述
            url: 可選的目標URL

        Returns:
            解析後的爬蟲意圖
        """
        intent = CrawlerIntent(description=description)

        # 識別網站類型
        intent.website_type = self._identify_website_type(description)

        # 提取數據目標
        intent.data_targets = self._extract_data_targets(description)

        # 提取提取模式
        intent.extraction_patterns = self._extract_patterns(description)

        # 解析約束條件
        intent.constraints = self._parse_constraints(description)

        # 計算置信度
        intent.confidence_score = self._calculate_confidence(intent)

        self.logger.info("description_parsed",
                        description=description[:100],
                        website_type=intent.website_type,
                        data_targets=len(intent.data_targets),
                        confidence=round(intent.confidence_score, 2))

        return intent

    def _identify_website_type(self, description: str) -> str:
        """識別網站類型"""
        description_lower = description.lower()

        scores = {}
        for site_type, keywords in self.website_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in description_lower:
                    score += 1
            if score > 0:
                scores[site_type] = score

        if scores:
            return max(scores, key=scores.get)

        return "generic"

    def _extract_data_targets(self, description: str) -> List[str]:
        """提取數據目標"""
        targets = []

        # 常見數據字段模式
        field_patterns = [
            (r'標題', 'title'),
            (r'內容|本文', 'content'),
            (r'作者', 'author'),
            (r'時間|日期', 'date'),
            (r'價格', 'price'),
            (r'圖片|圖片', 'images'),
            (r'連結|鏈接', 'links'),
            (r'評論|評價', 'reviews'),
            (r'規格|詳細信息', 'specifications'),
            (r'庫存|數量', 'stock')
        ]

        for pattern, field in field_patterns:
            if re.search(pattern, description):
                targets.append(field)

        # 基於上下文的推斷
        if '新聞' in description or '文章' in description:
            if 'title' not in targets:
                targets.extend(['title', 'content', 'date'])
        elif '商品' in description or '產品' in description:
            if 'title' not in targets:
                targets.extend(['title', 'price', 'images'])

        return list(set(targets))

    def _extract_patterns(self, description: str) -> List[str]:
        """提取提取模式"""
        patterns = []

        if '列表' in description or '清單' in description:
            patterns.append('list_extraction')
        if '詳情頁' in description or '詳細' in description:
            patterns.append('detail_page')
        if '分頁' in description or '下一頁' in description:
            patterns.append('pagination')
        if '搜尋' in description or '查詢' in description:
            patterns.append('search_based')

        return patterns

    def _parse_constraints(self, description: str) -> Dict[str, Any]:
        """解析約束條件"""
        constraints = {}

        for pattern, key in self.constraint_patterns:
            match = re.search(pattern, description)
            if match:
                constraints[key] = int(match.group(1))

        # 默認約束
        if not constraints.get('max_pages'):
            constraints['max_pages'] = 100  # 默認最多100頁

        return constraints

    def _calculate_confidence(self, intent: CrawlerIntent) -> float:
        """計算置信度評分"""
        confidence = 0.0

        # 網站類型識別
        if intent.website_type != "generic":
            confidence += 0.3

        # 數據目標數量
        confidence += min(len(intent.data_targets) * 0.1, 0.4)

        # 提取模式數量
        confidence += min(len(intent.extraction_patterns) * 0.1, 0.2)

        # 約束條件數量
        confidence += min(len(intent.constraints) * 0.05, 0.1)

        return min(confidence, 1.0)


class WebsiteStructureAnalyzer:
    """
    網站結構分析器
    分析目標網站的HTML結構，自動識別數據字段和CSS選擇器
    """

    def __init__(self, crawler_engine):
        self.crawler_engine = crawler_engine
        self.logger = get_logger(__name__)

    async def analyze_website(self, url: str) -> WebsiteAnalysis:
        """
        分析網站結構

        Args:
            url: 目標網站URL

        Returns:
            網站分析結果
        """
        analysis = WebsiteAnalysis(url=url)

        try:
            # 獲取首頁內容
            from .crawler_engine import CrawlConfig
            config = CrawlConfig(url=url, timeout=15.0)
            result = await self.crawler_engine.crawl(config)

            if not result.success:
                self.logger.warning("website_analysis_failed", url=url, status=result.status_code)
                return analysis

            # 解析HTML結構
            analysis.page_structure = await self._parse_page_structure(result.text)

            # 更新分析結果
            analysis.title = analysis.page_structure.get('title', '')
            analysis.meta_description = analysis.page_structure.get('meta_description', '')

            # 識別CMS類型
            analysis.cms_type = self._identify_cms(result)

            # 檢測分頁
            analysis.has_pagination = self._detect_pagination(result.text)

            # 檢測搜尋功能
            analysis.has_search = self._detect_search(result.text)

            # 估計數據量
            analysis.estimated_data_size = self._estimate_data_size(result.text)

            # 推薦選擇器
            analysis.recommended_selectors = await self._generate_recommended_selectors(result.text, analysis.page_structure)

        except Exception as e:
            self.logger.error("website_analysis_error", url=url, error=str(e))

        return analysis

    async def _parse_page_structure(self, html_content: str) -> Dict[str, Any]:
        """解析頁面HTML結構"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'lxml')

        structure = {
            'title': soup.title.string if soup.title else '',
            'headings': [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3'])],
            'meta_description': '',
            'forms': len(soup.find_all('form')),
            'tables': len(soup.find_all('table')),
            'lists': len(soup.find_all(['ul', 'ol'])),
            'links': len(soup.find_all('a')),
            'images': len(soup.find_all('img'))
        }

        # 獲取meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            structure['meta_description'] = meta_desc.get('content', '')

        # 分析常見數據容器
        structure['data_containers'] = self._analyze_data_containers(soup)

        return structure

    def _analyze_data_containers(self, soup) -> Dict[str, Any]:
        """分析可能的數據容器"""
        containers = {
            'articles': len(soup.find_all('article')),
            'divs_with_class': len(soup.find_all('div', class_=True)),
            'divs_with_id': len(soup.find_all('div', id=True)),
            'sections': len(soup.find_all('section')),
            'cards': len(soup.select('[class*="card"]')),
            'items': len(soup.select('[class*="item"]')),
            'products': len(soup.select('[class*="product"]'))
        }

        return containers

    def _identify_cms(self, result) -> str:
        """識別CMS類型"""
        # 檢查常見CMS的標誌
        cms_indicators = {
            'WordPress': ['wp-content', 'wp-includes'],
            'Joomla': ['joomla', 'com_content'],
            'Drupal': ['drupal', 'sites/all'],
            'Shopify': ['shopify', 'cdn.shopify.com'],
            'Magento': ['magento', 'Mage.Cookies']
        }

        content = (result.text + ' ' + ' '.join(result.headers.values())).lower()

        for cms, indicators in cms_indicators.items():
            if any(indicator.lower() in content for indicator in indicators):
                return cms

        return 'unknown'

    def _detect_pagination(self, html_content: str) -> bool:
        """檢測分頁功能"""
        pagination_patterns = [
            r'下一頁', r'previous', r'next', r'第\d+頁',
            r'page=\d+', r'offset=\d+', r'class="pagination"'
        ]

        for pattern in pagination_patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return True

        return False

    def _detect_search(self, html_content: str) -> bool:
        """檢測搜尋功能"""
        search_patterns = [
            r'<form[^>]*action="[^"]*search',
            r'<input[^>]*name="[^"]*search',
            r'class="search"', r'id="search"'
        ]

        for pattern in search_patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return True

        return False

    def _estimate_data_size(self, html_content: str) -> str:
        """估計網站數據量"""
        content_length = len(html_content)

        if content_length > 500000:
            return "large"
        elif content_length > 100000:
            return "medium"
        else:
            return "small"

    async def _generate_recommended_selectors(self, html_content: str,
                                            page_structure: Dict[str, Any]) -> Dict[str, str]:
        """生成推薦的CSS選擇器"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'lxml')

        selectors = {}

        # 分析頁面結構，生成候選選擇器
        candidates = self._find_selector_candidates(soup)

        # 為常見字段推薦選擇器
        field_mappings = {
            'title': ['h1', '.title', '[class*="title"]', '.article-title'],
            'content': ['.content', '.article-content', '[class*="content"]', '.main-content'],
            'date': ['.date', '[class*="date"]', '.time', '[datetime]'],
            'author': ['.author', '[class*="author"]', '[rel="author"]'],
            'price': ['.price', '[class*="price"]', '.cost'],
            'images': ['img', '.image img']
        }

        for field, patterns in field_mappings.items():
            for pattern in patterns:
                try:
                    elements = soup.select(pattern)
                    if elements and len(elements) <= 20:  # 避免過於寬泛的選擇器
                        selectors[field] = pattern
                        break
                except:
                    continue

        return selectors


class IntelligentConfigurationGenerator:
    """
    智能配置生成器
    基於分析結果和用戶意圖生成優化的爬蟲配置
    """

    def __init__(self, nlp_processor: NaturalLanguageProcessor,
                 structure_analyzer: WebsiteStructureAnalyzer):
        self.nlp_processor = nlp_processor
        self.structure_analyzer = structure_analyzer
        self.logger = get_logger(__name__)

        # 配置模板庫
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, Dict[str, Any]]:
        """加載爬蟲配置模板"""
        return {
            "news": {
                "selectors": {
                    "title": "h1, .title, .article-title",
                    "content": ".content, .article-content, .entry-content",
                    "date": ".date, .published, [datetime]",
                    "author": ".author, .byline, [rel='author']"
                },
                "navigation": "pagination",
                "data_mapping": {
                    "title": {"type": "string", "required": True},
                    "content": {"type": "text", "required": True},
                    "date": {"type": "date", "format": "auto"},
                    "author": {"type": "string", "required": False}
                }
            },
            "ecommerce": {
                "selectors": {
                    "title": ".product-title, .item-title, h1",
                    "price": ".price, .cost, .amount",
                    "images": ".product-image img, .gallery img",
                    "description": ".description, .product-description",
                    "specifications": ".specs, .details"
                },
                "navigation": "product_list",
                "data_mapping": {
                    "title": {"type": "string", "required": True},
                    "price": {"type": "number", "currency": True},
                    "images": {"type": "array", "max_items": 10},
                    "description": {"type": "text", "required": False}
                }
            },
            "social_media": {
                "selectors": {
                    "posts": ".post, .tweet, .status",
                    "author": ".username, .author, .handle",
                    "content": ".content, .text, .message",
                    "timestamp": ".time, .timestamp",
                    "likes": ".likes, .hearts",
                    "shares": ".shares, .retweets"
                },
                "navigation": "timeline",
                "data_mapping": {
                    "author": {"type": "string", "required": True},
                    "content": {"type": "text", "required": True},
                    "timestamp": {"type": "datetime", "format": "auto"}
                }
            }
        }

    async def generate_configuration(self, intent: CrawlerIntent,
                                    website_analysis: WebsiteAnalysis) -> GeneratedCrawlerConfig:
        """
        生成爬蟲配置

        Args:
            intent: 用戶意圖
            website_analysis: 網站分析結果

        Returns:
            生成的爬蟲配置
        """
        # 獲取適當模板
        template = self.templates.get(intent.website_type, self.templates.get("news", {}))

        config = GeneratedCrawlerConfig(
            name=self._generate_config_name(intent),
            description=intent.description,
            target_url=self._extract_urls_from_description(intent.description),
            selectors=self._generate_selectors(intent, website_analysis, template),
            data_mapping=self._generate_data_mapping(intent, template),
            navigation_strategy=self._determine_navigation_strategy(intent, website_analysis),
            retry_config=self._generate_retry_config(intent),
            rate_limits=self._generate_rate_limits(intent),
            validation_rules=self._generate_validation_rules(intent),
            quality_checks=self._generate_quality_checks(intent),
            confidence_level=intent.confidence_score,
            suggestions=self._generate_suggestions(intent, website_analysis)
        )

        self.logger.info("configuration_generated",
                        name=config.name,
                        confidence=round(config.confidence_level, 2),
                        selectors_count=len(config.selectors))

        return config

    def _generate_config_name(self, intent: CrawlerIntent) -> str:
        """生成配置名稱"""
        # 基於意圖和關鍵詞生成有意義的名稱
        keywords = []

        if intent.website_type != "generic":
            keywords.append(intent.website_type)

        if intent.data_targets:
            keywords.extend(intent.data_targets[:2])  # 最多取前兩個

        if keywords:
            return f"{'_'.join(keywords)}_crawler"
        else:
            # 生成基於描述的Hash簡稱
            hash_obj = hashlib.md5(intent.description.encode())
            return f"auto_crawler_{hash_obj.hexdigest()[:8]}"

    def _extract_urls_from_description(self, description: str) -> str:
        """從描述中提取URL"""
        import re
        url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))?)?'
        urls = re.findall(url_pattern, description)

        if urls:
            return urls[0]  # 返回第一個找到的URL

        return "https://example.com"  # 默認示例URL

    def _generate_selectors(self, intent: CrawlerIntent,
                           analysis: WebsiteAnalysis,
                           template: Dict[str, Any]) -> Dict[str, str]:
        """生成CSS選擇器"""
        selectors = {}

        # 使用分析結果中的推薦選擇器
        selectors.update(analysis.recommended_selectors)

        # 補充模板中的選擇器
        template_selectors = template.get("selectors", {})
        for key, selector in template_selectors.items():
            if key not in selectors and key in intent.data_targets:
                selectors[key] = selector

        # 為缺少的目標字段添加通用選擇器
        generic_selectors = {
            "title": "h1, h2, .title, [class*='title']",
            "content": ".content, .article, [class*='content']",
            "date": ".date, .time, [datetime]",
            "author": ".author, [class*='author']",
            "price": ".price, [class*='price']",
            "image": "img, .image",
            "link": "a[href]"
        }

        for target in intent.data_targets:
            if target not in selectors:
                selectors[target] = generic_selectors.get(target, f"[class*='{target}']")

        return selectors

    def _generate_data_mapping(self, intent: CrawlerIntent,
                              template: Dict[str, Any]) -> Dict[str, Any]:
        """生成數據映射"""
        mapping = {}

        template_mapping = template.get("data_mapping", {})
        mapping.update(template_mapping)

        # 為意圖中的每個目標創建映射
        for target in intent.data_targets:
            if target not in mapping:
                mapping[target] = {
                    "type": "string",
                    "required": True,
                    "validation": []
                }

        # 特殊處理某些字段類型
        field_types = {
            "price": {"type": "number", "pattern": r'\d+(?:\.\d+)?'},
            "date": {"type": "date", "format": "auto"},
            "images": {"type": "array", "max_items": 20},
            "links": {"type": "array", "max_items": 50}
        }

        for field, config in field_types.items():
            if field in mapping:
                mapping[field].update(config)

        return mapping

    def _determine_navigation_strategy(self, intent: CrawlerIntent,
                                      analysis: WebsiteAnalysis) -> str:
        """決定導航策略"""
        if analysis.has_pagination:
            return "pagination"
        elif intent.website_type == "ecommerce":
            return "product_listing"
        elif intent.website_type == "news":
            return "article_listing"
        elif intent.website_type == "social_media":
            return "timeline_scrolling"
        else:
            return "single_page"

    def _generate_retry_config(self, intent: CrawlerIntent) -> Dict[str, Any]:
        """生成重試配置"""
        base_config = {
            "max_retries": 3,
            "retry_delay": 1.0,
            "retry_backoff": "exponential",
            "retry_on_status_codes": [500, 502, 503, 504]
        }

        # 根據約束調整
        if intent.constraints.get('daily_limit'):
            # 如果有每日限制，更保守的重試策略
            base_config.update({
                "max_retries": 2,
                "retry_delay": 2.0
            })

        return base_config

    def _generate_rate_limits(self, intent: CrawlerIntent) -> Dict[str, Any]:
        """生成速率限制"""
        limits = {
            "requests_per_minute": 60,
            "delay_between_requests": 1.0,
            "respect_robots_txt": True,
            "random_delay": True
        }

        # 根據意圖調整限制
        if intent.website_type == "social_media":
            limits.update({
                "requests_per_minute": 30,
                "delay_between_requests": 2.0
            })

        frequency_minutes = intent.constraints.get('frequency_minutes')
        if frequency_minutes:
            limits["delay_between_requests"] = frequency_minutes * 60

        return limits

    def _generate_validation_rules(self, intent: CrawlerIntent) -> List[Dict[str, Any]]:
        """生成驗證規則"""
        rules = []

        # 基本驗證規則
        rules.append({
            "type": "required_fields",
            "fields": intent.data_targets[:3],  # 前三個字段設為必填
            "min_count": len(intent.data_targets) // 2  # 至少一半字段必須存在
        })

        # 字段特定驗證
        field_validations = {
            "price": {"type": "range", "min": 0, "max": 1000000},
            "date": {"type": "date_format", "formats": ["ISO", "US", "EU"]},
            "email": {"type": "regex", "pattern": r"^[^@]+@[^@]+\.[^@]+$"}
        }

        for target in intent.data_targets:
            if target in field_validations:
                rule = field_validations[target].copy()
                rule["field"] = target
                rules.append(rule)

        return rules

    def _generate_quality_checks(self, intent: CrawlerIntent) -> List[str]:
        """生成品質檢查"""
        checks = [
            "check_for_empty_fields",
            "validate_data_types",
            "check_for_duplicates",
            "verify_links_validity"
        ]

        # 根據網站類型添加特定檢查
        if intent.website_type == "news":
            checks.append("check_article_date_relevance")
            checks.append("validate_content_length")
        elif intent.website_type == "ecommerce":
            checks.append("verify_price_format")
            checks.append("check_product_availability")

        return checks

    def _generate_suggestions(self, intent: CrawlerIntent,
                            analysis: WebsiteAnalysis) -> List[str]:
        """生成改進建議"""
        suggestions = []

        # 基於置信度的建議
        if intent.confidence_score < 0.7:
            suggestions.append("請提供更詳細的描述，包括具體的數據字段和網站類型")

        # 基於分析結果的建議
        if not analysis.has_pagination and len(intent.extraction_patterns) > 0:
            suggestions.append("網站似乎沒有分頁功能，考慮調整為單頁面爬取")

        if analysis.cms_type != "unknown":
            suggestions.append(f"檢測到{CMS}系統，建議使用對應的模板")

        # 基於約束的建議
        constraints = intent.constraints
        if constraints.get('max_pages', 100) > 1000:
            suggestions.append("頁面數量較多，建議分批執行")

        return suggestions


class AICrawlerGenerator:
    """
    AI驅動爬蟲生成器主類
    整合所有組件，提供統一的API
    """

    def __init__(self, crawler_engine):
        self.nlp_processor = NaturalLanguageProcessor()
        self.structure_analyzer = WebsiteStructureAnalyzer(crawler_engine)
        self.config_generator = IntelligentConfigurationGenerator(
            self.nlp_processor, self.structure_analyzer
        )

        self.logger = get_logger(__name__)

        # 快取已分析的網站
        self.analysis_cache: Dict[str, WebsiteAnalysis] = {}
        self.cache_timeout = 3600  # 1小時快取

    async def generate_crawler_from_description(self, description: str,
                                                target_url: Optional[str] = None) -> GeneratedCrawlerConfig:
        """
        從自然語言描述生成爬蟲配置

        Args:
            description: 用戶自然語言描述
            target_url: 目標網站URL（可選）

        Returns:
            生成的爬蟲配置
        """
        self.logger.info("generating_crawler_from_description",
                        description=description[:100],
                        has_url=bool(target_url))

        start_time = datetime.utcnow()

        try:
            # 步驟1: 解析用戶意圖
            intent = await self.nlp_processor.parse_description(description, target_url)

            # 步驟2: 分析目標網站（如果提供URL）
            analysis = WebsiteAnalysis(url=target_url or "unknown")
            if target_url:
                # 檢查快取
                if target_url in self.analysis_cache:
                    cached_analysis = self.analysis_cache[target_url]
                    if (datetime.utcnow() - cached_analysis.analysis_timestamp).seconds < self.cache_timeout:
                        analysis = cached_analysis
                    else:
                        del self.analysis_cache[target_url]

                if analysis.url == "unknown":
                    analysis = await self.structure_analyzer.analyze_website(target_url)
                    if target_url:
                        self.analysis_cache[target_url] = analysis

            # 步驟3: 生成優化配置
            config = await self.config_generator.generate_configuration(intent, analysis)

            # 步驟4: 添加處理時間和最終建議
            processing_time = (datetime.utcnow() - start_time).total_seconds()

            config.suggestions.insert(0, f"配置生成完成，處理時間: {processing_time:.2f}秒")
            if config.confidence_level < 0.8:
                config.suggestions.insert(0, "⚠️ 配置置信度較低，建議人工檢查")

            self.logger.info("crawler_generation_completed",
                           processing_time=round(processing_time, 2),
                           confidence=round(config.confidence_level, 2))

            return config

        except Exception as e:
            self.logger.error("crawler_generation_failed",
                            description=description[:100],
                            error=str(e))
            raise

    async def optimize_existing_config(self, config_dict: Dict[str, Any],
                                       feedback: str) -> GeneratedCrawlerConfig:
        """
        優化現有爬蟲配置

        Args:
            config_dict: 現有配置字典
            feedback: 用戶反饋

        Returns:
            優化後的配置
        """
        # 基於反饋生成新的描述
        enhanced_description = f"{config_dict.get('description', '')} {feedback}"

        # 生成新配置
        new_config = await self.generate_crawler_from_description(enhanced_description)

        # 保留原配置的一些設定
        new_config.name = config_dict.get('name', new_config.name)

        return new_config

    async def get_template_recommendations(self, description: str,
                                          limit: int = 5) -> List[Dict[str, Any]]:
        """
        獲取模板推薦

        Args:
            description: 描述
            limit: 返回數量限制

        Returns:
            推薦模板列表
        """
        intent = await self.nlp_processor.parse_description(description)

        # 模擬模板推薦邏輯
        templates = [
            {"name": "新聞爬取模板", "score": 0.9, "tags": ["新聞", "文章"]},
            {"name": "電商商品模板", "score": 0.8, "tags": ["商品", "價格"]},
            {"name": "社交媒體模板", "score": 0.7, "tags": ["使用者", "貼文"]}
        ]

        # 根據意圖評分篩選
        recommendations = []
        for template in templates:
            score_multiplier = 1.0
            if intent.website_type == "新聞" and "新聞" in template["tags"]:
                score_multiplier = 1.2
            elif intent.website_type == "電商" and "商品" in template["tags"]:
                score_multiplier = 1.2

            template["final_score"] = template["score"] * score_multiplier
            recommendations.append(template)

        # 按得分排序
        recommendations.sort(key=lambda x: x["final_score"], reverse=True)

        return recommendations[:limit]


# 全域AI爬蟲生成器實例
_ai_crawler_generator: Optional[AICrawlerGenerator] = None


def init_ai_crawler_generator(crawler_engine) -> AICrawlerGenerator:
    """
    初始化AI爬蟲生成器

    Args:
        crawler_engine: 爬蟲引擎實例

    Returns:
        AI爬蟲生成器實例
    """
    global _ai_crawler_generator

    if _ai_crawler_generator is None:
        _ai_crawler_generator = AICrawlerGenerator(crawler_engine)

    return _ai_crawler_generator


def get_ai_crawler_generator() -> AICrawlerGenerator:
    """獲取AI爬蟲生成器實例"""
    if _ai_crawler_generator is None:
        raise RuntimeError("AI爬蟲生成器尚未初始化，請先調用init_ai_crawler_generator()")
    return _ai_crawler_generator
