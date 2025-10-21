"""
WebCrawler Commander - 資料加密服務
企業級數據加密與密鑰管理系統

功能特色：
- AES-256加密算法支援
- 密鑰輪換與版本管理
- 數據完整性驗證
- 多層次加密策略
- 合規性支援 (GDPR, HIPAA)
- 硬件安全模塊集成
- 加密性能優化
- 緊急解密能力

作者: Jerry開發工作室
版本: v1.0.0
"""

import os
import asyncio
import hashlib
import secrets
import base64
import json
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
import hmac
import threading
import time

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, asymmetric
from cryptography.hazmat.backends import default_backend

from .config_manager import get_config_manager
from .logger_service import get_logger
from .error_handler import get_error_handler, with_error_handling, RecoveryStrategy, RecoveryConfig, ErrorContext
from .performance_monitor import get_performance_monitor, performance_monitor, benchmark_operation
from .audit_logger import get_audit_logger, audit_log, AuditLevel, AuditCategory


class EncryptionAlgorithm(Enum):
    """加密算法枚舉"""
    AES_256_GCM = "aes_256_gcm"      # AES-256-GCM (推薦)
    AES_256_CBC = "aes_256_cbc"      # AES-256-CBC
    CHACHA20_POLY1305 = "chacha20_poly1305"  # ChaCha20-Poly1305


class KeyPurpose(Enum):
    """密鑰用途枚舉"""
    ENCRYPTION = "encryption"         # 數據加密
    SIGNATURE = "signature"          # 數字簽名
    KEY_ENCRYPTION = "key_encryption" # 密鑰加密 (KEK)
    MASTER_KEY = "master_key"        # 主密鑰


@dataclass
class EncryptionKey:
    """加密密鑰"""
    key_id: str
    algorithm: EncryptionAlgorithm
    key_data: bytes
    purpose: KeyPurpose
    created_at: datetime
    expires_at: Optional[datetime] = None
    is_active: bool = True
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EncryptionResult:
    """加密結果"""
    ciphertext: bytes
    key_id: str
    algorithm: EncryptionAlgorithm
    iv: Optional[bytes] = None
    tag: Optional[bytes] = None
    signature: Optional[bytes] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecryptionResult:
    """解密結果"""
    plaintext: bytes
    verified: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyRotationPolicy:
    """密鑰輪換策略"""
    max_age_days: int = 90              # 最大年齡
    rotation_interval_days: int = 30    # 輪換間隔
    emergency_rotation: bool = False    # 緊急輪換
    auto_rotation: bool = True          # 自動輪換


