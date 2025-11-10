# core/calculators/house_calculator.py
from .base_calculator import BaseCalculator
import numpy as np
from typing import Dict, Any, List


class HouseCalculator(BaseCalculator):
    """房屋计算器 - 处理正房、厢房等"""

    def calculate_pillars(self) -> Dict[str, Any]:
        """计算房屋柱子系统"""
        bay_widths = self.building_data.get("bay_widths", [3.0, 2.8, 2.8, 3.0])
        pillar_config = self.style_config.get("pillars", {})

        # 计算檐柱
        eave_pillar = pillar_config.get("eave", {})
        pillar_diameter = (
            eave_pillar.get("diameter_ratio", 0.077) * bay_widths[0]
        )  # 明间面阔比例
        pillar_height = eave_pillar.get("height_ratio", 0.8) * pillar_diameter

        pillars = []
        x_pos = 0
        for i, width in enumerate(bay_widths):
            pillars.append(
                {
                    "type": "eave_pillar",
                    "position": [x_pos + width / 2, 0, 0],
                    "diameter": pillar_diameter,
                    "height": pillar_height,
                    "role": self._get_pillar_role(i, len(bay_widths)),
                }
            )
            x_pos += width

        return {
            "pillars": pillars,
            "eave_pillar_diameter": pillar_diameter,
            "eave_pillar_height": pillar_height,
        }

    def calculate_beams(self) -> Dict[str, Any]:
        """计算房屋梁系统"""
        beam_config = self.style_config.get("beams", {})
        purlin_count = self.building_data.get("purlin_count", 4)

        beams = []
        if purlin_count == 4:
            # 四檩卷棚梁架
            beams.extend(self._calculate_four_purlin_beams())
        elif purlin_count == 5:
            # 五檩梁架
            beams.extend(self._calculate_five_purlin_beams())

        return {"beams": beams}

    def calculate_roof(self) -> Dict[str, Any]:
        """计算房屋屋顶"""
        roof_config = self.style_config.get("roof", {})
        return {
            "type": roof_config.get("type", "roll_shed"),
            "slope_ratio": roof_config.get("slope_ratio", 0.5),
            "overhang": roof_config.get("overhang", 0.3),
        }

    def _get_pillar_role(self, index: int, total: int) -> str:
        """获取柱子角色"""
        if index == 0 or index == total - 1:
            return "corner_pillar"
        elif index == total // 2:
            return "center_pillar"
        else:
            return "intermediate_pillar"

    def _calculate_four_purlin_beams(self) -> List[Dict]:
        """计算四檩梁架"""
        return [
            {"type": "eave_beam", "section": [0.2, 0.3], "position": [0, 0, 2.5]},
            {"type": "ridge_beam", "section": [0.18, 0.25], "position": [0, 0, 3.2]},
        ]
