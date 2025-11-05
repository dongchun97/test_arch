# import json


# class RuleEngine:
#     def __init__(self, rule_file):
#         with open(rule_file, "r", encoding="utf-8") as f:
#             self.rules = json.load(f)

#     def get_calculator_class(self, building_type):
#         return self.rules.get(building_type, {}).get("calculator_class")

#     def list_building_types(self):
#         return list(self.rules.keys())


# if __name__ == "__main__":
#     rule_file = "configs/rules.json"
#     rule = RuleEngine(rule_file)
#     result = rule.get_calculator_class("房屋")
#     print(result)

#     print(rule.list_building_types())

# core/rule_engine.py


from config_manager import ConfigManager


class RuleEngine:
    def __init__(self):
        self.config = ConfigManager()  # 加载配置,文件夹路径
        self.rules = []

    def register(self, func):
        """注册规则函数"""
        self.rules.append(func)
        return func

    def evaluate(self, data):
        """统一执行所有规则"""
        result = {}
        for rule in self.rules:
            result.update(rule(data, self.config.config))
        return result


engine = RuleEngine()
config = engine.config.config


@engine.register
def roof_rule(data, config):
    roof_form = data["category_info"]["roof_forms"]
    rule = config.get("roof_forms")["roof_forms"][roof_form]
    return {"roof_slope": rule["slope_ratio"]}


@engine.register
def grade_rule(data, config):
    grade = data["category_info"]["construction_grades"]
    if grade == "小式":
        grade = "small_style"
    elif grade == "大式":
        grade = "large_style"
    rule = config.get("geometry_config")[grade]
    return {"column_height": rule.get("eave_pillar_height", {})}


@engine.register
def corridor_rule(data, config):
    corridor = data["category_info"]["corridor"]
    rule = config.get("roof_forms")["corridors"][corridor]
    return {"wall_enclosure": rule["walls"]}


if __name__ == "__main__":
    from numpy import array

    data = {
        "basic_info": {
            "garden_name": "CC",
            "garden_id": "W01L_ABC",
            "building_id": "10",
            "building_name": "松篁深处",
        },
        "category_info": {
            "building_category": "房屋",
            "sub_category": "正房",
            "roof_forms": "歇山",
            "ridge_types": "卷棚",
            "construction_grades": "大式",
            "corridor": "无廊",
        },
        "precision_info": {"pricision": ""},
        "dimension_info": {
            "num_lin": 6,
            "num_bays": 5,
            "bay_widths": array([1.0, 1.0, 1.0]),
            "depth_total": array(1.5),
            "eave_step": array(0.35),
        },
    }

    # print(data["category_info"]["roof_forms"])
    # print(roof_rule(data, config))
    # print(grade_rule(data, config))
    # print(data["category_info"]["corridor"])
    # print(corridor_rule(data, config))

    # # print(config.keys())
    rusult = engine.evaluate(data)
    print(rusult)
