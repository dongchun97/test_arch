import tomllib

class ConfigManager:
    """统一的配置管理器"""

    def __init__(self):
        self.app_settings = self._load_toml("app_settings.toml")
        self.building_classfication = self._load_toml("building_classification.toml")

    def _load_toml(self, cfg_path):
        with open(f"configs/{cfg_path}", "rb") as f:
            return tomllib.load(f)

    def get_classification(self, category, grade):
        return self.building_classfication.get(category, {}).get(grade, {})
    
    def get_app_settings(self):
        return self.app_settings


if __name__ == "__main__":
    config_manager = ConfigManager()
    category = config_manager.get_classification("construction_grades","grade_2")
    print(category)
