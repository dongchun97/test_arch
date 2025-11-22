# xieshan_calculator.py
from ..base_calculator import BaseCalculator


class XieshanCalculator(BaseCalculator):
    """
    歇山屋顶的计算器。
    输入：
        building_data  —— data_loader + form_inference 输出的整合字典
        form_rule      —— config_manager 提供的该屋面形式的参数规则

    输出：
        通过 calculate() 返回一个 dict，包含计算结果
    """

    def __init__(self, building_data: dict, form_rule: dict):
        super().__init__()
        self.data = building_data
        self.rule = form_rule

    # -----------------------------------------------------
    # 核心入口
    # -----------------------------------------------------
    def calculate(self) -> dict:
        """
        主计算流程
        """
        num_bays = self.data["dimension_info"]["num_bays"]
        bay_widths = self.data["dimension_info"]["bay_widths"]
        total_depth = self.data["dimension_info"]["depth_total"]
        eave_step = self.data["dimension_info"]["eave_step"]

        # 从规则中取典型比例
        roof_slope = self.rule.get("roof_slope", 25)  # 典型屋面坡度
        ridge_height_ratio = self.rule.get("ridge_height_ratio", 0.18)

        # 计算屋脊高度
        ridge_height = self._calc_ridge_height(total_depth, ridge_height_ratio)

        # 计算檩数
        lin_count = self._calc_lin_count(total_depth)

        # 计算屋面坡度相关的构件
        slope_data = self._compute_slope_info(roof_slope, ridge_height)

        # 汇总返回
        return {
            "roof_type": "歇山",
            "num_bays": num_bays,
            "bay_widths": (
                bay_widths.tolist() if hasattr(bay_widths, "tolist") else bay_widths
            ),
            "total_depth": float(total_depth),
            "eave_step": float(eave_step),
            "ridge_height": ridge_height,
            "lin_count": lin_count,
            "slope_info": slope_data,
        }

    # -----------------------------------------------------
    # 局部计算模块
    # -----------------------------------------------------
    def _calc_ridge_height(self, total_depth, ratio):
        """
        根据总进深与比例推算屋脊高度（清式常用规则）
        """
        return float(total_depth) * ratio

    def _calc_lin_count(self, total_depth):
        """
        根据清式：小屋 → 4檩；普通 → 5～6檩；大式 → 7～9檩
        这里简单按进深推算，也可改为规则表驱动
        """
        d = float(total_depth)
        if d < 2.0:
            return 4
        elif d < 3.0:
            return 6
        else:
            return 8

    def _compute_slope_info(self, slope_angle, ridge_height):
        """
        根据坡度估算举折、檐口高度、翼角等（示例版，可自行扩展）
        """
        import math

        slope_rad = math.radians(slope_angle)

        # 假设举折 = 屋脊高度 * 30%
        jut = ridge_height * 0.3

        # 檐口高度估算（示意）
        eave_height = ridge_height - jut * math.cos(slope_rad)

        return {"slope_angle": slope_angle, "jut": jut, "eave_height": eave_height}
