# CH2 代碼示例 - 2.2 網站指紋分析核心實現

## 指紋識別引擎核心實現

### WebFingerprint 主服務類

```python
import logging
import hashlib
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum
from urllib.parse import urlparse

class TechType(Enum):
    """技術類型枚舉"""
    SERVER = "server"
    LANGUAGE = "language"
    FRAMEWORK = "framework"
    CMS = "cms"
    DATABASE = "database"
    CDN = "cdn"
    ANALYTICS = "analytics"
    SECURITY = "security"

class AntiCrawlLevel(Enum):
    """反爬級別"""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    EXTREME = 4

class WebFingerprintAnalyzer:
    """網站指紋分析引擎核心服務"""
    
    def __init__(
        self,
        db: 'Database',
        fingerprint_db: 'FingerprintDatabase',
        config: Dict
    ):
        self.db = db
        self.fingerprint_db = fingerprint_db
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 技術棧特徵規則
        self.tech_signatures = self._load_tech_signatures()
        
        # 反爬特徵規則
        self.anticrawl_signatures = self._load_anticrawl_signatures()
    
    def analyze_website(
        self,
        url: str,
        response_data: Dict,
        user_id: str
    ) -> Dict:
        """
        分析網站指紋
        
        Args:
            url: 目標網站 URL
            response_data: 網站響應數據
                {
                    'status_code': 200,
                    'headers': {...},
                    'html': '<html>...',
                    'cookies': {...},
                    'request_time': 0.5
                }
            user_id: 用戶 ID
            
        Returns:
            完整的指紋分析結果
        """
        try:
            # 1. 提取基本信息
            domain = urlparse(url).netloc
            
            # 2. 識別技術棧
            tech_stack = self._identify_tech_stack(response_data)
            
            # 3. 檢測反爬機制
            anticrawl_info = self._detect_anticrawl_mechanisms(response_data)
            
            # 4. 分析內容特徵
            content_features = self._analyze_content_features(response_data)
            
            # 5. 生成指紋簽名
            fingerprint_signature = self._generate_fingerprint_signature(
                domain,
                tech_stack,
                anticrawl_info,
                content_features
            )
            
            # 6. 構建完整結果
            result = {
                'fingerprint_id': f"fp-{hashlib.md5(url.encode()).hexdigest()[:8]}",
                'url': url,
                'domain': domain,
                'analysis_time': datetime.utcnow().isoformat(),
                'tech_stack': tech_stack,
                'anticrawl': anticrawl_info,
                'content_features': content_features,
                'fingerprint_signature': fingerprint_signature,
                'confidence_score': self._calculate_confidence(
                    tech_stack,
                    anticrawl_info,
                    content_features
                ),
                'recommendations': self._generate_crawler_recommendations(
                    tech_stack,
                    anticrawl_info
                )
            }
            
            # 7. 保存指紋記錄
            self._save_fingerprint_record(result, user_id)
            
            # 8. 發布分析完成事件
            self._publish_analysis_event(result, user_id)
            
            self.logger.info(f"Website analysis completed for {domain}")
            return result
            
        except Exception as e:
            self.logger.error(f"Website analysis failed: {str(e)}")
            raise
    
    def _identify_tech_stack(self, response_data: Dict) -> Dict:
        """識別技術棧"""
        tech_stack = {
            'servers': [],
            'languages': [],
            'frameworks': [],
            'cms': [],
            'databases': [],
            'cdns': [],
            'analytics': [],
            'security': []
        }
        
        headers = response_data.get('headers', {})
        html = response_data.get('html', '')
        
        # 1. 服務器識別
        server = self._identify_server(headers)
        if server:
            tech_stack['servers'].append(server)
        
        # 2. 編程語言識別
        languages = self._identify_languages(headers, html)
        tech_stack['languages'].extend(languages)
        
        # 3. 前端框架識別
        frameworks = self._identify_frameworks(html)
        tech_stack['frameworks'].extend(frameworks)
        
        # 4. CMS 識別
        cms = self._identify_cms(headers, html)
        if cms:
            tech_stack['cms'].append(cms)
        
        # 5. CDN 識別
        cdns = self._identify_cdns(headers)
        tech_stack['cdns'].extend(cdns)
        
        # 6. 分析工具識別
        analytics = self._identify_analytics(html)
        tech_stack['analytics'].extend(analytics)
        
        return tech_stack
    
    def _identify_server(self, headers: Dict) -> Optional[Dict]:
        """識別服務器軟件"""
        server_header = headers.get('Server', '')
        
        for signature in self.tech_signatures.get('servers', []):
            if signature['pattern'] in server_header.lower():
                return {
                    'name': signature['name'],
                    'version': self._extract_version(server_header, signature),
                    'confidence': signature.get('confidence', 0.9),
                    'identified_from': 'Server header'
                }
        
        return None
    
    def _identify_languages(self, headers: Dict, html: str) -> List[Dict]:
        """識別編程語言"""
        languages = []
        
        # PHP 識別
        if 'X-Powered-By' in headers:
            powered_by = headers['X-Powered-By'].lower()
            if 'php' in powered_by:
                languages.append({
                    'name': 'PHP',
                    'version': self._extract_version(powered_by, {'name': 'PHP'}),
                    'confidence': 0.95
                })
        
        # JavaScript/Node.js 識別
        if any(pattern in html for pattern in ['__NUXT__', 'nextjs-', 'remix']):
            languages.append({
                'name': 'Node.js',
                'confidence': 0.85
            })
        
        # Python 識別
        if 'Django' in html or 'Flask' in html:
            languages.append({
                'name': 'Python',
                'confidence': 0.9
            })
        
        return languages
    
    def _identify_frameworks(self, html: str) -> List[Dict]:
        """識別前端框架"""
        frameworks = []
        
        patterns = {
            'React': ['__REACT_DEVTOOLS_GLOBAL_HOOK__', 'react-'],
            'Angular': ['ng-app', 'angular.js', 'angular.min.js'],
            'Vue': ['__VUE__', 'v-app', 'vue.js'],
            'jQuery': ['jquery.js', 'jQuery'],
            'Bootstrap': ['bootstrap.css', 'bootstrap.min.css']
        }
        
        for framework, signatures in patterns.items():
            if any(sig in html for sig in signatures):
                frameworks.append({
                    'name': framework,
                    'confidence': 0.85
                })
        
        return frameworks
    
    def _identify_cms(self, headers: Dict, html: str) -> Optional[Dict]:
        """識別 CMS"""
        cms_patterns = {
            'WordPress': ['wp-content', 'wp-includes', 'wordpress'],
            'Drupal': ['drupal.js', 'drupal-', 'sites/default'],
            'Joomla': ['joomla', 'com_'],
            'Magento': ['magento', 'mage/'],
            'Shopify': ['cdn.shopify.com', 'Shopify']
        }
        
        for cms, patterns in cms_patterns.items():
            if any(pattern in html.lower() for pattern in patterns):
                return {
                    'name': cms,
                    'confidence': 0.9,
                    'identified_from': 'HTML content'
                }
        
        return None
    
    def _identify_cdns(self, headers: Dict) -> List[Dict]:
        """識別 CDN"""
        cdns = []
        
        cdn_headers = {
            'Cloudflare': ['Server', 'CF-Ray'],
            'Akamai': ['AkamaiGHost', 'Server'],
            'Fastly': ['X-Cache', 'X-Served-By']
        }
        
        for cdn, check_headers in cdn_headers.items():
            if any(h in headers for h in check_headers):
                cdns.append({
                    'name': cdn,
                    'confidence': 0.95
                })
        
        return cdns
    
    def _identify_analytics(self, html: str) -> List[Dict]:
        """識別分析工具"""
        analytics = []
        
        patterns = {
            'Google Analytics': ['ga.js', 'gtag', 'GA_ID'],
            'Baidu Analytics': ['baidu.js', '_baidu_'],
            'Segment': ['segment.com', 'analytics.js'],
            'Mixpanel': ['mixpanel', 'mp.']
        }
        
        for tool, signs in patterns.items():
            if any(sign in html for sign in signs):
                analytics.append({
                    'name': tool,
                    'confidence': 0.85
                })
        
        return analytics
    
    def _detect_anticrawl_mechanisms(self, response_data: Dict) -> Dict:
        """檢測反爬機制"""
        anticrawl_info = {
            'level': AntiCrawlLevel.NONE.value,
            'mechanisms': [],
            'details': {}
        }
        
        headers = response_data.get('headers', {})
        html = response_data.get('html', '')
        
        # 1. User-Agent 檢測
        if self._check_useragent_detection(headers):
            anticrawl_info['mechanisms'].append('user_agent_detection')
            anticrawl_info['details']['user_agent'] = {
                'required': True,
                'recommendations': ['使用真實 User-Agent']
            }
        
        # 2. IP 限制檢測
        if self._check_ip_restriction(headers):
            anticrawl_info['mechanisms'].append('ip_restriction')
            anticrawl_info['details']['ip_restriction'] = {
                'detected': True,
                'recommendations': ['使用代理或 VPN']
            }
        
        # 3. 速率限制檢測
        rate_limit = self._detect_rate_limiting(headers)
        if rate_limit:
            anticrawl_info['mechanisms'].append('rate_limiting')
            anticrawl_info['details']['rate_limiting'] = rate_limit
        
        # 4. JS 挑戰檢測
        if self._check_js_challenge(html):
            anticrawl_info['mechanisms'].append('js_challenge')
            anticrawl_info['details']['js_challenge'] = {
                'type': 'javascript_execution_required',
                'recommendations': ['使用 Selenium 或 Playwright']
            }
        
        # 5. CAPTCHA 檢測
        if self._check_captcha(html, headers):
            anticrawl_info['mechanisms'].append('captcha')
            anticrawl_info['details']['captcha'] = {
                'type': 'reCAPTCHA or similar',
                'recommendations': ['集成 CAPTCHA 解決服務']
            }
        
        # 6. 行為驗證檢測
        if self._check_behavior_verification(html):
            anticrawl_info['mechanisms'].append('behavior_verification')
            anticrawl_info['details']['behavior_verification'] = {
                'type': 'mouse_movement_click_pattern',
                'recommendations': ['模擬真實用戶行為']
            }
        
        # 7. 指紋檢測
        if self._check_fingerprinting(html):
            anticrawl_info['mechanisms'].append('fingerprinting')
            anticrawl_info['details']['fingerprinting'] = {
                'type': 'Canvas WebGL AudioContext',
                'recommendations': ['使用無頭瀏覽器或代理']
            }
        
        # 計算反爬級別
        anticrawl_info['level'] = len(anticrawl_info['mechanisms'])
        
        return anticrawl_info
    
    def _check_useragent_detection(self, headers: Dict) -> bool:
        """檢查 User-Agent 檢測"""
        return 'User-Agent' in headers or any(
            'user-agent' in h.lower() for h in headers
        )
    
    def _check_ip_restriction(self, headers: Dict) -> bool:
        """檢查 IP 限制"""
        return 'X-Forwarded-For' in headers or 'CF-Connecting-IP' in headers
    
    def _detect_rate_limiting(self, headers: Dict) -> Optional[Dict]:
        """檢測速率限制"""
        if 'X-RateLimit-Limit' in headers or 'RateLimit-Limit' in headers:
            return {
                'detected': True,
                'limit': headers.get('X-RateLimit-Limit', 'unknown'),
                'window': headers.get('X-RateLimit-Window', 'unknown')
            }
        return None
    
    def _check_js_challenge(self, html: str) -> bool:
        """檢查 JS 挑戰"""
        return any(sig in html for sig in [
            '<script>var chk_bro',
            'bot.js',
            'challenge.js',
            'check_browser'
        ])
    
    def _check_captcha(self, html: str, headers: Dict) -> bool:
        """檢查 CAPTCHA"""
        captcha_sigs = [
            'recaptcha', 'hcaptcha', 'geetest',
            'cloudflare', 'captcha', 'challenge'
        ]
        return any(sig in html.lower() for sig in captcha_sigs)
    
    def _check_behavior_verification(self, html: str) -> bool:
        """檢查行為驗證"""
        return any(sig in html.lower() for sig in [
            'mousemove', 'mousedown', 'click',
            'user_action', 'behavior_check'
        ])
    
    def _check_fingerprinting(self, html: str) -> bool:
        """檢查指紋檢測"""
        return any(sig in html.lower() for sig in [
            'canvas', 'webgl', 'audiocontext',
            'navigator.plugins', 'webdriver'
        ])
    
    def _analyze_content_features(self, response_data: Dict) -> Dict:
        """分析內容特徵"""
        html = response_data.get('html', '')
        
        return {
            'page_size': len(html),
            'dom_complexity': self._calculate_dom_complexity(html),
            'script_count': html.count('<script'),
            'style_count': html.count('<style') + html.count('<link'),
            'dynamic_content': self._detect_dynamic_content(html),
            'encoding': response_data.get('encoding', 'utf-8'),
            'response_time': response_data.get('request_time', 0)
        }
    
    def _calculate_dom_complexity(self, html: str) -> float:
        """計算 DOM 複雜度"""
        # 簡化計算
        tag_count = sum(1 for tag in [
            '<div', '<p', '<span', '<section', '<article',
            '<header', '<footer', '<nav', '<main'
        ] if tag in html)
        
        return min(tag_count / 100, 1.0)
    
    def _detect_dynamic_content(self, html: str) -> Dict:
        """檢測動態內容"""
        has_ajax = any(sig in html for sig in ['ajax', 'fetch', 'XMLHttpRequest'])
        has_websocket = 'WebSocket' in html or 'ws://' in html
        
        return {
            'ajax': has_ajax,
            'websocket': has_websocket,
            'frame_based': '<iframe' in html,
            'json_ld': '<script type="application/ld+json"' in html
        }
    
    def _generate_fingerprint_signature(
        self,
        domain: str,
        tech_stack: Dict,
        anticrawl_info: Dict,
        content_features: Dict
    ) -> str:
        """生成指紋簽名"""
        # 組合所有特徵
        signature_data = json.dumps({
            'domain': domain,
            'tech_stack': tech_stack,
            'anticrawl_mechanisms': anticrawl_info['mechanisms'],
            'content_complexity': content_features['dom_complexity']
        }, sort_keys=True)
        
        # 計算 SHA256 哈希
        return hashlib.sha256(signature_data.encode()).hexdigest()[:16]
    
    def _calculate_confidence(
        self,
        tech_stack: Dict,
        anticrawl_info: Dict,
        content_features: Dict
    ) -> float:
        """計算分析置信度"""
        base_score = 0.5
        
        # 技術棧識別越多，置信度越高
        tech_count = sum(len(v) for v in tech_stack.values() if isinstance(v, list))
        base_score += (tech_count * 0.05) * 0.25
        
        # 反爬檢測越準確，置信度越高
        anticrawl_confidence = (5 - anticrawl_info['level']) / 5 * 0.25
        base_score += anticrawl_confidence
        
        # 內容特徵越豐富，置信度越高
        base_score += content_features['dom_complexity'] * 0.25
        
        return min(base_score, 1.0)
    
    def _generate_crawler_recommendations(
        self,
        tech_stack: Dict,
        anticrawl_info: Dict
    ) -> List[Dict]:
        """生成爬蟲配置建議"""
        recommendations = []
        
        # 基於技術棧的建議
        for server in tech_stack.get('servers', []):
            recommendations.append({
                'category': 'server_specific',
                'suggestion': f"針對 {server['name']} 的優化配置",
                'priority': 'high'
            })
        
        # 基於反爬的建議
        for mechanism in anticrawl_info['mechanisms']:
            if mechanism == 'js_challenge':
                recommendations.append({
                    'category': 'anti_crawl',
                    'suggestion': '需要 JavaScript 渲染引擎（Selenium/Playwright）',
                    'priority': 'critical'
                })
            elif mechanism == 'rate_limiting':
                recommendations.append({
                    'category': 'rate_limit',
                    'suggestion': '實施延遲和随機化策略',
                    'priority': 'high'
                })
            elif mechanism == 'captcha':
                recommendations.append({
                    'category': 'captcha',
                    'suggestion': '集成 CAPTCHA 解決服務或使用無頭瀏覽器',
                    'priority': 'critical'
                })
        
        return recommendations
    
    def _save_fingerprint_record(self, result: Dict, user_id: str):
        """保存指紋記錄到數據庫"""
        pass
    
    def _publish_analysis_event(self, result: Dict, user_id: str):
        """發布分析完成事件"""
        pass
    
    def _load_tech_signatures(self) -> Dict:
        """加載技術棧特徵規則"""
        return {
            'servers': [
                {'name': 'Apache', 'pattern': 'apache', 'confidence': 0.9},
                {'name': 'Nginx', 'pattern': 'nginx', 'confidence': 0.95},
                {'name': 'IIS', 'pattern': 'microsoft-iis', 'confidence': 0.95}
            ]
        }
    
    def _load_anticrawl_signatures(self) -> Dict:
        """加載反爬特徵規則"""
        return {
            'js_challenges': ['bot.js', 'challenge.js'],
            'captchas': ['recaptcha', 'hcaptcha']
        }
    
    def _extract_version(self, header_value: str, signature: Dict) -> Optional[str]:
        """從 header 提取版本號"""
        # 簡化實現
        parts = header_value.split('/')
        if len(parts) > 1:
            return parts[1].split()[0]
        return None
```