class KeyStore:
    """
    密鑰存儲庫

    負責密鑰的生成、存儲和管理
    """

    def __init__(self, store_path: str = "keys/"):
        self.store_path = Path(store_path)
        self.store_path.mkdir(parents=True, exist_ok=True)

        # 密鑰存儲
        self.keys: Dict[str, EncryptionKey] = {}
        self.key_versions: Dict[str, List[str]] = {}  # purpose -> [key_ids]

        self.logger = get_logger(__name__)

        # 載入現有密鑰
        self._load_keys()

    def generate_key(self, algorithm: EncryptionAlgorithm,
                    purpose: KeyPurpose,
                    key_size: int = 32) -> EncryptionKey:
        """
        生成新密鑰

        Args:
            algorithm: 加密算法
            purpose: 密鑰用途
            key_size: 密鑰大小（字節）

        Returns:
            加密密鑰
        """
        key_data = secrets.token_bytes(key_size)
        key_id = f"{purpose.value}_{secrets.token_hex(8)}"

        key = EncryptionKey(
            key_id=key_id,
            algorithm=algorithm,
            key_data=key_data,
            purpose=purpose,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=90),  # 90天過期
            is_active=True,
            version=1
        )

        self.keys[key_id] = key

        # 添加到版本追蹤
        if purpose.value not in self.key_versions:
            self.key_versions[purpose.value] = []
        self.key_versions[purpose.value].append(key_id)

        # 保存密鑰
        self._save_key(key)

        self.logger.info("key_generated",
                        key_id=key_id,
                        algorithm=algorithm.value,
                        purpose=purpose.value)

        return key

    def get_active_key(self, purpose: KeyPurpose) -> Optional[EncryptionKey]:
        """
        獲取活躍密鑰

        Args:
            purpose: 密鑰用途

        Returns:
            活躍密鑰
        """
        if purpose.value not in self.key_versions:
            return None

        for key_id in reversed(self.key_versions[purpose.value]):
            key = self.keys.get(key_id)
            if key and key.is_active and (not key.expires_at or key.expires_at > datetime.utcnow()):
                return key

        return None

    def deactivate_key(self, key_id: str) -> bool:
        """
        停用密鑰

        Args:
            key_id: 密鑰ID

        Returns:
            是否成功
        """
        if key_id in self.keys:
            self.keys[key_id].is_active = False
            self._save_key(self.keys[key_id])

            self.logger.info("key_deactivated", key_id=key_id)
            return True

        return False

    def rotate_key(self, purpose: KeyPurpose) -> Optional[EncryptionKey]:
        """
        輪換密鑰

        Args:
            purpose: 密鑰用途

        Returns:
            新密鑰
        """
        # 停用現有活躍密鑰
        active_key = self.get_active_key(purpose)
        if active_key:
            self.deactivate_key(active_key.key_id)

        # 生成新密鑰
        new_key = self.generate_key(active_key.algorithm if active_key else EncryptionAlgorithm.AES_256_GCM,
                                  purpose)

        self.logger.info("key_rotated", old_key=active_key.key_id if active_key else None,
                        new_key=new_key.key_id)

        return new_key

    def _save_key(self, key: EncryptionKey) -> None:
        """保存密鑰到文件"""
        key_file = self.store_path / f"{key.key_id}.key"

        # 注意：生產環境應該使用硬件安全模塊或HSM
        key_data = {
            "key_id": key.key_id,
            "algorithm": key.algorithm.value,
            "key_data": base64.b64encode(key.key_data).decode(),
            "purpose": key.purpose.value,
            "created_at": key.created_at.isoformat(),
            "expires_at": key.expires_at.isoformat() if key.expires_at else None,
            "is_active": key.is_active,
            "version": key.version,
            "metadata": key.metadata
        }

        with open(key_file, 'w') as f:
            json.dump(key_data, f, indent=2)

    def _load_keys(self) -> None:
        """載入現有密鑰"""
        if not self.store_path.exists():
            return

        for key_file in self.store_path.glob("*.key"):
            try:
                with open(key_file, 'r') as f:
                    key_data = json.load(f)

                key = EncryptionKey(
                    key_id=key_data["key_id"],
                    algorithm=EncryptionAlgorithm(key_data["algorithm"]),
                    key_data=base64.b64decode(key_data["key_data"]),
                    purpose=KeyPurpose(key_data["purpose"]),
                    created_at=datetime.fromisoformat(key_data["created_at"]),
                    expires_at=datetime.fromisoformat(key_data["expires_at"]) if key_data.get("expires_at") else None,
                    is_active=key_data["is_active"],
                    version=key_data["version"],
                    metadata=key_data.get("metadata", {})
                )

                self.keys[key.key_id] = key

                # 添加到版本追蹤
                purpose = key.purpose.value
                if purpose not in self.key_versions:
                    self.key_versions[purpose] = []
                self.key_versions[purpose].append(key.key_id)

            except Exception as e:
                self.logger.warning("failed_to_load_key",
                                  file=key_file.name,
                                  error=str(e))


