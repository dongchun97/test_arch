# core/calculators/house_calculator.py
from .base_calculator import BaseCalculator


class HouseCalculator(BaseCalculator):
    """
    房屋类建筑计算器：根据檩数、屋顶形式、等级制度计算主要尺寸。
    """

    def compute(self, form_name: str) -> dict:
        # 读取综合规则（形态+等级+屋顶等）
        rule = self.rule_manager.get_form(form_name)

        # 应用 modular_system 调整
        rule = self._apply_modular_system(rule)

        # 计算构件比例
        structure_params = self._calculate_structure(rule)
        roof_params = self._calculate_roof(rule)

        return {
            "form_name": form_name,
            "modular_system": rule.get("modular_system"),
            **structure_params,
            **roof_params,
        }

    def _calculate_structure(self, rule: dict) -> dict:
        """计算柱、梁等尺寸"""
        num_purlins = rule.get("num_purlins", 5)
        modular_scale = rule.get("modular_scale", 0.15)
        beam_span = self._scale_value(num_purlins * modular_scale * 10)

        return {
            "num_purlins": num_purlins,
            "beam_span": beam_span,
            "pillar_height": self._scale_value(modular_scale * 8),
        }

    def _calculate_roof(self, rule: dict) -> dict:
        """根据屋顶类型计算高度与倾角"""
        roof_type = rule.get("roof_type", "roll_shed")
        if roof_type == "roll_shed":
            pitch = 18
        elif roof_type == "hard_mountain":
            pitch = 25
        else:
            pitch = 20
        return {"roof_type": roof_type, "roof_pitch": pitch}
