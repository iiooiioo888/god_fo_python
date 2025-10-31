# CH7 代碼示例 - 7.2 資料合規與安全中心實現

## 合規性引擎

```python
import asyncio
import logging
from typing import Dict, List, Any
from datetime import datetime
import hashlib
import json

class ComplianceEngine:
    """合規性檢查引擎"""
    
    def __init__(self, db: 'Database', config: Dict):
        self.db = db
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.checkers = self._init_checkers()
    
    def _init_checkers(self):
        """初始化檢查器"""
        return {
            'gdpr': GDPRChecker(),
            'ccpa': CCPAChecker(),
            'pii': PIIDetector(),
            'encryption': EncryptionValidator()
        }
    
    async def check_compliance(
        self,
        data_source_id: str,
        data: Dict
    ) -> Dict[str, Any]:
        """檢查數據合規性"""
        results = {}
        
        for checker_name, checker in self.checkers.items():
            try:
                result = await checker.check(data)
                results[checker_name] = {
                    'passed': result.get('passed', False),
                    'issues': result.get('issues', []),
                    'timestamp': datetime.utcnow().isoformat()
                }
            except Exception as e:
                self.logger.error(f"Checker {checker_name} failed: {str(e)}")
                results[checker_name] = {'passed': False, 'error': str(e)}
        
        # 保存檢查結果
        await self._save_compliance_record(data_source_id, results)
        
        return results
    
    async def _save_compliance_record(self, data_source_id: str, results: Dict):
        """保存合規性檢查記錄"""
        sql = """
        INSERT INTO compliance_records (
            data_source_id, check_results, passed, created_at
        ) VALUES (
            %(data_source_id)s, %(check_results)s, %(passed)s, %(created_at)s
        )
        """
        
        passed = all(r.get('passed', False) for r in results.values())
        
        self.db.execute(sql, {
            'data_source_id': data_source_id,
            'check_results': json.dumps(results),
            'passed': passed,
            'created_at': datetime.utcnow().isoformat()
        })

class GDPRChecker:
    """GDPR 合規檢查"""
    
    async def check(self, data: Dict) -> Dict:
        """檢查 GDPR 合規性"""
        issues = []
        
        # 檢查個人數據最小化
        if not self._verify_data_minimization(data):
            issues.append("未遵循數據最小化原則")
        
        # 檢查用戶同意
        if not data.get('user_consent'):
            issues.append("缺少用戶同意記錄")
        
        # 檢查數據保留期
        if not self._verify_retention_policy(data):
            issues.append("數據保留期不符合規定")
        
        return {
            'passed': len(issues) == 0,
            'issues': issues
        }
    
    def _verify_data_minimization(self, data: Dict) -> bool:
        """驗證數據最小化"""
        required_fields = ['user_id', 'created_at']
        return all(field in data for field in required_fields)
    
    def _verify_retention_policy(self, data: Dict) -> bool:
        """驗證保留政策"""
        return 'retention_period' in data

class CCPAChecker:
    """CCPA 合規檢查"""
    
    async def check(self, data: Dict) -> Dict:
        """檢查 CCPA 合規性"""
        issues = []
        
        # 檢查數據訪問權限
        if not self._verify_access_rights(data):
            issues.append("未提供數據訪問接口")
        
        # 檢查刪除權
        if not self._verify_deletion_capability(data):
            issues.append("未支持數據刪除功能")
        
        return {
            'passed': len(issues) == 0,
            'issues': issues
        }
    
    def _verify_access_rights(self, data: Dict) -> bool:
        return 'access_api_endpoint' in data
    
    def _verify_deletion_capability(self, data: Dict) -> bool:
        return 'deletion_supported' in data

class PIIDetector:
    """個人身份信息檢測"""
    
    async def check(self, data: Dict) -> Dict:
        """檢測 PII 數據"""
        pii_found = []
        
        # 檢測電子郵件
        if self._detect_email(data):
            pii_found.append("檢測到電子郵件")
        
        # 檢測電話號碼
        if self._detect_phone(data):
            pii_found.append("檢測到電話號碼")
        
        # 檢測身份證號
        if self._detect_id_number(data):
            pii_found.append("檢測到身份證號")
        
        return {
            'passed': len(pii_found) == 0,
            'pii_types': pii_found
        }
    
    def _detect_email(self, data: Dict) -> bool:
        import re
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        data_str = json.dumps(data)
        return bool(re.search(email_pattern, data_str))
    
    def _detect_phone(self, data: Dict) -> bool:
        import re
        phone_pattern = r'\b\d{10,11}\b'
        data_str = json.dumps(data)
        return bool(re.search(phone_pattern, data_str))
    
    def _detect_id_number(self, data: Dict) -> bool:
        # 身份證號檢測
        return False

class EncryptionValidator:
    """加密驗證器"""
    
    async def check(self, data: Dict) -> Dict:
        """驗證加密狀態"""
        issues = []
        
        # 檢查傳輸加密
        if not self._verify_transport_encryption(data):
            issues.append("傳輸未加密")
        
        # 檢查存儲加密
        if not self._verify_storage_encryption(data):
            issues.append("存儲未加密")
        
        return {
            'passed': len(issues) == 0,
            'issues': issues
        }
    
    def _verify_transport_encryption(self, data: Dict) -> bool:
        return data.get('encryption_method') in ['TLS', 'SSL']
    
    def _verify_storage_encryption(self, data: Dict) -> bool:
        return data.get('storage_encrypted', False)
```

---

## 相關文件引用

- **主文檔**: [7.2 詳細功能清單](../ch7-2-詳細功能清單.md)
- **數據庫**: [代碼示例 - 數據庫定義](ch7-code-02-database-schema.md)
- **API 示例**: [代碼示例 - API 端點](ch7-code-03-api-examples.md)
