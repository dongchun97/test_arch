import tomllib
from pathlib import Path

class ConfigManager:
    def __init__(self, config_path: str = "configs/base_config.toml"):
        self.config_path = Path(config_path)
        self.config = {}
        self.load_config()

    def load_config(self):
        with open(self.config_path, "rb") as f:
            self.config = tomllib.load(f)

    def get(self, section: str, key: str, default=None):
        """通用访问接口"""
        return self.config.get(section, {}).get(key, default)

    @property
    def paths(self):
        return self.config.get("paths", {})

    @property
    def system(self):
        return self.config.get("system", {})

    @property
    def modeling(self):
        return self.config.get("modeling", {})

    @property
    def output(self):
        return self.config.get("output", {})
