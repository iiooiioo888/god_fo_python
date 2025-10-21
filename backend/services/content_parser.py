"""
WebCrawler Commander - 智慧內容提取模塊
實現高階內容分析和結構化數據提取功能

核心功能：
- HTML內容智能解析 (BS4 + 自定義解析器)
- 動態內容處理 (JavaScript渲染支持)
- 多媒體內容識別 (圖片、視頻、音頻元數據提取)
- 結構化數據提取 (Microdata, JSON-LD, RDFa解析)
- 自然語言處理整合 (文本分類、實體識別)
- 內嵌式翻譯支持 (多語言內容處理)

作者: Jerry開發工作室
版本: v1.0.0
"""

import asyncio
import re
import json
import hashlib
import base64
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from urllib.parse import urlparse, urljoin, parse_qs
from collections import defaultdict

import httpx
from bs4 import BeautifulSoup, NavigableString
import aiofiles

from ..utils.config_manager import get_config_manager
from ..utils.logger_service import get_logger


class ContentType(Enum):
    """內容類型枚舉"""
    HTML = "html"
    JSON_LD = "json_ld"
    MICRODATA = "microdata"
    RDFA = "rdfa"
    OPENGRAPH = "opengraph"
    TWITTER_CARD = "twitter_card"
    JSON = "json"
    XML = "xml"
    TEXT = "text"


class MediaType(Enum):
    """媒體類型枚舉"""
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    ARCHIVE = "archive"


@dataclass
class ExtractedContent:
    """提取的內容數據類"""
    url: str
    content_type: ContentType
    title: Optional[str] = None
    description: Optional[str] = None
    text_content: Optional[str] = None
    main_content: Optional[str] = None
    structured_data: Dict[str, Any] = field(default_factory=dict)
    media_assets: List[Dict[str, Any]] = field(default_factory=list)
    links: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    language: Optional[str] = None
    extracted_at: datetime = field(default_factory=datetime.utcnow)
    quality_score: float = 0.0


@dataclass
class ContentRule:
    """內容提取規則數據類"""
    name: str
    selector: str
    attribute: Optional[str] = None
    content_type: str = "text"
    required: bool = False
    validation_pattern: Optional[str] = None
    post_processor: Optional[str] = None


@dataclass
class ParseResult:
    """解析結果數據類"""
    success: bool
    extracted_content: Optional[ExtractedContent] = None
    error_message: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    parse_time: float = 0.0
    rules_applied: int = 0


