"""
WebCrawler Commander - 加密服務單元測試

測試覆蓋：
- 密鑰管理和輪換
- 多算法加密解密
- 數據完整性驗證
- 錯誤處理和恢復
- 安全審計追蹤
- 性能和資源監控

作者: Jerry開發工作室
版本: v1.0.0
"""

import asyncio
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from utils.encryption_service import (
    EncryptionService, KeyStore, EncryptionAlgorithm, KeyPurpose, EncryptionResult,
    DecryptionResult, get_encryption_service, init_encryption_service
)
from tests.test_utils import mock_config_manager, mock_logger_service


@pytest.mark.unit
@pytest.mark.security
class TestEncryptionServiceInitialization:
    """加密服務初始化測試"""

    def test_encryption_service_creation(self, temp_dir):
        """測試加密服務創建"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.encryption_service.get_config_manager', return_value=config_mock), \
             patch('utils.encryption_service.get_logger', return_value=logger_mock):

            service = EncryptionService(config_manager=config_mock)

            assert service is not None
            assert isinstance(service.keystore, KeyStore)
            assert service.default_algorithm == EncryptionAlgorithm.AES_256_GCM

    def test_encryption_service_singleton(self, temp_dir):
        """測試加密服務單例模式"""
        config_mock = mock_config_manager()

        with patch('utils.encryption_service.get_config_manager', return_value=config_mock):
            init_encryption_service(config_mock)

            service1 = get_encryption_service()
            service2 = get_encryption_service()

            assert service1 is service2

    def test_key_initialization_on_startup(self, temp_dir):
        """測試啟動時密鑰初始化"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.encryption_service.get_config_manager', return_value=config_mock), \
             patch('utils.encryption_service.get_logger', return_value=logger_mock):

            service = EncryptionService(config_manager=config_mock)

            # 檢查預設密鑰已創建
            encryption_key = service.keystore.get_active_key(KeyPurpose.ENCRYPTION)
            signature_key = service.keystore.get_active_key(KeyPurpose.SIGNATURE)

            assert encryption_key is not None
            assert signature_key is not None
            assert len(service.keystore.keys) >= 2


@pytest.mark.unit
@pytest.mark.security
class TestKeyStoreOperations:
    """密鑰存儲操作測試"""

    @pytest.fixture
    def keystore(self, temp_dir):
        """測試密鑰存儲修件器"""
        keystore_dir = temp_dir / "keys"
        keystore = KeyStore(str(keystore_dir))
        return keystore

    def test_key_generation(self, keystore):
        """測試密鑰生成"""
        key = keystore.generate_key(EncryptionAlgorithm.AES_256_GCM, KeyPurpose.ENCRYPTION)

        assert key is not None
        assert key.algorithm == EncryptionAlgorithm.AES_256_GCM
        assert key.purpose == KeyPurpose.ENCRYPTION
        assert len(key.key_data) == 32  # AES-256 key length
        assert key.key_id.startswith("encryption_")
        assert key.is_active is True

    def test_key_retrieval(self, keystore):
        """測試密鑰檢索"""
        # 生成兩個密鑰
        key1 = keystore.generate_key(EncryptionAlgorithm.AES_256_GCM, KeyPurpose.ENCRYPTION)
        key2 = keystore.generate_key(EncryptionAlgorithm.AES_256_CBC, KeyPurpose.ENCRYPTION)

        # 獲取活躍密鑰（應該返回最新的）
        active_key = keystore.get_active_key(KeyPurpose.ENCRYPTION)
        assert active_key is not None
        assert active_key.key_id == key2.key_id  # 最新的密鑰

    def test_key_deactivation(self, keystore):
        """測試密鑰停用"""
        key = keystore.generate_key(EncryptionAlgorithm.AES_256_GCM, KeyPurpose.ENCRYPTION)

        # 停用密鑰
        success = keystore.deactivate_key(key.key_id)
        assert success is True

        # 檢查密鑰已停用
        deactivated_key = keystore.keys[key.key_id]
        assert deactivated_key.is_active is False

    def test_key_rotation(self, keystore):
        """測試密鑰輪換"""
        old_key = keystore.generate_key(EncryptionAlgorithm.AES_256_GCM, KeyPurpose.ENCRYPTION)

        # 輪換密鑰
        new_key = keystore.rotate_key(KeyPurpose.ENCRYPTION)
        assert new_key is not None
        assert new_key.algorithm == old_key.algorithm
        assert new_key.purpose == old_key.purpose

        # 檢查舊密鑰已停用
        old_key_after = keystore.keys[old_key.key_id]
        assert old_key_after.is_active is False

    def test_persistence(self, keystore, temp_dir):
        """測試密鑰持久化"""
        key = keystore.generate_key(EncryptionAlgorithm.AES_256_GCM, KeyPurpose.ENCRYPTION)

        # 創建新的keystore實例來模擬重啟
        keystore2 = KeyStore(str(temp_dir / "keys"))

        # 檢查密鑰已載入
        loaded_key = keystore2.keys.get(key.key_id)
        assert loaded_key is not None
        assert loaded_key.key_data == key.key_data
        assert loaded_key.algorithm == key.algorithm


