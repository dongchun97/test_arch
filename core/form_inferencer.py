# core/form_inferencer.py
from typing import Dict


class FormInferencer:
    """
    推断建筑形态信息：
    1. infer_num_lin() — 根据檐步和进深计算檩数、脊距
    2. _infer_form_name() — 根据 ridge_type + grade + 檩数 生成形态名
    """

    def __init__(self, building_data: Dict):
        self.building_data = building_data

    def _infer_num_lin(self):
        """
        根据进深与檐步计算檩数和过垄脊距离。
        depth_total // eave_step + 2 = 檩数
        depth_total % eave_step = 过垄脊距离
        """
        depth_total = float(
            self.building_data.get("dimension_info", {}).get("depth_total", {})
        )
        eave_step = float(
            self.building_data.get("dimension_info", {}).get("eave_step", {})
        )

        num_lin = int(depth_total // eave_step + 2)
        ridge_distance = round(depth_total % eave_step, 3)

        self.building_data["dimension_info"].update(
            {"num_lin": num_lin, "ridge_distance": ridge_distance}
        )

        return num_lin

    def _infer_form_name(self):
        """
        组合形态名，例如 “六檩卷棚大式”
        """
        cat = self.building_data.get("category_info", {})
        ridge_type = cat.get("ridge_types", "")
        grade = cat.get("construction_grades", "")

        num_lin = self._infer_num_lin()

        num_cn = self._num_to_cn(num_lin)
        return f"{num_cn}檩{ridge_type}{grade}"

    @staticmethod
    def _num_to_cn(num: int) -> str:
        cn_map = {3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八"}
        return cn_map.get(num, str(num))

    def run(self):
        """完整推断流程，写回 building_data 并返回"""
        self._infer_num_lin()

        form_name = self._infer_form_name()
        self.building_data["category_info"]["form_name"] = form_name

        return self.building_data


if __name__ == "__main__":
    from numpy import array

    test_building_data = {
        "category_info": {
            "building_category": "房屋",
            "sub_category": "正房",
            "roof_forms": "歇山",
            "ridge_types": "卷棚",
            "construction_grades": "大式",
            "corridor": "无廊",
        },
        "dimension_info": {
            "num_bays": 5,
            "bay_widths": array([1.0, 1.0, 1.0]),
            "depth_total": array(1.5),
            "eave_step": array(0.35),
        },
    }

    infered_data = FormInferencer(test_building_data).run()
    # print(infered_data)
    print(infered_data["category_info"]["form_name"])
