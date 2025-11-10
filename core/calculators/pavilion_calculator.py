# core/calculators/pavilion_calculator.py
from .base_calculator import BaseCalculator
import numpy as np
from typing import Dict, Any, List


class PavilionCalculator(BaseCalculator):
    """亭子计算器 - 处理四角亭、六角亭等"""

    def calculate_pillars(self) -> Dict[str, Any]:
        """计算亭子柱子系统（圆形或多边形布局）"""
        sides = self._get_pavilion_sides()
        radius = self.building_data.get("span_width", 3.0) / 2

        pillars = []
        for i in range(sides):
            angle = 2 * np.pi * i / sides
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)

            pillars.append(
                {
                    "type": "pavilion_pillar",
                    "position": [x, y, 0],
                    "diameter": 0.15,  # 亭柱较细
                    "height": 2.5,  # 亭柱较低
                    "angle": angle,
                }
            )

        return {"pillars": pillars, "layout_type": "circular", "sides": sides}

    def calculate_beams(self) -> Dict[str, Any]:
        """计算亭子梁系统（联系梁）"""
        sides = self._get_pavilion_sides()

        beams = []
        for i in range(sides):
            beams.append(
                {
                    "type": "ring_beam",
                    "section": [0.15, 0.2],
                    "position": [0, 0, 2.2],  # 柱顶联系梁
                }
            )

        return {"beams": beams}

    def calculate_roof(self) -> Dict[str, Any]:
        """计算亭子屋顶（攒尖顶）"""
        return {
            "type": "pyramidal_roof",
            "slope_ratio": 0.7,  # 亭顶较陡
            "peak_height": 1.5,
        }

    def _get_pavilion_sides(self) -> int:
        """获取亭子边数"""
        sub_category = self.building_data.get("sub_category", "")
        if "四角" in sub_category:
            return 4
        elif "六角" in sub_category:
            return 6
        elif "八角" in sub_category:
            return 8
        else:
            return 6  # 默认六角亭
