"""
WebCrawler Commander - 配置管理器單元測試

測試覆蓋：
- 配置載入與解析
- 配置獲取與設置
- 環境覆蓋
- 熱重載功能
- 配置統計信息

作者: Jerry開發工作室
版本: v1.0.0
"""

import os
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from utils.config_manager import ConfigManager, get_config_manager, init_config_manager
from tests.test_utils import TestDataFactory, temp_file


@pytest.mark.unit
@pytest.mark.config
class TestConfigManagerInitialization:
    """配置管理器初始化測試"""

    def test_config_manager_creation(self):
        """測試配置管理器創建"""
        with temp_file() as config_file:
            # 創建測試配置文件
            config_data = """
app:
  name: "Test App"
  version: "1.0.0"
server:
  port: 3000
"""
            config_file.write_text(config_data)

            # 創建配置管理器
            config_dir = config_file.parent
            manager = ConfigManager(
                config_dir=str(config_dir),
                environment="test"
            )

            assert manager is not None
            assert manager.config_dir == str(config_dir)
            assert manager.environment == "test"

    def test_config_manager_singleton(self):
        """測試配置管理器單例模式"""
        with temp_file() as config_file:
            config_data = "app:\n  name: 'Test'\n"
            config_file.write_text(config_data)

            # 初始化管理器
            init_config_manager(str(config_file.parent))

            # 獲取實例
            manager1 = get_config_manager()
            manager2 = get_config_manager()

            assert manager1 is manager2

    def test_invalid_config_directory(self):
        """測試無效配置目錄"""
        with pytest.raises(FileNotFoundError):
            ConfigManager("/nonexistent/path")


@pytest.mark.unit
@pytest.mark.config
class TestConfigManagerOperations:
    """配置管理器操作測試"""

    @pytest.fixture
    def config_manager(self, temp_dir):
        """測試配置管理器修件器"""
        # 創建測試配置
        config_data = {
            "app": {
                "name": "Test App",
                "version": "1.0.0",
                "environment": "test"
            },
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "test_db"
            },
            "features": {
                "crawling": True,
                "analysis": False
            }
        }

        import yaml
        config_file = temp_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)

        manager = ConfigManager(str(temp_dir), "test")
        return manager

    def test_get_simple_value(self, config_manager):
        """測試獲取簡單值"""
        assert config_manager.get("app.name") == "Test App"
        assert config_manager.get("database.port") == 5432
        assert config_manager.get("features.crawling") is True

    def test_get_with_default(self, config_manager):
        """測試獲取帶默認值"""
        assert config_manager.get("nonexistent.key", "default") == "default"
        assert config_manager.get("app.missing", 42) == 42

    def test_get_nonexistent_key(self, config_manager):
        """測試獲取不存在的鍵"""
        assert config_manager.get("completely.missing.path") is None
        assert config_manager.get("some.deep.nested.value") is None

    def test_get_nested_object(self, config_manager):
        """測試獲取嵌套對象"""
        app_config = config_manager.get("app")
        assert isinstance(app_config, dict)
        assert app_config["name"] == "Test App"
        assert app_config["version"] == "1.0.0"

    def test_set_value(self, config_manager, temp_dir):
        """測試設置值"""
        # 設置新值
        result = config_manager.set("custom.new_value", "test_value")
        assert result is True

        # 驗證設置成功
        assert config_manager.get("custom.new_value") == "test_value"

        # 測試設置嵌套值
        result = config_manager.set("nested.deep.value", 123)
        assert result is True
        assert config_manager.get("nested.deep.value") == 123

    def test_set_invalid_path(self, config_manager):
        """測試設置無效路徑"""
        with pytest.raises(ValueError):
            config_manager.set("", "value")

    def test_reload_configuration(self, config_manager, temp_dir):
        """測試配置重載"""
        import yaml

        # 修改配置文件
        config_file = temp_dir / "config.yaml"
        updated_config = {
            "app": {
                "name": "Updated App",
                "version": "2.0.0"
            }
        }

        with open(config_file, 'w') as f:
            yaml.dump(updated_config, f)

        # 重載配置
        result = config_manager.reload()
        assert result is True

        # 驗證重載成功
        assert config_manager.get("app.name") == "Updated App"
        assert config_manager.get("app.version") == "2.0.0"


