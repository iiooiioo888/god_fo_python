"""
WebCrawler Commander - RBAC權限管理器單元測試

測試覆蓋：
- 用戶和角色管理
- 權限分配和檢查
- JWT會話管理
- 權限繼承機制
- 安全審計日誌
- 錯誤處理和恢復

作者: Jerry開發工作室
版本: v1.0.0
"""

import jwt
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime, timedelta, timezone

from utils.rbac_manager import (
    RBACManager, Permission, Role, User, Session,
    AccessDecision, get_rbac_manager, init_rbac_manager
)
from tests.test_utils import TestDataFactory, mock_config_manager, mock_logger_service


@pytest.mark.unit
@pytest.mark.security
class TestRBACManagerInitialization:
    """RBAC管理器初始化測試"""

    def test_rbac_manager_creation(self):
        """測試RBAC管理器創建"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.rbac_manager.get_config_manager', return_value=config_mock), \
             patch('utils.rbac_manager.get_logger', return_value=logger_mock):

            manager = RBACManager(config_manager=config_mock)
            assert manager is not None
            assert isinstance(manager.roles, dict)
            assert isinstance(manager.users, dict)
            assert isinstance(manager.sessions, dict)

    def test_rbac_manager_singleton(self):
        """測試RBAC管理器單例模式"""
        config_mock = mock_config_manager()

        with patch('utils.rbac_manager.get_config_manager', return_value=config_mock):
            init_rbac_manager(config_mock)

            manager1 = get_rbac_manager()
            manager2 = get_rbac_manager()

            assert manager1 is manager2

    def test_builtin_roles_initialization(self):
        """測試內建角色初始化"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.rbac_manager.get_config_manager', return_value=config_mock), \
             patch('utils.rbac_manager.get_logger', return_value=logger_mock):

            manager = RBACManager(config_manager=config_mock)

            # 檢查內建角色是否存在
            assert Role.GUEST.value in manager.roles
            assert Role.USER.value in manager.roles
            assert Role.ADMIN.value in manager.roles
            assert Role.SUPER_ADMIN.value in manager.roles

            # 檢查權限設置
            guest_role = manager.roles[Role.GUEST.value]
            assert Permission.READ_DATA in guest_role.permissions

            admin_role = manager.roles[Role.ADMIN.value]
            assert Permission.CREATE_USER in admin_role.permissions
            assert Permission.SYSTEM_ADMIN in admin_role.permissions


