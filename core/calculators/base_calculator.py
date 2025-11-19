# calculators/base_calculator.py

class BaseCalculator:

    def __init__(self, config):
        self.config = config

    # ------ 公共计算：柱网（基础结构） ------
    def compute_grid(self, dimension_info):
        num_bays = dimension_info["num_bays"]
        bay_widths = dimension_info["bay_widths"]

        x_coords = [0]
        for w in bay_widths:
            x_coords.append(x_coords[-1] + w)

        # 输出柱位矩阵（可扩展）
        grid = {
            "x": x_coords,
            "depth": dimension_info["depth_total"],
        }
        return grid

    # ------ 公共计算：举架系统（高度、檩位等） ------
    def compute_jujia(self):
        cfg = self.config

        pillar_diameter = cfg["pillar_diameter_base"]
        pillar_height = pillar_diameter * cfg["pillar_height_ratio"]

        beam_length = pillar_diameter * cfg["beam_length_ratio"]

        heights = {
            "pillar_height": pillar_height,
            "beam_length": beam_length
        }
        return heights

    # ------ 主流程（形态 calculator 会 override） ------
    def compute(self, building_info):
        grid = self.compute_grid(building_info["dimension_info"])
        heights = self.compute_jujia()

        return {
            "grid": grid,
            "heights": heights,
            "config": self.config
        }
