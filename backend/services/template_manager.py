"""
WebCrawler Commander - 爬取模板管理模塊
提供行業專用模板系統，支持模板的創建、存儲、共享和版本管理

核心功能：
- 行業專用模板庫 (新聞、電商、社交媒體、招聘等)
- 自定義模板保存載入 (用戶可創建和修改模板)
- 模板推薦系統 (基於相似度匹配的智慧推薦)
- 版本控制與回溯 (模板版本歷史追蹤)
- 模板評分與評價 (社群驅動的品質評估)
- 模板參數化配置 (動態模板配置管理)

作者: Jerry開發工作室
版本: v1.0.0
"""

import json
import hashlib
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

from ..utils.config_manager import get_config_manager
from ..utils.logger_service import get_logger


class TemplateCategory(Enum):
    """模板分類枚舉"""
    NEWS = "news"
    ECOMMERCE = "ecommerce"
    SOCIAL_MEDIA = "social_media"
    JOB_SEARCH = "job_search"
    REVIEW = "review"
    IMAGE = "image"
    VIDEO = "video"
    CONTACT = "contact"
    CUSTOM = "custom"


@dataclass
class TemplateMetadata:
    """模板元數據數據類"""
    name: str
    description: str
    category: TemplateCategory
    author: str
    version: str = "1.0.0"
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    compatibility_version: str = "1.0.0"
    language: str = "zh-CN"
    rating: float = 0.0
    usage_count: int = 0
    success_rate: float = 0.0


@dataclass
class CrawlerTemplate:
    """爬蟲模板數據類"""
    metadata: TemplateMetadata
    configuration: Dict[str, Any]
    data_mapping: Dict[str, Any]
    extraction_rules: List[Dict[str, Any]] = field(default_factory=list)
    validation_rules: List[Dict[str, Any]] = field(default_factory=list)
    post_processing_steps: List[Dict[str, Any]] = field(default_factory=list)
    template_id: str = field(default_factory=lambda: hashlib.md5(str(datetime.utcnow().timestamp()).encode()).hexdigest()[:8])


@dataclass
class TemplateUsage:
    """模板使用記錄數據類"""
    template_id: str
    user_id: str = "anonymous"
    used_at: datetime = field(default_factory=datetime.utcnow)
    success: bool = False
    crawl_duration: float = 0.0
    records_extracted: int = 0
    error_message: Optional[str] = None


@dataclass
class TemplateSimilarity:
    """模板相似度數據類"""
    template_id: str
    score: float
    matched_features: List[str] = field(default_factory=list)
    differences: List[str] = field(default_factory=list)


