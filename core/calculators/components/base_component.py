# core/calculators/components/base_component.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from .dataclasses import ComponentResult


class BaseComponentCalculator(ABC):
    """
    所有构件计算器的统一接口
    """

    @abstractmethod
    def calculate(self, params: Dict[str, Any]) -> ComponentResult:
        """
        参数由上游 calculator（比如 xieshan_calculator）组织好后传入
        返回纯几何数据，绝不创建 bpy 对象
        """
        pass

    def _apply_shoufen(self, height: float, base_diameter: float) -> float:
        """收分通用算法，可被子类复用"""
        ...
