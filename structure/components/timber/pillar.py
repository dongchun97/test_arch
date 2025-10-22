"""
structure/components/timber/pillar.py
--------------------------------------
封装柱子构件：
- 调用 geometry/pillar.py 生成 bmesh
- 创建 mesh 和 object
- 支持批量生成柱网
"""

import sys, pathlib

sys.path.append(str(pathlib.Path.cwd()))
print(sys.path)

# from geometry import make_pillar_bmesh
import bpy
from core import FrameGeometryCalculator


# class PillarNet:
#     """
#     批量生成柱网
#     """

#     def __init__(
#         self,
#         coords_list: list,
#         D: float = 0.3,
#         H: float = 3.0,
#         taper_ratio: float = 1.0,
#         segments: int = 8,
#         name_prefix: str = "Pillar",
#         material: bpy.types.Material = None,
#     ):
#         """
#         coords_list: [(x, y, z), ...] 柱子位置列表
#         """
#         self.coords_list = coords_list
#         self.D = D
#         self.H = H
#         self.taper_ratio = taper_ratio
#         self.segments = segments
#         self.name_prefix = name_prefix
#         self.material = material

#         self.mesh = None
#         self.obj = None
#         self.get_pillar_mesh()
#         self.pillars = []  # 保存 Pillar 实例
#         self.objects = []  # 保存 bpy objects
#         self.build_all()

#     def get_pillar_mesh(self):
#         """
#         根据参数生成柱子对象
#         """
#         # 生成bmesh
#         bm = make_pillar_bmesh(
#             D=self.D, H=self.H, segments=self.segments, taper_ratio=self.taper_ratio
#         )

#         # 转成mesh
#         self.mesh = bpy.data.meshes.new(f"{self.name_prefix}_Mesh")
#         bm.to_mesh(self.mesh)
#         bm.free()

#         return self.mesh

#     def build_all(self):
#         """
#         遍历坐标列表生成柱子
#         """
#         for i, coord in enumerate(self.coords_list):
#             pillar_name = f"{self.name_prefix}_{i+1}"
#             pillar = Pillar(
#                 D=self.D,
#                 H=self.H,
#                 location=coord,
#                 taper_ratio=self.taper_ratio,
#                 segments=self.segments,
#                 name=pillar_name,
#                 material=self.material,
#             )
#             self.pillars.append(pillar)
#             self.objects.append(pillar.obj)

#         print(f"已生成 {len(self.pillars)} 根柱子。")
#         return self.objects


if __name__ == "__main__":

    dimension_info={'num_purlins': 4, 'num_bays': 5, 'bay_widths': [1.0, 1.0, 1.0], 'depth_total': 1.5, 'eave_step':0.35, 'ridge_step': 0.1, 'D': 0.8}
    result=FrameGeometryCalculator(**dimension_info)
    result.compute_all()
    print(result['x_grid'])