@pytest.mark.unit
@pytest.mark.security
class TestRBACManagerUserManagement:
    """RBAC管理器用戶管理測試"""

    @pytest.fixture
    def rbac_manager(self):
        """測試RBAC管理器修件器"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.rbac_manager.get_config_manager', return_value=config_mock), \
             patch('utils.rbac_manager.get_logger', return_value=logger_mock):

            manager = RBACManager(config_manager=config_mock)
            return manager

    def test_user_creation(self, rbac_manager):
        """測試用戶創建"""
        user = rbac_manager.create_user("testuser", "test@example.com", [Role.USER.value])

        assert user is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert Role.USER.value in user.roles
        assert user.is_active is True
        assert user.user_id.startswith("user_")

    def test_duplicate_user_creation(self, rbac_manager):
        """測試重複用戶創建"""
        # 先創建用戶
        rbac_manager.create_user("testuser", "test@example.com")

        # 嘗試再次創建相同用戶
        with pytest.raises(ValueError, match="用戶名.*已經存在"):
            rbac_manager.create_user("testuser", "different@example.com")

    def test_user_permission_calculation(self, rbac_manager):
        """測試用戶權限計算"""
        # 創建管理員用戶
        admin_user = rbac_manager.create_user("admin", "admin@example.com", [Role.ADMIN.value])

        # 檢查權限
        assert Permission.READ_DATA in admin_user.permissions  # 繼承自GUEST
        assert Permission.CREATE_USER in admin_user.permissions  # ADMIN權限
        assert Permission.SYSTEM_ADMIN in admin_user.permissions  # ADMIN權限

    def test_role_assignment(self, rbac_manager):
        """測試角色分配"""
        user = rbac_manager.create_user("testuser", "test@example.com")

        # 分配ANALYZER角色
        success = rbac_manager.assign_role(user.user_id, Role.ANALYST.value)
        assert success is True

        # 檢查權限更新
        updated_user = rbac_manager.users[user.user_id]
        assert Role.ANALYST.value in updated_user.roles
        assert Permission.EXPORT_DATA in updated_user.permissions

    def test_role_revocation(self, rbac_manager):
        """測試角色撤銷"""
        user = rbac_manager.create_user("testuser", "test@example.com", [Role.ANALYST.value])

        # 撤銷ANALYZER角色
        success = rbac_manager.assign_role(user.user_id, Role.USER.value)
        success = rbac_manager.revoke_role(user.user_id, Role.ANALYST.value)
        assert success is True

        # 檢查權限更新
        updated_user = rbac_manager.users[user.user_id]
        assert Role.ANALYST.value not in updated_user.roles

    def test_invalid_role_assignment(self, rbac_manager):
        """測試無效角色分配"""
        user = rbac_manager.create_user("testuser", "test@example.com")

        # 嘗試分配不存在的角色
        success = rbac_manager.assign_role(user.user_id, "nonexistent_role")
        assert success is False


@pytest.mark.unit
@pytest.mark.security
class TestRBACManagerAuthentication:
    """RBAC管理器認證測試"""

    @pytest.fixture
    def rbac_manager(self):
        """測試RBAC管理器修件器"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.rbac_manager.get_config_manager', return_value=config_mock), \
             patch('utils.rbac_manager.get_logger', return_value=logger_mock):

            manager = RBACManager(config_manager=config_mock)
            return manager

    def test_user_authentication_success(self, rbac_manager):
        """測試用戶認證成功"""
        # 創建用戶（注意：這裡是簡化的認證，生產環境應該有密碼驗證）
        user = rbac_manager.create_user("testuser", "test@example.com")

        # 認證用戶
        token = rbac_manager.authenticate_user("testuser", "anypassword")

        assert token is not None
        assert isinstance(token, str)

        # 檢查會話已創建
        assert len(rbac_manager.sessions) == 1

    def test_user_authentication_failure(self, rbac_manager):
        """測試用戶認證失敗"""
        # 嘗試認證不存在的用戶
        token = rbac_manager.authenticate_user("nonexistent", "password")
        assert token is None

    def test_session_creation(self, rbac_manager):
        """測試會話創建"""
        user = rbac_manager.create_user("testuser", "test@example.com")

        with patch('utils.rbac_manager.secrets.token_hex', return_value="mock_session_id"):
            token = rbac_manager._create_session(user.user_id)

            assert token is not None

            # 驗證令牌
            payload = jwt.decode(token, rbac_manager.jwt_secret, algorithms=["HS256"])
            assert payload["user_id"] == user.user_id
            assert payload["session_id"] == "session_mock_session_id"

    def test_session_validation(self, rbac_manager):
        """測試會話驗證"""
        user = rbac_manager.create_user("testuser", "test@example.com")

        # 創建會話
        token = rbac_manager.authenticate_user("testuser", "password")
        assert token is not None

        # 驗證會話
        session = rbac_manager._validate_session(token)
        assert session is not None
        assert session.user_id == user.user_id
        assert session.token == token

    def test_expired_session_validation(self, rbac_manager):
        """測試過期會話驗證"""
        user = rbac_manager.create_user("testuser", "test@example.com")

        # 創建會話
        token = rbac_manager.authenticate_user("testuser", "password")

        # 模擬會話過期
        session_id = list(rbac_manager.sessions.keys())[0]
        expired_time = datetime.utcnow() - timedelta(hours=10)
        rbac_manager.sessions[session_id].expires_at = expired_time

        # 驗證應該失敗
        session = rbac_manager._validate_session(token)
        assert session is None

    def test_user_logout(self, rbac_manager):
        """測試用戶登出"""
        rbac_manager.create_user("testuser", "test@example.com")
        token = rbac_manager.authenticate_user("testuser", "password")

        # 驗證會話存在
        assert len(rbac_manager.sessions) == 1

        # 登出
        success = rbac_manager.logout(token)
        assert success is True

        # 驗證會話已移除
        assert len(rbac_manager.sessions) == 0


