import tomllib

app_settings = "app_settings.toml"
building_classification = "building_classification.toml"


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

    def get_app_settings(self, category, grade):
        return self.app_settings.get(category, {}).get(grade, {})


class ConfigLoader(ConfigManager):
    """
    配置加载器
    """

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.structure_name = data["structure_name"]

    @property
    def get_scale(self):
        return self.get_app_settings("default", "scale")

    # 获取configs精度和建筑形式
    def get_structure_and_precision(self):
        # 获取config精度
        precision_level = "medium_level"
        modual_precision = self.get_app_settings("precision", precision_level)
        # 获取config建筑形式
        building_forms = self.get_classification("building_forms", self.structure_name)
        return {"building_forms": building_forms, "segments": modual_precision}


if __name__ == "__main__":

    data = {
        "basic_info": {
            "garden_name": "CC",
            "garden_id": "W01L",
            "sub_garden_name": "ABC",
            "building_id": "10",
            "building_name": "松篁深处",
        },
        "structure_info": {
            "building_category": "房屋",
            "sub_category": "正房",
            "construction_grades": "大式",
            "roof_forms": "歇山",
            "ridge_types": "卷棚",
            "corridor": "无廊",
        },
        "precision_info": {"pricision": ""},
        "dimension_info": {
            "num_lin": 6,
            "num_bays": 5,
            "bay_widths": [1.0, 1.0, 1.0],
            "depth_total": 1.5,
            "eave_step": 0.35,
        },
        "structure_name": "六檩卷棚大式",
    }
    loader = ConfigLoader(data)
    print(loader.get_structure_and_precision())
    print(loader.get_scale)
