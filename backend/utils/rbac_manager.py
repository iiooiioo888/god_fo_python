"""
WebCrawler Commander - RBAC權限管理器
企業級角色基於存取控制系統

功能特色：
- 角色與權限的靈活配置
- 動態權限檢查與執行
- 多層級權限繼承
- 會話管理與令牌驗證
- 安全策略與規範執行
- 實時權限稽核

作者: Jerry開發工作室
版本: v1.0.0
"""

import asyncio
import hashlib
import secrets
import time
from typing import Dict, List, Optional, Any, Set, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import jwt

from .config_manager import get_config_manager
from .logger_service import get_logger
from .error_handler import get_error_handler, with_error_handling, RecoveryStrategy, RecoveryConfig, ErrorContext
from .performance_monitor import get_performance_monitor, performance_monitor, benchmark_operation
from .audit_logger import get_audit_logger, audit_log, AuditLevel, AuditCategory


class Permission(Enum):
    """系統權限枚舉"""
    # 數據訪問權限
    READ_DATA = "read_data"
    WRITE_DATA = "write_data"
    DELETE_DATA = "delete_data"
    EXPORT_DATA = "export_data"

    # 系統管理權限
    CREATE_USER = "create_user"
    DELETE_USER = "delete_user"
    MANAGE_USERS = "manage_users"
    MANAGE_ROLES = "manage_roles"

    # 爬蟲操作權限
    CREATE_CRAWLER = "create_crawler"
    RUN_CRAWLER = "run_crawler"
    STOP_CRAWLER = "stop_crawler"
    DELETE_CRAWLER = "delete_crawler"

    # 系統監控權限
    VIEW_METRICS = "view_metrics"
    VIEW_LOGS = "view_logs"
    SYSTEM_ADMIN = "system_admin"

    # 數據處理權限
    PROCESS_DATA = "process_data"
    MANAGE_PIPELINES = "manage_pipelines"


class Role(Enum):
    """系統角色枚舉"""
    GUEST = "guest"
    USER = "user"
    ANALYST = "analyst"
    DATA_ENGINEER = "data_engineer"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


@dataclass
class RoleDefinition:
    """角色定義"""
    name: str
    permissions: Set[Permission] = field(default_factory=set)
    description: str = ""
    inherits_from: Optional[str] = None
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class User:
    """用戶對象"""
    user_id: str
    username: str
    email: str
    roles: Set[str] = field(default_factory=set)
    permissions: Set[Permission] = field(default_factory=set)
    is_active: bool = True
    last_login: Optional[datetime] = None
    session_token: Optional[str] = None
    session_expires: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Session:
    """會話對象"""
    session_id: str
    user_id: str
    token: str
    expires_at: datetime
    permissions: Set[Permission] = field(default_factory=set)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AccessRequest:
    """存取請求"""
    user_id: str
    resource: str
    action: Permission
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


class AccessDecision(Enum):
    """存取決策"""
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_2FA = "require_2fa"