@pytest.mark.unit
@pytest.mark.config
class TestConfigManagerEnvironmentHandling:
    """配置管理器環境處理測試"""

    def test_environment_override(self, temp_dir):
        """測試環境覆蓋"""
        import yaml

        # 創建基礎配置
        base_config = {"app": {"name": "Base App", "feature": True}}
        base_file = temp_dir / "config.yaml"
        with open(base_file, 'w') as f:
            yaml.dump(base_config, f)

        # 創建環境特定配置
        env_config = {"app": {"name": "Test App"}, "test": {"enabled": True}}
        env_file = temp_dir / "config.test.yaml"
        with open(env_file, 'w') as f:
            yaml.dump(env_config, f)

        # 創建管理器
        manager = ConfigManager(str(temp_dir), "test")

        # 驗證環境覆蓋
        assert manager.get("app.name") == "Test App"  # 被覆蓋
        assert manager.get("app.feature") is True     # 未被覆蓋
        assert manager.get("test.enabled") is True    # 新增配置

    def test_environment_file_not_found(self, temp_dir):
        """測試環境文件不存在"""
        import yaml

        # 創建基礎配置
        base_config = {"app": {"name": "Base App"}}
        base_file = temp_dir / "config.yaml"
        with open(base_file, 'w') as f:
            yaml.dump(base_config, f)

        # 創建管理器（指定不存在的環境）
        manager = ConfigManager(str(temp_dir), "nonexistent")

        # 應該使用基礎配置
        assert manager.get("app.name") == "Base App"


@pytest.mark.unit
@pytest.mark.config
class TestConfigManagerStatistics:
    """配置管理器統計測試"""

    def test_get_config_stats(self, temp_dir):
        """測試配置統計"""
        import yaml

        config_data = {
            "app": {"name": "Test", "version": "1.0"},
            "database": {"host": "localhost", "port": 5432},
            "features": ["crawling", "analysis"]
        }

        config_file = temp_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)

        manager = ConfigManager(str(temp_dir), "test")
        stats = manager.get_config_stats()

        assert isinstance(stats, dict)
        assert "load_count" in stats
        assert stats["load_count"] >= 1


@pytest.mark.unit
@pytest.mark.config
class TestConfigManagerErrorHandling:
    """配置管理器錯誤處理測試"""

    def test_malformed_yaml_file(self, temp_dir):
        """測試格式錯誤的YAML文件"""
        # 創建格式錯誤的配置文件
        config_file = temp_dir / "config.yaml"
        with open(config_file, 'w') as f:
            f.write("app:\n  name: Test\n    invalid: yaml: structure:\n")

        with pytest.raises(Exception):
            ConfigManager(str(temp_dir), "test")

    def test_readonly_filesystem(self, temp_dir):
        """測試只讀文件系統"""
        import yaml
        from unittest.mock import patch

        config_data = {"app": {"name": "Test"}}
        config_file = temp_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)

        manager = ConfigManager(str(temp_dir), "test")

        # 模擬文件系統錯誤
        with patch('builtins.open', side_effect=PermissionError("Read-only filesystem")):
            with pytest.raises(PermissionError):
                manager.reload()

    def test_memory_limit_exceeded(self, temp_dir):
        """測試記憶體限制超出"""
        import yaml

        # 創建很大的配置造成記憶體問題（模擬）
        large_config = {"large_data": "x" * 1024 * 1024}  # 1MB數據
        config_file = temp_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(large_config, f)

        # 應該能夠正常處理（除非真實記憶體不足）
        manager = ConfigManager(str(temp_dir), "test")
        data = manager.get("large_data")
        assert len(data) == 1024 * 1024


@pytest.mark.unit
@pytest.mark.config
@pytest.mark.slow
class TestConfigManagerPerformance:
    """配置管理器性能測試"""

    def test_multiple_get_operations(self, config_manager, performance_profiler):
        """測試多次獲取操作性能"""
        with performance_profiler.measure("config_get_operations"):
            for i in range(1000):
                _ = config_manager.get("app.name")
                _ = config_manager.get("database.port")
                _ = config_manager.get("nonexistent.key", "default")

        # 閾值檢查（1000次操作應該在1秒內完成）
        performance_profiler.assert_performance_threshold(
            "config_get_operations", 1.0, "lt", "s"
        )

    def test_concurrent_config_access(self, config_manager):
        """測試並發配置訪問"""
        import threading
        import time

        results = []
        errors = []

        def access_config(thread_id):
            try:
                for i in range(100):
                    value = config_manager.get("app.name")
                    results.append((thread_id, value))
                    time.sleep(0.001)  # 小的延遲模擬真實情況
            except Exception as e:
                errors.append((thread_id, str(e)))

        # 創建多線程
        threads = []
        for i in range(5):
            thread = threading.Thread(target=access_config, args=(i,))
            threads.append(thread)

        # 啟動線程
        for thread in threads:
            thread.start()

        # 等待完成
        for thread in threads:
            thread.join(timeout=10)

        # 驗證結果
        assert len(results) == 500  # 5線程 * 100次操作
        assert len(errors) == 0     # 不應該有錯誤
        assert all(value == "Test App" for _, value in results)


if __name__ == "__main__":
    pytest.main([__file__, "--verbose", "--cov=utils.config_manager", "--cov-report=html"])