---

## 指紋數據庫管理

### FingerprintDatabase 類

```python
class FingerprintDatabase:
    """指紋數據庫管理服務"""
    
    def __init__(self, db: 'Database', config: Dict):
        self.db = db
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def store_fingerprint(
        self,
        fingerprint_data: Dict,
        user_id: str
    ) -> str:
        """存儲指紋記錄"""
        fingerprint_id = fingerprint_data['fingerprint_id']
        
        sql = """
        INSERT INTO website_fingerprints (
            fingerprint_id, domain, url, tech_stack, anticrawl_mechanisms,
            fingerprint_signature, confidence_score, created_by, created_at
        ) VALUES (
            %(fingerprint_id)s, %(domain)s, %(url)s, %(tech_stack)s,
            %(anticrawl_mechanisms)s, %(fingerprint_signature)s,
            %(confidence_score)s, %(user_id)s, %(created_at)s
        )
        """
        
        params = {
            'fingerprint_id': fingerprint_id,
            'domain': fingerprint_data['domain'],
            'url': fingerprint_data['url'],
            'tech_stack': json.dumps(fingerprint_data['tech_stack']),
            'anticrawl_mechanisms': json.dumps(
                fingerprint_data['anticrawl']['mechanisms']
            ),
            'fingerprint_signature': fingerprint_data['fingerprint_signature'],
            'confidence_score': fingerprint_data['confidence_score'],
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat()
        }
        
        self.db.execute(sql, params)
        self.logger.info(f"Fingerprint {fingerprint_id} stored successfully")
        
        return fingerprint_id
    
    def get_fingerprint(self, fingerprint_id: str) -> Optional[Dict]:
        """獲取指紋記錄"""
        sql = """
        SELECT * FROM website_fingerprints
        WHERE fingerprint_id = %(fingerprint_id)s
        """
        
        row = self.db.fetchone(sql, {'fingerprint_id': fingerprint_id})
        return row
    
    def search_by_domain(self, domain: str) -> List[Dict]:
        """按域名搜尋指紋"""
        sql = """
        SELECT * FROM website_fingerprints
        WHERE domain LIKE %(domain)s
        ORDER BY created_at DESC
        """
        
        rows = self.db.fetchall(sql, {'domain': f"%{domain}%"})
        return rows
    
    def update_fingerprint_quality(
        self,
        fingerprint_id: str,
        quality_score: float,
        status: str
    ):
        """更新指紋質量評分"""
        sql = """
        UPDATE website_fingerprints
        SET confidence_score = %(quality_score)s, status = %(status)s,
            updated_at = %(updated_at)s
        WHERE fingerprint_id = %(fingerprint_id)s
        """
        
        params = {
            'fingerprint_id': fingerprint_id,
            'quality_score': quality_score,
            'status': status,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        self.db.execute(sql, params)
```

---

## 相關文件引用

- **主文檔**: [2.2 詳細功能清單](../ch2-2-詳細功能清單.md)
- **搜尋匹配服務**: [代碼示例 - 指紋匹配](ch2-code-02-fingerprint-matching.md)
- **數據庫架構**: [代碼示例 - 數據庫定義](ch2-code-03-database-schema.md)
- **API 示例**: [代碼示例 - API 端點](ch2-code-04-api-examples.md)