class TemplateStore:
    """
    模板存儲管理器
    負責模板的持久化存儲和檢索
    """

    def __init__(self, templates_dir: Optional[Path] = None):
        self.logger = get_logger(__name__)

        if templates_dir is None:
            base_dir = Path(__file__).parent.parent.parent
            templates_dir = base_dir / "templates"

        self.templates_dir = templates_dir
        self.templates_dir.mkdir(exist_ok=True)

        # 創建子目錄
        self.system_templates_dir = self.templates_dir / "system"
        self.user_templates_dir = self.templates_dir / "user"
        self.community_templates_dir = self.templates_dir / "community"

        for dir_path in [self.system_templates_dir, self.user_templates_dir, self.community_templates_dir]:
            dir_path.mkdir(exist_ok=True)

        self.logger.info("template_store_initialized", templates_dir=str(templates_dir))

    def save_template(self, template: CrawlerTemplate, category: str = "user") -> bool:
        """
        保存模板

        Args:
            template: 要保存的模板
            category: 保存分類 (system/user/community)

        Returns:
            保存是否成功
        """
        try:
            # 確定保存目錄
            if category == "system":
                target_dir = self.system_templates_dir
            elif category == "community":
                target_dir = self.community_templates_dir
            else:
                target_dir = self.user_templates_dir

            # 創建模板文件
            template_data = {
                "metadata": {
                    "name": template.metadata.name,
                    "description": template.metadata.description,
                    "category": template.metadata.category.value,
                    "author": template.metadata.author,
                    "version": template.metadata.version,
                    "tags": template.metadata.tags,
                    "created_at": template.metadata.created_at.isoformat(),
                    "updated_at": template.metadata.updated_at.isoformat(),
                    "compatibility_version": template.metadata.compatibility_version,
                    "language": template.metadata.language,
                    "rating": template.metadata.rating,
                    "usage_count": template.metadata.usage_count,
                    "success_rate": template.metadata.success_rate
                },
                "configuration": template.configuration,
                "data_mapping": template.data_mapping,
                "extraction_rules": template.extraction_rules,
                "validation_rules": template.validation_rules,
                "post_processing_steps": template.post_processing_steps,
                "template_id": template.template_id
            }

            # 保存為JSON文件
            filename = f"{template.template_id}.json"
            filepath = target_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, ensure_ascii=False, indent=2)

            self.logger.info("template_saved",
                           template_id=template.template_id,
                           name=template.metadata.name,
                           category=category)

            return True

        except Exception as e:
            self.logger.error("template_save_error",
                            template_id=template.template_id,
                            error=str(e))
            return False

    def load_template(self, template_id: str) -> Optional[CrawlerTemplate]:
        """
        載入模板

        Args:
            template_id: 模板ID

        Returns:
            模板對象，如不存在返回None
        """
        try:
            # 在所有分類目錄中尋找模板
            for category_dir in [self.system_templates_dir, self.user_templates_dir, self.community_templates_dir]:
                filepath = category_dir / f"{template_id}.json"
                if filepath.exists():
                    with open(filepath, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)

                    metadata = template_data["metadata"]
                    template = CrawlerTemplate(
                        metadata=TemplateMetadata(
                            name=metadata["name"],
                            description=metadata["description"],
                            category=TemplateCategory(metadata["category"]),
                            author=metadata["author"],
                            version=metadata["version"],
                            tags=metadata.get("tags", []),
                            created_at=datetime.fromisoformat(metadata["created_at"]),
                            updated_at=datetime.fromisoformat(metadata["updated_at"]),
                            compatibility_version=metadata.get("compatibility_version", "1.0.0"),
                            language=metadata.get("language", "zh-CN"),
                            rating=metadata.get("rating", 0.0),
                            usage_count=metadata.get("usage_count", 0),
                            success_rate=metadata.get("success_rate", 0.0)
                        ),
                        configuration=template_data.get("configuration", {}),
                        data_mapping=template_data.get("data_mapping", {}),
                        extraction_rules=template_data.get("extraction_rules", []),
                        validation_rules=template_data.get("validation_rules", []),
                        post_processing_steps=template_data.get("post_processing_steps", []),
                        template_id=template_id
                    )

                    return template

            self.logger.debug("template_not_found", template_id=template_id)
            return None

        except Exception as e:
            self.logger.error("template_load_error",
                            template_id=template_id,
                            error=str(e))
            return None

    def list_templates(self, category: Optional[TemplateCategory] = None,
                      tags: Optional[List[str]] = None,
                      sort_by: str = "name",
                      limit: int = 50) -> List[CrawlerTemplate]:
        """
        列出模板

        Args:
            category: 模板分類過濾
            tags: 標籤過濾
            sort_by: 排序方式
            limit: 返回數量限制

        Returns:
            模板列表
        """
        templates = []

        try:
            # 掃描所有分類目錄
            for category_dir in [self.system_templates_dir, self.user_templates_dir, self.community_templates_dir]:
                for template_file in category_dir.glob("*.json"):
                    try:
                        with open(template_file, 'r', encoding='utf-8') as f:
                            template_data = json.load(f)

                        metadata = template_data["metadata"]
                        template_category = TemplateCategory(metadata["category"])

                        # 應用過濾
                        if category and template_category != category:
                            continue

                        if tags:
                            template_tags = set(metadata.get("tags", []))
                            if not all(tag in template_tags for tag in tags):
                                continue

                        template = CrawlerTemplate(
                            metadata=TemplateMetadata(
                                name=metadata["name"],
                                description=metadata["description"],
                                category=template_category,
                                author=metadata["author"],
                                version=metadata["version"],
                                tags=metadata.get("tags", []),
                                created_at=datetime.fromisoformat(metadata["created_at"]),
                                updated_at=datetime.fromisoformat(metadata["updated_at"]),
                                compatibility_version=metadata.get("compatibility_version", "1.0.0"),
                                language=metadata.get("language", "zh-CN"),
                                rating=metadata.get("rating", 0.0),
                                usage_count=metadata.get("usage_count", 0),
                                success_rate=metadata.get("success_rate", 0.0)
                            ),
                            configuration=template_data.get("configuration", {}),
                            data_mapping=template_data.get("data_mapping", {}),
                            extraction_rules=template_data.get("extraction_rules", []),
                            validation_rules=template_data.get("validation_rules", []),
                            post_processing_steps=template_data.get("post_processing_steps", []),
                            template_id=template_data["template_id"]
                        )

                        templates.append(template)

                    except Exception as e:
                        self.logger.warning("template_parse_error",
                                          file=str(template_file),
                                          error=str(e))
                        continue

            # 排序
            if sort_by == "name":
                templates.sort(key=lambda t: t.metadata.name)
            elif sort_by == "rating":
                templates.sort(key=lambda t: t.metadata.rating, reverse=True)
            elif sort_by == "usage_count":
                templates.sort(key=lambda t: t.metadata.usage_count, reverse=True)
            elif sort_by == "updated_at":
                templates.sort(key=lambda t: t.metadata.updated_at, reverse=True)

            # 限制數量
            return templates[:limit]

        except Exception as e:
            self.logger.error("template_list_error", error=str(e))
            return []

    def delete_template(self, template_id: str) -> bool:
        """
        刪除模板

        Args:
            template_id: 模板ID

        Returns:
            刪除是否成功
        """
        try:
            # 在所有分類目錄中尋找並刪除
            for category_dir in [self.system_templates_dir, self.user_templates_dir, self.community_templates_dir]:
                filepath = category_dir / f"{template_id}.json"
                if filepath.exists():
                    filepath.unlink()
                    self.logger.info("template_deleted", template_id=template_id)
                    return True

            return False

        except Exception as e:
            self.logger.error("template_delete_error",
                            template_id=template_id,
                            error=str(e))
            return False