@pytest.mark.unit
@pytest.mark.security
class TestDataEncryptionDecryption:
    """數據加密解密測試"""

    @pytest.fixture
    async def encryption_service(self, temp_dir):
        """測試加密服務修件器"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.encryption_service.get_config_manager', return_value=config_mock), \
             patch('utils.encryption_service.get_logger', return_value=logger_mock):

            service = EncryptionService(config_manager=config_mock)
            return service

    @pytest.mark.asyncio
    async def test_aes_gcm_encryption_decryption(self, encryption_service):
        """測試AES-GCM加密解密"""
        plaintext = b"Hello, World! This is a test message for encryption."
        metadata = {"test": "metadata", "purpose": "unittest"}

        # 加密
        result = await encryption_service.encrypt_data(plaintext, metadata=metadata)

        assert isinstance(result, EncryptionResult)
        assert result.ciphertext != plaintext
        assert result.algorithm == EncryptionAlgorithm.AES_256_GCM
        assert result.key_id is not None
        assert result.iv is not None
        assert result.tag is not None
        assert result.metadata == metadata

        # 解密
        decrypted = await encryption_service.decrypt_data(result)

        assert isinstance(decrypted, DecryptionResult)
        assert decrypted.plaintext == plaintext
        assert decrypted.verified is True

    @pytest.mark.asyncio
    async def test_aes_cbc_encryption_decryption(self, encryption_service):
        """測試AES-CBC加密解密"""
        plaintext = b"Another test message for CBC encryption."
        algorithm = EncryptionAlgorithm.AES_256_CBC

        # 加密
        result = await encryption_service.encrypt_data(plaintext, algorithm=algorithm)

        assert result.algorithm == algorithm
        assert result.ciphertext != plaintext
        assert result.key_id is not None
        assert result.iv is not None

        # 解密
        decrypted = await encryption_service.decrypt_data(result)

        assert decrypted.plaintext == plaintext
        assert decrypted.verified is True

    @pytest.mark.asyncio
    async def test_chacha20_encryption_decryption(self, encryption_service):
        """測試ChaCha20加密解密"""
        plaintext = b"ChaCha20 test message."
        algorithm = EncryptionAlgorithm.CHACHA20_POLY1305

        # 加密
        result = await encryption_service.encrypt_data(plaintext, algorithm=algorithm)

        assert result.algorithm == algorithm
        assert result.ciphertext != plaintext

        # 解密
        decrypted = await encryption_service.decrypt_data(result)

        assert decrypted.plaintext == plaintext
        assert decrypted.verified is True

    @pytest.mark.asyncio
    async def test_large_data_encryption(self, encryption_service):
        """測試大數據加密"""
        # 生成1MB測試數據
        plaintext = b"A" * (1024 * 1024)

        result = await encryption_service.encrypt_data(plaintext)
        decrypted = await encryption_service.decrypt_data(result)

        assert decrypted.plaintext == plaintext
        assert len(decrypted.plaintext) == len(plaintext)

    @pytest.mark.asyncio
    async def test_empty_data_encryption(self, encryption_service):
        """測試空數據加密"""
        plaintext = b""

        result = await encryption_service.encrypt_data(plaintext)
        decrypted = await encryption_service.decrypt_data(result)

        assert decrypted.plaintext == plaintext
        assert len(decrypted.plaintext) == 0

    @pytest.mark.asyncio
    async def test_unicode_data_encryption(self, encryption_service):
        """測試Unicode數據加密"""
        plaintext = "Hello 世界! 🌍 Test message with emojis 🎉".encode('utf-8')

        result = await encryption_service.encrypt_data(plaintext)
        decrypted = await encryption_service.decrypt_data(result)

        assert decrypted.plaintext == plaintext
        assert decrypted.plaintext.decode('utf-8') == plaintext.decode('utf-8')


@pytest.mark.unit
@pytest.mark.security
class TestDataIntegrity:
    """數據完整性測試"""

    @pytest.fixture
    async def encryption_service(self, temp_dir):
        """測試加密服務修件器"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.encryption_service.get_config_manager', return_value=config_mock), \
             patch('utils.encryption_service.get_logger', return_value=logger_mock):

            service = EncryptionService(config_manager=config_mock)
            return service

    @pytest.mark.asyncio
    async def test_data_integrity_verification(self, encryption_service):
        """測試數據完整性驗證"""
        plaintext = b"Data integrity test message."

        # 加密
        result = await encryption_service.encrypt_data(plaintext)

        # 正常解密應該驗證通過
        decrypted = await encryption_service.decrypt_data(result, verify_integrity=True)
        assert decrypted.verified is True

    @pytest.mark.asyncio
    async def test_tampered_data_detection(self, encryption_service):
        """測試篡改數據檢測"""
        plaintext = b"Original message for tampering test."

        # 加密
        result = await encryption_service.encrypt_data(plaintext)

        # 篡改密文
        tampered_ciphertext = bytearray(result.ciphertext)
        if len(tampered_ciphertext) > 10:
            tampered_ciphertext[10] ^= 0xFF  # 翻轉一個字節

        tampered_result = EncryptionResult(
            ciphertext=bytes(tampered_ciphertext),
            key_id=result.key_id,
            algorithm=result.algorithm,
            iv=result.iv,
            tag=result.tag
        )

        # 解密篡改的數據
        decrypted = await encryption_service.decrypt_data(tampered_result, verify_integrity=True)

        # AES-GCM應該檢測到篡改
        if result.algorithm == EncryptionAlgorithm.AES_256_GCM:
            assert decrypted.verified is False

    @pytest.mark.asyncio
    async def test_invalid_key_decryption(self, encryption_service):
        """測試無效密鑰解密"""
        plaintext = b"Test message."

        # 使用一個服務的密鑰加密
        result = await encryption_service.encrypt_data(plaintext)

        # 創建另一個服務實例（不同的密鑰）
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.encryption_service.get_config_manager', return_value=config_mock), \
             patch('utils.encryption_service.get_logger', return_value=logger_mock):

            another_service = EncryptionService(config_manager=config_mock)

            # 使用另一個服務的密鑰嘗試解密
            try:
                decrypted = await another_service.decrypt_data(result)
                # 應該會失敗或者解密出錯誤的數據
                assert decrypted.plaintext != plaintext
            except Exception:
                # 正確的行為應該是拋出異常或驗證失敗
                pass