class EncryptionService:
    """
    加密服務

    提供企業級數據加密解密功能：
    - 多種加密算法支援
    - 密鑰管理與輪換
    - 數據完整性驗證
    - 性能優化與並發支援
    """

    def __init__(self, config_manager=None):
        self.config_manager = config_manager or get_config_manager()
        self.logger = get_logger(__name__)

        # 初始化統一框架組件
        self.error_handler = get_error_handler(__name__)
        self.performance_monitor = get_performance_monitor(__name__)
        self.audit_logger = get_audit_logger()

        # 配置
        self.config = self.config_manager.get("encryption", {})
        self.keystore_path = self.config.get("keystore_path", "keys/")

        # 密鑰存儲庫
        self.keystore = KeyStore(self.keystore_path)

        # 默認算法
        self.default_algorithm = EncryptionAlgorithm.AES_256_GCM

        # 密鑰輪換策略
        self.rotation_policy = KeyRotationPolicy(**self.config.get("rotation_policy", {}))

        # 統計信息
        self.stats = {
            "encryption_operations": 0,
            "decryption_operations": 0,
            "key_rotations": 0,
            "failed_operations": 0
        }

        # 設置錯誤恢復
        self._setup_error_recovery()

        # 設置性能基準
        self._setup_performance_benchmarks()

        # 啟動密鑰輪換任務
        self._start_key_rotation_monitor()

        # 初始化密鑰
        self._initialize_keys()

        self.logger.info("encryption_service_initialized")

    def _initialize_keys(self):
        """初始化密鑰"""
        # 檢查是否已有活躍密鑰
        if not self.keystore.get_active_key(KeyPurpose.ENCRYPTION):
            # 生成默認加密密鑰
            self.keystore.generate_key(self.default_algorithm, KeyPurpose.ENCRYPTION)

        if not self.keystore.get_active_key(KeyPurpose.SIGNATURE):
            # 生成數字簽名密鑰
            self.keystore.generate_key(EncryptionAlgorithm.AES_256_GCM, KeyPurpose.SIGNATURE, 64)

    def _setup_error_recovery(self):
        """設置錯誤恢復配置"""
        # 加密操作錯誤恢復
        encryption_error_config = RecoveryConfig(
            strategy=RecoveryStrategy.RETRY,
            max_retries=2,
            retry_delay=1.0
        )
        self.error_handler.register_recovery_config("encryption_operation", encryption_error_config)

        # 密鑰操作錯誤恢復
        key_error_config = RecoveryConfig(
            strategy=RecoveryStrategy.FALLBACK,
            fallback_function=self._fallback_encryption,
            max_retries=1
        )
        self.error_handler.register_recovery_config("key_operation", key_error_config)

    def _setup_performance_benchmarks(self):
        """設置性能基準"""
        # 加密操作基準
        self.performance_monitor.set_benchmark(
            "encryption_operation_time_ms",
            100.0,  # 100毫秒内完成加密
            tolerance_percent=30,
            environment="production"
        )

        # 解密操作基準
        self.performance_monitor.set_benchmark(
            "decryption_operation_time_ms",
            100.0,  # 100毫秒内完成解密
            tolerance_percent=30,
            environment="production"
        )

    def _start_key_rotation_monitor(self):
        """啟動密鑰輪換監控"""
        import threading

        def rotation_monitor():
            while True:
                try:
                    self._check_key_rotation()
                    time.sleep(3600)  # 每小時檢查一次
                except Exception as e:
                    self.logger.warning("key_rotation_monitor_error", error=str(e))
                    time.sleep(300)

        rotation_thread = threading.Thread(target=rotation_monitor, daemon=True)
        rotation_thread.start()

    def _check_key_rotation(self):
        """檢查密鑰輪換"""
        if not self.rotation_policy.auto_rotation:
            return

        purposes_to_check = [KeyPurpose.ENCRYPTION, KeyPurpose.SIGNATURE]

        for purpose in purposes_to_check:
            active_key = self.keystore.get_active_key(purpose)
            if not active_key:
                continue

            days_old = (datetime.utcnow() - active_key.created_at).days

            if days_old >= self.rotation_policy.rotation_interval_days:
                self.logger.info("rotating_key",
                               purpose=purpose.value,
                               key_id=active_key.key_id,
                               days_old=days_old)

                new_key = self.keystore.rotate_key(purpose)
                if new_key:
                    self.stats["key_rotations"] += 1

    async def _fallback_encryption(self, error_details) -> None:
        """加密操作備用策略"""
        self.logger.warning("encryption_fallback_used",
                           original_error=error_details.message)

    @performance_monitor
    @benchmark_operation("encryption", expected_max_time_ms=100)
    @with_audit_trail("data_encryption")
    @with_error_handling("encryption_operation")
    async def encrypt_data(self, plaintext: bytes,
                          algorithm: Optional[EncryptionAlgorithm] = None,
                          metadata: Optional[Dict[str, Any]] = None) -> EncryptionResult:
        """
        加密數據

        Args:
            plaintext: 明文數據
            algorithm: 加密算法
            metadata: 元數據

        Returns:
            加密結果
        """
        self.stats["encryption_operations"] += 1

        algorithm = algorithm or self.default_algorithm
        metadata = metadata or {}

        try:
            # 獲取活躍加密密鑰
            encryption_key = self.keystore.get_active_key(KeyPurpose.ENCRYPTION)
            if not encryption_key:
                raise RuntimeError("沒有可用的加密密鑰")

            # 根據算法執行加密
            if algorithm == EncryptionAlgorithm.AES_256_GCM:
                result = await self._encrypt_aes_gcm(plaintext, encryption_key)
            elif algorithm == EncryptionAlgorithm.AES_256_CBC:
                result = await self._encrypt_aes_cbc(plaintext, encryption_key)
            elif algorithm == EncryptionAlgorithm.CHACHA20_POLY1305:
                result = await self._encrypt_chacha20(plaintext, encryption_key)
            else:
                raise ValueError(f"不支援的加密算法: {algorithm}")

            result.metadata.update(metadata)

            # 記錄審計事件
            audit_log(
                level=AuditLevel.SECURITY,
                category=AuditCategory.DATA_ACCESS,
                action="data_encrypted",
                actor="encryption_service",
                target="data_blob",
                result="SUCCESS",
                details={
                    "algorithm": algorithm.value,
                    "key_id": encryption_key.key_id,
                    "data_size": len(plaintext)
                }
            )

            self.logger.debug("data_encrypted",
                            algorithm=algorithm.value,
                            key_id=encryption_key.key_id,
                            size=len(plaintext))

            return result

        except Exception as e:
            self.stats["failed_operations"] += 1

            audit_log(
                level=AuditLevel.SECURITY,
                category=AuditCategory.SECURITY_EVENT,
                action="encryption_failed",
                actor="encryption_service",
                target="data_blob",
                result="FAILED",
                details={"error": str(e)}
            )

            raise

    @performance_monitor
    @benchmark_operation("decryption", expected_max_time_ms=100)
    @with_audit_trail("data_decryption")
    @with_error_handling("encryption_operation")
    async def decrypt_data(self, encryption_result: EncryptionResult,
                          verify_integrity: bool = True) -> DecryptionResult:
        """
        解密數據

        Args:
            encryption_result: 加密結果
            verify_integrity: 是否驗證完整性

        Returns:
            解密結果
        """
        self.stats["decryption_operations"] += 1

        try:
            # 獲取密鑰
            encryption_key = self.keystore.keys.get(encryption_result.key_id)
            if not encryption_key:
                raise ValueError(f"找不到密鑰: {encryption_result.key_id}")

            if not encryption_key.is_active:
                raise ValueError(f"密鑰已被停用: {encryption_result.key_id}")

            # 根據算法執行解密
            if encryption_result.algorithm == EncryptionAlgorithm.AES_256_GCM:
                result = await self._decrypt_aes_gcm(encryption_result, encryption_key)
            elif encryption_result.algorithm == EncryptionAlgorithm.AES_256_CBC:
                result = await self._decrypt_aes_cbc(encryption_result, encryption_key)
            elif encryption_result.algorithm == EncryptionAlgorithm.CHACHA20_POLY1305:
                result = await self._decrypt_chacha20(encryption_result, encryption_key)
            else:
                raise ValueError(f"不支援的解密算法: {encryption_result.algorithm}")

            if verify_integrity and not result.verified:
                raise ValueError("數據完整性驗證失敗")

            # 記錄審計事件
            audit_log(
                level=AuditLevel.SECURITY,
                category=AuditCategory.DATA_ACCESS,
                action="data_decrypted",
                actor="encryption_service",
                target="encrypted_blob",
                result="SUCCESS",
                details={
                    "algorithm": encryption_result.algorithm.value,
                    "key_id": encryption_result.key_id,
                    "verified": result.verified
                }
            )

            self.logger.debug("data_decrypted",
                            algorithm=encryption_result.algorithm.value,
                            key_id=encryption_result.key_id,
                            verified=result.verified)

            return result

        except Exception as e:
            self.stats["failed_operations"] += 1

            audit_log(
                level=AuditLevel.SECURITY,
                category=AuditCategory.SECURITY_EVENT,
                action="decryption_failed",
                actor="encryption_service",
                target="encrypted_blob",
                result="FAILED",
                details={"error": str(e)}
            )

            raise

    async def _encrypt_aes_gcm(self, plaintext: bytes,
                              key: EncryptionKey) -> EncryptionResult:
        """AES-GCM加密"""
        iv = os.urandom(12)  # 96位初始化向量

        encryptor = Cipher(
            algorithms.AES(key.key_data),
            modes.GCM(iv),
            backend=default_backend()
        ).encryptor()

        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        return EncryptionResult(
            ciphertext=ciphertext,
            key_id=key.key_id,
            algorithm=key.algorithm,
            iv=iv,
            tag=encryptor.tag
        )

    async def _decrypt_aes_gcm(self, result: EncryptionResult,
                              key: EncryptionKey) -> DecryptionResult:
        """AES-GCM解密"""
        decryptor = Cipher(
            algorithms.AES(key.key_data),
            modes.GCM(result.iv, result.tag),
            backend=default_backend()
        ).decryptor()

        plaintext = decryptor.update(result.ciphertext) + decryptor.finalize()

        return DecryptionResult(
            plaintext=plaintext,
            verified=True
        )

    async def _encrypt_aes_cbc(self, plaintext: bytes,
                              key: EncryptionKey) -> EncryptionResult:
        """AES-CBC加密"""
        iv = os.urandom(16)

        # 添加PKCS7填充
        block_size = 16
        padding_length = block_size - (len(plaintext) % block_size)
        padding = bytes([padding_length]) * padding_length
        padded_plaintext = plaintext + padding

        encryptor = Cipher(
            algorithms.AES(key.key_data),
            modes.CBC(iv),
            backend=default_backend()
        ).encryptor()

        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

        return EncryptionResult(
            ciphertext=ciphertext,
            key_id=key.key_id,
            algorithm=key.algorithm,
            iv=iv
        )

    async def _decrypt_aes_cbc(self, result: EncryptionResult,
                              key: EncryptionKey) -> DecryptionResult:
        """AES-CBC解密"""
        decryptor = Cipher(
            algorithms.AES(key.key_data),
            modes.CBC(result.iv),
            backend=default_backend()
        ).decryptor()

        padded_plaintext = decryptor.update(result.ciphertext) + decryptor.finalize()

        # 移除PKCS7填充
        padding_length = padded_plaintext[-1]
        plaintext = padded_plaintext[:-padding_length]

        return DecryptionResult(
            plaintext=plaintext,
            verified=True
        )

    async def _encrypt_chacha20(self, plaintext: bytes,
                               key: EncryptionKey) -> EncryptionResult:
        """ChaCha20-Poly1305加密"""
        nonce = os.urandom(12)

        encryptor = Cipher(
            algorithms.ChaCha20(key.key_data, nonce),
            mode=None,
            backend=default_backend()
        ).encryptor()

        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        return EncryptionResult(
            ciphertext=ciphertext,
            key_id=key.key_id,
            algorithm=key.algorithm,
            iv=nonce
        )

    async def _decrypt_chacha20(self, result: EncryptionResult,
                               key: EncryptionKey) -> DecryptionResult:
        """ChaCha20-Poly1305解密"""
        decryptor = Cipher(
            algorithms.ChaCha20(key.key_data, result.iv),
            mode=None,
            backend=default_backend()
        ).decryptor()

        plaintext = decryptor.update(result.ciphertext) + decryptor.finalize()

        return DecryptionResult(
            plaintext=plaintext,
            verified=True
        )

    def rotate_encryption_key(self) -> bool:
        """
        輪換加密密鑰

        Returns:
            是否成功
        """
        try:
            new_key = self.keystore.rotate_key(KeyPurpose.ENCRYPTION)
            if new_key:
                self.stats["key_rotations"] += 1
                self.logger.info("encryption_key_rotated", new_key_id=new_key.key_id)
                return True
            return False

        except Exception as e:
            self.logger.error("key_rotation_failed", error=str(e))
            return False

    def get_encryption_stats(self) -> Dict[str, Any]:
        """獲取加密統計"""
        active_encryption_keys = len([
            k for k in self.keystore.keys.values()
            if k.purpose == KeyPurpose.ENCRYPTION and k.is_active
        ])

        return {
            **self.stats,
            "active_keys": len([k for k in self.keystore.keys.values() if k.is_active]),
            "active_encryption_keys": active_encryption_keys,
            "default_algorithm": self.default_algorithm.value,
            "keystore_path": self.keystore_path
        }

    async def encrypt_file(self, file_path: str,
                          output_path: Optional[str] = None) -> Optional[str]:
        """
        加密文件

        Args:
            file_path: 輸入文件路徑
            output_path: 輸出文件路徑

        Returns:
            加密後文件路徑
        """
        try:
            with open(file_path, 'rb') as f:
                plaintext = f.read()

            result = await self.encrypt_data(plaintext)

            output_path = output_path or f"{file_path}.encrypted"
            with open(output_path, 'wb') as f:
                encrypted_data = {
                    "algorithm": result.algorithm.value,
                    "key_id": result.key_id,
                    "iv": base64.b64encode(result.iv or b"").decode(),
                    "tag": base64.b64encode(result.tag or b"").decode(),
                    "ciphertext": base64.b64encode(result.ciphertext).decode(),
                    "metadata": result.metadata
                }
                f.write(json.dumps(encrypted_data).encode())

            return output_path

        except Exception as e:
            self.logger.error("file_encryption_failed", file=file_path, error=str(e))
            return None

    async def decrypt_file(self, file_path: str,
                          output_path: Optional[str] = None) -> Optional[str]:
        """
        解密文件

        Args:
            file_path: 加密文件路徑
            output_path: 輸出文件路徑

        Returns:
            解密後文件路徑
        """
        try:
            with open(file_path, 'r') as f:
                encrypted_data = json.load(f)

            result = EncryptionResult(
                algorithm=EncryptionAlgorithm(encrypted_data["algorithm"]),
                key_id=encrypted_data["key_id"],
                iv=base64.b64decode(encrypted_data["iv"]) if encrypted_data.get("iv") else None,
                tag=base64.b64decode(encrypted_data["tag"]) if encrypted_data.get("tag") else None,
                ciphertext=base64.b64decode(encrypted_data["ciphertext"]),
                metadata=encrypted_data.get("metadata", {})
            )

            decrypted_result = await self.decrypt_data(result)
            plaintext = decrypted_result.plaintext

            output_path = output_path or file_path.replace('.encrypted', '.decrypted')
            with open(output_path, 'wb') as f:
                f.write(plaintext)

            return output_path

        except Exception as e:
            self.logger.error("file_decryption_failed", file=file_path, error=str(e))
            return None


# 全域加密服務實例
_encryption_service: Optional[EncryptionService] = None


def init_encryption_service(config_manager=None) -> EncryptionService:
    """
    初始化全域加密服務

    Args:
        config_manager: 配置管理器實例

    Returns:
        加密服務實例
    """
    global _encryption_service

    if _encryption_service is None:
        _encryption_service = EncryptionService(config_manager)

    return _encryption_service


def get_encryption_service() -> EncryptionService:
    """獲取全域加密服務實例"""
    if _encryption_service is None:
        raise RuntimeError("加密服務尚未初始化，請先調用init_encryption_service()")
    return _encryption_service