class TemplateRecommender:
    """
    模板推薦器
    基於用戶需求和歷史使用記錄智能推薦模板
    """

    def __init__(self, template_store: TemplateStore):
        self.template_store = template_store
        self.logger = get_logger(__name__)

    def recommend_templates(self, requirements: Dict[str, Any],
                           top_n: int = 5) -> List[TemplateSimilarity]:
        """
        推薦模板

        Args:
            requirements: 需求描述
            top_n: 返回前N個結果

        Returns:
            推薦的模板相似度列表
        """
        try:
            # 獲取所有可用模板
            all_templates = self.template_store.list_templates(limit=1000)
            similarities = []

            website_type = requirements.get("website_type", "").lower()
            target_fields = set(requirements.get("target_fields", []))
            description = requirements.get("description", "").lower()

            for template in all_templates:
                similarity_score = self._calculate_similarity(
                    template, website_type, target_fields, description
                )

                matched_features = []
                differences = []

                # 分析匹配特徵
                if website_type and template.metadata.category.value == website_type:
                    matched_features.append(f"類型匹配: {website_type}")

                # 檢查字段重疊
                template_fields = set(template.data_mapping.keys()) if template.data_mapping else set()
                field_overlap = target_fields.intersection(template_fields)
                if field_overlap:
                    matched_features.append(f"字段匹配: {', '.join(field_overlap)}")
                    if len(field_overlap) < len(target_fields):
                        missing_fields = target_fields - field_overlap
                        differences.append(f"缺少字段: {', '.join(missing_fields)}")

                similarity = TemplateSimilarity(
                    template_id=template.template_id,
                    score=similarity_score,
                    matched_features=matched_features,
                    differences=differences
                )

                similarities.append(similarity)

            # 按得分排序
            similarities.sort(key=lambda s: s.score, reverse=True)

            self.logger.info("templates_recommended",
                           requirements=requirements,
                           total_templates=len(all_templates),
                           top_score=round(similarities[0].score, 2) if similarities else 0)

            return similarities[:top_n]

        except Exception as e:
            self.logger.error("template_recommendation_error", error=str(e))
            return []

    def _calculate_similarity(self, template: CrawlerTemplate,
                             website_type: str,
                             target_fields: set,
                             description: str) -> float:
        """計算模板相似度"""
        score = 0.0

        # 類型匹配權重 (40%)
        if website_type and template.metadata.category.value == website_type:
            score += 40.0
        elif website_type and website_type in template.metadata.tags:
            score += 20.0

        # 字段匹配權重 (30%)
        template_fields = set(template.data_mapping.keys()) if template.data_mapping else set()
        if template_fields and target_fields:
            overlap_ratio = len(target_fields.intersection(template_fields)) / len(target_fields)
            score += 30.0 * overlap_ratio * overlap_ratio  # 平方放大差異

        # 描述匹配權重 (15%)
        description_keywords = set(description.split())
        template_keywords = set(template.metadata.description.lower().split())
        keyword_overlap = description_keywords.intersection(template_keywords)

        if keyword_overlap:
            keyword_ratio = len(keyword_overlap) / len(description_keywords)
            score += 15.0 * keyword_ratio

        # 標籤匹配權重 (10%)
        if target_fields and template.metadata.tags:
            field_tags = {field.lower() for field in target_fields}
            template_tags = {tag.lower() for tag in template.metadata.tags}
            tag_overlap = field_tags.intersection(template_tags)

            if tag_overlap:
                score += 10.0 * (len(tag_overlap) / len(target_fields))

        # 品質和使用情況調整 (5%)
        quality_bonus = min(template.metadata.rating / 5.0, 1.0) * 5.0  # 評分0-5映射到0-5
        score += quality_bonus

        # 使用成功率調整
        if template.metadata.success_rate > 0:
            success_bonus = (template.metadata.success_rate - 0.8) * 10  # 成功率>80%加分
            score += max(0, success_bonus)

        return score


