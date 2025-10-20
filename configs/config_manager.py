import tomllib


# config/manager.py
class ConfigManager:
    """统一的配置管理器"""

    def __init__(self):
        self.building_classfications = self._load_toml("building_classification.toml")

    def _load_toml(self, cfg_path):
        with open(f"configs/{cfg_path}", "rb") as f:
            return tomllib.load(f)

    def get_building_classfications(self):
        """获取建筑形式配置"""
        return self.building_classfications


if __name__ == "__main__":
    config_manager = ConfigManager()
    category = config_manager.get_building_classfications()
    print(category['building_categories'].building)