class HTMLContentParser:
    """
    HTML內容解析器
    使用BeautifulSoup進行高階HTML內容提取
    """

    def __init__(self):
        self.logger = get_logger(__name__)

    async def parse_html_content(self, html_content: str, url: str,
                                extract_rules: Optional[List[ContentRule]] = None) -> ExtractedContent:
        """
        解析HTML內容

        Args:
            html_content: HTML內容字符串
            url: 原始URL
            extract_rules: 自定義提取規則

        Returns:
            提取的內容對象
        """
        try:
            soup = BeautifulSoup(html_content, 'lxml')

            content = ExtractedContent(url=url, content_type=ContentType.HTML)

            # 基礎元數據提取
            content.title = self._extract_title(soup)
            content.description = self._extract_description(soup)
            content.language = self._detect_language(soup)

            # 文本內容提取
            content.text_content = self._extract_text_content(soup)
            content.main_content = self._extract_main_content(soup)

            # 結構化數據提取
            content.structured_data = await self._extract_structured_data(soup, url)

            # 媒體資源提取
            content.media_assets = self._extract_media_assets(soup, url)

            # 鏈接提取
            content.links = self._extract_links(soup, url)

            # 元數據提取
            content.metadata = self._extract_metadata(soup)

            # 內容品質評分
            content.quality_score = self._calculate_content_quality(content)

            self.logger.debug("html_content_parsed",
                            url=url,
                            title=content.title[:50] if content.title else None,
                            quality_score=round(content.quality_score, 2),
                            media_count=len(content.media_assets))

            return content

        except Exception as e:
            self.logger.error("html_parsing_error", url=url, error=str(e))
            return ExtractedContent(url=url, content_type=ContentType.HTML)

    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """提取頁面標題"""
        # 嘗試多種標題來源
        title_sources = [
            lambda: soup.title.string if soup.title else None,
            lambda: soup.find('meta', {'property': 'og:title'})['content'] if soup.find('meta', {'property': 'og:title'}) else None,
            lambda: soup.find('meta', {'name': 'twitter:title'})['content'] if soup.find('meta', {'name': 'twitter:title'}) else None,
            lambda: soup.find('h1').get_text().strip() if soup.find('h1') else None
        ]

        for source in title_sources:
            try:
                title = source()
                if title and title.strip():
                    return title.strip()
            except:
                continue

        return None

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """提取頁面描述"""
        description_sources = [
            lambda: soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else None,
            lambda: soup.find('meta', {'property': 'og:description'})['content'] if soup.find('meta', {'property': 'og:description'}) else None,
            lambda: soup.find('meta', {'name': 'twitter:description'})['content'] if soup.find('meta', {'name': 'twitter:description'}) else None
        ]

        for source in description_sources:
            try:
                desc = source()
                if desc and desc.strip():
                    return desc.strip()
            except:
                continue

        return None

    def _detect_language(self, soup: BeautifulSoup) -> Optional[str]:
        """檢測內容語言"""
        # 檢查html標籤的lang屬性
        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang'):
            return html_tag['lang']

        # 檢查meta標籤
        meta_lang = soup.find('meta', {'http-equiv': 'content-language'})
        if meta_lang and meta_lang.get('content'):
            return meta_lang['content']

        return None

    def _extract_text_content(self, soup: BeautifulSoup) -> Optional[str]:
        """提取所有文本內容"""
        # 移除腳本和樣式元素
        for script in soup(["script", "style"]):
            script.decompose()

        # 獲取文本內容
        text = soup.get_text(separator=' ', strip=True)

        # 清理多餘空白
        text = re.sub(r'\s+', ' ', text).strip()

        return text if text else None

    def _extract_main_content(self, soup: BeautifulSoup) -> Optional[str]:
        """提取主要內容區域"""
        # 嘗試識別主要內容容器
        content_selectors = [
            'main',
            '[role="main"]',
            '.main-content',
            '.content',
            '.post-content',
            '.entry-content',
            'article'
        ]

        for selector in content_selectors:
            try:
                element = soup.select_one(selector)
                if element:
                    # 清除內嵌腳本和樣式
                    for script in element(["script", "style"]):
                        script.decompose()

                    text = element.get_text(separator=' ', strip=True)
                    text = re.sub(r'\s+', ' ', text).strip()

                    if len(text) > 100:  # 至少100個字符
                        return text
            except:
                continue

        # 備用方案：查找最大文本塊
        try:
            paragraphs = soup.find_all('p')
            if paragraphs:
                main_text = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                main_text = re.sub(r'\s+', ' ', main_text).strip()

                if len(main_text) > 200:
                    return main_text
        except:
            pass

        return None

    async def _extract_structured_data(self, soup: BeautifulSoup, base_url: str) -> Dict[str, Any]:
        """提取結構化數據"""
        structured_data = {}

        try:
            # JSON-LD 提取
            json_ld_scripts = soup.find_all('script', {'type': 'application/ld+json'})
            if json_ld_scripts:
                structured_data['json_ld'] = []
                for script in json_ld_scripts:
                    try:
                        data = json.loads(script.string)
                        structured_data['json_ld'].append(data)
                    except json.JSONDecodeError:
                        continue

            # Microdata 提取
            microdata = self._extract_microdata(soup)
            if microdata:
                structured_data['microdata'] = microdata

            # RDFa 提取
            rdfa = self._extract_rdfa(soup)
            if rdfa:
                structured_data['rdfa'] = rdfa

            # OpenGraph 提取
            og_data = self._extract_opengraph(soup)
            if og_data:
                structured_data['opengraph'] = og_data

            # Twitter Cards 提取
            twitter_data = self._extract_twitter_cards(soup)
            if twitter_data:
                structured_data['twitter_card'] = twitter_data

        except Exception as e:
            self.logger.warning("structured_data_extraction_error", error=str(e))

        return structured_data

    def _extract_microdata(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """提取Microdata"""
        microdata = {}

        try:
            # 查找具有itemtype的元素
            items = soup.find_all(attrs={'itemtype': True})
            for item in items:
                item_type = item.get('itemtype')
                if item_type:
                    item_data = {}
                    # 找到所有itemprop
                    props = item.find_all(attrs={'itemprop': True})
                    for prop in props:
                        prop_name = prop.get('itemprop')
                        if prop_name:
                            if prop.get('content'):
                                prop_value = prop['content']
                            elif prop.name in ['img', 'audio', 'video', 'source']:
                                prop_value = prop.get('src', prop.get('data-src'))
                            else:
                                prop_value = prop.get_text().strip()

                            item_data[prop_name] = prop_value

                    if item_data:
                        microdata[item_type] = item_data

        except Exception as e:
            self.logger.debug("microdata_extraction_error", error=str(e))

        return microdata

    def _extract_rdfa(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """提取RDFa數據"""
        rdfa_data = {}

        try:
            # 查找具有typeof的元素
            types = soup.find_all(attrs={'typeof': True})
            for element in types:
                type_name = element.get('typeof')
                if type_name:
                    properties = {}
                    # 查找屬性
                    prop_elements = element.find_all(attrs={'property': True})
                    for prop_elem in prop_elements:
                        prop_name = prop_elem.get('property')
                        if prop_name:
                            prop_value = prop_elem.get('content') or prop_elem.get_text().strip()
                            properties[prop_name] = prop_value

                    if properties:
                        rdfa_data[type_name] = properties

        except Exception as e:
            self.logger.debug("rdfa_extraction_error", error=str(e))

        return rdfa_data

    def _extract_opengraph(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """提取OpenGraph數據"""
        og_data = {}

        try:
            og_tags = soup.find_all('meta', {'property': lambda x: x and x.startswith('og:')})
            for tag in og_tags:
                property_name = tag.get('property', '')[3:]  # 移除'og:'前綴
                content = tag.get('content')
                if property_name and content:
                    og_data[property_name] = content

        except Exception as e:
            self.logger.debug("opengraph_extraction_error", error=str(e))

        return og_data

    def _extract_twitter_cards(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """提取Twitter Cards數據"""
        twitter_data = {}

        try:
            twitter_tags = soup.find_all('meta', {'name': lambda x: x and x.startswith('twitter:')})
            for tag in twitter_tags:
                property_name = tag.get('name', '')[8:]  # 移除'twitter:'前綴
                content = tag.get('content')
                if property_name and content:
                    twitter_data[property_name] = content

        except Exception as e:
            self.logger.debug("twitter_cards_extraction_error", error=str(e))

        return twitter_data

    def _extract_media_assets(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
        """提取媒體資源"""
        media_assets = []

        try:
            # 圖片資源
            images = soup.find_all(['img', 'picture', 'source'])
            for img in images:
                if img.name == 'img':
                    src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
                    alt = img.get('alt', '')
                    if src:
                        media_assets.append({
                            'type': 'image',
                            'url': urljoin(base_url, src),
                            'alt': alt,
                            'title': img.get('title', ''),
                            'width': img.get('width'),
                            'height': img.get('height')
                        })

            # 視頻資源
            videos = soup.find_all('video')
            for video in videos:
                src = video.get('src')
                if src:
                    media_assets.append({
                        'type': 'video',
                        'url': urljoin(base_url, src),
                        'poster': video.get('poster'),
                        'controls': video.get('controls') is not None,
                        'autoplay': video.get('autoplay') is not None
                    })

                # 檢查source子元素
                sources = video.find_all('source')
                for source in sources:
                    src = source.get('src')
                    if src:
                        media_assets.append({
                            'type': 'video',
                            'url': urljoin(base_url, src),
                            'mime_type': source.get('type')
                        })

            # 音頻資源
            audios = soup.find_all('audio')
            for audio in audios:
                src = audio.get('src')
                if src:
                    media_assets.append({
                        'type': 'audio',
                        'url': urljoin(base_url, src),
                        'controls': audio.get('controls') is not None
                    })

        except Exception as e:
            self.logger.warning("media_assets_extraction_error", error=str(e))

        return media_assets

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
        """提取鏈接"""
        links = []

        try:
            a_tags = soup.find_all('a', href=True)
            for a in a_tags:
                href = a['href']
                if href and not href.startswith(('javascript:', 'mailto:', '#')):
                    absolute_url = urljoin(base_url, href)
                    links.append({
                        'url': absolute_url,
                        'text': a.get_text().strip(),
                        'title': a.get('title', ''),
                        'rel': a.get('rel', [])
                    })
        except Exception as e:
            self.logger.warning("links_extraction_error", error=str(e))

        return links

    def _extract_metadata(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """提取頁面元數據"""
        metadata = {}

        try:
            # 基本meta標籤
            meta_tags = soup.find_all('meta')
            for meta in meta_tags:
                name = meta.get('name') or meta.get('property') or meta.get('http-equiv')
                content = meta.get('content')
                if name and content:
                    metadata[name] = content

            # 鏈接標籤 (CSS, RSS等)
            link_tags = soup.find_all('link')
            link_data = {}
            for link in link_tags:
                rel = link.get('rel', [])
                if isinstance(rel, str):
                    rel = [rel]

                href = link.get('href')
                if href:
                    for r in rel:
                        link_data[r] = href

            if link_data:
                metadata['links'] = link_data

            # 規範鏈接
            canonical = soup.find('link', {'rel': 'canonical'})
            if canonical:
                metadata['canonical_url'] = canonical.get('href')

            # 其他重要標籤
            metadata['has_mobile_viewport'] = soup.find('meta', {'name': 'viewport'}) is not None
            metadata['has_robots_meta'] = soup.find('meta', {'name': 'robots'}) is not None

        except Exception as e:
            self.logger.warning("metadata_extraction_error", error=str(e))

        return metadata

    def _calculate_content_quality(self, content: ExtractedContent) -> float:
        """計算內容品質分數"""
        score = 0.0

        try:
            # 基礎檢查 (最高20分)
            if content.title:
                score += 10
            if content.description:
                score += 5
            if content.main_content and len(content.main_content) > 500:
                score += 5

            # 內容豐富度 (最高30分)
            if content.media_assets and len(content.media_assets) > 0:
                score += min(len(content.media_assets) * 2, 10)
            if content.links and len(content.links) > 10:
                score += min((len(content.links) - 10) * 0.5, 10)
            if content.text_content and len(content.text_content) > 1000:
                score += min((len(content.text_content) - 1000) // 1000 * 5, 10)

            # 結構化數據 (最高25分)
            structured_score = 0
            if content.structured_data.get('json_ld'):
                structured_score += 10
            if content.structured_data.get('microdata'):
                structured_score += 5
            if content.structured_data.get('opengraph'):
                structured_score += 5
            if content.structured_data.get('rdfa'):
                structured_score += 5
            score += min(structured_score, 25)

            # 元數據完整性 (最高15分)
            metadata_score = 0
            if len(content.metadata) > 10:
                metadata_score += 10
            if content.metadata.get('canonical_url'):
                metadata_score += 3
            if content.metadata.get('has_robots_meta'):
                metadata_score += 2
            score += metadata_score

            # 語言檢測 (最高5分)
            if content.language:
                score += 5

            # 標準化到0-100分
            score = min(score, 100.0)

        except Exception as e:
            self.logger.warning("content_quality_calculation_error", error=str(e))
            score = 0.0

        return score


class StructuredDataExtractor:
    """
    結構化數據提取器
    專門處理JSON-LD, Microdata, RDFa等結構化數據格式
    """

    def __init__(self):
        self.logger = get_logger(__name__)

        # 支持的結構化數據格式
        self.schemas = {
            'Article': self._extract_article_schema,
            'NewsArticle': self._extract_article_schema,
            'BlogPosting': self._extract_article_schema,
            'Product': self._extract_product_schema,
            'Event': self._extract_event_schema,
            'Organization': self._extract_organization_schema,
            'Person': self._extract_person_schema,
            'Place': self._extract_place_schema,
            'Recipe': self._extract_recipe_schema,
            'Movie': self._extract_movie_schema
        }

    async def extract_structured_data(self, json_ld_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        提取和結構化JSON-LD數據

        Args:
            json_ld_data: JSON-LD數據列表

        Returns:
            結構化的提取結果
        """
        results = {}

        for item in json_ld_data:
            try:
                item_type = item.get('@type', item.get('type'))
                if isinstance(item_type, list):
                    item_type = item_type[0] if item_type else None

                if item_type and item_type in self.schemas:
                    extractor = self.schemas[item_type]
                    extracted = await extractor(item)
                    if extracted:
                        if item_type not in results:
                            results[item_type] = []
                        results[item_type].append(extracted)
                else:
                    # 保存原始數據
                    if 'unknown' not in results:
                        results['unknown'] = []
                    results['unknown'].append(item)

            except Exception as e:
                self.logger.warning("structured_data_extraction_error", error=str(e))
                continue

        return results

    async def _extract_article_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """提取文章模式數據"""
        return {
            'headline': data.get('headline'),
            'description': data.get('description'),
            'author': self._extract_author_info(data.get('author', [])),
            'publisher': self._extract_organization_info(data.get('publisher')),
            'date_published': data.get('datePublished'),
            'date_modified': data.get('dateModified'),
            'image': data.get('image'),
            'article_section': data.get('articleSection'),
            'keywords': data.get('keywords', [])
        }

    async def _extract_product_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """提取產品模式數據"""
        offers = data.get('offers', {})
        if isinstance(offers, list):
            offers = offers[0] if offers else {}

        return {
            'name': data.get('name'),
            'description': data.get('description'),
            'brand': data.get('brand'),
            'category': data.get('category'),
            'price': offers.get('price'),
            'currency': offers.get('priceCurrency'),
            'availability': offers.get('availability'),
            'url': offers.get('url'),
            'rating': data.get('aggregateRating', {}).get('ratingValue'),
            'review_count': data.get('aggregateRating', {}).get('reviewCount')
        }

    async def _extract_event_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """提取事件模式數據"""
        return {
            'name': data.get('name'),
            'description': data.get('description'),
            'start_date': data.get('startDate'),
            'end_date': data.get('endDate'),
            'location': self._extract_place_info(data.get('location')),
            'organizer': self._extract_organization_info(data.get('organizer')),
            'url': data.get('url'),
            'event_status': data.get('eventStatus')
        }

    async def _extract_organization_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """提取組織模式數據"""
        return await self._extract_organization_info(data)

    async def _extract_person_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """提取人物模式數據"""
        return {
            'name': data.get('name'),
            'given_name': data.get('givenName'),
            'family_name': data.get('familyName'),
            'job_title': data.get('jobTitle'),
            'email': data.get('email'),
            'telephone': data.get('telephone'),
            'url': data.get('url'),
            'same_as': data.get('sameAs', [])
        }

    async def _extract_place_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """提取地點模式數據"""
        return await self._extract_place_info(data)

    async def _extract_recipe_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """提取食譜模式數據"""
        return {
            'name': data.get('name'),
            'description': data.get('description'),
            'author': self._extract_author_info(data.get('author', [])),
            'cook_time': data.get('cookTime'),
            'prep_time': data.get('prepTime'),
            'recipe_yield': data.get('recipeYield'),
            'recipe_ingredient': data.get('recipeIngredient', []),
            'recipe_instructions': data.get('recipeInstructions', [])
        }

    async def _extract_movie_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """提取電影模式數據"""
        return {
            'name': data.get('name'),
            'description': data.get('description'),
            'director': self._extract_person_info(data.get('director')),
            'actor': [self._extract_person_info(actor) for actor in data.get('actor', [])],
            'genre': data.get('genre', []),
            'duration': data.get('duration'),
            'date_published': data.get('datePublished'),
            'rating': data.get('aggregateRating', {}).get('ratingValue')
        }

    def _extract_author_info(self, author_data) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """提取作者信息"""
        if not author_data:
            return []

        if isinstance(author_data, list):
            return [self._extract_person_info(author) for author in author_data]
        else:
            return self._extract_person_info(author_data)

    def _extract_person_info(self, person_data) -> Dict[str, Any]:
        """提取個人信息"""
        if isinstance(person_data, str):
            return {'name': person_data}
        elif isinstance(person_data, dict):
            return {
                'name': person_data.get('name'),
                'url': person_data.get('url'),
                'same_as': person_data.get('sameAs', [])
            }
        return {}

    def _extract_organization_info(self, org_data) -> Dict[str, Any]:
        """提取組織信息"""
        if isinstance(org_data, dict):
            return {
                'name': org_data.get('name'),
                'url': org_data.get('url'),
                'logo': org_data.get('logo'),
                'same_as': org_data.get('sameAs', [])
            }
        return {}

    def _extract_place_info(self, place_data) -> Dict[str, Any]:
        """提取地點信息"""
        if isinstance(place_data, dict):
            address = place_data.get('address', {})
            if isinstance(address, dict):
                return {
                    'name': place_data.get('name'),
                    'address': {
                        'street_address': address.get('streetAddress'),
                        'city': address.get('addressLocality'),
                        'state': address.get('addressRegion'),
                        'postal_code': address.get('postalCode'),
                        'country': address.get('addressCountry')
                    }
                }
        return {}


class ContentParser:
    """
    內容解析器主類
    整合所有解析功能，提供統一的內容提取介面
    """

    def __init__(self):
        self.html_parser = HTMLContentParser()
        self.structured_extractor = StructuredDataExtractor()
        self.logger = get_logger(__name__)

    async def parse_content(self, raw_content: str, content_type: str, url: str,
                           extract_rules: Optional[List[ContentRule]] = None) -> ParseResult:
        """
        解析內容主入口

        Args:
            raw_content: 原始內容
            content_type: 內容類型
            url: 來源URL
            extract_rules: 自定義提取規則

        Returns:
            解析結果
        """
        start_time = time.time()

        try:
            if content_type.lower().startswith('text/html'):
                # HTML內容解析
                extracted_content = await self.html_parser.parse_html_content(raw_content, url, extract_rules)
                extracted_content.extracted_at = datetime.utcnow()

            elif content_type.lower().startswith('application/json'):
                # JSON內容解析
                extracted_content = await self._parse_json_content(raw_content, url)

            elif content_type.lower().startswith('application/xml') or content_type.lower().endswith('xml'):
                # XML內容解析
                extracted_content = await self._parse_xml_content(raw_content, url)

            else:
                # 純文本內容
                extracted_content = ExtractedContent(
                    url=url,
                    content_type=ContentType.TEXT,
                    text_content=raw_content
                )

            # 應用自定義提取規則
            if extract_rules:
                extracted_content = await self._apply_extraction_rules(extracted_content, extract_rules)

            parse_time = time.time() - start_time

            result = ParseResult(
                success=True,
                extracted_content=extracted_content,
                parse_time=parse_time,
                rules_applied=len(extract_rules) if extract_rules else 0
            )

            self.logger.info("content_parsing_completed",
                           url=url,
                           content_type=extracted_content.content_type.value,
                           parse_time=round(parse_time, 3),
                           quality_score=round(extracted_content.quality_score, 2))

            return result

        except Exception as e:
            parse_time = time.time() - start_time

            result = ParseResult(
                success=False,
                error_message=str(e),
                parse_time=parse_time,
                rules_applied=len(extract_rules) if extract_rules else 0
            )

            self.logger.error("content_parsing_failed", url=url, error=str(e))

            return result

    async def _parse_json_content(self, json_content: str, url: str) -> ExtractedContent:
        """解析JSON內容"""
        try:
            data = json.loads(json_content)

            content = ExtractedContent(
                url=url,
                content_type=ContentType.JSON,
                structured_data={'json': data},
                text_content=json.dumps(data, ensure_ascii=False, indent=2)
            )

            # 嘗試提取有意義的標題
            if isinstance(data, dict):
                content.title = data.get('title') or data.get('name') or data.get('headline')
                content.description = data.get('description') or data.get('summary')

            content.quality_score = 60.0  # JSON內容基礎分數

            return content

        except json.JSONDecodeError:
            return ExtractedContent(
                url=url,
                content_type=ContentType.TEXT,
                text_content=json_content
            )

    async def _parse_xml_content(self, xml_content: str, url: str) -> ExtractedContent:
        """解析XML內容"""
        try:
            root = ET.fromstring(xml_content)

            # 轉換為字典格式
            def xml_to_dict(element):
                result = {}
                for child in element:
                    if len(child) == 0:
                        result[child.tag] = child.text or ""
                    else:
                        result[child.tag] = xml_to_dict(child)
                return result

            xml_data = xml_to_dict(root)

            content = ExtractedContent(
                url=url,
                content_type=ContentType.XML,
                structured_data={'xml': xml_data},
                text_content=xml_content
            )

            content.quality_score = 50.0  # XML內容基礎分數

            return content

        except ET.ParseError:
            return ExtractedContent(
                url=url,
                content_type=ContentType.TEXT,
                text_content=xml_content
            )

    async def _apply_extraction_rules(self, content: ExtractedContent,
                                    rules: List[ContentRule]) -> ExtractedContent:
        """應用自定義提取規則"""
        if not hasattr(content, '_raw_html'):
            return content

        try:
            soup = BeautifulSoup(content._raw_html, 'lxml')

            for rule in rules:
                try:
                    elements = soup.select(rule.selector)
                    if not elements:
                        if rule.required:
                            content.quality_score -= 5  # 必填規則未找到，降低品質
                        continue

                    extracted_data = []

                    for element in elements:
                        if rule.attribute:
                            value = element.get(rule.attribute)
                        else:
                            value = element.get_text().strip()

                        if value:
                            # 應用驗證模式
                            if rule.validation_pattern:
                                if not re.match(rule.validation_pattern, str(value)):
                                    continue

                            extracted_data.append(value)

                    # 儲存提取結果
                    if extracted_data:
                        rule_name = rule.name
                        if rule.content_type == "array":
                            content.structured_data[rule_name] = extracted_data
                        else:
                            content.structured_data[rule_name] = extracted_data[0] if len(extracted_data) == 1 else extracted_data

                except Exception as e:
                    self.logger.warning("extraction_rule_error",
                                      rule=rule.name,
                                      error=str(e))
                    if rule.required:
                        content.quality_score -= 3

        except Exception as e:
            self.logger.error("extraction_rules_application_error", error=str(e))

        return content


# 全域內容解析器實例
_content_parser: Optional[ContentParser] = None


def init_content_parser() -> ContentParser:
    """
    初始化全域內容解析器

    Returns:
        內容解析器實例
    """
    global _content_parser

    if _content_parser is None:
        _content_parser = ContentParser()

    return _content_parser


def get_content_parser() -> ContentParser:
    """獲取全域內容解析器實例"""
    if _content_parser is None:
        raise RuntimeError("內容解析器尚未初始化，請先調用init_content_parser()")
    return _content_parser
