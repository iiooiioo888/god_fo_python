# CH3 代碼示例 - 3.3 告警和報警系統

## 告警服務實現

```python
import logging
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

class AlertLevel(Enum):
    """告警級別"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AlertService:
    """告警和報警服務"""
    
    def __init__(
        self,
        db: 'Database',
        notification_service: 'NotificationService',
        config: Dict
    ):
        self.db = db
        self.notification_service = notification_service
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 告警配置
        self.alert_thresholds = config.get('alert_thresholds', {})
        self.alert_channels = config.get('alert_channels', {
            'email': True,
            'slack': True,
            'dingtalk': False
        })
    
    async def send_alert(
        self,
        alert_data: Dict
    ) -> str:
        """
        發送告警
        
        Args:
            alert_data: 告警數據
                {
                    'level': 'critical',
                    'datasource_id': 'ds_001',
                    'message': '資料源不可用',
                    'metrics': {...}
                }
                
        Returns:
            告警 ID
        """
        try:
            # 1. 創建告警記錄
            alert_id = self._create_alert_record(alert_data)
            
            # 2. 檢查告警規則
            should_send, channels = self._check_alert_rules(alert_data, alert_id)
            
            if should_send:
                # 3. 發送通知
                tasks = []
                
                if channels.get('email'):
                    tasks.append(self._send_email_alert(alert_data, alert_id))
                
                if channels.get('slack'):
                    tasks.append(self._send_slack_alert(alert_data, alert_id))
                
                if channels.get('dingtalk'):
                    tasks.append(self._send_dingtalk_alert(alert_data, alert_id))
                
                if tasks:
                    await asyncio.gather(*tasks)
            
            self.logger.info(f"Alert {alert_id} sent successfully")
            return alert_id
            
        except Exception as e:
            self.logger.error(f"Failed to send alert: {str(e)}")
            raise
    
    def _create_alert_record(self, alert_data: Dict) -> str:
        """建立告警記錄"""
        import uuid
        alert_id = f"alert-{uuid.uuid4().hex[:8]}"
        
        sql = """
        INSERT INTO alerts (
            alert_id, datasource_id, level, message, metrics,
            created_at, status
        ) VALUES (
            %(alert_id)s, %(datasource_id)s, %(level)s, %(message)s,
            %(metrics)s, %(created_at)s, 'active'
        )
        """
        
        params = {
            'alert_id': alert_id,
            'datasource_id': alert_data.get('datasource_id'),
            'level': alert_data.get('level', 'info'),
            'message': alert_data.get('message'),
            'metrics': json.dumps(alert_data.get('metrics', {})),
            'created_at': datetime.utcnow().isoformat()
        }
        
        self.db.execute(sql, params)
        return alert_id
    
    def _check_alert_rules(self, alert_data: Dict, alert_id: str) -> tuple:
        """檢查告警規則"""
        level = alert_data.get('level', 'info')
        datasource_id = alert_data.get('datasource_id')
        
        # 獲取告警規則
        rules = self.db.fetchall(
            "SELECT * FROM alert_rules WHERE datasource_id = %s OR datasource_id IS NULL",
            (datasource_id,)
        )
        
        should_send = True
        channels = self.alert_channels.copy()
        
        for rule in rules:
            # 檢查規則條件
            if rule.get('enabled') and self._match_rule(alert_data, rule):
                # 應用規則
                channels = {
                    'email': rule.get('email_enabled', True),
                    'slack': rule.get('slack_enabled', True),
                    'dingtalk': rule.get('dingtalk_enabled', False)
                }
                break
        
        return should_send, channels
    
    def _match_rule(self, alert_data: Dict, rule: Dict) -> bool:
        """檢查告警規則是否匹配"""
        # 簡化實現
        level = alert_data.get('level')
        rule_level = rule.get('level')
        
        level_order = {'info': 0, 'warning': 1, 'error': 2, 'critical': 3}
        return level_order.get(level, 0) >= level_order.get(rule_level, 0)
    
    async def _send_email_alert(self, alert_data: Dict, alert_id: str):
        """發送郵件告警"""
        try:
            await self.notification_service.send_email({
                'to': self._get_alert_recipients(alert_data),
                'subject': f"[{alert_data.get('level').upper()}] 資料源告警",
                'body': self._format_alert_message(alert_data, alert_id)
            })
        except Exception as e:
            self.logger.error(f"Email alert failed: {str(e)}")
    
    async def _send_slack_alert(self, alert_data: Dict, alert_id: str):
        """發送 Slack 告警"""
        try:
            await self.notification_service.send_slack({
                'channel': '#data-alerts',
                'message': self._format_slack_alert(alert_data, alert_id)
            })
        except Exception as e:
            self.logger.error(f"Slack alert failed: {str(e)}")
    
    async def _send_dingtalk_alert(self, alert_data: Dict, alert_id: str):
        """發送釘釘告警"""
        try:
            await self.notification_service.send_dingtalk({
                'message': self._format_dingtalk_alert(alert_data, alert_id)
            })
        except Exception as e:
            self.logger.error(f"DingTalk alert failed: {str(e)}")
    
    def _get_alert_recipients(self, alert_data: Dict) -> List[str]:
        """獲取告警接收者"""
        datasource_id = alert_data.get('datasource_id')
        
        # 查詢資料源所有者
        datasource = self.db.fetchone(
            "SELECT owner_id FROM data_sources WHERE id = %s",
            (datasource_id,)
        )
        
        if datasource:
            owner = self.db.fetchone(
                "SELECT email FROM users WHERE id = %s",
                (datasource.get('owner_id'),)
            )
            if owner:
                return [owner.get('email')]
        
        return []
    
    def _format_alert_message(self, alert_data: Dict, alert_id: str) -> str:
        """格式化告警郵件"""
        return f"""
告警 ID: {alert_id}
級別: {alert_data.get('level')}
資料源: {alert_data.get('datasource_id')}
消息: {alert_data.get('message')}
時間: {datetime.utcnow().isoformat()}
指標: {json.dumps(alert_data.get('metrics', {}), indent=2)}
        """
    
    def _format_slack_alert(self, alert_data: Dict, alert_id: str) -> Dict:
        """格式化 Slack 告警"""
        return {
            'text': alert_data.get('message'),
            'attachments': [{
                'color': self._get_alert_color(alert_data.get('level')),
                'fields': [
                    {'title': '告警 ID', 'value': alert_id, 'short': True},
                    {'title': '級別', 'value': alert_data.get('level'), 'short': True},
                    {'title': '資料源', 'value': alert_data.get('datasource_id'), 'short': True},
                ]
            }]
        }
    
    def _format_dingtalk_alert(self, alert_data: Dict, alert_id: str) -> Dict:
        """格式化釘釘告警"""
        return {
            'msgtype': 'markdown',
            'markdown': {
                'title': f"[{alert_data.get('level').upper()}] 資料源告警",
                'text': f"""
## 資料源告警

- **告警 ID**: {alert_id}
- **級別**: {alert_data.get('level')}
- **資料源**: {alert_data.get('datasource_id')}
- **消息**: {alert_data.get('message')}
- **時間**: {datetime.utcnow().isoformat()}
                """
            }
        }
    
    def _get_alert_color(self, level: str) -> str:
        """獲取告警顏色"""
        colors = {
            'info': '#36a64f',
            'warning': '#ff9900',
            'error': '#ff6666',
            'critical': '#ff0000'
        }
        return colors.get(level, '#cccccc')
```

