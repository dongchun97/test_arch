import importlib
from configs import ConfigManager


class CalculatorFactory:

    @classmethod
    def create_calculator(cls, category_info, dimension_info):
        """
        根据建筑形态创建对应的 Calculator。
        """

        cfg = ConfigManager()

        roof_form = category_info["roof_forms"]
        form_name = category_info["form_name"]

        # 1. 获取类路径（来自 JSON）
        class_path = cfg.get_class_mapping(roof_form) 

        if class_path is None:
            raise ValueError(f"Unknown roof form: {roof_form}")

        # 2. 动态加载类
        module_name, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        CalculatorClass = getattr(module, class_name)


        # 3. 获取 TOML 规则
        form_config = cfg.get_building_form(form_name)

        # 4. 实例化 Calculator
        return CalculatorClass(
            config=form_config,
            category_info=category_info,
            dimension_info=dimension_info,
        )
    

if __name__ == "__main__":
    CalculatorFactory.create_calculator()