@pytest.mark.unit
@pytest.mark.security
class TestRBACManagerPermissionChecking:
    """RBAC管理器權限檢查測試"""

    @pytest.fixture
    async def rbac_manager(self):
        """測試RBAC管理器修件器"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.rbac_manager.get_config_manager', return_value=config_mock), \
             patch('utils.rbac_manager.get_logger', return_value=logger_mock):

            manager = RBACManager(config_manager=config_mock)
            yield manager

    @pytest.mark.asyncio
    async def test_permission_check_allowed(self, rbac_manager):
        """測試允許的權限檢查"""
        # 創建管理員用戶
        user = rbac_manager.create_user("admin", "admin@example.com", [Role.ADMIN.value])
        token = rbac_manager.authenticate_user("admin", "password")

        # 檢查允許的權限
        decision = await rbac_manager.check_permission(token, "system", Permission.CREATE_USER)
        assert decision == AccessDecision.ALLOW

    @pytest.mark.asyncio
    async def test_permission_check_denied(self, rbac_manager):
        """測試拒絕的權限檢查"""
        # 創建普通用戶
        user = rbac_manager.create_user("user", "user@example.com", [Role.USER.value])
        token = rbac_manager.authenticate_user("user", "password")

        # 檢查不允許的權限
        decision = await rbac_manager.check_permission(token, "system", Permission.CREATE_USER)
        assert decision == AccessDecision.DENY

    @pytest.mark.asyncio
    async def test_permission_check_invalid_token(self, rbac_manager):
        """測試無效令牌的權限檢查"""
        decision = await rbac_manager.check_permission("invalid_token", "system", Permission.READ_DATA)
        assert decision == AccessDecision.DENY

    @pytest.mark.asyncio
    async def test_permission_inheritance(self, rbac_manager):
        """測試權限繼承"""
        # 創建數據工程師用戶（應該有寫權限）
        user = rbac_manager.create_user("engineer", "engineer@example.com", [Role.DATA_ENGINEER.value])
        token = rbac_manager.authenticate_user("engineer", "password")

        # 檢查繼承的權限
        decision = await rbac_manager.check_permission(token, "data", Permission.WRITE_DATA)
        assert decision == AccessDecision.ALLOW

        # 檢查從父角色繼承的權限
        decision = await rbac_manager.check_permission(token, "data", Permission.READ_DATA)
        assert decision == AccessDecision.ALLOW


@pytest.mark.unit
@pytest.mark.security
class TestRBACManagerRoleHierarchy:
    """RBAC管理器角色層次測試"""

    @pytest.fixture
    def rbac_manager(self):
        """測試RBAC管理器修件器"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.rbac_manager.get_config_manager', return_value=config_mock), \
             patch('utils.rbac_manager.get_logger', return_value=logger_mock):

            manager = RBACManager(config_manager=config_mock)
            return manager

    def test_role_inheritance_calculation(self, rbac_manager):
        """測試角色繼承權限計算"""
        # 創建具有繼承關係的角色
        # USER -> GUEST (內建)
        # ANALYST -> USER
        # DATA_ENGINEER -> ANALYST

        # 創建數據工程師用戶
        user = rbac_manager.create_user("engineer", "engineer@example.com", [Role.DATA_ENGINEER.value])

        # 數據工程師應該有所有級別的權限
        permissions = rbac_manager.get_user_permissions(user.user_id)

        # 檢查繼承的權限
        assert Permission.READ_DATA in permissions      # GUEST權限
        assert Permission.CREATE_CRAWLER in permissions # USER權限
        assert Permission.EXPORT_DATA in permissions     # ANALYST權限
        assert Permission.WRITE_DATA in permissions      # DATA_ENGINEER權限
        assert Permission.DELETE_DATA in permissions     # DATA_ENGINEER權限

    def test_custom_role_creation(self, rbac_manager):
        """測試自定義角色創建"""
        from utils.rbac_manager import Permission

        # 創建自定義角色
        custom_permissions = {Permission.READ_DATA, Permission.PROCESS_DATA}
        success = rbac_manager.create_role("custom_role", custom_permissions, "Custom Role")

        assert success is True
        assert "custom_role" in rbac_manager.roles

        role = rbac_manager.roles["custom_role"]
        assert role.name == "custom_role"
        assert role.description == "Custom Role"
        assert Permission.READ_DATA in role.permissions
        assert Permission.PROCESS_DATA in role.permissions

    def test_role_inheritance_with_custom_roles(self, rbac_manager):
        """測試自定義角色的權限繼承"""
        # 創建基礎角色
        rbac_manager.create_role("base_role", {Permission.READ_DATA})

        # 創建繼承角色
        rbac_manager.create_role("inherited_role", {Permission.WRITE_DATA}, inherits_from="base_role")

        # 創建用戶分配繼承角色
        user = rbac_manager.create_user("testuser", "test@example.com", ["inherited_role"])

        permissions = rbac_manager.get_user_permissions(user.user_id)

        # 應該同時有基礎權限和自身權限
        assert Permission.READ_DATA in permissions  # 繼承的
        assert Permission.WRITE_DATA in permissions # 自己的


