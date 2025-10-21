"""
WebCrawler Commander - 數據品質管控模塊
實現全面的數據驗證、檢查和品質評估系統

核心功能：
- 結構驗證 (Schema Validation) - 數據結構完整性檢查
- 業務規則檢查 (Business Rules Validation) - 領域邏輯驗證
- 數據完整性驗證 (Data Integrity Checks) - 參考完整性和一致性
- 數據格式標準化 (Format Normalization) - 統一數據表示格式
- 品質評分系統 (Quality Scoring) - 多維度品質評估

作者: Jerry開發工作室
版本: v1.0.0
"""

import re
import hashlib
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, Counter
from pathlib import Path

from ..utils.config_manager import get_config_manager
from ..utils.logger_service import get_logger


class ValidationSeverity(Enum):
    """驗證嚴重程度枚舉"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class DataQualityDimension(Enum):
    """數據品質維度枚舉"""
    COMPLETENESS = "completeness"      # 完整性
    ACCURACY = "accuracy"             # 準確性
    CONSISTENCY = "consistency"       # 一致性
    TIMELINESS = "timeliness"         # 及時性
    UNIQUENESS = "uniqueness"         # 唯一性
    VALIDITY = "validity"            # 有效性


@dataclass
class ValidationIssue:
    """驗證問題數據類"""
    field: str
    issue_type: str
    severity: ValidationSeverity
    message: str
    value: Optional[Any] = None
    suggested_value: Optional[Any] = None
    rule_name: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class DataQualityScore:
    """數據品質評分數據類"""
    total_score: float = 0.0
    dimension_scores: Dict[DataQualityDimension, float] = field(default_factory=dict)
    issue_count: int = 0
    issue_breakdown: Dict[ValidationSeverity, int] = field(default_factory=dict)
    validated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ValidationRule:
    """驗證規則數據類"""
    name: str
    rule_type: str
    severity: ValidationSeverity
    condition: str
    message_template: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    target_fields: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def apply(self, data: Dict[str, Any]) -> List[ValidationIssue]:
        """應用驗證規則"""
        raise NotImplementedError("子類必須實現此方法")


@dataclass
class ValidationResult:
    """驗證結果數據類"""
    is_valid: bool
    issues: List[ValidationIssue]
    quality_score: DataQualityScore
    processed_records: int = 0
    validation_time: float = 0.0
    rules_applied: int = 0


class DataStructureValidator:
    """
    數據結構驗證器
    檢查數據的結構完整性和類型一致性
    """

    def __init__(self):
        self.logger = get_logger(__name__)

    def validate_structure(self, data: Dict[str, Any], schema: Dict[str, Any]) -> List[ValidationIssue]:
        """
        驗證數據結構

        Args:
            data: 要驗證的數據
            schema: 數據結構模式

        Returns:
            驗證問題列表
        """
        issues = []

        try:
            # 檢查必需字段
            required_fields = schema.get('required', [])
            for field in required_fields:
                if field not in data or data[field] is None or (isinstance(data[field], str) and not data[field].strip()):
                    issues.append(ValidationIssue(
                        field=field,
                        issue_type="missing_required_field",
                        severity=ValidationSeverity.ERROR,
                        message=f"必需字段 '{field}' 為空或缺失",
                        value=data.get(field)
                    ))

            # 檢查字段類型
            field_types = schema.get('properties', {})
            for field, field_schema in field_types.items():
                if field in data and data[field] is not None:
                    type_issues = self._validate_field_type(field, data[field], field_schema)
                    issues.extend(type_issues)

            # 檢查字段範圍
            for field, field_schema in field_types.items():
                if field in data and data[field] is not None:
                    range_issues = self._validate_field_range(field, data[field], field_schema)
                    issues.extend(range_issues)

            # 檢查枚舉值
            for field, field_schema in field_types.items():
                if field in data and data[field] is not None:
                    enum_issues = self._validate_enum_values(field, data[field], field_schema)
                    issues.extend(enum_issues)

        except Exception as e:
            self.logger.error("structure_validation_error", error=str(e))
            issues.append(ValidationIssue(
                field="",
                issue_type="validation_error",
                severity=ValidationSeverity.CRITICAL,
                message=f"結構驗證過程發生錯誤: {str(e)}"
            ))

        return issues

    def _validate_field_type(self, field: str, value: Any, field_schema: Dict[str, Any]) -> List[ValidationIssue]:
        """驗證字段類型"""
        issues = []
        expected_type = field_schema.get('type')

        if not expected_type:
            return issues

        # 類型映射
        type_checks = {
            'string': lambda v: isinstance(v, str),
            'number': lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
            'integer': lambda v: isinstance(v, int) and not isinstance(v, bool),
            'boolean': lambda v: isinstance(v, bool),
            'array': lambda v: isinstance(v, list),
            'object': lambda v: isinstance(v, dict)
        }

        expected_check = type_checks.get(expected_type)
        if expected_check and not expected_check(value):
            issues.append(ValidationIssue(
                field=field,
                issue_type="type_mismatch",
                severity=ValidationSeverity.ERROR,
                message=f"字段 '{field}' 類型不正確，期望 {expected_type}，實際為 {type(value).__name__}",
                value=value
            ))

        return issues

    def _validate_field_range(self, field: str, value: Any, field_schema: Dict[str, Any]) -> List[ValidationIssue]:
        """驗證字段範圍"""
        issues = []
        constraints = field_schema.get('constraints', {})

        # 字符串長度檢查
        if isinstance(value, str):
            min_length = constraints.get('min_length')
            max_length = constraints.get('max_length')

            if min_length and len(value) < min_length:
                issues.append(ValidationIssue(
                    field=field,
                    issue_type="string_too_short",
                    severity=ValidationSeverity.WARNING,
                    message=f"字段 '{field}' 長度過短，至少需要 {min_length} 個字符",
                    value=value
                ))

            if max_length and len(value) > max_length:
                issues.append(ValidationIssue(
                    field=field,
                    issue_type="string_too_long",
                    severity=ValidationSeverity.WARNING,
                    message=f"字段 '{field}' 長度過長，最多允許 {max_length} 個字符",
                    value=value,
                    suggested_value=value[:max_length] + "..."
                ))

        # 數值範圍檢查
        elif isinstance(value, (int, float)):
            minimum = constraints.get('minimum')
            maximum = constraints.get('maximum')

            if minimum is not None and value < minimum:
                issues.append(ValidationIssue(
                    field=field,
                    issue_type="value_too_low",
                    severity=ValidationSeverity.WARNING,
                    message=f"字段 '{field}' 值過小，最小允許值為 {minimum}",
                    value=value,
                    suggested_value=minimum
                ))

            if maximum is not None and value > maximum:
                issues.append(ValidationIssue(
                    field=field,
                    issue_type="value_too_high",
                    severity=ValidationSeverity.WARNING,
                    message=f"字段 '{field}' 值過大，最大允許值為 {maximum}",
                    value=value,
                    suggested_value=maximum
                ))

        return issues

    def _validate_enum_values(self, field: str, value: Any, field_schema: Dict[str, Any]) -> List[ValidationIssue]:
        """驗證枚舉值"""
        issues = []
        enum_values = field_schema.get('enum')

        if enum_values and value not in enum_values:
            # 查找最相似的建議值
            suggested_value = self._find_closest_match(value, enum_values) if isinstance(value, str) else None

            issues.append(ValidationIssue(
                field=field,
                issue_type="invalid_enum_value",
                severity=ValidationSeverity.ERROR,
                message=f"字段 '{field}' 的值 '{value}' 不在允許的枚舉值中",
                value=value,
                suggested_value=suggested_value
            ))

        return issues

    def _find_closest_match(self, value: str, candidates: List[str]) -> Optional[str]:
        """查找最相似的字串"""
        if not candidates:
            return None

        # 簡單的Levenshtein距離實現
        def levenshtein_distance(s1: str, s2: str) -> int:
            if len(s1) < len(s2):
                return levenshtein_distance(s2, s1)

            if len(s2) == 0:
                return len(s1)

            previous_row = list(range(len(s2) + 1))
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row

            return previous_row[-1]

        # 查找最小距離的候選值
        closest = min(candidates, key=lambda x: levenshtein_distance(value.lower(), x.lower()))
        distance = levenshtein_distance(value.lower(), closest.lower())

        # 如果距離太遠，不建議
        if distance > len(value) // 2:
            return None

        return closest


class BusinessRulesValidator:
    """
    業務規則驗證器
    應用領域特定的業務邏輯規則
    """

    def __init__(self):
        self.logger = get_logger(__name__)
        self._custom_rules: Dict[str, Callable] = {}

    def add_custom_rule(self, name: str, rule_func: Callable):
        """添加自定義驗證規則"""
        self._custom_rules[name] = rule_func

    def validate_business_rules(self, data: Dict[str, Any], rules: List[Dict[str, Any]]) -> List[ValidationIssue]:
        """
        驗證業務規則

        Args:
            data: 要驗證的數據
            rules: 業務規則列表

        Returns:
            驗證問題列表
        """
        issues = []

        for rule in rules:
            try:
                rule_issues = self._apply_business_rule(data, rule)
                issues.extend(rule_issues)
            except Exception as e:
                self.logger.warning("business_rule_application_error",
                                  rule_name=rule.get('name', 'unknown'),
                                  error=str(e))
                issues.append(ValidationIssue(
                    field=rule.get('target_field', ''),
                    issue_type="rule_execution_error",
                    severity=ValidationSeverity.WARNING,
                    message=f"業務規則 '{rule.get('name', 'unknown')}' 執行失敗: {str(e)}",
                    rule_name=rule.get('name')
                ))

        return issues

    def _apply_business_rule(self, data: Dict[str, Any], rule: Dict[str, Any]) -> List[ValidationIssue]:
        """應用單個業務規則"""
        issues = []
        rule_type = rule.get('type')
        rule_name = rule.get('name', 'unnamed_rule')

        if rule_type == 'dependency':
            issues.extend(self._check_dependency_rule(data, rule))
        elif rule_type == 'range_comparison':
            issues.extend(self._check_range_comparison_rule(data, rule))
        elif rule_type == 'format_validation':
            issues.extend(self._check_format_validation_rule(data, rule))
        elif rule_type == 'cross_field_validation':
            issues.extend(self._check_cross_field_validation_rule(data, rule))
        elif rule_type == 'custom' and rule_name in self._custom_rules:
            issues.extend(self._custom_rules[rule_name](data, rule))
        else:
            issues.append(ValidationIssue(
                field=rule.get('target_field', ''),
                issue_type="unknown_rule_type",
                severity=ValidationSeverity.WARNING,
                message=f"未知的規則類型: {rule_type}",
                rule_name=rule_name,
                value=rule_type
            ))

        return issues

    def _check_dependency_rule(self, data: Dict[str, Any], rule: Dict[str, Any]) -> List[ValidationIssue]:
        """檢查依賴規則"""
        issues = []
        primary_field = rule.get('primary_field')
        dependent_field = rule.get('dependent_field')
        condition = rule.get('condition', 'exists')

        if not primary_field or not dependent_field:
            return issues

        primary_value = data.get(primary_field)
        dependent_value = data.get(dependent_field)

        if condition == 'exists' and primary_value and not dependent_value:
            issues.append(ValidationIssue(
                field=dependent_field,
                issue_type="missing_dependent_field",
                severity=ValidationSeverity.ERROR,
                message=f"字段 '{dependent_field}' 依賴於 '{primary_field}'，但 '{primary_field}' 存在時必須提供",
                rule_name=rule.get('name'),
                value=dependent_value
            ))

        return issues

    def _check_range_comparison_rule(self, data: Dict[str, Any], rule: Dict[str, Any]) -> List[ValidationIssue]:
        """檢查範圍比較規則"""
        issues = []
        field1 = rule.get('field1')
        field2 = rule.get('field2')
        comparison = rule.get('comparison', 'lt')

        if not field1 or not field2:
            return issues

        value1 = data.get(field1)
        value2 = data.get(field2)

        if value1 is None or value2 is None:
            return issues

        try:
            comparisons = {
                'lt': lambda a, b: a < b,
                'le': lambda a, b: a <= b,
                'gt': lambda a, b: a > b,
                'ge': lambda a, b: a >= b,
                'eq': lambda a, b: a == b
            }

            if comparison in comparisons and not comparisons[comparison](value1, value2):
                operator_names = {
                    'lt': '小於', 'le': '小於等於', 'gt': '大於',
                    'ge': '大於等於', 'eq': '等於'
                }

                issues.append(ValidationIssue(
                    field=field1,
                    issue_type="range_comparison_failed",
                    severity=ValidationSeverity.ERROR,
                    message=f"字段 '{field1}' ({value1}) 必須{operator_names.get(comparison, comparison)} '{field2}' ({value2})",
                    rule_name=rule.get('name'),
                    value=value1
                ))

        except (TypeError, ValueError):
            pass  # 如果值不能比較，跳過

        return issues

    def _check_format_validation_rule(self, data: Dict[str, Any], rule: Dict[str, Any]) -> List[ValidationIssue]:
        """檢查格式驗證規則"""
        issues = []
        target_field = rule.get('target_field')
        pattern = rule.get('pattern')
        format_type = rule.get('format_type')

        if not target_field:
            return issues

        value = data.get(target_field)
        if value is None:
            return issues

        if not isinstance(value, str):
            value = str(value)

        # 使用正則表達式模式
        if pattern:
            try:
                if not re.match(pattern, value):
                    issues.append(ValidationIssue(
                        field=target_field,
                        issue_type="format_validation_failed",
                        severity=ValidationSeverity.ERROR,
                        message=f"字段 '{target_field}' 格式不符合規則: {rule.get('description', '無效格式')}",
                        rule_name=rule.get('name'),
                        value=value
                    ))
            except re.error:
                self.logger.warning("invalid_regex_pattern",
                                  pattern=pattern,
                                  rule_name=rule.get('name'))

        # 預定義格式類型
        elif format_type:
            if format_type == 'email':
                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
                    issues.append(ValidationIssue(
                        field=target_field,
                        issue_type="invalid_email",
                        severity=ValidationSeverity.ERROR,
                        message=f"字段 '{target_field}' 不是有效的郵箱地址",
                        rule_name=rule.get('name'),
                        value=value
                    ))

        return issues

    def _check_cross_field_validation_rule(self, data: Dict[str, Any], rule: Dict[str, Any]) -> List[ValidationIssue]:
        """檢查跨字段驗證規則"""
        issues = []
        fields = rule.get('fields', [])
        operation = rule.get('operation', 'sum')

        if len(fields) < 2:
            return issues

        values = []
        missing_fields = []

        for field in fields:
            value = data.get(field)
            if value is None:
                missing_fields.append(field)
            else:
                try:
                    values.append(float(value))
                except (ValueError, TypeError):
                    missing_fields.append(field)

        if missing_fields:
            return issues  # 如果有字段缺失，先跳過

        try:
            # 應用操作
            if operation == 'sum':
                result = sum(values)
            elif operation == 'product':
                result = 1
                for v in values:
                    result *= v
            elif operation == 'average':
                result = statistics.mean(values)
            else:
                return issues

            # 檢查結果條件
            expected_result = rule.get('expected_result')
            if expected_result is not None:
                tolerance = rule.get('tolerance', 0.01)

                if not (abs(result - expected_result) <= tolerance):
                    issues.append(ValidationIssue(
                        field=fields[0],
                        issue_type="cross_field_validation_failed",
                        severity=ValidationSeverity.WARNING,
                        message=f"字段組合驗證失敗: {fields} 的 {operation} 結果應為 {expected_result}，實際為 {result:.2f}",
                        rule_name=rule.get('name'),
                        value=result
                    ))

        except (ZeroDivisionError, OverflowError):
            issues.append(ValidationIssue(
                field=fields[0],
                issue_type="cross_field_calculation_error",
                severity=ValidationSeverity.WARNING,
                message=f"字段組合計算錯誤: {operation} 操作失敗",
                rule_name=rule.get('name')
            ))

        return issues


class DataIntegrityValidator:
    """
    數據完整性驗證器
    確保數據參考完整性和邏輯一致性
    """

    def __init__(self):
        self.logger = get_logger(__name__)
        self._reference_data: Dict[str, set] = defaultdict(set)

    def set_reference_data(self, reference_name: str, data: List[Any]):
        """設置參考數據"""
        self._reference_data[reference_name] = set(data)

    def validate_referential_integrity(self, data: Dict[str, Any],
                                     integrity_rules: List[Dict[str, Any]]) -> List[ValidationIssue]:
        """
        驗證參考完整性

        Args:
            data: 要驗證的數據
            integrity_rules: 完整性規則列表

        Returns:
            驗證問題列表
        """
        issues = []

        for rule in integrity_rules:
            try:
                rule_type = rule.get('type')

                if rule_type == 'foreign_key':
                    issues.extend(self._check_foreign_key(data, rule))
                elif rule_type == 'unique_constraint':
                    issues.extend(self._check_unique_constraint(data, rule))
                elif rule_type == 'check_constraint':
                    issues.extend(self._check_check_constraint(data, rule))

            except Exception as e:
                self.logger.warning("integrity_rule_error",
                                  rule_name=rule.get('name', 'unknown'),
                                  error=str(e))

        return issues

    def _check_foreign_key(self, data: Dict[str, Any], rule: Dict[str, Any]) -> List[ValidationIssue]:
        """檢查外鍵約束"""
        issues = []
        field = rule.get('field')
        reference_table = rule.get('reference_table')
        reference_field = rule.get('reference_field', field)

        if not field or not reference_table:
            return issues

        value = data.get(field)
        if value is None:
            return issues  # NULL值允許

        reference_set = self._reference_data.get(reference_table)
        if reference_set is None:
            issues.append(ValidationIssue(
                field=field,
                issue_type="reference_data_not_found",
                severity=ValidationSeverity.CRITICAL,
                message=f"字段 '{field}' 的參考數據 '{reference_table}' 未設置",
                rule_name=rule.get('name'),
                value=value
            ))
            return issues

        # 這裡應該檢查值是否存在於參考數據中
        # 注意：實際情況中，這通常需要查詢數據庫
        # 這裡僅做簡單的集合檢查示例

        if value not in reference_set:
            issues.append(ValidationIssue(
                field=field,
                issue_type="foreign_key_violation",
                severity=ValidationSeverity.ERROR,
                message=f"字段 '{field}' 的值 '{value}' 在參考表 '{reference_table}' 中不存在",
                rule_name=rule.get('name'),
                value=value
            ))

        return issues

    def _check_unique_constraint(self, data: Dict[str, Any], rule: Dict[str, Any]) -> List[ValidationIssue]:
        """檢查唯一性約束"""
        issues = []
        fields = rule.get('fields', [])
        scope = rule.get('scope', 'global')  # global 或 record_set

        if not fields:
            return issues

        # 對於每個字段組合創建鍵
        key_parts = []
        for field in fields:
            value = data.get(field)
            if value is not None:
                key_parts.append(str(value))
            else:
                key_parts.append('')  # 將NULL視為空字符串

        key = '|'.join(key_parts)

        # 在實際應用中，這裡會檢查數據庫或記錄集中的唯一性
        # 這裡只是示例邏輯

        if len(fields) == 1 and data.get(fields[0]) is None:
            return issues  # NULL值通常不參與唯一性檢查

        # 模擬發現重複（實際實現會查詢數據庫）
        # 這裡只是為了展示邏輯

        return issues  # 在實際實現中會添加重複檢查邏輯

    def _check_check_constraint(self, data: Dict[str, Any], rule: Dict[str, Any]) -> List[ValidationIssue]:
        """檢查檢查約束"""
        issues = []
        expression = rule.get('expression')
        field = rule.get('field')

        if not expression:
            return issues

        # 簡單的表達式評估（在實際應用中應該更安全）
        try:
            # 創建安全的評估上下文
            safe_dict = dict(data)  # 淺拷貝
            safe_dict.update({
                'len': len,
                'sum': sum,
                'min': min,
                'max': max,
                'abs': abs
            })

            result = eval(expression, {"__builtins__": {}}, safe_dict)

            if not result:
                issues.append(ValidationIssue(
                    field=field or rule.get('target_field', ''),
                    issue_type="check_constraint_violation",
                    severity=ValidationSeverity.ERROR,
                    message=f"檢查約束失敗: {rule.get('description', expression)}",
                    rule_name=rule.get('name'),
                    value=result
                ))

        except Exception as e:
            issues.append(ValidationIssue(
                field=field or rule.get('target_field', ''),
                issue_type="constraint_evaluation_error",
                severity=ValidationSeverity.WARNING,
                message=f"檢查約束評估錯誤: {str(e)}",
                rule_name=rule.get('name')
            ))

        return issues


class FormatNormalizer:
    """
    格式標準化器
    統一數據表示格式，提升一致性
    """

    def __init__(self):
        self.logger = get_logger(__name__)

    def normalize_data(self, data: Dict[str, Any], format_rules: Dict[str, Any]) -> Tuple[Dict[str, Any], List[ValidationIssue]]:
        """
        標準化數據格式

        Args:
            data: 要標準化的數據
            format_rules: 格式規則

        Returns:
            (標準化後的數據, 警告列表)
        """
        normalized_data = {}
        warnings = []

        try:
            for field, value in data.items():
                if value is None:
                    normalized_data[field] = value
                    continue

                field_rules = format_rules.get(field, {})

                # 字符串標準化
                if isinstance(value, str):
                    normalized_data[field] = self._normalize_string(value, field_rules)
                # 數值標準化
                elif isinstance(value, (int, float)):
                    normalized_data[field] = self._normalize_number(value, field_rules)
                # 日期時間標準化
                elif isinstance(value, (datetime, str)) and field_rules.get('type') == 'datetime':
                    normalized_data[field], field_warnings = self._normalize_datetime(value, field_rules)
                    warnings.extend(field_warnings)
                else:
                    normalized_data[field] = value

        except Exception as e:
            self.logger.error("data_normalization_error", error=str(e))
            warnings.append(ValidationIssue(
                field="",
                issue_type="normalization_error",
                severity=ValidationSeverity.WARNING,
                message=f"數據標準化過程發生錯誤: {str(e)}"
            ))

        return normalized_data, warnings

    def _normalize_string(self, value: str, rules: Dict[str, Any]) -> str:
        """標準化字符串"""
        normalized = value.strip()

        # 大小寫標準化
        case_rule = rules.get('case')
        if case_rule == 'upper':
            normalized = normalized.upper()
        elif case_rule == 'lower':
            normalized = normalized.lower()
        elif case_rule == 'title':
            normalized = normalized.title()

        # Unicode規範化
        if rules.get('unicode_normalize'):
            import unicodedata
            normalized = unicodedata.normalize('NFC', normalized)

        # 移除多餘空白
        if rules.get('collapse_whitespace', True):
            import re
            normalized = re.sub(r'\s+', ' ', normalized)

        return normalized

    def _normalize_number(self, value: Union[int, float], rules: Dict[str, Any]) -> Union[int, float]:
        """標準化數值"""
        if not isinstance(value, (int, float)):
            return value

        # 精度控制
        precision = rules.get('precision')
        if precision is not None and isinstance(value, float):
            value = round(value, precision)

        # 範圍約束
        min_val = rules.get('min')
        max_val = rules.get('max')

        if min_val is not None:
            value = max(value, min_val)
        if max_val is not None:
            value = min(value, max_val)

        return value

    def _normalize_datetime(self, value: Union[str, datetime], rules: Dict[str, Any]) -> Tuple[Optional[str], List[ValidationIssue]]:
        """標準化日期時間"""
        warnings = []

        try:
            import dateutil.parser

            if isinstance(value, str):
                parsed_dt = dateutil.parser.parse(value)
            elif isinstance(value, datetime):
                parsed_dt = value
            else:
                warnings.append(ValidationIssue(
                    field="",
                    issue_type="datetime_parse_error",
                    severity=ValidationSeverity.WARNING,
                    message=f"無法解析日期時間值: {value}"
                ))
                return None, warnings

            # 格式化為指定格式
            output_format = rules.get('format', 'ISO')
            if output_format == 'ISO':
                normalized = parsed_dt.isoformat()
            elif output_format == 'timestamp':
                normalized = str(int(parsed_dt.timestamp()))
            else:
                normalized = parsed_dt.strftime(output_format)

            return normalized, warnings

        except Exception as e:
            warnings.append(ValidationIssue(
                field="",
                issue_type="datetime_normalization_error",
                severity=ValidationSeverity.WARNING,
                message=f"日期時間標準化失敗: {str(e)}",
                value=value
            ))
            return None, warnings


class QualityScorer:
    """
    品質評分器
    多維度數據品質評估系統
    """

    def __init__(self):
        self.logger = get_logger(__name__)

    def calculate_quality_score(self, data_list: List[Dict[str, Any]],
                               validation_issues: List[ValidationIssue]) -> DataQualityScore:
        """
        計算數據品質評分

        Args:
            data_list: 數據記錄列表
            validation_issues: 驗證問題列表

        Returns:
            品質評分結果
        """
        if not data_list:
            return DataQualityScore()

        score = DataQualityScore()
        total_records = len(data_list)

        # 統計驗證問題
        issue_count = len(validation_issues)
        issue_breakdown = defaultdict(int)

        for issue in validation_issues:
            issue_breakdown[issue.severity] += 1

        score.issue_count = issue_count
        score.issue_breakdown = dict(issue_breakdown)

        # 計算各維度分數
        dimensions = {
            DataQualityDimension.COMPLETENESS: self._calculate_completeness(data_list),
            DataQualityDimension.ACCURACY: self._calculate_accuracy(validation_issues, total_records),
            DataQualityDimension.CONSISTENCY: self._calculate_consistency(data_list),
            DataQualityDimension.TIMELINESS: self._calculate_timeliness(data_list),
            DataQualityDimension.UNIQUENESS: self._calculate_uniqueness(data_list),
            DataQualityDimension.VALIDITY: self._calculate_validity(validation_issues, total_records)
        }

        score.dimension_scores = {dim: func_score for dim, func_score in dimensions.items()}

        # 計算總體分數
        weights = {
            DataQualityDimension.COMPLETENESS: 0.25,
            DataQualityDimension.ACCURACY: 0.25,
            DataQualityDimension.CONSISTENCY: 0.15,
            DataQualityDimension.VALIDITY: 0.15,
            DataQualityDimension.UNIQUENESS: 0.10,
            DataQualityDimension.TIMELINESS: 0.10
        }

        total_score = 0.0
        for dimension, weight in weights.items():
            total_score += score.dimension_scores[dimension] * weight

        score.total_score = max(0.0, min(100.0, total_score))

        self.logger.debug("quality_score_calculated",
                         total_records=total_records,
                         issues=issue_count,
                         dimensions=[(d.value, f"{s:.1f}") for d, s in score.dimension_scores.items()],
                         final_score=f"{score.total_score:.1f}")

        return score

    def _calculate_completeness(self, data_list: List[Dict[str, Any]]) -> float:
        """計算完整性分數"""
        if not data_list:
            return 0.0

        # 收集所有字段
        all_fields = set()
        for record in data_list:
            all_fields.update(record.keys())

        if not all_fields:
            return 100.0

        total_fields = len(all_fields)
        total_checks = len(data_list) * total_fields
        filled_fields = 0

        for record in data_list:
            for field in all_fields:
                value = record.get(field)
                if value is not None and (not isinstance(value, str) or value.strip()):
                    filled_fields += 1

        completeness = (filled_fields / total_checks) * 100 if total_checks > 0 else 100.0
        return completeness

    def _calculate_accuracy(self, issues: List[ValidationIssue], total_records: int) -> float:
        """計算準確性分數"""
        error_issues = [issue for issue in issues if issue.severity in (ValidationSeverity.ERROR, ValidationSeverity.CRITICAL)]
        error_count = len(error_issues)

        # 基於錯誤密度計算準確性
        if error_count == 0:
            return 100.0

        # 簡單的錯誤密度計算（可根據具體需求調整）
        error_density = error_count / total_records

        accuracy = max(0.0, 100.0 - (error_density * 200))  # 每個錯誤降低2分，最多降低到0
        return accuracy

    def _calculate_consistency(self, data_list: List[Dict[str, Any]]) -> float:
        """計算一致性分數"""
        if len(data_list) < 2:
            return 100.0

        # 分析字段類型一致性
        field_type_consistency = self._analyze_field_type_consistency(data_list)

        # 分析值範圍一致性（對於數值字段）
        field_range_consistency = self._analyze_field_range_consistency(data_list)

        # 綜合評分
        consistency_score = (field_type_consistency * 0.7) + (field_range_consistency * 0.3)
        return consistency_score

    def _analyze_field_type_consistency(self, data_list: List[Dict[str, Any]]) -> float:
        """分析字段類型一致性"""
        if not data_list:
            return 100.0

        # 統計每個字段的類型分佈
        field_types = defaultdict(Counter)

        for record in data_list:
            for field, value in record.items():
                if value is not None:
                    type_name = type(value).__name__
                    field_types[field][type_name] += 1

        # 計算類型一致性
        total_consistency = 0
        field_count = len(field_types)

        for field, type_counts in field_types.items():
            total_values = sum(type_counts.values())
            if total_values > 0:
                most_common_count = max(type_counts.values())
                field_consistency = (most_common_count / total_values) * 100
                total_consistency += field_consistency

        return total_consistency / field_count if field_count > 0 else 100.0

    def _analyze_field_range_consistency(self, data_list: List[Dict[str, Any]]) -> float:
        """分析字段範圍一致性"""
        # 簡化的範圍一致性分析（實際實現可更複雜）
        return 85.0  # 固定值，實際應基於數據統計計算

    def _calculate_timeliness(self, data_list: List[Dict[str, Any]]) -> float:
        """計算及時性分數"""
        # 簡化的及時性評估（實際應檢查數據的新鮮度）
        return 90.0

    def _calculate_uniqueness(self, data_list: List[Dict[str, Any]]) -> float:
        """計算唯一性分數"""
        if not data_list:
            return 100.0

        # 簡單的重複記錄檢測
        unique_records = len(set(json.dumps(record, sort_keys=True, default=str) for record in data_list))
        uniqueness = (unique_records / len(data_list)) * 100 if data_list else 100.0

        return uniqueness

    def _calculate_validity(self, issues: List[ValidationIssue], total_records: int) -> float:
        """計算有效性分數"""
        critical_issues = [issue for issue in issues if issue.severity == ValidationSeverity.CRITICAL]
        error_issues = [issue for issue in issues if issue.severity == ValidationSeverity.ERROR]

        total_issues = len(critical_issues) + len(error_issues)

        if total_issues == 0:
            return 100.0

        # 計算有效性分數
        validity_penalty = min(total_issues / total_records * 100, 100.0)
        validity = max(0.0, 100.0 - validity_penalty)

        return validity


class DataValidator:
    """
    數據驗證器主類
    整合所有驗證功能，提供統一的數據品質管控介面
    """

    def __init__(self):
        self.logger = get_logger(__name__)

        # 初始化組件
        self.structure_validator = DataStructureValidator()
        self.business_rules_validator = BusinessRulesValidator()
        self.integrity_validator = DataIntegrityValidator()
        self.format_normalizer = FormatNormalizer()
        self.quality_scorer = QualityScorer()

        # 載入配置
        self.config = get_config_manager().get("validator", {})
        self.validation_schemas = self.config.get("schemas", {})

    async def validate_data(self, data: Union[Dict[str, Any], List[Dict[str, Any]]],
                           schema_name: Optional[str] = None,
                           business_rules: Optional[List[Dict[str, Any]]] = None,
                           integrity_rules: Optional[List[Dict[str, Any]]] = None,
                           format_rules: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """
        全面數據驗證入口

        Args:
            data: 要驗證的數據（單個記錄或記錄列表）
            schema_name: 結構模式名稱
            business_rules: 業務規則列表
            integrity_rules: 完整性規則列表
            format_rules: 格式標準化規則

        Returns:
            驗證結果
        """
        import time
        start_time = time.time()

        # 確保數據是列表格式
        if isinstance(data, dict):
            data_list = [data]
        elif isinstance(data, list):
            data_list = data
        else:
            raise ValueError("數據必須是字典或字典列表")

        all_issues = []
        processed_records = len(data_list)

        try:
            # 1. 結構驗證
            schema = self.validation_schemas.get(schema_name, self.config.get("default_schema", {})) if schema_name else {}
            for record in data_list:
                structure_issues = self.structure_validator.validate_structure(record, schema)
                all_issues.extend(structure_issues)

            # 2. 業務規則驗證
            if business_rules:
                for record in data_list:
                    business_issues = self.business_rules_validator.validate_business_rules(record, business_rules)
                    all_issues.extend(business_issues)

            # 3. 完整性驗證
            if integrity_rules:
                for record in data_list:
                    integrity_issues = self.integrity_validator.validate_referential_integrity(record, integrity_rules)
                    all_issues.extend(integrity_issues)

            # 4. 格式標準化（可選）
            normalized_data = {}
            if format_rules:
                for i, record in enumerate(data_list):
                    normalized, format_warnings = self.format_normalizer.normalize_data(record, format_rules)
                    normalized_data[i] = normalized
                    # 將格式化警告轉換為驗證問題
                    for warning in format_warnings:
                        all_issues.append(ValidationIssue(
                            field=warning.field,
                            issue_type=warning.issue_type,
                            severity=warning.severity,
                            message=warning.message
                        ))

            # 5. 品質評分
            quality_score = self.quality_scorer.calculate_quality_score(data_list, all_issues)

            # 構建結果
            is_valid = not any(issue.severity in (ValidationSeverity.ERROR, ValidationSeverity.CRITICAL)
                             for issue in all_issues)

            result = ValidationResult(
                is_valid=is_valid,
                issues=all_issues,
                quality_score=quality_score,
                processed_records=processed_records,
                validation_time=time.time() - start_time,
                rules_applied=len(schema.get('properties', {})) +
                            (len(business_rules) if business_rules else 0) +
                            (len(integrity_rules) if integrity_rules else 0)
            )

            self.logger.info("data_validation_completed",
                           records_processed=processed_records,
                           issues_found=len(all_issues),
                           is_valid=is_valid,
                           quality_score=round(quality_score.total_score, 2))

            return result

        except Exception as e:
            self.logger.error("data_validation_error", error=str(e))
            return ValidationResult(
                is_valid=False,
                issues=[ValidationIssue(
                    field="",
                    issue_type="validation_system_error",
                    severity=ValidationSeverity.CRITICAL,
                    message=f"驗證系統錯誤: {str(e)}"
                )],
                quality_score=DataQualityScore(),
                processed_records=processed_records,
                validation_time=time.time() - start_time
            )

    def add_validation_schema(self, name: str, schema: Dict[str, Any]):
        """添加驗證模式"""
        self.validation_schemas[name] = schema
        self.logger.info("validation_schema_added", schema_name=name)

    def get_validation_schemas(self) -> Dict[str, Dict[str, Any]]:
        """獲取所有驗證模式"""
        return self.validation_schemas.copy()

    def get_quality_report(self, validation_result: ValidationResult) -> Dict[str, Any]:
        """生成品質報告"""
        report = {
            "summary": {
                "records_processed": validation_result.processed_records,
                "is_valid": validation_result.is_valid,
                "total_issues": len(validation_result.issues),
                "processing_time_seconds": round(validation_result.validation_time, 3)
            },
            "quality_score": {
                "overall_score": round(validation_result.quality_score.total_score, 2),
                "dimension_scores": {
                    dim.value: round(score, 2)
                    for dim, score in validation_result.quality_score.dimension_scores.items()
                },
                "issue_breakdown": validation_result.quality_score.issue_breakdown
            },
            "issues": [
                {
                    "field": issue.field,
                    "type": issue.issue_type,
                    "severity": issue.severity.value,
                    "message": issue.message,
                    "value": issue.value,
                    "suggested_value": issue.suggested_value
                }
                for issue in validation_result.issues[:50]  # 限制返回數量
            ],
            "recommendations": self._generate_recommendations(validation_result)
        }

        return report

    def _generate_recommendations(self, result: ValidationResult) -> List[str]:
        """生成改進建議"""
        recommendations = []

        quality = result.quality_score

        # 基於整體品質評分
        if quality.total_score < 60:
            recommendations.append("數據品質嚴重不足，建議重新評估數據採集流程")

        # 基於維度分數
        if quality.dimension_scores.get(DataQualityDimension.COMPLETENESS, 100) < 80:
            recommendations.append("數據完整性不高，補充缺失字段值")

        if quality.dimension_scores.get(DataQualityDimension.ACCURACY, 100) < 80:
            recommendations.append("數據準確性需要改進，檢查數據來源和處理邏輯")

        if quality.dimension_scores.get(DataQualityDimension.CONSISTENCY, 100) < 80:
            recommendations.append("數據一致性不足，統一字段格式和類型")

        # 基於問題數量
        if result.quality_score.issue_count > result.processed_records:
            recommendations.append("發現大量數據問題，建議實施自動化數據清理")

        return recommendations


# 全域數據驗證器實例
_data_validator: Optional[DataValidator] = None


def init_data_validator() -> DataValidator:
    """
    初始化全域數據驗證器

    Returns:
        數據驗證器實例
    """
    global _data_validator

    if _data_validator is None:
        _data_validator = DataValidator()

    return _data_validator


def get_data_validator() -> DataValidator:
    """獲取全域數據驗證器實例"""
    if _data_validator is None:
        raise RuntimeError("數據驗證器尚未初始化，請先調用init_data_validator()")
    return _data_validator