---

## 告警規則引擎

```python
class AlertRuleEngine:
    """告警規則引擎"""
    
    def __init__(self, db: 'Database', config: Dict):
        self.db = db
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def create_alert_rule(
        self,
        datasource_id: str,
        rule_config: Dict,
        user_id: str
    ) -> str:
        """建立告警規則"""
        import uuid
        rule_id = f"rule-{uuid.uuid4().hex[:8]}"
        
        sql = """
        INSERT INTO alert_rules (
            rule_id, datasource_id, name, level, condition,
            email_enabled, slack_enabled, dingtalk_enabled,
            created_by, created_at
        ) VALUES (
            %(rule_id)s, %(datasource_id)s, %(name)s, %(level)s,
            %(condition)s, %(email)s, %(slack)s, %(dingtalk)s,
            %(user_id)s, %(created_at)s
        )
        """
        
        params = {
            'rule_id': rule_id,
            'datasource_id': datasource_id,
            'name': rule_config.get('name'),
            'level': rule_config.get('level', 'warning'),
            'condition': json.dumps(rule_config.get('condition', {})),
            'email': rule_config.get('email_enabled', True),
            'slack': rule_config.get('slack_enabled', True),
            'dingtalk': rule_config.get('dingtalk_enabled', False),
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat()
        }
        
        self.db.execute(sql, params)
        return rule_id
```

---

## 相關文件引用

- **核心監測**: [代碼示例 - 健康監測](ch3-code-01-health-monitor.md)
- **數據庫架構**: [代碼示例 - 數據庫定義](ch3-code-03-database-schema.md)
- **API 示例**: [代碼示例 - API 端點](ch3-code-04-api-examples.md)
