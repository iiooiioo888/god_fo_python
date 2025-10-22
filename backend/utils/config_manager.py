"""
WebCrawler Commander - 配置管理器
根據安全性要求和企業級標準實現統一配置管理

核心功能：
- 多格式配置支援 (YAML/JSON/TOML)
- 環境變數分層覆蓋
- 配置驗證與錯誤檢查
- 熱重載機制
- 敏感信息加密存儲
- 回滾與版本控制

作者: Jerry開發工作室
版本: v1.0.0
"""

import os
import json
import yaml
import toml
import hashlib
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod

import structlog
from pydantic import BaseModel, ValidationError, Field
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import watchfiles
import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading
import time


class ConfigFormat(Enum):
    """支援的配置文件格式"""
    YAML = "yaml"
    JSON = "json"
    TOML = "toml"


class Environment(Enum):
    """環境類型"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class EncryptionProvider(ABC):
    """配置加密提供者抽象基類"""

    @abstractmethod
    def encrypt(self, data: str) -> str:
        """加密數據"""
        pass

    @abstractmethod
    def decrypt(self, encrypted_data: str) -> str:
        """解密數據"""
        pass


class FernetEncryptionProvider(EncryptionProvider):
    """Fernet對稱加密提供者"""

    def __init__(self, key: Optional[str] = None):
        if key is None:
            # 生成一個32字节的密鑰
            key = base64.urlsafe_b64encode(os.urandom(32)).decode()
        self.key = key
        self.cipher = Fernet(key.encode())

    def encrypt(self, data: str) -> str:
        """加密字符串數據"""
        try:
            encrypted = self.cipher.encrypt(data.encode())
            return encrypted.decode()
        except Exception as e:
            structlog.get_logger().error(
                "config_encryption_failed",
                error=str(e),
                operation="encrypt"
            )
            raise

    def decrypt(self, encrypted_data: str) -> str:
        """解密字符串數據"""
        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except InvalidToken:
            raise ValueError("無效的加密數據或密鑰")
        except Exception as e:
            structlog.get_logger().error(
                "config_decryption_failed",
                error=str(e),
                operation="decrypt"
            )
            raise


class ConfigSource(ABC):
    """配置源抽象基類"""

    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """載入配置"""
        pass

    @abstractmethod
    def save(self, config: Dict[str, Any]) -> None:
        """保存配置"""
        pass

    @property
    @abstractmethod
    def priority(self) -> int:
        """配置源優先級 (數字越小優先級越高)"""
        pass


class FileConfigSource(ConfigSource):
    """文件配置源"""

    def __init__(self, file_path: Union[str, Path], format_type: ConfigFormat,
                 encoding: str = 'utf-8', priority: int = 10):
        self.file_path = Path(file_path)
        self.format_type = format_type
        self.encoding = encoding
        self._priority = priority
        self.last_modified = None

    def load(self) -> Dict[str, Any]:
        """從文件載入配置"""
        if not self.file_path.exists():
            return {}

        try:
            with open(self.file_path, 'r', encoding=self.encoding) as f:
                content = f.read()

            # 更新最後修改時間
            self.last_modified = self.file_path.stat().st_mtime

            if self.format_type == ConfigFormat.JSON:
                return json.loads(content)
            elif self.format_type == ConfigFormat.YAML:
                return yaml.safe_load(content) or {}
            elif self.format_type == ConfigFormat.TOML:
                return toml.loads(content)
            else:
                raise ValueError(f"不支援的格式: {self.format_type}")

        except Exception as e:
            structlog.get_logger().error(
                "config_file_load_failed",
                file_path=str(self.file_path),
                format_type=self.format_type.value,
                error=str(e)
            )
            return {}

    def save(self, config: Dict[str, Any]) -> None:
        """保存配置到文件"""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.file_path, 'w', encoding=self.encoding) as f:
                if self.format_type == ConfigFormat.JSON:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                elif self.format_type == ConfigFormat.YAML:
                    yaml.dump(config, f, default_flow_style=False,
                             allow_unicode=True, indent=2)
                elif self.format_type == ConfigFormat.TOML:
                    f.write(toml.dumps(config))
                else:
                    raise ValueError(f"不支援的格式: {self.format_type}")

            # 更新修改時間
            self.last_modified = self.file_path.stat().st_mtime

            structlog.get_logger().info(
                "config_file_saved",
                file_path=str(self.file_path),
                format_type=self.format_type.value
            )

        except Exception as e:
            structlog.get_logger().error(
                "config_file_save_failed",
                file_path=str(self.file_path),
                error=str(e)
            )
            raise

    @property
    def priority(self) -> int:
        return self._priority


class EnvironmentConfigSource(ConfigSource):
    """環境變數配置源"""

    def __init__(self, prefix: str = "WEBCRAWLER_", priority: int = 1):
        self.prefix = prefix.upper()
        self._priority = priority

    def load(self) -> Dict[str, Any]:
        """從環境變數載入配置"""
        config = {}
        prefix_len = len(self.prefix)

        for key, value in os.environ.items():
            if key.startswith(self.prefix):
                # 移除前綴並轉換為小寫下劃線格式
                config_key = key[prefix_len:].lower().replace('_', '.')
                config_value = self._parse_env_value(value)
                self._set_nested_value(config, config_key.split('.'), config_value)

        return config

    def save(self, config: Dict[str, Any]) -> None:
        """環境變數不支持保存"""
        structlog.get_logger().warning(
            "environment_config_readonly",
            message="環境變數配置源為只讀"
        )

    def _parse_env_value(self, value: str) -> Union[str, int, float, bool, List, Dict]:
        """解析環境變數值"""
        value = value.strip()

        # 嘗試解析為布林值
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'

        # 嘗試解析為數字
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            pass

        # 嘗試解析為JSON
        if value.startswith(('{', '[')):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass

        # 默認為字符串
        return value

    def _set_nested_value(self, config: Dict[str, Any], keys: List[str], value: Any):
        """設置嵌套字典值"""
        if len(keys) == 1:
            config[keys[0]] = value
        else:
            if keys[0] not in config:
                config[keys[0]] = {}
            elif not isinstance(config[keys[0]], dict):
                config[keys[0]] = {}
            self._set_nested_value(config[keys[0]], keys[1:], value)

    @property
    def priority(self) -> int:
        return self._priority


class ConfigValidator(BaseModel):
    """配置驗證器"""

    # 系統基礎配置
    app_name: str = Field(default="WebCrawler Commander", min_length=1)
    version: str = Field(default="1.0.0")
    environment: str = Field(default="development", pattern="^(development|testing|staging|production)$")

    # 服務器配置
    server_host: str = Field(default="0.0.0.0")
    server_port: int = Field(default=8000, gt=0, le=65535)
    server_workers: int = Field(default=1, ge=1)

    # 數據庫配置 (加密存儲)
    database_url: Optional[str] = None
    database_pool_size: int = Field(default=20, ge=1, le=100)
    database_max_overflow: int = Field(default=30, ge=0, le=100)

    # Redis配置 (加密存儲)
    redis_url: Optional[str] = None
    redis_cluster: bool = Field(default=False)
    redis_pool_size: int = Field(default=20, ge=1)

    # 爬蟲配置
    crawler_timeout: float = Field(default=30.0, gt=0)
    crawler_max_concurrent: int = Field(default=100, ge=1, le=1000)
    crawler_user_agent_rotation: bool = Field(default=True)

    # 代理配置
    proxy_enabled: bool = Field(default=True)
    proxy_validation_interval: int = Field(default=300, ge=60)
    proxy_health_threshold: float = Field(default=0.8, ge=0, le=1)

    # 安全配置
    security_jwt_secret: Optional[str] = None
    security_jwt_algorithm: str = Field(default="HS256")
    security_jwt_expiration: int = Field(default=3600, ge=300)

    # 日誌配置
    logging_level: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    logging_file_path: Optional[Path] = None
    logging_max_file_size: str = Field(default="10 MB")
    logging_backup_count: int = Field(default=5, ge=1)

    # 資源限制
    resources_max_memory_mb: int = Field(default=1024, ge=128)
    resources_max_cpu_percent: float = Field(default=80.0, ge=1, le=100)
    resources_max_connections: int = Field(default=1000, ge=1)

    class Config:
        validate_assignment = True


@dataclass
class ConfigMetadata:
    """配置元數據"""
    version: str = "1.0"
    created_at: datetime = field(default_factory=datetime.utcnow)
    modified_at: datetime = field(default_factory=datetime.utcnow)
    checksum: str = ""
    environment: str = "development"
    sources: List[str] = field(default_factory=list)


class ConfigurationError(Exception):
    """配置相關錯誤"""
    pass


class ValidationError(ConfigurationError):
    """配置驗證錯誤"""
    pass


class ConfigManager:
    """
    統一配置管理器

    實現企業級配置管理需求：
    - 多來源配置支持
    - 環境變數覆蓋
    - 熱重載機制
    - 安全加密存儲
    - 配置版本控制
    """

    def __init__(self,
                 config_dir: Union[str, Path] = "config",
                 environment: str = None,
                 encryption_key: Optional[str] = None,
                 watch_exclude: Optional[List[str]] = None):
        self.config_dir = Path(config_dir)
        self.environment = environment or os.getenv("WEBCRAWLER_ENV", "development")
        self.logger = structlog.get_logger(__name__)

        # 初始化加密提供者
        self.encryption = FernetEncryptionProvider(encryption_key)

        # 監視排除模式
        self._watch_exclude = watch_exclude or ["logs", "__pycache__", "*.tmp", "*.bak"]

        # 配置源列表 (按優先級排序)
        self.sources: List[ConfigSource] = []
        self._init_config_sources()

        # 配置快取
        self._config_cache: Dict[str, Any] = {}
        self._config_metadata = ConfigMetadata(environment=self.environment)

        # 驗證器
        self.validator = ConfigValidator

        # 熱重載相關
        self._hot_reload_enabled = True
        self._watch_thread: Optional[threading.Thread] = None
        self._stop_watching = threading.Event()
        self._reload_callbacks: List[Callable] = []

        # 統計信息
        self._load_count = 0
        self._reload_count = 0
        self._last_load_time = None

        self.logger.info("config_manager_initialized", environment=self.environment)

    def _init_config_sources(self):
        """初始化配置源"""
        # 1. 環境變數 (最高優先級)
        self.sources.append(EnvironmentConfigSource())

        # 2. 環境特定配置文件
        env_config_path = self.config_dir / f"config.{self.environment}.yaml"
        if env_config_path.exists():
            self.sources.append(FileConfigSource(
                env_config_path, ConfigFormat.YAML, priority=5
            ))

        # 3. 默認配置文件
        default_config_path = self.config_dir / "config.yaml"
        if default_config_path.exists():
            self.sources.append(FileConfigSource(
                default_config_path, ConfigFormat.YAML, priority=10
            ))

        # 排序來源 (按優先級)
        self.sources.sort(key=lambda s: s.priority)

    def load_config(self, validate: bool = True) -> Dict[str, Any]:
        """
        載入配置 (合併所有來源)

        Args:
            validate: 是否進行配置驗證

        Returns:
            配置字典
        """
        try:
            merged_config = {}

            # 從每個來源載入並合併配置
            for source in self.sources:
                source_config = source.load()
                self.logger.debug("config_source_loaded",
                                source=source.__class__.__name__,
                                config_keys=list(source_config.keys()))

                # 深度合併配置
                merged_config = self._deep_merge(merged_config, source_config)

            # 處理編碼配置
            merged_config = self._process_encrypted_fields(merged_config)

            # 驗證配置
            if validate:
                merged_config = self._validate_config(merged_config)

            # 更新快取和元數據
            self._config_cache = merged_config
            self._config_metadata.modified_at = datetime.utcnow()
            self._config_metadata.checksum = self._calculate_checksum(merged_config)
            self._config_metadata.sources = [
                source.__class__.__name__ for source in self.sources
            ]

            # 更新統計
            self._load_count += 1
            self._last_load_time = datetime.utcnow()

            self.logger.info("config_loaded_successfully",
                           source_count=len(self.sources),
                           config_keys=len(merged_config))

            return merged_config

        except Exception as e:
            self.logger.error("config_load_failed", error=str(e))
            raise ConfigurationError(f"配置載入失敗: {e}") from e

    def get(self, key: str, default: Any = None) -> Any:
        """
        獲取配置值 (支持點分隔鍵路徑)

        Args:
            key: 配置鍵 (例如: "database.host")
            default: 默認值

        Returns:
            配置值
        """
        if not self._config_cache:
            self.load_config()

        keys = key.split('.')
        value = self._config_cache

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any, save_to_file: bool = False) -> None:
        """
        設置配置值

        Args:
            key: 配置鍵
            value: 配置值
            save_to_file: 是否保存到文件
        """
        keys = key.split('.')
        config = self._config_cache if self._config_cache else {}

        # 設置嵌套值
        self._set_nested_value(config, keys, value)
        self._config_cache = config

        # 更新元數據
        self._config_metadata.modified_at = datetime.utcnow()
        self._config_metadata.checksum = self._calculate_checksum(config)

        if save_to_file and len(self.sources) > 1:
            # 保存到第一個文件源
            file_sources = [s for s in self.sources if isinstance(s, FileConfigSource)]
            if file_sources:
                file_sources[0].save(config)

        self.logger.info("config_value_set", key=key, value_type=type(value).__name__)

    def enable_hot_reload(self, callback: Optional[Callable] = None):
        """
        啟用熱重載

        Args:
            callback: 重載完成後的回調函數
        """
        if callback:
            self._reload_callbacks.append(callback)

        if not self._watch_thread or not self._watch_thread.is_alive():
            self._watch_thread = threading.Thread(
                target=self._watch_config_files,
                daemon=True
            )
            self._watch_thread.start()

            self.logger.info("hot_reload_enabled")

    def disable_hot_reload(self):
        """禁用熱重載"""
        self._hot_reload_enabled = False
        self._stop_watching.set()

        if self._watch_thread:
            self._watch_thread.join(timeout=5)

        self.logger.info("hot_reload_disabled")

    def get_config_stats(self) -> Dict[str, Any]:
        """獲取配置統計信息"""
        return {
            "load_count": self._load_count,
            "reload_count": self._reload_count,
            "last_load_time": self._last_load_time.isoformat() if self._last_load_time else None,
            "source_count": len(self.sources),
            "cache_size": len(self._config_cache),
            "metadata": {
                "version": self._config_metadata.version,
                "created_at": self._config_metadata.created_at.isoformat(),
                "modified_at": self._config_metadata.modified_at.isoformat(),
                "checksum": self._config_metadata.checksum[:8] + "...",
                "environment": self._config_metadata.environment
            }
        }

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """深度合併字典"""
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result

    def _process_encrypted_fields(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """處理加密字段"""
        encrypted_fields = [
            'database.password',
            'database.url',
            'redis.url',
            'security.jwt.secret',
            'security.encryption.key'
        ]

        result = config.copy()

        for field_path in encrypted_fields:
            # 直接從配置字典獲取值，避免遞歸調用
            keys = field_path.split('.')
            encrypted_value = self._get_nested_value(config, keys)
            if encrypted_value and isinstance(encrypted_value, str):
                try:
                    # 嘗試解密
                    if encrypted_value.startswith('encrypted:'):
                        decrypted = self.encryption.decrypt(encrypted_value[10:])
                        self._set_nested_value(result, keys, decrypted)
                except Exception:
                    # 如果解密失敗，保留原值但記錄警告
                    self.logger.warning("config_decryption_failed", field=field_path)

        return result

    def _get_nested_value(self, config: Dict[str, Any], keys: List[str]) -> Any:
        """獲取嵌套字典值"""
        value = config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return None

    def _validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """驗證配置"""
        try:
            # 刪除驗證器不需要的字段
            validator_config = {}
            validator_fields = self.validator.__fields__.keys()

            for key, value in config.items():
                if key in validator_fields:
                    validator_config[key] = value

            # 進行驗證
            validated = self.validator(**validator_config)
            return config

        except ValidationError as e:
            self.logger.error("config_validation_failed", errors=e.errors())
            raise ValidationError("配置驗證失敗", errors=e.errors()) from e

    def _calculate_checksum(self, config: Dict[str, Any]) -> str:
        """計算配置校驗和"""
        config_str = json.dumps(config, sort_keys=True, default=str)
        return hashlib.sha256(config_str.encode()).hexdigest()

    def _set_nested_value(self, config: Dict[str, Any], keys: List[str], value: Any):
        """設置嵌套字典值"""
        if len(keys) == 1:
            config[keys[0]] = value
        else:
            if keys[0] not in config:
                config[keys[0]] = {}
            elif not isinstance(config[keys[0]], dict):
                config[keys[0]] = {}
            self._set_nested_value(config[keys[0]], keys[1:], value)

    def _watch_config_files(self):
        """監視配置文件變化"""
        file_paths = [
            source.file_path
            for source in self.sources
            if isinstance(source, FileConfigSource)
        ]

        if not file_paths:
            self.logger.warning("no_config_files_to_watch")
            return

        self.logger.debug("starting_config_file_watcher", files=file_paths)

        def on_change(path):
            if self._stop_watching.is_set():
                return

            self.logger.info("config_file_changed", path=path)
            try:
                self._trigger_reload()
            except Exception as e:
                self.logger.error("config_reload_failed", error=str(e))

        try:
            # 使用watchfiles庫監視文件變化
            import asyncio
            from watchfiles import awatch

            async def watch_task():
                async for changes in awatch(*file_paths, ignore_patterns=self._watch_exclude):
                    for change_type, path in changes:
                        if change_type.name in ('modified', 'created'):
                            on_change(path)

            asyncio.run(watch_task())

        except KeyboardInterrupt:
            pass
        except Exception as e:
            self.logger.error("config_watcher_error", error=str(e))

    def _trigger_reload(self):
        """觸發配置重載"""
        old_checksum = self._config_metadata.checksum

        try:
            new_config = self.load_config()
            new_checksum = self._calculate_checksum(new_config)

            if old_checksum != new_checksum:
                self._reload_count += 1
                self.logger.info("config_reloaded", reload_count=self._reload_count)

                # 執行回調
                for callback in self._reload_callbacks:
                    try:
                        callback(new_config)
                    except Exception as e:
                        self.logger.error("reload_callback_failed",
                                        callback=callback.__name__,
                                        error=str(e))
            else:
                self.logger.debug("config_unmodified_skip_reload")

        except Exception as e:
            self.logger.error("config_reload_error", error=str(e))

    def __enter__(self):
        """上下文管理器入口"""
        self.load_config()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.disable_hot_reload()


# 全域配置實例
_config_manager: Optional[ConfigManager] = None


def init_config_manager(config_dir: Union[str, Path] = "config",
                       environment: str = None,
                       encryption_key: Optional[str] = None,
                       enable_hot_reload: bool = True,
                       watch_exclude: Optional[List[str]] = None) -> ConfigManager:
    """
    初始化全域配置管理器

    Args:
        config_dir: 配置目錄
        environment: 環境類型
        encryption_key: 加密密鑰
        enable_hot_reload: 是否啟用熱重載

    Returns:
        配置管理器實例
    """
    global _config_manager

    _config_manager = ConfigManager(config_dir, environment, encryption_key, watch_exclude)

    if enable_hot_reload:
        _config_manager.enable_hot_reload()

    return _config_manager


def get_config_manager() -> ConfigManager:
    """獲取全域配置管理器實例"""
    if _config_manager is None:
        raise ConfigurationError("配置管理器尚未初始化，請先調用init_config_manager()")
    return _config_manager


def get_config(key: str, default: Any = None) -> Any:
    """便捷函數：獲取配置值"""
    return get_config_manager().get(key, default)


def set_config(key: str, value: Any, save_to_file: bool = False) -> None:
    """便捷函數：設置配置值"""
    return get_config_manager().set(key, value, save_to_file)
