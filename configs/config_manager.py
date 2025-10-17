import tomllib


# config/manager.py
class ConfigManager:
    """统一的配置管理器"""

    def __init__(self):
        self.building_forms = self._load_toml("building_forms.toml")
        self.geometry_ratio = self._load_toml("geometry_ratio.toml")
        self.base_config = self._load_toml("base_config.toml")

    def _load_toml(self, filename):
        with open(f"configs/{filename}", "rb") as f:
            return tomllib.load(f)

    def get_building_forms(self):
        """获取建筑形式配置"""
        return self.building_forms

    def get_geometry_ratio(self):
        """获取构件配置"""
        return self.geometry_ratio

    def get_base_config(self):
        """获取构件配置"""
        return self.base_config


if __name__ == "__main__":
    config_manager = ConfigManager()
    # field_mapping = config_manager.get_field_mapping()
    # print(field_mapping)
    geometry = config_manager.get_geometry_ratio()
    print(geometry)
