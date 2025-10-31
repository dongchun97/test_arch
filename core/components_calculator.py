import numpy as np
from dataclasses import dataclass, asdict
import math
from config_loader import ConfigLoader


@dataclass
class Beam:
    start: tuple
    end: tuple
    length: float
    type: str  # x_beam, y_beam, eave_beam, corner_beam, ridge_beam


@dataclass
class Wall:
    base_line: tuple  # [(x1, y1), (x2, y2)]
    height: float
    type: str  # gable, partition


class FrameGeometryCalculator:
    """
    清式建筑：平面柱网与主要梁枋、山墙几何计算类
    num_bays:楹数
    bay_widths:面阔列表[1.2, 1.0, 1.0]
    depth_total:通进深
    eave_step:檐步架
    symmetry=True,

    : diameter
    : height
    : num_purlins
    : ridge_distance
    : x_grid
    : y_grid
    : pillars_coords
    : beams
    : walls
    """

    def __init__(
        self,
        globle_scale,
        num_bays,
        bay_widths,
        depth_total,
        eave_step,
        symmetry=True,
    ):
        self.globle_scale = globle_scale
        self.num_bays = num_bays
        self.bay_widths = bay_widths
        self.depth_total = depth_total
        self.eave_step = eave_step
        self.symmetry = symmetry

        # 初始化空数据
        self.diameter = None
        self.height = None
        self.num_purlins = None
        self.ridge_distance = None
        self.x_grid = None
        self.y_grid = None
        self.pillar_coords = None
        self.beams = []
        self.walls = []

    # --------------------------------------------------------
    # 主流程入口
    # --------------------------------------------------------
    def compute_all(self):
        self._compute_eave_and_ridge_distance()
        self._compute_grids()
        self._compute_pillars_coords()
        self._compute_beams()
        self._compute_gables()
        self._compute_eave_and_corner_beams()
        return self._export_result()

    def _compute_eave_and_ridge_distance(self):

        self.diameter = self.bay_widths[0] * 0.08
        self.height = self.bay_widths[0] * 0.07

        self.num_purlins = int(self.depth_total // self.eave_step) + 2  # 檩数
        self.ridge_distance = self.depth_total % self.eave_step  # 脊步架

    # --------------------------------------------------------
    # Step 1: 面阔与进深坐标网格
    # --------------------------------------------------------
    def _compute_grids(self):
        """
        计算面阔与进深坐标网格，返回x_grid, y_grid
        """
        if self.symmetry:
            # 左右对称展开
            half = self.bay_widths[::-1]
            full_bays = half + self.bay_widths[1:]
        else:
            full_bays = self.bay_widths

        x_grid = np.zeros(len(full_bays) + 1)
        for i, w in enumerate(full_bays):
            x_grid[i + 1] = x_grid[i] + w
        x_grid -= x_grid[-1] / 2

        # 进深方向
        if self.num_purlins == 8:
            depth_segments = [
                self.eave_step,
                self.eave_step,
                self.eave_step,
                self.ridge_distance,
                self.eave_step,
                self.eave_step,
                self.eave_step,
            ]
        elif self.num_purlins == 6:
            depth_segments = [
                self.eave_step,
                self.eave_step,
                self.ridge_distance,
                self.eave_step,
                self.eave_step,
            ]
        elif self.num_purlins == 4:
            depth_segments = [
                self.eave_step,
                self.ridge_distance,
                self.eave_step,
            ]
        # else:
        #     inner_depth = self.depth_total - 2 * self.eave_step
        #     seg = inner_depth / (self.num_purlins - 2)
        #     depth_segments = (
        #         [self.eave_step] + [seg] * (self.num_purlins - 2) + [self.eave_step]
        #     )

        y_grid = np.zeros(len(depth_segments) + 1)
        for i, d in enumerate(depth_segments):
            y_grid[i + 1] = y_grid[i] + d
        y_grid -= self.depth_total / 2

        self.x_grid, self.y_grid = x_grid, y_grid

    # --------------------------------------------------------
    # Step 2: 柱网坐标
    # --------------------------------------------------------
    def _compute_pillars_coords(self):
        """
        计算平面柱网坐标，返回pillar_coords
        """
        X, Y = np.meshgrid(self.x_grid, self.y_grid)
        Z = np.zeros_like(X)
        self.pillar_coords = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=1)

    # --------------------------------------------------------
    # Step 3: 梁枋（包括进深梁与面阔梁）
    # --------------------------------------------------------
    def _compute_beams(self):
        """
        计算梁枋
        """

        # 面阔梁 (沿x方向)
        for y in self.y_grid:
            for i in range(len(self.x_grid) - 1):
                start = np.round((self.x_grid[i], y), 2)
                end = np.round((self.x_grid[i + 1], y), 2)
                self.beams.append(Beam(start, end, end[0] - start[0], "x_beam"))

        # 进深梁 (沿y方向)
        for x in self.x_grid:
            for j in range(len(self.y_grid) - 1):
                start = np.round((x, self.y_grid[j]), 2)
                end = np.round((x, self.y_grid[j + 1]), 2)
                self.beams.append(Beam(start, end, end[1] - start[1], "y_beam"))

    # --------------------------------------------------------
    # Step 4: 山墙（一般在最前、最后一排檩柱）
    # --------------------------------------------------------
    def _compute_gables(self):
        """
        计算山墙
        """
        front_line = [
            (self.x_grid[0], self.y_grid[0]),
            (self.x_grid[-1], self.y_grid[0]),
        ]
        back_line = [
            (self.x_grid[0], self.y_grid[-1]),
            (self.x_grid[-1], self.y_grid[-1]),
        ]
        wall_height = self.diameter * 15  # 仅示例，可用比例代替
        self.walls.append(Wall(front_line, wall_height, "gable"))
        self.walls.append(Wall(back_line, wall_height, "gable"))

    # --------------------------------------------------------
    # Step 5: 老檐枋、老角梁（基于檐口两侧）
    # --------------------------------------------------------
    def _compute_eave_and_corner_beams(self):
        """
        计算老檐枋和老角梁
        """
        # 前檐老檐枋
        y_front = self.y_grid[0]
        y_back = self.y_grid[-1]

        self.beams.append(
            Beam(
                (self.x_grid[0], y_front),
                (self.x_grid[-1], y_front),
                self.x_grid[-1] - self.x_grid[0],
                "eave_beam_front",
            )
        )
        self.beams.append(
            Beam(
                (self.x_grid[0], y_back),
                (self.x_grid[-1], y_back),
                self.x_grid[-1] - self.x_grid[0],
                "eave_beam_back",
            )
        )

        # 四角老角梁
        corners = [
            ((self.x_grid[0], y_front), (self.x_grid[1], self.y_grid[1])),
            ((self.x_grid[-1], y_front), (self.x_grid[-2], self.y_grid[1])),
            ((self.x_grid[0], y_back), (self.x_grid[1], self.y_grid[-2])),
            ((self.x_grid[-1], y_back), (self.x_grid[-2], self.y_grid[-2])),
        ]
        for start, end in corners:
            length = round(math.dist(start, end), 2)
            self.beams.append(
                Beam(np.round((start), 2), np.round((end), 2), length, "corner_beam")
            )

    # --------------------------------------------------------
    # Step 6: 导出
    # --------------------------------------------------------
    def _export_result(self):
        return {
            "diameter": self.diameter,
            "height": self.height,
            "num_purlins": self.num_purlins,
            "ridge_distance": self.ridge_distance,
            "x_grid": self.x_grid,
            "y_grid": self.y_grid,
            "pillars_coords": self.pillar_coords,
            "beams": [asdict(b) for b in self.beams],
            "walls": [asdict(w) for w in self.walls],
        }


if __name__ == "__main__":

    from numpy import array

    data = {
        "category_info": {
            "building_category": "房屋",
            "sub_category": "正房",
            "roof_forms": "歇山",
            "corridor": "无廊",
        },
        "precision_info": {"pricision": ""},
        "dimension_info": {
            "num_lin": 6,
            "num_bays": 5,
            "bay_widths": [1.0, 1.0, 1.0],
            "depth_total": array(1.5),
            "eave_step": array(0.35),
        },
        "structure_name": "六檩卷棚大式",
    }
    dimension_info = data["dimension_info"]
    structure_name = data["structure_name"]

    configloader = ConfigLoader(data)
    globe_scale = configloader.get_scale

    calc = FrameGeometryCalculator(**dimension_info)
    calc.compute_all()

    # print(calc.diameter)
    # print(calc.height)
    # print(calc.x_grid)
    # print(calc.y_grid)
