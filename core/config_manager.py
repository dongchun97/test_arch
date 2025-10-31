from pathlib import Path
from typing import Any, Dict, Optional, TypedDict, Union
from functools import lru_cache
import tomllib
from dataclasses import dataclass
from abc import ABC, abstractmethod


class AppConfig(TypedDict, total=False):
    scale: float
    precision: Dict[str, Any]
    default: Dict[str, Any]


class BuildingClassification(TypedDict, total=False):
    building_forms: Dict[str, Any]
    # 其他分类字段...


@dataclass(frozen=True)
class ConfigPaths:
    """配置路径容器"""

    app_settings: Path
    building_classification: Path

    @classmethod
    def from_base_dir(cls, base_dir: Union[str, Path] = "configs") -> "ConfigPaths":
        base_path = Path(base_dir)
        return cls(
            app_settings=base_path / "app_settings.toml",
            building_classification=base_path / "building_classification.toml",
        )


class BaseConfigLoader(ABC):
    """配置加载器抽象基类"""

    @abstractmethod
    def get_app_settings(self, *keys: str) -> Any:
        pass

    @abstractmethod
    def get_classification(self, *keys: str) -> Any:
        pass


class ConfigManager(BaseConfigLoader):
    """类型安全的配置管理器"""

    def __init__(self, config_paths: ConfigPaths):
        self._paths = config_paths
        self._app_settings: Optional[AppConfig] = None
        self._building_classification: Optional[BuildingClassification] = None
        self._load_configs()

    def _load_configs(self) -> None:
        """加载所有配置文件"""
        self._app_settings = self._load_toml(self._paths.app_settings)
        self._building_classification = self._load_toml(
            self._paths.building_classification
        )

    @staticmethod
    def _load_toml(file_path: Path) -> Dict[str, Any]:
        """安全加载TOML文件"""
        try:
            with file_path.open("rb") as f:
                return tomllib.load(f)
        except FileNotFoundError:
            raise ConfigError(f"配置文件不存在: {file_path}")
        except tomllib.TOMLDecodeError as e:
            raise ConfigError(f"配置文件格式错误 {file_path}: {e}")
        except Exception as e:
            raise ConfigError(f"加载配置文件失败 {file_path}: {e}")

    def _get_nested_value(self, config_dict: Dict[str, Any], keys: tuple) -> Any:
        """安全获取嵌套配置值"""
        current = config_dict
        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return None
            current = current[key]
        return current

    @lru_cache(maxsize=128)
    def get_app_settings(self, *keys: str) -> Any:
        """获取应用设置（带缓存）"""
        if self._app_settings is None:
            raise ConfigError("应用配置未加载")
        return self._get_nested_value(self._app_settings, keys)

    @lru_cache(maxsize=128)
    def get_classification(self, *keys: str) -> Any:
        """获取分类配置（带缓存）"""
        if self._building_classification is None:
            raise ConfigError("分类配置未加载")
        return self._get_nested_value(self._building_classification, keys)

    def reload(self) -> None:
        """重新加载配置并清空缓存"""
        self._load_configs()
        self.get_app_settings.cache_clear()
        self.get_classification.cache_clear()

    @property
    def app_settings(self) -> AppConfig:
        """直接访问应用配置"""
        if self._app_settings is None:
            raise ConfigError("应用配置未加载")
        return self._app_settings

    @property
    def building_classification(self) -> BuildingClassification:
        """直接访问分类配置"""
        if self._building_classification is None:
            raise ConfigError("分类配置未加载")
        return self._building_classification


class ConfigError(Exception):
    """配置相关异常"""

    pass