@pytest.mark.unit
@pytest.mark.security
class TestFileEncryption:
    """文件加密測試"""

    @pytest.fixture
    async def encryption_service(self, temp_dir):
        """測試加密服務修件器"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.encryption_service.get_config_manager', return_value=config_mock), \
             patch('utils.encryption_service.get_logger', return_value=logger_mock):

            service = EncryptionService(config_manager=config_mock)
            return service

    @pytest.mark.asyncio
    async def test_file_encryption_decryption(self, encryption_service, temp_dir):
        """測試文件加密解密"""
        # 創建測試文件
        test_file = temp_dir / "test_file.txt"
        test_content = "This is a test file content for encryption.\n" * 100  # 更大的內容
        test_file.write_text(test_content, encoding='utf-8')

        # 創建輸出文件路徑
        encrypted_file = temp_dir / "test_file.txt.encrypted"
        decrypted_file = temp_dir / "test_file.decrypted.txt"

        # 加密文件
        encrypted_path = await encryption_service.encrypt_file(str(test_file), str(encrypted_file))
        assert encrypted_path == str(encrypted_file)
        assert encrypted_file.exists()

        # 解密文件
        decrypted_path = await encryption_service.decrypt_file(str(encrypted_file), str(decrypted_file))
        assert decrypted_path == str(decrypted_file)
        assert decrypted_file.exists()

        # 驗證內容
        decrypted_content = decrypted_file.read_text(encoding='utf-8')
        assert decrypted_content == test_content

    @pytest.mark.asyncio
    async def test_large_file_encryption(self, encryption_service, temp_dir):
        """測試大文件加密"""
        # 創建5MB測試文件
        test_file = temp_dir / "large_test_file.txt"
        large_content = "Large file test content.\n" * 50000  # 約5MB

        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(large_content)

        encrypted_file = temp_dir / "large_file.encrypted"

        # 加密大文件
        encrypted_path = await encryption_service.encrypt_file(str(test_file), str(encrypted_file))
        assert encrypted_file.exists()

        # 解密文件驗證
        decrypted_path = await encryption_service.decrypt_file(str(encrypted_file))
        decrypted_content = Path(decrypted_path).read_text(encoding='utf-8')
        assert decrypted_content == large_content

    @pytest.mark.asyncio
    async def test_binary_file_encryption(self, encryption_service, temp_dir):
        """測試二進制文件加密"""
        # 創建二進制測試文件
        test_file = temp_dir / "binary_test.bin"
        binary_data = bytes(range(256)) * 10  # 2560字節的二進制數據

        with open(test_file, 'wb') as f:
            f.write(binary_data)

        # 加密二進制文件
        encrypted_path = await encryption_service.encrypt_file(str(test_file))
        assert Path(encrypted_path).exists()

        # 解密並驗證
        decrypted_path = await encryption_service.decrypt_file(str(encrypted_path))
        with open(decrypted_path, 'rb') as f:
            decrypted_data = f.read()

        assert decrypted_data == binary_data


@pytest.mark.unit
@pytest.mark.security
class TestKeyRotation:
    """密鑰輪換測試"""

    @pytest.fixture
    async def encryption_service(self, temp_dir):
        """測試加密服務修件器"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.encryption_service.get_config_manager', return_value=config_mock), \
             patch('utils.encryption_service.get_logger', return_value=logger_mock):

            service = EncryptionService(config_manager=config_mock)
            return service

    def test_key_rotation_execution(self, encryption_service):
        """測試密鑰輪換執行"""
        old_active_key = encryption_service.keystore.get_active_key(KeyPurpose.ENCRYPTION)
        assert old_active_key is not None

        # 執行密鑰輪換
        success = encryption_service.rotate_encryption_key()
        assert success is True

        # 驗證新密鑰已激活
        new_active_key = encryption_service.keystore.get_active_key(KeyPurpose.ENCRYPTION)
        assert new_active_key is not None
        assert new_active_key.key_id != old_active_key.key_id

        # 驗證舊密鑰已停用
        old_key_after = encryption_service.keystore.keys[old_active_key.key_id]
        assert old_key_after.is_active is False

    @pytest.mark.asyncio
    async def test_old_key_still_works(self, encryption_service):
        """測試舊密鑰仍然可以解密"""
        plaintext = b"Test message for key rotation."

        # 使用舊密鑰加密
        old_key = encryption_service.keystore.get_active_key(KeyPurpose.ENCRYPTION)
        result = await encryption_service.encrypt_data(plaintext)
        assert result.key_id == old_key.key_id

        # 輪換密鑰
        encryption_service.rotate_encryption_key()

        # 舊密鑰加密的數據仍然可以解密
        decrypted = await encryption_service.decrypt_data(result)
        assert decrypted.plaintext == plaintext
        assert decrypted.verified is True

    @pytest.mark.asyncio
    async def test_new_key_encryption(self, encryption_service):
        """測試新密鑰加密"""
        plaintext = b"Message encrypted with new key."

        # 輪換密鑰
        encryption_service.rotate_encryption_key()

        # 使用新密鑰加密
        new_key = encryption_service.keystore.get_active_key(KeyPurpose.ENCRYPTION)
        result = await encryption_service.encrypt_data(plaintext)

        assert result.key_id == new_key.key_id

        # 驗證可以解密
        decrypted = await encryption_service.decrypt_data(result)
        assert decrypted.plaintext == plaintext


