# calculators/base_calculator.py
from abc import ABC, abstractmethod
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class BaseCalculator(ABC):
    """
    所有屋面形态计算器的基类。

    特点：
    - 统一 building_data 与 form_rule 输入
    - 提供基础结构计算（柱网、进深、举架、規制比例）
    - 子类仅需 override calculate()，无需覆盖基础方法
    """

    def __init__(self, building_data: dict, form_rule: dict):
        """
        building_data : 完整建筑数据（含 basic_info / category_info / dimension_info ...）
        form_rule     : 来自 config 的该屋面形式规则（比例、尺寸、构造系统等）
        """
        self.data = building_data
        self.rule = form_rule

        self.dim = self.data["dimension_info"]
        self.main_bay = self.dim["bay_widths"][0]

        # 计算结果
        self.result = {
            "grid": None,
            "heights": None,
        }

    # -------------------------------------------------------
    # 通用方法：柱网计算
    # -------------------------------------------------------
    def calculate_grid(self) -> Dict[str, Any]:

        num_bays = self.dim["num_bays"]
        bay_widths = self.dim["bay_widths"]
        depth_total = float(self.dim["depth_total"])

        # 纵向坐标
        x_coords = [0]
        for w in bay_widths:
            x_coords.append(x_coords[-1] + float(w))

        grid = {
            "num_bays": num_bays,
            "bay_widths": bay_widths,
            "main_bay": float(self.main_bay),
            "x_coords": x_coords,
            "depth_total": depth_total,
        }

        logger.debug(f"[Grid] num_bays={num_bays}, x_coords={x_coords}")
        return grid

    # -------------------------------------------------------
    # 通用方法：高度计算
    # -------------------------------------------------------
    def calculate_heights(self):
        """
        通用高度规则：基于 form_rule 和标准比例。
        """
        base_height = self.rule.get("base_height", self.main_bay * 0.25)
        eave_height = self.rule.get("base_ratio", self.main_bay * 0.85)

        self.result["heights"] = {
            "base": base_height,
            "body": eave_height,
        }

    # -------------------------------------------------------
    # 通用方法：举架（柱高 / 梁长 / 构件比例）
    # -------------------------------------------------------
    def calculate_frame_system(self) -> Dict[str, float]:
        """
        基于 form_rule 的比例系数计算主要构件高度。
        典型参数：
            - pillar_diameter_base
            - pillar_height_ratio
            - beam_length_ratio
        """
        rule = self.rule

        d = rule.get("pillar_diameter_base", 0.45)
        h_ratio = rule.get("pillar_height_ratio", 8.0)
        beam_ratio = rule.get("beam_length_ratio", 1.2)

        pillar_height = d * h_ratio
        beam_length = d * beam_ratio

        logger.debug(
            f"[Frame] d={d}, pillar_height={pillar_height}, beam_length={beam_length}"
        )

        return {
            "pillar_diameter": d,
            "pillar_height": pillar_height,
            "beam_length": beam_length,
        }

    # -------------------------------------------------------
    # 通用方法：屋面坡度与典型构造
    # -------------------------------------------------------
    def calculate_roof_slope(self) -> Dict[str, float]:
        """
        slope_angle / ridge_height_ratio 来自 form_rule
        """
        rule = self.rule

        total_depth = float(self.dim["depth_total"])
        slope_angle = rule.get("roof_slope", 25)
        ridge_ratio = rule.get("ridge_height_ratio", 0.18)

        ridge_height = total_depth * ridge_ratio

        return {"slope_angle": slope_angle, "ridge_height": ridge_height}

    # -------------------------------------------------------
    # 屋顶计算（核心差异点）
    # -------------------------------------------------------
    @abstractmethod
    def calculate_roof(self):
        """
        各类屋顶（卷棚、歇山、硬山、庑殿等）形态差异巨大。
        子类负责：脊、坡度、进深/面宽方向的屋面构造。
        """
        ...

    # -------------------------------------------------------
    # 主流程 —— 子类必须 override
    # -------------------------------------------------------
    @abstractmethod
    def calculate(self) -> Dict[str, Any]:
        """
        每种屋面形态（歇山、硬山、卷棚、大脊顶等）必须实现自己的主计算逻辑
        """
        pass

    # -------------------------------------------------------
    # 总计算流程
    # -------------------------------------------------------
    def calculate_all(self):
        self.calculate_grid()
        self.calculate_heights()
        return self._pack(
            grid=self.result["grid"],
            heights=self.result["heights"],
        )

    # -------------------------------------------------------
    # 公共包装：为子类提供标准返回结构
    # -------------------------------------------------------
    def _pack(self, **kwargs):
        """
        统一的返回格式方法，不同 Calculator 用它来返回结果。
        """
        return {
            "basic_info": self.data["basic_info"],
            "category_info": self.data["category_info"],
            "dimension_info": self.data["dimension_info"],
            "rule": self.rule,
            "results": kwargs,
        }
