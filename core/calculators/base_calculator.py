# core/calculators/base_calculator.py
from abc import ABC, abstractmethod


class BaseCalculator(ABC):
    """
    所有计算器的抽象基类。
    """

    def __init__(self, rule_manager):
        self.rule_manager = rule_manager
        base_settings = rule_manager.rules.get("settings", {}).get("settings", {})
        self.scale = base_settings.get("scale", 100)
        self.units = base_settings.get("default_units", "meters")

    @abstractmethod
    def compute(self, form_name: str) -> dict:
        pass

    def _scale_value(self, value: float) -> float:
        return value * self.scale
