import importlib


class CalculatorFactory:
    def __init__(self, rule_manager):
        """
        :param rule_manager: RuleManager 实例，用于加载 rules.json
        """
        self.rule_manager = rule_manager

    def create(self, category: str):
        """根据规则表（rules.json）动态创建计算器实例"""
        rule = self.rule_manager.get_rule(category)
        if not rule:
            raise ValueError(f"未定义类别对应规则：{category}")

        # 从规则中取出计算器类名与配置文件路径
        calculator_class_name = rule.get("calculator_class")
        config_file = rule.get("config_file")

        if not calculator_class_name:
            raise ValueError(f"规则中缺少 calculator_class: {category}")

        # 动态导入对应模块（例如 core.calculators.house_calculator）
        module_name = f"core.calculators.{calculator_class_name.lower()}"
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            raise ImportError(f"未找到模块 {module_name}")

        # 获取类对象
        calculator_class = getattr(module, calculator_class_name, None)
        if not calculator_class:
            raise ImportError(f"未找到类 {calculator_class_name} 于模块 {module_name}")

        # 初始化计算器实例
        calculator = calculator_class(
            rule_manager=self.rule_manager, config_file=config_file
        )
        return calculator
