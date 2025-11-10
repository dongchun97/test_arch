# core/calculators/base_calculator.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import numpy as np


class BaseCalculator(ABC):
    """计算器基类 - 定义统一接口"""

    def __init__(self, building_config: Dict[str, Any]):
        self.building_config = building_config
        self.building_data = building_config.get("building_data", {})
        self.style_config = building_config.get("style_config", {})
        self.results = {}

    @abstractmethod
    def calculate_pillars(self) -> Dict[str, Any]:
        """计算柱子系统"""
        pass

    @abstractmethod
    def calculate_beams(self) -> Dict[str, Any]:
        """计算梁系统"""
        pass

    @abstractmethod
    def calculate_roof(self) -> Dict[str, Any]:
        """计算屋顶系统"""
        pass

    def calculate_all(self) -> Dict[str, Any]:
        """计算所有构件"""
        self.results = {
            "pillars": self.calculate_pillars(),
            "beams": self.calculate_beams(),
            "roof": self.calculate_roof(),
            "purlins": self.calculate_purlins(),
            "metadata": self._get_metadata(),
        }
        return self.results

    def calculate_purlins(self) -> Dict[str, Any]:
        """计算檩条系统（通用实现）"""
        purlin_count = self.building_data.get("purlin_count", 4)
        span_width = self.building_data.get("span_width", 8.0)

        return {
            "purlin_count": purlin_count,
            "positions": self._calculate_purlin_positions(purlin_count),
            "diameters": self._calculate_purlin_diameters(purlin_count),
        }

    def _calculate_purlin_positions(self, purlin_count: int) -> List[float]:
        """计算檩条位置"""
        depth_total = self.building_data.get("depth_total", 6.0)
        return np.linspace(0, depth_total, purlin_count).tolist()

    def _calculate_purlin_diameters(self, purlin_count: int) -> List[float]:
        """计算檩条直径"""
        base_diameter = self.style_config.get("purlin_diameter", 0.25)
        return [base_diameter] * purlin_count

    def _get_metadata(self) -> Dict[str, Any]:
        """获取计算元数据"""
        return {
            "calculator_type": self.__class__.__name__,
            "building_style": self.style_config.get("style_name", "unknown"),
            "timestamp": np.datetime64("now"),
        }

    def _scale_value(self, value: float) -> float:
        return value * self.scale
