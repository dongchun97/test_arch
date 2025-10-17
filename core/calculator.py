import numpy as np
from dataclasses import dataclass, asdict
import math


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
    num_lintels:檩数
    num_bays:楹数
    bay_widths:面阔列表[1.2, 1.0, 1.0]
    depth_total:通进深
    eave_step:檐步架
    D,
    symmetry=True,
    """

    def __init__(
        self,
        num_lintels,
        num_bays,
        bay_widths,
        depth_total,
        eave_step,
        D,
        symmetry=True,
    ):
        self.num_lintels = num_lintels
        self.num_bays = num_bays
        self.bay_widths = bay_widths
        self.depth_total = depth_total
        self.eave_step = eave_step
        self.D = D
        self.symmetry = symmetry

        # 初始化空数据
        self.x_grid = None
        self.y_grid = None
        self.pillar_coords = None
        self.beams = []
        self.walls = []
        self.compute_all()  # 进行计算,可初始化或非初始化

    # --------------------------------------------------------
    # 主流程入口
    # --------------------------------------------------------
    def compute_all(self):
        self._compute_grids()
        self._compute_pillars()
        self._compute_beams()
        self._compute_gables()
        self._compute_eave_and_corner_beams()
        return self._export_result()

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
        if self.num_lintels == 6:
            depth_segments = [self.eave_step, 0.5, self.D * 3, 0.5, self.eave_step]
        else:
            inner_depth = self.depth_total - 2 * self.eave_step
            seg = inner_depth / (self.num_lintels - 2)
            depth_segments = (
                [self.eave_step] + [seg] * (self.num_lintels - 2) + [self.eave_step]
            )

        y_grid = np.zeros(len(depth_segments) + 1)
        for i, d in enumerate(depth_segments):
            y_grid[i + 1] = y_grid[i] + d
        y_grid -= y_grid[-1] / 2

        self.x_grid, self.y_grid = x_grid, y_grid

    # --------------------------------------------------------
    # Step 2: 柱网坐标
    # --------------------------------------------------------
    def _compute_pillars(self):
        """
        计算平面柱网坐标，返回pillar_coords
        """
        X, Y = np.meshgrid(self.x_grid, self.y_grid)
        self.pillar_coords = np.stack([X.ravel(), Y.ravel()], axis=1)

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
        wall_height = self.D * 15  # 仅示例，可用比例代替
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
            "x_grid": self.x_grid.tolist(),
            "y_grid": self.y_grid.tolist(),
            "pillars": self.pillar_coords.tolist(),
            "beams": [asdict(b) for b in self.beams],
            "walls": [asdict(w) for w in self.walls],
        }


if __name__ == "__main__":
    calc = FrameGeometryCalculator(
        num_lintels=6,
        num_bays=5,
        bay_widths=[1.2, 1.0, 1.0],
        depth_total=2.3,
        eave_step=0.4,
        D=0.1,
    )

    # result = calc.compute_all()

    # print("柱网数量:", len(result["pillars"]))
    # print("梁数:", len(result["beams"]))
    # print("山墙数:", len(result["walls"]))
    # print("首个老角梁:", [b for b in result["beams"] if b["type"] == "corner_beam"][0])

    result = calc.x_grid
    print(result)