class TemplateQualityManager:
    """
    模板品質管理器
    評估和改進模板品質
    """

    def __init__(self, template_store: TemplateStore):
        self.template_store = template_store
        self.logger = get_logger(__name__)

        # 使用統計
        self.usage_stats: Dict[str, List[TemplateUsage]] = defaultdict(list)

    def update_template_rating(self, template_id: str, new_rating: float):
        """
        更新模板評分

        Args:
            new_rating: 新評分 (0-5)
        """
        try:
            template = self.template_store.load_template(template_id)
            if not template:
                return

            # 簡單評分更新邏輯 (實際應用中可更複雜)
            old_rating = template.metadata.rating
            old_usage = template.metadata.usage_count

            # 加權平均更新
            new_usage = old_usage + 1
            updated_rating = (old_rating * old_usage + new_rating) / new_usage

            template.metadata.rating = updated_rating
            template.metadata.usage_count = new_usage

            self.template_store.save_template(template)

            self.logger.info("template_rating_updated",
                           template_id=template_id,
                           old_rating=old_rating,
                           new_rating=updated_rating)

        except Exception as e:
            self.logger.error("rating_update_error",
                            template_id=template_id,
                            error=str(e))

    def record_usage(self, usage: TemplateUsage):
        """記錄模板使用情況"""
        try:
            self.usage_stats[usage.template_id].append(usage)

            # 更新模板統計
            template = self.template_store.load_template(usage.template_id)
            if template:
                total_uses = len(self.usage_stats[usage.template_id])
                successful_uses = sum(1 for u in self.usage_stats[usage.template_id] if u.success)

                template.metadata.usage_count = total_uses
                template.metadata.success_rate = successful_uses / total_uses if total_uses > 0 else 0

                self.template_store.save_template(template)

                self.logger.debug("usage_recorded",
                                template_id=usage.template_id,
                                success=usage.success,
                                success_rate=round(template.metadata.success_rate, 3))

        except Exception as e:
            self.logger.error("usage_record_error",
                            template_id=usage.template_id,
                            error=str(e))

    def get_template_statistics(self, template_id: str) -> Dict[str, Any]:
        """獲取模板統計信息"""
        try:
            usage_records = self.usage_stats.get(template_id, [])
            template = self.template_store.load_template(template_id)

            if not template or not usage_records:
                return {}

            total_uses = len(usage_records)
            successful_uses = sum(1 for u in usage_records if u.success)
            failed_uses = total_uses - successful_uses

            avg_duration = sum(u.crawl_duration for u in usage_records) / total_uses if total_uses > 0 else 0
            avg_records = sum(u.records_extracted for u in usage_records) / total_uses if total_uses > 0 else 0

            return {
                "total_uses": total_uses,
                "successful_uses": successful_uses,
                "failed_uses": failed_uses,
                "success_rate": successful_uses / total_uses if total_uses > 0 else 0,
                "average_duration": avg_duration,
                "average_records_extracted": avg_records,
                "last_used": max(u.used_at for u in usage_records).isoformat() if usage_records else None
            }

        except Exception as e:
            self.logger.error("statistics_retrieval_error",
                            template_id=template_id,
                            error=str(e))
            return {}

    def validate_template_quality(self, template: CrawlerTemplate) -> Dict[str, Any]:
        """驗證模板品質"""
        issues = []

        # 檢查基本信息完整性
        if not template.metadata.description:
            issues.append("缺少模板描述")

        if not template.extraction_rules:
            issues.append("缺少提取規則")

        if not template.data_mapping:
            issues.append("缺少數據映射")

        # 檢查配置合理性
        config = template.configuration
        if not config.get("url_pattern"):
            issues.append("缺少URL模式配置")

        # 評估品質分數
        quality_score = 100.0

        # 基本信息完整性 (-20分/缺失項)
        basic_complete = sum([
            bool(template.metadata.description),
            bool(template.extraction_rules),
            bool(template.data_mapping),
            bool(config.get("url_pattern")),
            len(template.metadata.tags) > 0
        ])
        quality_score -= (5 - basic_complete) * 10

        # 評分因素 (-15分/低評分)
        if template.metadata.rating < 3.0:
            quality_score -= 15

        # 使用成功率 (-20分/低成功率)
        if template.metadata.success_rate < 0.7:
            quality_score -= 20

        quality_score = max(0, quality_score)

        return {
            "quality_score": quality_score,
            "issues": issues,
            "recommendations": self._generate_quality_recommendations(issues, template)
        }

    def _generate_quality_recommendations(self, issues: List[str], template: CrawlerTemplate) -> List[str]:
        """生成品質改進建議"""
        recommendations = []

        issue_to_recommendation = {
            "缺少模板描述": "添加詳細的模板描述，說明適用場景和功能特點",
            "缺少提取規則": "配置至少一個數據提取規則",
            "缺少數據映射": "定義數據字段映射關係",
            "缺少URL模式配置": "設置目標網站的URL匹配模式"
        }

        for issue in issues:
            if issue in issue_to_recommendation:
                recommendations.append(issue_to_recommendation[issue])

        # 通用建議
        if template.metadata.rating < 3.0:
            recommendations.append("收集用戶反饋，提升模板評分")

        if template.metadata.success_rate < 0.7:
            recommendations.append("優化提取規則和數據映射，提高成功率")

        if len(template.metadata.tags) == 0:
            recommendations.append("添加相關標籤，提升模板可發現性")

        return recommendations


