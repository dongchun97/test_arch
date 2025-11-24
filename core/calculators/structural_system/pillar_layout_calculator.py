# calculators/structural/pillar_layout_calculator.py

from typing import List, Tuple


class PillarLayoutCalculator:
    """
    专门负责柱网坐标(position)计算的模块。
    - 输入 building_data + 配置 rule
    - 输出柱位坐标
    """

    def __init__(self, building_data: dict, rule: dict):
        self.data = building_data
        self.rule = rule

        # 输出
        self.axis_x = []     # x方向轴线位置
        self.axis_y = []     # y方向轴线位置
        self.pillar_positions = []  # 所有柱的3D坐标

    # ---------------------------------------------------------
    # 一、主入口
    # ---------------------------------------------------------
    def calculate(self):
        self._calc_axis_x()
        self._calc_axis_y()
        self._generate_pillar_positions()

        return {
            "axis_x": self.axis_x,
            "axis_y": self.axis_y,
            "pillar_positions": self.pillar_positions
        }

    # ---------------------------------------------------------
    # 二、水平方向：面阔方向(x 轴)柱网
    # ---------------------------------------------------------
    def _calc_axis_x(self):
        """
        依据：
        - 明间面阔
        - 次间比例
        - 尽间比例（如：尽间需凸出山墙）
        来计算 x 方向轴线位置
        """

        dim = self.data["dimension_info"]
        cat = self.data["category_info"]

        jian = cat["jian_number"]          # 总间数，如 5间
        main_span = dim["main_span"]       # 明间面阔
        flank_ratio = self.rule.get("flank_ratio", 0.8)
        end_extra = self.rule.get("gables_extend", 0.2)  # 尽间出墙，如悬山/歇山

        # 分间宽度
        spans = []
        for i in range(jian):
            if i == jian // 2:  # 明间
                spans.append(main_span)
            else:
                spans.append(main_span * flank_ratio)

        # 若结构为悬山或歇山，尽间凸出
        spans[0] += end_extra
        spans[-1] += end_extra

        # 计算轴线
        x = 0.0
        self.axis_x.append(x)

        for w in spans:
            x += w
            self.axis_x.append(x)

    # ---------------------------------------------------------
    # 三、进深方向(y 轴)柱网
    # ---------------------------------------------------------
    def _calc_axis_y(self):
        """
        根据进深分间、步架规则计算 y 方向位置
        """

        dim = self.data["dimension_info"]

        depth_span = dim.get("depth_span", 1.5)
        depth_jian = self.data["category_info"].get("depth_jian_number", 2)

        y = 0.0
        self.axis_y.append(y)

        for _ in range(depth_jian):
            y += depth_span
            self.axis_y.append(y)

    # ---------------------------------------------------------
    # 四、组合生成柱坐标
    # ---------------------------------------------------------
    def _generate_pillar_positions(self):
        """
        将 Axis X × Axis Y 组合成完整柱位网格
        """
        z_base = self.rule.get("pillar_base_level", 0.0)

        positions = []
        for x in self.axis_x:
            for y in self.axis_y:
                positions.append((x, y, z_base))

        self.pillar_positions = positions