class RBACManager:
    """
    RBAC權限管理器

    提供企業級權限管理功能：
    - 角色與權限的靈活配置
    - 動態權限檢查與執行
    - 多層級權限繼承
    - 會話管理與令牌驗證
    - 安全策略與規範執行
    - 實時權限稽核
    """

    def __init__(self, config_manager=None):
        self.config_manager = config_manager or get_config_manager()
        self.logger = get_logger(__name__)

        # 初始化統一框架組件
        self.error_handler = get_error_handler(__name__)
        self.performance_monitor = get_performance_monitor(__name__)
        self.audit_logger = get_audit_logger()

        # 角色和權限存儲
        self.roles: Dict[str, RoleDefinition] = {}
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, Session] = {}

        # 配置
        self.config = self.config_manager.get("rbac", {})
        self.jwt_secret = self.config.get("jwt_secret", secrets.token_hex(32))
        self.session_timeout = self.config.get("session_timeout_minutes", 480)  # 8小時

        # 權限快取
        self.permission_cache: Dict[str, Dict[str, bool]] = {}
        self.cache_timeout = self.config.get("cache_timeout_seconds", 300)

        # 統計信息
        self.stats = {
            "total_users": 0,
            "active_sessions": 0,
            "permission_checks": 0,
            "access_denied": 0,
            "access_allowed": 0
        }

        # 初始化內建角色
        self._initialize_builtin_roles()

        # 設置錯誤恢復
        self._setup_error_recovery()

        # 設置性能基準
        self._setup_performance_benchmarks()

        # 啟動背景清理任務
        self._start_background_cleanup()

        self.logger.info("rbac_manager_initialized")

    def _initialize_builtin_roles(self):
        """初始化內建角色"""

        # Guest角色 - 最少權限
        guest_role = RoleDefinition(
            name=Role.GUEST.value,
            permissions={Permission.READ_DATA},
            description="訪客用戶，僅能查看公共數據",
            is_active=True
        )
        self.roles[Role.GUEST.value] = guest_role

        # User角色 - 基本用戶權限
        user_role = RoleDefinition(
            name=Role.USER.value,
            permissions={
                Permission.READ_DATA,
                Permission.CREATE_CRAWLER,
                Permission.RUN_CRAWLER,
                Permission.STOP_CRAWLER,
                Permission.PROCESS_DATA
            },
            description="普通用戶，可以進行基本數據處理",
            inherts_from=Role.GUEST.value,
            is_active=True
        )
        self.roles[Role.USER.value] = user_role

        # Analyst角色 - 分析師權限
        analyst_role = RoleDefinition(
            name=Role.ANALYST.value,
            permissions={
                Permission.EXPORT_DATA,
                Permission.VIEW_METRICS,
                Permission.VIEW_LOGS,
                Permission.MANAGE_PIPELINES
            },
            description="數據分析師，可以導出數據和查看系統指標",
            inherits_from=Role.USER.value,
            is_active=True
        )
        self.roles[Role.ANALYST.value] = analyst_role

        # Data Engineer角色 - 數據工程師權限
        engineer_role = RoleDefinition(
            name=Role.DATA_ENGINEER.value,
            permissions={
                Permission.WRITE_DATA,
                Permission.DELETE_DATA,
                Permission.DELETE_CRAWLER
            },
            description="數據工程師，可以修改和刪除數據",
            inherits_from=Role.ANALYST.value,
            is_active=True
        )
        self.roles[Role.DATA_ENGINEER.value] = engineer_role

        # Admin角色 - 管理員權限
        admin_role = RoleDefinition(
            name=Role.ADMIN.value,
            permissions={
                Permission.CREATE_USER,
                Permission.DELETE_USER,
                Permission.MANAGE_USERS,
                Permission.MANAGE_ROLES,
                Permission.SYSTEM_ADMIN
            },
            description="系統管理員，可以管理用戶和角色",
            inherits_from=Role.DATA_ENGINEER.value,
            is_active=True
        )
        self.roles[Role.ADMIN.value] = admin_role

        # Super Admin角色 - 超級管理員權限
        super_admin_role = RoleDefinition(
            name=Role.SUPER_ADMIN.value,
            permissions=set(),  # 擁有所有權限
            description="超級管理員，擁有系統全部權限",
            inherits_from=Role.ADMIN.value,
            is_active=True
        )
        self.roles[Role.SUPER_ADMIN.value] = super_admin_role

    def _setup_error_recovery(self):
        """設置錯誤恢復配置"""
        # 權限檢查錯誤恢復
        permission_error_config = RecoveryConfig(
            strategy=RecoveryStrategy.RETRY,
            max_retries=2
        )
        self.error_handler.register_recovery_config("permission_check", permission_error_config)

        # 認證錯誤恢復
        auth_error_config = RecoveryConfig(
            strategy=RecoveryStrategy.DENY
        )
        self.error_handler.register_recovery_config("authentication_error", auth_error_config)

    def _setup_performance_benchmarks(self):
        """設置性能基準"""
        # 權限檢查響應時間基準
        self.performance_monitor.set_benchmark(
            "permission_check_time_ms",
            50.0,  # 50毫秒内完成檢查
            tolerance_percent=50,
            environment="production"
        )

        # 會話創建時間基準
        self.performance_monitor.set_benchmark(
            "session_creation_time_ms",
            100.0,  # 100毫秒内創建會話
            tolerance_percent=30,
            environment="production"
        )

    def _start_background_cleanup(self):
        """啟動背景清理任務"""
        # 使用線程定期清理過期會話和快取
        import threading

        def cleanup_worker():
            while True:
                try:
                    self._cleanup_expired_sessions()
                    self._cleanup_cache()
                    time.sleep(300)  # 每5分鐘清理一次
                except Exception as e:
                    self.logger.warning("cleanup_worker_error", error=str(e))

        cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        cleanup_thread.start()

    def _cleanup_expired_sessions(self):
        """清理過期會話"""
        now = datetime.utcnow()
        expired_sessions = []

        for session_id, session in self.sessions.items():
            if session.expires_at < now:
                expired_sessions.append(session_id)

        for session_id in expired_sessions:
            del self.sessions[session_id]

        if expired_sessions:
            self.logger.info("expired_sessions_cleaned", count=len(expired_sessions))

    def _cleanup_cache(self):
        """清理過期快取"""
        # 簡單的快取清理邏輯
        # 實際實現會有更複雜的LRU策略
        pass

    def create_user(self, username: str, email: str, roles: Optional[List[str]] = None) -> User:
        """
        創建用戶

        Args:
            username: 用戶名
            email: 郵箱
            roles: 角色列表

        Returns:
            用戶對象
        """
        if username in [user.username for user in self.users.values()]:
            raise ValueError(f"用戶名 {username} 已經存在")

        user_id = f"user_{secrets.token_hex(8)}"
        user = User(
            user_id=user_id,
            username=username,
            email=email,
            roles=set(roles or [Role.GUEST.value]),
            is_active=True
        )

        # 計算用戶權限
        user.permissions = self._calculate_user_permissions(user)

        self.users[user_id] = user
        self.stats["total_users"] = len(self.users)

        audit_log(
            level=AuditLevel.ACTION,
            category=AuditCategory.DATA_ACCESS,
            action="user_created",
            actor="system",
            target=user_id,
            result="SUCCESS",
            details={"username": username, "roles": list(user.roles)}
        )

        self.logger.info("user_created", user_id=user_id, username=username)
        return user

    def authenticate_user(self, username: str, password: str) -> Optional[str]:
        """
        認證用戶

        Args:
            username: 用戶名
            password: 密碼

        Returns:
            會話令牌，如果認證成功
        """
        # 注意：這是簡化的認證實現
        # 生產環境應該使用安全的密碼哈希和數據庫

        for user in self.users.values():
            if user.username == username and user.is_active:
                # 創建會話
                session_token = self._create_session(user.user_id)
                user.last_login = datetime.utcnow()

                audit_log(
                    level=AuditLevel.ACTION,
                    category=AuditCategory.DATA_ACCESS,
                    action="user_authenticated",
                    actor=user.user_id,
                    target="authentication",
                    result="SUCCESS",
                    details={"username": username}
                )

                return session_token

        audit_log(
            level=AuditLevel.SECURITY,
            category=AuditCategory.SECURITY_EVENT,
            action="authentication_failed",
            actor="unknown",
            target="authentication",
            result="FAILED",
            details={"username": username}
        )

        return None

    def _create_session(self, user_id: str, ip_address: str = None) -> str:
        """
        創建會話

        Args:
            user_id: 用戶ID
            ip_address: IP地址

        Returns:
            會話令牌
        """
        session_id = f"session_{secrets.token_hex(16)}"
        expires_at = datetime.utcnow() + timedelta(minutes=self.session_timeout)

        user = self.users.get(user_id)
        if not user:
            raise ValueError(f"用戶 {user_id} 不存在")

        session = Session(
            session_id=session_id,
            user_id=user_id,
            token=self._generate_jwt_token(session_id, user_id, expires_at),
            expires_at=expires_at,
            permissions=user.permissions.copy(),
            ip_address=ip_address
        )

        self.sessions[session_id] = session
        self.stats["active_sessions"] = len(self.sessions)

        self.logger.debug("session_created", session_id=session_id, user_id=user_id)
        return session.token

    def _generate_jwt_token(self, session_id: str, user_id: str, expires_at: datetime) -> str:
        """生成JWT令牌"""
        payload = {
            "session_id": session_id,
            "user_id": user_id,
            "exp": int(expires_at.timestamp()),
            "iat": int(datetime.utcnow().timestamp())
        }

        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")

    def _calculate_user_permissions(self, user: User) -> Set[Permission]:
        """計算用戶權限"""
        permissions = set()

        # 從角色繼承權限
        for role_name in user.roles:
            role_perms = self._get_role_permissions(role_name)
            permissions.update(role_perms)

        return permissions

    def _get_role_permissions(self, role_name: str) -> Set[Permission]:
        """獲取角色權限（包括繼承）"""
        permissions = set()
        visited_roles = set()

        def collect_permissions(role: str):
            if role in visited_roles:
                return  # 避免循環依賴

            visited_roles.add(role)

            role_def = self.roles.get(role)
            if not role_def or not role_def.is_active:
                return

            # 添加角色權限
            permissions.update(role_def.permissions)

            # 處理權限繼承
            if role_def.inherits_from:
                collect_permissions(role_def.inherits_from)

        collect_permissions(role_name)
        return permissions

    @performance_monitor
    @benchmark_operation("permission_check", expected_max_time_ms=50)
    @with_error_handling("permission_check")
    async def check_permission(self, token: str, resource: str, action: Permission,
                              context: Optional[Dict[str, Any]] = None) -> AccessDecision:
        """
        檢查權限

        Args:
            token: 會話令牌
            resource: 資源
            action: 權限動作
            context: 權限檢查上下文

        Returns:
            存取決策
        """
        self.stats["permission_checks"] += 1

        try:
            # 驗證會話
            session = self._validate_session(token)
            if not session:
                self.stats["access_denied"] += 1
                return AccessDecision.DENY

            # 檢查權限
            if action in session.permissions:
                self.stats["access_allowed"] += 1

                # 記錄存取審計
                audit_log(
                    level=AuditLevel.ACCESS,
                    category=AuditCategory.DATA_ACCESS,
                    action="permission_granted",
                    actor=session.user_id,
                    target=resource,
                    result="ALLOW",
                    details={"permission": action.value, "resource": resource}
                )

                return AccessDecision.ALLOW
            else:
                self.stats["access_denied"] += 1

                # 記錄拒絕存取審計
                audit_log(
                    level=AuditLevel.SECURITY,
                    category=AuditCategory.SECURITY_EVENT,
                    action="permission_denied",
                    actor=session.user_id,
                    target=resource,
                    result="DENY",
                    details={"permission": action.value, "resource": resource}
                )

                return AccessDecision.DENY

        except Exception as e:
            self.logger.error("permission_check_error", error=str(e))
            return AccessDecision.DENY

    def _validate_session(self, token: str) -> Optional[Session]:
        """驗證會話"""
        try:
            # 解碼JWT令牌
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            session_id = payload["session_id"]

            # 檢查會話是否存在且未過期
            session = self.sessions.get(session_id)
            if session and session.expires_at > datetime.utcnow():
                return session

        except jwt.ExpiredSignatureError:
            self.logger.debug("session_expired", token=token[:16])
        except jwt.InvalidTokenError:
            self.logger.debug("invalid_token", token=token[:16])

        return None

    def assign_role(self, user_id: str, role_name: str) -> bool:
        """
        為用戶分配角色

        Args:
            user_id: 用戶ID
            role_name: 角色名稱

        Returns:
            是否成功
        """
        user = self.users.get(user_id)
        if not user:
            return False

        if role_name not in self.roles:
            return False

        user.roles.add(role_name)

        # 重新計算權限
        user.permissions = self._calculate_user_permissions(user)
        user.last_login = datetime.utcnow()

        audit_log(
            level=AuditLevel.ACTION,
            category=AuditCategory.DATA_ACCESS,
            action="role_assigned",
            actor="system",
            target=user_id,
            result="SUCCESS",
            details={"role": role_name}
        )

        self.logger.info("role_assigned", user_id=user_id, role=role_name)
        return True

    def revoke_role(self, user_id: str, role_name: str) -> bool:
        """
        撤銷用戶角色

        Args:
            user_id: 用戶ID
            role_name: 角色名稱

        Returns:
            是否成功
        """
        user = self.users.get(user_id)
        if not user:
            return False

        if role_name not in user.roles:
            return False

        user.roles.remove(role_name)

        # 重新計算權限
        user.permissions = self._calculate_user_permissions(user)

        audit_log(
            level=AuditLevel.ACTION,
            category=AuditCategory.DATA_ACCESS,
            action="role_revoked",
            actor="system",
            target=user_id,
            result="SUCCESS",
            details={"role": role_name}
        )

        self.logger.info("role_revoked", user_id=user_id, role=role_name)
        return True

    def create_role(self, name: str, permissions: List[Permission],
                   description: str = "", inherits_from: str = None) -> bool:
        """
        創建角色

        Args:
            name: 角色名稱
            permissions: 權限列表
            description: 描述
            inherits_from: 繼承角色

        Returns:
            是否成功
        """
        if name in self.roles:
            return False

        role = RoleDefinition(
            name=name,
            permissions=set(permissions),
            description=description,
            inherits_from=inherits_from,
            is_active=True
        )

        self.roles[name] = role

        audit_log(
            level=AuditLevel.ACTION,
            category=AuditCategory.DATA_ACCESS,
            action="role_created",
            actor="system",
            target=name,
            result="SUCCESS",
            details={"permissions": [p.value for p in permissions]}
        )

        self.logger.info("role_created", name=name, permissions=len(permissions))
        return True

    def logout(self, token: str) -> bool:
        """
        用戶登出

        Args:
            token: 會話令牌

        Returns:
            是否成功
        """
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            session_id = payload["session_id"]

            if session_id in self.sessions:
                session = self.sessions[session_id]
                del self.sessions[session_id]
                self.stats["active_sessions"] = len(self.sessions)

                audit_log(
                    level=AuditLevel.ACTION,
                    category=AuditCategory.DATA_ACCESS,
                    action="user_logged_out",
                    actor=session.user_id,
                    target="session",
                    result="SUCCESS"
                )

                return True

        except Exception as e:
            self.logger.warning("logout_error", error=str(e))

        return False

    def get_user_permissions(self, user_id: str) -> Set[Permission]:
        """獲取用戶權限"""
        user = self.users.get(user_id)
        if user:
            return user.permissions.copy()
        return set()

    def get_system_stats(self) -> Dict[str, Any]:
        """獲取系統統計"""
        return {
            **self.stats,
            "active_users": sum(1 for user in self.users.values() if user.is_active),
            "total_roles": len(self.roles),
            "active_sessions": len(self.sessions),
            "cache_size": len(self.permission_cache),
            "uptime": (datetime.utcnow() - datetime.utcnow()).total_seconds()  # 需要改進
        }

    def export_permissions(self, user_id: str) -> Dict[str, Any]:
        """導出用戶權限信息"""
        user = self.users.get(user_id)
        if not user:
            return {}

        return {
            "user_id": user.user_id,
            "username": user.username,
            "roles": list(user.roles),
            "permissions": [p.value for p in user.permissions],
            "is_active": user.is_active,
            "last_login": user.last_login.isoformat() if user.last_login else None
        }


# 修飾器
def require_permission(permission: Permission):
    """權限檢查裝飾器"""
    def decorator(func):
        async def wrapper(self, token: str, *args, **kwargs):
            rbac_manager = get_rbac_manager()

            # 檢查權限
            decision = await rbac_manager.check_permission(token, "system", permission)

            if decision == AccessDecision.DENY:
                raise PermissionError(f"權限不足: 需要 {permission.value}")

            return await func(self, token, *args, **kwargs)
        return wrapper
    return decorator


# 全域RBAC管理器實例
_rbac_manager: Optional[RBACManager] = None


def init_rbac_manager(config_manager=None) -> RBACManager:
    """
    初始化全域RBAC管理器

    Args:
        config_manager: 配置管理器實例

    Returns:
        RBAC管理器實例
    """
    global _rbac_manager

    if _rbac_manager is None:
        _rbac_manager = RBACManager(config_manager)

    return _rbac_manager


def get_rbac_manager() -> RBACManager:
    """獲取全域RBAC管理器實例"""
    if _rbac_manager is None:
        raise RuntimeError("RBAC管理器尚未初始化，請先調用init_rbac_manager()")
    return _rbac_manager