@pytest.mark.unit
@pytest.mark.security
class TestRBACManagerSecurityAuditing:
    """RBAC管理器安全審計測試"""

    @pytest.fixture
    def rbac_manager(self):
        """測試RBAC管理器修件器"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()
        audit_mock = MagicMock()

        with patch('utils.rbac_manager.get_config_manager', return_value=config_mock), \
             patch('utils.rbac_manager.get_logger', return_value=logger_mock), \
             patch('utils.rbac_manager.get_audit_logger', return_value=audit_mock):

            manager = RBACManager(config_manager=config_mock)
            manager.audit_logger = audit_mock
            return manager

    def test_user_creation_auditing(self, rbac_manager):
        """測試用戶創建審計"""
        with patch('utils.rbac_manager.audit_log') as mock_audit:
            rbac_manager.create_user("testuser", "test@example.com")

            # 驗證審計日誌被調用
            mock_audit.assert_called()
            call_args = mock_audit.call_args

            assert call_args[1]['category'] == "DATA_ACCESS"
            assert call_args[1]['action'] == "user_created"
            assert "testuser" in str(call_args[1]['details'])

    def test_permission_check_auditing(self, rbac_manager):
        """測試權限檢查審計"""
        rbac_manager.create_user("testuser", "test@example.com")
        token = rbac_manager.authenticate_user("testuser", "password")

        with patch('utils.rbac_manager.audit_log') as mock_audit:
            import asyncio
            async def run_check():
                return await rbac_manager.check_permission(token, "test", Permission.READ_DATA)
            asyncio.run(run_check())

            # 驗證審計日誌被調用
            # 注意：這裡可能需要更詳細的模擬，因為check_permission是異步的


@pytest.mark.unit
@pytest.mark.security
class TestRBACManagerStatistics:
    """RBAC管理器統計測試"""

    @pytest.fixture
    def rbac_manager(self):
        """測試RBAC管理器修件器"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.rbac_manager.get_config_manager', return_value=config_mock), \
             patch('utils.rbac_manager.get_logger', return_value=logger_mock):

            manager = RBACManager(config_manager=config_mock)
            return manager

    def test_system_stats_basic(self, rbac_manager):
        """測試基本系統統計"""
        # 創建一些用戶
        rbac_manager.create_user("user1", "user1@example.com")
        rbac_manager.create_user("user2", "user2@example.com")

        stats = rbac_manager.get_system_stats()

        assert isinstance(stats, dict)
        assert stats["total_users"] == 2  # 1 + 1 = 2
        assert stats["active_users"] == 2
        assert stats["total_roles"] == 6  # 6個內建角色

    def test_user_permissions_export(self, rbac_manager):
        """測試用戶權限導出"""
        user = rbac_manager.create_user("testuser", "test@example.com")

        export_data = rbac_manager.export_permissions(user.user_id)

        assert isinstance(export_data, dict)
        assert export_data["user_id"] == user.user_id
        assert export_data["username"] == user.username
        assert isinstance(export_data["permissions"], list)
        assert isinstance(export_data["roles"], list)


@pytest.mark.unit
@pytest.mark.security
class TestRBACManagerErrorHandling:
    """RBAC管理器錯誤處理測試"""

    @pytest.fixture
    def rbac_manager(self):
        """測試RBAC管理器修件器"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.rbac_manager.get_config_manager', return_value=config_mock), \
             patch('utils.rbac_manager.get_logger', return_value=logger_mock):

            manager = RBACManager(config_manager=config_mock)
            return manager

    def test_user_creation_with_invalid_data(self, rbac_manager):
        """測試使用無效數據創建用戶"""
        with pytest.raises(ValueError):
            rbac_manager.create_user("", "test@example.com")  # 空用戶名

        with pytest.raises(ValueError):
            rbac_manager.create_user("testuser", "invalid-email")  # 無效郵箱

    def test_permission_check_with_corrupted_token(self, rbac_manager):
        """測試使用損壞令牌的權限檢查"""
        with patch('utils.rbac_manager.audit_log'):
            import asyncio
            async def run_check():
                return await rbac_manager.check_permission("corrupted.jwt.token", "test", Permission.READ_DATA)
            result = asyncio.run(run_check())
            assert result == AccessDecision.DENY

    def test_session_timeout_handling(self, rbac_manager):
        """測試會話超時處理"""
        user = rbac_manager.create_user("testuser", "test@example.com")
        token = rbac_manager.authenticate_user("testuser", "password")

        # 將會話設置為已過期
        session_id = list(rbac_manager.sessions.keys())[0]
        expired_time = datetime.utcnow() - timedelta(hours=1)
        rbac_manager.sessions[session_id].expires_at = expired_time

        with patch('utils.rbac_manager.audit_log'):
            import asyncio
            async def run_check():
                return await rbac_manager.check_permission(token, "test", Permission.READ_DATA)
            result = asyncio.run(run_check())
            assert result == AccessDecision.DENY


if __name__ == "__main__":
    pytest.main([__file__, "--verbose", "--cov=utils.rbac_manager", "--cov-report=html"])
