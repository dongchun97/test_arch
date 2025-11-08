# core/calculator_factory.py
from .calculators import HouseCalculator


class CalculatorFactory:
    """
    根据建筑类别或规则自动选择计算器。
    """

    def __init__(self, rule_manager):
        self.rule_manager = rule_manager

    def create(self, category: str):
        """根据类别或规则返回相应的计算器实例"""
        # 此处可以从 rules.json 读取映射，也可直接判断
        if category in ["building_form", "house", "小式房屋", "大式房屋"]:
            return HouseCalculator(self.rule_manager, self.config_manager)
        raise ValueError(f"未定义类别对应计算器：{category}")