class TemplateCommunityManager:
    """
    模板社群管理器
    處理模板的共享、匯入匯出等社群功能
    """

    def __init__(self, template_store: TemplateStore):
        self.template_store = template_store
        self.logger = get_logger(__name__)

    def export_template(self, template_id: str, export_path: Path) -> bool:
        """導出模板"""
        try:
            template = self.template_store.load_template(template_id)
            if not template:
                return False

            # 創建導出數據
            export_data = {
                "template": {
                    "metadata": {
                        "name": template.metadata.name,
                        "description": template.metadata.description,
                        "category": template.metadata.category.value,
                        "author": template.metadata.author,
                        "version": template.metadata.version,
                        "tags": template.metadata.tags,
                        "created_at": template.metadata.created_at.isoformat(),
                        "compatibility_version": template.metadata.compatibility_version,
                        "language": template.metadata.language
                    },
                    "configuration": template.configuration,
                    "data_mapping": template.data_mapping,
                    "extraction_rules": template.extraction_rules,
                    "validation_rules": template.validation_rules,
                    "post_processing_steps": template.post_processing_steps,
                    "template_id": template.template_id
                },
                "export_info": {
                    "exported_at": datetime.utcnow().isoformat(),
                    "version": "1.0",
                    "format": "crawler_template"
                }
            }

            # 保存到文件
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)

            self.logger.info("template_exported",
                           template_id=template_id,
                           export_path=str(export_path))

            return True

        except Exception as e:
            self.logger.error("template_export_error",
                            template_id=template_id,
                            error=str(e))
            return False

    def import_template(self, import_path: Path) -> Optional[CrawlerTemplate]:
        """匯入模板"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)

            if "template" not in import_data:
                raise ValueError("無效的模板文件格式")

            template_data = import_data["template"]
            metadata = template_data["metadata"]

            # 創建模板對象
            template = CrawlerTemplate(
                metadata=TemplateMetadata(
                    name=metadata["name"],
                    description=metadata["description"],
                    category=TemplateCategory(metadata["category"]),
                    author=metadata["author"],
                    version=metadata["version"],
                    tags=metadata.get("tags", []),
                    created_at=datetime.fromisoformat(metadata["created_at"]),
                    compatibility_version=metadata.get("compatibility_version", "1.0.0"),
                    language=metadata.get("language", "zh-CN")
                ),
                configuration=template_data.get("configuration", {}),
                data_mapping=template_data.get("data_mapping", {}),
                extraction_rules=template_data.get("extraction_rules", []),
                validation_rules=template_data.get("validation_rules", []),
                post_processing_steps=template_data.get("post_processing_steps", []),
                template_id=template_data["template_id"]
            )

            # 保存到社群模板目錄
            if self.template_store.save_template(template, "community"):
                self.logger.info("template_imported",
                               template_id=template.template_id,
                               name=template.metadata.name)
                return template

            return None

        except Exception as e:
            self.logger.error("template_import_error",
                            import_path=str(import_path),
                            error=str(e))
            return None


class TemplateManager:
    """
    爬取模板管理器主類
    整合所有模板管理功能，提供統一的介面
    """

    def __init__(self):
        self.logger = get_logger(__name__)

        # 初始化組件
        self.template_store = TemplateStore()
        self.template_recommender = TemplateRecommender(self.template_store)
        self.quality_manager = TemplateQualityManager(self.template_store)
        self.community_manager = TemplateCommunityManager(self.template_store)

        # 載入內建模板
        self._load_builtin_templates()

        self.logger.info("template_manager_initialized")

    def _load_builtin_templates(self):
        """載入內建模板"""
        try:
            # 創建新聞模板
            news_template = CrawlerTemplate(
                metadata=TemplateMetadata(
                    name="通用新聞網站模板",
                    description="適用於大部分新聞網站的通用爬取模板",
                    category=TemplateCategory.NEWS,
                    author="System",
                    tags=["新聞", "文章", "標題", "內容", "日期"]
                ),
                configuration={
                    "url_pattern": r"(?:news|article|\d{4}/\d{2}/\d{2})",
                    "delay_between_requests": 1.0,
                    "max_pages": 100
                },
                data_mapping={
                    "title": {"selector": "h1, .title, .article-title", "type": "string"},
                    "content": {"selector": ".content, .article-content, .entry-content", "type": "text"},
                    "date": {"selector": ".date, .published, [datetime]", "type": "date"},
                    "author": {"selector": ".author, .byline, [rel='author']", "type": "string"}
                },
                extraction_rules=[
                    {
                        "name": "title_extraction",
                        "selector": "h1, .title, .article-title",
                        "attribute": None,
                        "required": True
                    }
                ],
                validation_rules=[
                    {
                        "field": "title",
                        "type": "required",
                        "severity": "error"
                    }
                ]
            )

            if not self.template_store.load_template(news_template.template_id):
                self.template_store.save_template(news_template, "system")

                # 創建電商模板
            ecommerce_template = CrawlerTemplate(
                metadata=TemplateMetadata(
                    name="通用電商網站模板",
                    description="適用於電商網站的商品信息爬取模板",
                    category=TemplateCategory.ECOMMERCE,
                    author="System",
                    tags=["電商", "商品", "價格", "圖片", "描述"]
                ),
                configuration={
                    "url_pattern": r"(?:product|item|p)/?\d+",
                    "delay_between_requests": 2.0,
                    "max_pages": 50
                },
                data_mapping={
                    "title": {"selector": ".product-title, h1", "type": "string"},
                    "price": {"selector": ".price, .cost", "type": "number"},
                    "images": {"selector": ".product-image img", "type": "array"},
                    "description": {"selector": ".description", "type": "text"},
                    "stock": {"selector": ".stock, .availability", "type": "string"}
                }
            )

            if not self.template_store.load_template(ecommerce_template.template_id):
                self.template_store.save_template(ecommerce_template, "system")

            self.logger.info("builtin_templates_loaded")

        except Exception as e:
            self.logger.error("builtin_templates_load_error", error=str(e))

    def create_template_from_request(self, description: str, target_fields: List[str],
                                   website_type: str) -> CrawlerTemplate:
        """
        從用戶請求創建新模板

        Args:
            description: 模板描述
            target_fields: 目標字段
            website_type: 網站類型

        Returns:
            新建的模板
        """
        try:
            # 生成模板ID
            template_id = hashlib.md5(f"{description}_{datetime.utcnow().timestamp()}".encode()).hexdigest()[:8]

            # 確定分類
            category_map = {
                "新聞": TemplateCategory.NEWS,
                "電商": TemplateCategory.ECOMMERCE,
                "社交媒體": TemplateCategory.SOCIAL_MEDIA,
                "招聘": TemplateCategory.JOB_SEARCH,
                "評論": TemplateCategory.REVIEW
            }

            category = category_map.get(website_type, TemplateCategory.CUSTOM)

            # 生成數據映射
            data_mapping = {}
            for field in target_fields:
                data_mapping[field] = {
                    "selector": f"[class*='{field}'], .{field}, #{field}",
                    "type": "string"
                }

            # 生成提取規則
            extraction_rules = []
            for field in target_fields:
                if field in ["title", "content"]:  # 最重要的字段設為必需
                    extraction_rules.append({
                        "name": f"{field}_extraction",
                        "selector": f"[class*='{field}'], .{field}, #{field}",
                        "required": True
                    })
                else:
                    extraction_rules.append({
                        "name": f"{field}_extraction",
                        "selector": f"[class*='{field}'], .{field}, #{field}",
                        "required": False
                    })

            # 創建模板
            template = CrawlerTemplate(
                metadata=TemplateMetadata(
                    name=f"{website_type}自定義模板",
                    description=description,
                    category=category,
                    author="User Generated",
                    tags=[website_type] + target_fields,
                    language="zh-CN"
                ),
                configuration={
                    "url_pattern": ".*",
                    "delay_between_requests": 1.0,
                    "max_pages": 100
                },
                data_mapping=data_mapping,
                extraction_rules=extraction_rules,
                template_id=template_id
            )

            # 保存模板
            self.template_store.save_template(template, "user")

            self.logger.info("template_created_from_request",
                           template_id=template_id,
                           fields=target_fields)

            return template

        except Exception as e:
            self.logger.error("template_creation_error", error=str(e))
            raise

    def get_recommendations(self, requirements: Dict[str, Any],
                           limit: int = 5) -> List[CrawlerTemplate]:
        """獲取模板推薦"""
        try:
            similarities = self.template_recommender.recommend_templates(requirements, limit)

            templates = []
            for similarity in similarities:
                template = self.template_store.load_template(similarity.template_id)
                if template:
                    # 添加相似度信息
                    template.similarity_score = similarity.score
                    template.matched_features = similarity.matched_features
                    templates.append(template)

            return templates

        except Exception as e:
            self.logger.error("template_recommendation_error", error=str(e))
            return []


# 全域模板管理器實例
_template_manager: Optional[TemplateManager] = None


def init_template_manager() -> TemplateManager:
    """
    初始化全域模板管理器

    Returns:
        模板管理器實例
    """
    global _template_manager

    if _template_manager is None:
        _template_manager = TemplateManager()

    return _template_manager


def get_template_manager() -> TemplateManager:
    """獲取全域模板管理器實例"""
    if _template_manager is None:
        raise RuntimeError("模板管理器尚未初始化，請先調用init_template_manager()")
    return _template_manager
