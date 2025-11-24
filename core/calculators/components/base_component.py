# core/calculators/components/base_component.py
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseComponentCalculator(ABC):
    """
    所有构件计算器的统一接口
    """
    def __init__(self, building_data: dict, form_rule: dict):
        self.data = building_data
        self.rule = form_rule

        self.dim = self.data["dimension_info"]
        self.main_bay = self.dim["bay_widths"][0]

    @abstractmethod
    def calculate(self, params: Dict[str, Any]):
        """
        参数由上游 calculator（比如 xieshan_calculator）组织好后传入
        返回纯几何数据，绝不创建 bpy 对象
        """
        pass
