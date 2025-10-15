import tomllib


# config/manager.py
class ConfigManager:
    """统一的配置管理器"""

    def __init__(self):
        self.field_mapping = self._load_toml("field_mapping.toml")
        self.building_forms = self._load_toml("building_forms.toml")
        self.geometry = self._load_toml("geometry.toml")
        self.naming_standard = self._load_toml("naming_standard.toml")

    def _load_toml(self, filename):
        with open(f"configs/{filename}", "rb") as f:
            return tomllib.load(f)

    def get_field_mapping(self):
        """获取字段映射配置"""
        return self.field_mapping

    def get_building_forms(self):
        """获取建筑形式配置"""
        return self.building_forms

    def get_geometry_rules(self):
        """获取构件配置"""
        return self.geometry

    def get_naming_standard(self):
        """获取构件配置"""
        return self.naming_standard


if __name__ == "__main__":
    config_manager = ConfigManager()
    # field_mapping = config_manager.get_field_mapping()
    # print(field_mapping)
    geometry = config_manager.get_geometry_rules()
    print(geometry)
