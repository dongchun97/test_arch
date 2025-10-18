import numpy as np
from typing import Dict, Any
from dataclasses import dataclass, asdict
import math
import bpy, bmesh
from mathutils import Vector
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class DataLoader:
    """数据加载器
    职责：
    1. 读取CSV数据
    2. 提供结构化的建筑数据
    3. 支持建筑数据获取功能
    """

    def __init__(self, path: str):
        self.path = path
        self.headers = []
        self.data = None
        self.building_data = None
        self._load_csv()

    def _load_csv(self) -> np.ndarray:
        """加载CSV数据"""

        raw_data = np.genfromtxt(self.path, delimiter=",", dtype=str, encoding="utf-8")
        self.headers = raw_data[0, :].tolist()
        self.data = raw_data[2:, :]

        return self.data

    def get_str_value(
        self, row: np.ndarray, field_name: str, as_float: bool = False
    ) -> Any:
        try:
            idx = self.headers.index(field_name)
            val = str(row[idx]).strip()

            if as_float:
                try:
                    return float(val) if val else np.nan
                except ValueError:
                    return np.nan
            return val
        except Exception as e:
            return np.nan if as_float else ""

    def get_building_data(self, row_index: int) -> Dict[str, Any]:
        """获取指定行的建筑数据

        Args:
            row_index: 行索引

        Returns:
            结构化的建筑数据字典
        """
        if self.data is None:
            raise ValueError("数据尚未加载。请先调用 load_csv。")

        if row_index < 0 or row_index >= len(self.data):
            raise ValueError(f"行索引 {row_index} 超出范围")

        row = self.data[row_index]

        # 1. 基础信息
        basic_info = {
            "garden_name": self.get_str_value(row, "园林名称"),
            "garden_id": self.get_str_value(row, "园中园编号"),
            "sub_garden_name": self.get_str_value(row, "园中园名称"),
            "building_id": self.get_str_value(row, "建筑编号"),
            "building_name": self.get_str_value(row, "建筑名称"),
        }

        # 2. 构造信息
        structure_info = {
            "construction": self.get_str_value(row, "建筑形式"),
            "corridor": self.get_str_value(row, "出廊"),
        }

        # 3. 描述信息
        description_info = {
            "form": self.get_str_value(row, "描述1"),
        }

        num_lintels = None
        construction = structure_info.get("construction")
        if "四檩" in construction:
            num_lintels = 4
        elif "五檩" in construction:
            num_lintels = 5
        elif "六檩" in construction:
            num_lintels = 6
        elif "七檩" in construction:
            num_lintels = 7
        elif "八檩" in construction:
            num_lintels = 8

        # 5. 尺寸信息
        # 5.1 面阔数据
        all_bays = np.array(
            [
                self.get_str_value(row, "明间", True),
                self.get_str_value(row, "次间", True),
                self.get_str_value(row, "二次间", True),
                self.get_str_value(row, "三次间", True),
            ]
        )

        bay_widths = all_bays[~np.isnan(all_bays)]

        bays = len(bay_widths) * 2 - 1

        # 5.2 进深数据
        depth_total = np.array(self.get_str_value(row, "通进深", True))
        eave_step = np.array(self.get_str_value(row, "檐步架", True))

        # 5.3 檐柱径
        D = all_bays[0] * 0.8

        # 组合所有数据
        self.building_data = {
            "basic_info": basic_info,
            "structure_info": structure_info,
            "description_info": description_info,
            "dimension_info": {
                "num_lintels": num_lintels,
                "num_bays": bays,
                "bay_widths": bay_widths.tolist(),
                "depth_total": float(depth_total),
                "eave_step": float(eave_step),
                "D": float(D),
            },
        }

        return self.building_data


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


def create_pillars(result):

    name = "pillars"
    bm = bmesh.new()

    for x, y in result["pillar_coords"]:
        v = bmesh.ops.create_vert(bm, co=Vector((x, y, 0)))

    for beam in result["beam_data"]["x_beams"]:
        v1 = Vector((*beam["start"], 0))
        v2 = Vector((*beam["end"], 0))
        bmesh.ops.create_edge(bm, verts=[bm.verts.new(v1), bm.verts.new(v2)])

        mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.data.collections["Collection"].objects.link(obj)

    bm.to_mesh(mesh)
    bm.free()


def process_data_file(file_path):
    """主流程协调器"""

    # 1. 加载数据
    loader = DataLoader(file_path)
    data = loader.get_building_data(1)  # 加载数据行
    dimension = data["dimension_info"]

    # 2. 计算数据
    result = FrameGeometryCalculator(**dimension)
    create_pillars(result)

    # # 3. 结构化数据
    # structurer = Assembler()
    # structured_objects = structurer.create_objects(standardized_data)

    # 4. 返回或保存结果
    # return structured_objects
    return result


def generator(file_path):
    return process_data_file(file_path)


def main():

    data = "data/data-2.csv"
    generator(data)


main()
