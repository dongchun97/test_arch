import importlib
from configs import ConfigManager


class CalculatorFactory:

    @classmethod
    def create_calculator(cls, building_data: dict):
        category = building_data["category_info"]
        roof_form = category["roof_forms"]
        form_name = category["form_name"]

        # 1. 查类
        class_path = ConfigManager.get_class_mapping(roof_form)

        module, classname = class_path.rsplit(".", 1)
        CalculatorClass = getattr(importlib.import_module(module), classname)

        # 2. 查规则
        form_rule = ConfigManager.get_building_rules(form_name)

        # 3. 实例化
        return CalculatorClass(building_data, form_rule)


if __name__ == "__main__":
    from numpy import array

    building_data = {
        "category_info": {
            "building_category": "房屋",
            "sub_category": "正房",
            "roof_forms": "歇山",
            "ridge_types": "卷棚",
            "construction_grades": "大式",
            "corridor": "无廊",
            "form_name": "六檩卷棚大式",
        },
        "dimension_info": {
            "num_bays": 5,
            "bay_widths": array([1.0, 1.0, 1.0]),
            "depth_total": array(1.5),
            "eave_step": array(0.35),
            "num_lin": 6,
            "ridge_distance": 0.1,
        },
    }
    CalculatorFactory.create_calculator(building_data)