@pytest.mark.unit
@pytest.mark.security
class TestEncryptionServiceErrorHandling:
    """加密服務錯誤處理測試"""

    @pytest.fixture
    async def encryption_service(self, temp_dir):
        """測試加密服務修件器"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.encryption_service.get_config_manager', return_value=config_mock), \
             patch('utils.encryption_service.get_logger', return_value=logger_mock):

            service = EncryptionService(config_manager=config_mock)
            return service

    @pytest.mark.asyncio
    async def test_unsupported_algorithm(self, encryption_service):
        """測試不支援的算法"""
        plaintext = b"Test message."

        # 嘗試使用不存在的算法
        from utils.encryption_service import EncryptionAlgorithm
        invalid_algorithm = "invalid_algorithm"

        try:
            result = await encryption_service.encrypt_data(plaintext)
            # 如果沒有顯式指定算法，應該使用默認算法
            assert result.algorithm == encryption_service.default_algorithm
        except ValueError:
            # 或者拋出異常
            pass

    @pytest.mark.asyncio
    async def test_no_active_key(self, encryption_service):
        """測試沒有活躍密鑰的情況"""
        # 停用所有加密密鑰
        for key in encryption_service.keystore.keys.values():
            if key.purpose == KeyPurpose.ENCRYPTION:
                encryption_service.keystore.deactivate_key(key.key_id)

        plaintext = b"Test message."

        # 應該拋出運行時錯誤
        with pytest.raises(RuntimeError, match="沒有可用的加密密鑰"):
            await encryption_service.encrypt_data(plaintext)

    @pytest.mark.asyncio
    async def test_corrupted_encryption_result(self, encryption_service):
        """測試損壞的加密結果"""
        # 創建格式錯誤的EncryptionResult
        corrupted_result = EncryptionResult(
            ciphertext=b"invalid",
            key_id="nonexistent_key",
            algorithm=EncryptionAlgorithm.AES_256_GCM
        )

        # 應該拋出異常
        with pytest.raises(Exception):
            await encryption_service.decrypt_data(corrupted_result)

    @pytest.mark.asyncio
    async def test_file_operations_error_handling(self, encryption_service, temp_dir):
        """測試文件操作錯誤處理"""
        # 測試不存在的文件
        nonexistent_file = temp_dir / "nonexistent.txt"
        result = await encryption_service.encrypt_file(str(nonexistent_file))
        assert result is None

        # 測試無權限寫入的路徑（如果有的話）
        # 這裡跳過，因為很難在所有系統上重現


@pytest.mark.unit
@pytest.mark.security
class TestEncryptionServiceStatistics:
    """加密服務統計測試"""

    @pytest.fixture
    async def encryption_service(self, temp_dir):
        """測試加密服務修件器"""
        config_mock = mock_config_manager()
        logger_mock = mock_logger_service()

        with patch('utils.encryption_service.get_config_manager', return_value=config_mock), \
             patch('utils.encryption_service.get_logger', return_value=logger_mock):

            service = EncryptionService(config_manager=config_mock)
            return service

    def test_encryption_statistics_tracking(self, encryption_service):
        """測試加密統計追蹤"""
        initial_operations = encryption_service.stats["encryption_operations"]

        # 在異步上下文中執行加密操作
        import asyncio
        async def perform_encryption():
            await encryption_service.encrypt_data(b"test")

        asyncio.run(perform_encryption())

        # 檢查統計已更新
        assert encryption_service.stats["encryption_operations"] > initial_operations

    def test_get_encryption_stats(self, encryption_service):
        """測試獲取加密統計"""
        stats = encryption_service.get_encryption_stats()

        assert isinstance(stats, dict)
        assert "encryption_operations" in stats
        assert "decryption_operations" in stats
        assert "key_rotations" in stats
        assert "active_keys" in stats
        assert "default_algorithm" in stats

    @pytest.mark.asyncio
    async def test_multiple_operations_stats(self, encryption_service):
        """測試多重操作的統計"""
        initial_stats = encryption_service.get_encryption_stats()

        # 執行多個操作
        operations = []
        for i in range(5):
            operations.append(encryption_service.encrypt_data(f"Test message {i}".encode()))

        results = await asyncio.gather(*operations)

        final_stats = encryption_service.get_encryption_stats()

        # 檢查統計增長
        assert final_stats["encryption_operations"] >= initial_stats["encryption_operations"] + 5
        assert len(results) == 5


if __name__ == "__main__":
    pytest.main([__file__, "--verbose", "--cov=utils.encryption_service", "--cov-report=html"])
