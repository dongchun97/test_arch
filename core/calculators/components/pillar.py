# calculators/pillar_calculator.py

from dataclasses import dataclass
from typing import Dict, Callable


@dataclass
class PillarSpec:
    diameter: float
    height: float
    # 未来可加字段


class PillarCalculator:
    """
    单一类管理：檐柱、金柱、童柱、角柱等所有的柱子计算逻辑
    """

    def __init__(self, building_data, config):
        self.data = building_data
        self.config = config

        # 分发表：柱类型 -> 对应计算方法
        self._pillar_dispatcher: Dict[str, Callable] = {
            "yan_zhu": self._calc_yan_zhu,       # 檐柱
            "jin_zhu": self._calc_jin_zhu,       # 金柱
            "tong_zhu": self._calc_tong_zhu,     # 童柱
            "jiao_zhu": self._calc_jiao_zhu,     # 角柱（如需要）
        }

    # -----------------------
    #   外部统一接口
    # -----------------------
    def calc_pillar(self, pillar_type: str) -> PillarSpec:
        """
        统一计算接口
        """
        if pillar_type not in self._pillar_dispatcher:
            raise ValueError(f"Unknown pillar type: {pillar_type}")

        return self._pillar_dispatcher[pillar_type]()

    # -----------------------
    #   下方是若干具体逻辑方法
    # -----------------------

    def _calc_yan_zhu(self) -> PillarSpec:
        span = self.data.main_span
        ratio = self.config.pillar_diameter_ratio["yan_zhu"]

        diameter = span * ratio
        height = self._calc_default_pillar_height()

        return PillarSpec(
            diameter=diameter,
            height=height,
        )

    def _calc_jin_zhu(self) -> PillarSpec:
        span = self.data.secondary_span
        ratio = self.config.pillar_diameter_ratio["jin_zhu"]

        diameter = span * ratio
        height = self._calc_default_pillar_height()

        return PillarSpec(
            diameter=diameter,
            height=height,
        )

    def _calc_tong_zhu(self) -> PillarSpec:
        span = self.data.main_span
        ratio = self.config.pillar_diameter_ratio["tong_zhu"]

        diameter = span * ratio * 0.8  # 示例：童柱更细

        return PillarSpec(
            diameter=diameter,
            height=self._calc_default_pillar_height() * 0.8,
        )

    # -----------------------
    #   共用的私有方法
    # -----------------------

    def _calc_default_pillar_height(self):
        return self.data.floor_height * self.config.pillar_height_scale
