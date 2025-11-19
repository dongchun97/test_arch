# =============================================================================
# Project: structure/ 模块模板（可运行的 Python 测试版）
# 说明：此文件包含多个模块的源码片段（按文件划分）。
# 复制到你的项目中对应文件即可（例如 structure/utils.py 等）。
# 为了能在没有 Blender 环境下测试，模块使用了一个兼容层 try/except 导入 bpy，
# 若不可用则使用 MockBpy，便于单元测试和开发。
# =============================================================================

# -----------------------------------------------------------------------------
# file: component_calculator_schema.py
# -----------------------------------------------------------------------------
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Any

Vector3 = Tuple[float, float, float]

@dataclass
class PillarSpec:
    id: str
    coord: Vector3
    diameter: float
    height: float
    role: str = "main"  # main/aux

@dataclass
class BeamSpec:
    id: str
    start: Vector3
    end: Vector3
    section_width: float
    section_height: float
    elevation: float
    role: str = "beam"

@dataclass
class RoofSpec:
    roof_type: str
    ridge_height: float
    eave_height: float
    num_purlins: int
    extra: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Levels:
    base: float
    pillar_top: float
    beam_top: float
    roof_top: float

@dataclass
class ComponentCalcResult:
    # 基本网格数据
    pillars: List[PillarSpec]
    beams: List[BeamSpec]
    roof: RoofSpec

    # 网格格柵/参考线
    x_grid: List[float]
    y_grid: List[float]

    # 关键尺寸
    eave_diameter: float
    eave_height: float
    num_purlins: int
    ridge_distance: float

    # 各主要标高
    levels: Levels

    # 原始输入引用（便于回溯）
    source_reference: Dict[str, Any] = field(default_factory=dict)

    # 附加信息
    metadata: Dict[str, Any] = field(default_factory=dict)

# ----------------------------------------------------------------------------
# usage: component_calculator 应返回 ComponentCalcResult 实例，字段含义如下：
# - pillars: 列表，每个 PillarSpec 含 id, coord(x,y,z), diameter, height, role
# - beams: 列表，每个 BeamSpec 含 id, start(x,y,z), end(x,y,z), section, elevation
# - roof: RoofSpec 描述屋顶参数
# - x_grid, y_grid: 参考轴线位置（世界坐标局部坐标）\# - levels: 主要标高
# - eave_* / num_purlins / ridge_distance: 便于组件创建的尺寸参数
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# file: structure/__init__.py
# -----------------------------------------------------------------------------
# package init

# -----------------------------------------------------------------------------
# file: structure/_bpy_compat.py
# -----------------------------------------------------------------------------
# 兼容层：尝试导入 bpy；如果不可用，使用 MockBpy 便于测试
try:
    import bpy
    from mathutils import Vector
except Exception:
    # 轻量 Mock 实现（用于非 Blender 环境下测试）
    import math

    class MockObject:
        def __init__(self, name, mesh=None):
            self.name = name
            self.location = (0, 0, 0)
            self.rotation_euler = (0, 0, 0)
            self.data = mesh

        def copy(self):
            return MockObject(self.name + "_copy", self.data)

    class MockMesh:
        def __init__(self, name):
            self.name = name

    class MockCollection:
        def __init__(self, name):
            self.name = name
            self.objects = []

        def objects_link(self, obj):
            self.objects.append(obj)

    class MockBpy:
        data = type('d', (), {'meshes': {}, 'objects': {}, 'collections': {}})()
        context = type('c', (), {'scene': type('s', (), {'collection': None})()})()

        @staticmethod
        def data_meshes_get(name):
            return MockBpy.data.meshes.get(name)

        @staticmethod
        def data_objects_new(name, mesh=None):
            obj = MockObject(name, mesh)
            MockBpy.data.objects[name] = obj
            return obj

        @staticmethod
        def data_meshes_new(name):
            m = MockMesh(name)
            MockBpy.data.meshes[name] = m
            return m

    bpy = MockBpy()
    def Vector(t):
        return tuple(t)


# # -----------------------------------------------------------------------------
# # file: example_usage.py
# # -----------------------------------------------------------------------------
# # 这是一个示例，演示如何在没有 Blender 的环境下进行单元测试。
# from component_calculator_schema import (
#     ComponentCalcResult, PillarSpec, BeamSpec, RoofSpec, Levels
# )


def example():
    pillars = [PillarSpec(id='p1', coord=(0,0,0), diameter=0.32, height=3.6)]
    beams = [BeamSpec(id='b1', start=(0,0,3.6), end=(2,0,3.6), section_width=0.2, section_height=0.25, elevation=3.6)]
    roof = RoofSpec(roof_type='roll_shed', ridge_height=7.5, eave_height=3.6, num_purlins=5)
    levels = Levels(base=0.0, pillar_top=3.6, beam_top=3.8, roof_top=7.5)
    calc = ComponentCalcResult(
        pillars=pillars,
        beams=beams,
        roof=roof,
        x_grid=[0.0, 2.0],
        y_grid=[0.0, 3.0],
        eave_diameter=0.32,
        eave_height=3.6,
        num_purlins=5,
        ridge_distance=2.0,
        levels=levels,
        source_reference={'source':'example'},
        metadata={}
    )

    # 创建 prototype objects
    from structure.components.pillar import create_pillar
    from structure.components.beam import create_beam
    from structure.components.roof import create_roof

    pillar_proto = create_pillar(0.32, 3.6)
    beam_proto = create_beam(0.2, 0.25, 2.0)
    roof_proto = create_roof('roll_shed', {'num_purlins':5})

    from structure.assembler import assemble_building
    res = assemble_building(calc, {'pillar': pillar_proto, 'beam': beam_proto, 'roof': roof_proto}, {'name':'test_building'})
    print('assemble result:', res)


if __name__ == '__main__':
    
    calc_output_example = {
    "basic_info": {
        "building_name": "前殿",
        "building_type": "卷棚",
        "construction_grade": "小式",
        "module": 3.2,                       # 模数（米）
        "num_bays": 3,                       # 面阔三间
        "num_purlins": 4,                    # 四檩
        "orientation": "south",              # 朝向
        "has_dougong": False,
    },

    "structure_info": {
        "width": 3 * 3.2,                    # 面阔：三间
        "depth": 3 * 3.2,                    # 进深：三架抬梁，无论结构都可以表达
        "pillar_count": 12,                  # 典型三间四檩房屋的柱数
        "beam_count": 8,
        "roof_system": "卷棚",
    },

    "description_info": {
        "summary": "小式卷棚顶建筑，面阔三间，四檩，采用抬梁式结构。",
        "historical_style": "清式营造",
        "remarks": "柱高稍低，以体现卷棚顶舒缓的立面比例。"
    },

    # ----------------------------------------------------------
    # 这部分会在 Blender 里被替换为真实对象
    # 在非 Blender 环境中可以是 Mock 对象
    # ----------------------------------------------------------
    "components_objs": {
        "pillar": "PillarTemplateMesh",      # 真实环境中是 bpy.data.meshes[...]        
        "beam":   "BeamTemplateMesh",
        "roof":   "RoofTemplateMesh",
    },

    # ----------------------------------------------------------
    # 坐标信息（核心数据！structure 模块真正依赖的就是这些）
    # 示例以三间、四檩、3.2m 模数为例
    # ----------------------------------------------------------
    "coordinates": {

        # 12 根柱（前檐、中檐、后檐）
        "pillars_coords": [
            {"id": "P1",  "pos": (0.0,   0.0,   0.0), "type": "eave"},
            {"id": "P2",  "pos": (3.2,   0.0,   0.0), "type": "eave"},
            {"id": "P3",  "pos": (6.4,   0.0,   0.0), "type": "eave"},

            {"id": "P4",  "pos": (0.0,   3.2,   0.0), "type": "inner"},
            {"id": "P5",  "pos": (3.2,   3.2,   0.0), "type": "inner"},
            {"id": "P6",  "pos": (6.4,   3.2,   0.0), "type": "inner"},

            {"id": "P7",  "pos": (0.0,   6.4,   0.0), "type": "eave"},
            {"id": "P8",  "pos": (3.2,   6.4,   0.0), "type": "eave"},
            {"id": "P9",  "pos": (6.4,   6.4,   0.0), "type": "eave"},
        ],

        # 梁坐标（按抬梁式基本逻辑）
        "beams_coords": [
            {
                "id": "B1",
                "type": "transverse_beam",
                "start": (0.0, 0.0, 3.2),
                "end":   (6.4, 0.0, 3.2),
                "level": "eave"
            },
            {
                "id": "B2",
                "type": "transverse_beam",
                "start": (0.0, 3.2, 3.5),
                "end":   (6.4, 3.2, 3.5),
                "level": "inner"
            },
            {
                "id": "B3",
                "type": "transverse_beam",
                "start": (0.0, 6.4, 3.2),
                "end":   (6.4, 6.4, 3.2),
                "level": "eave"
            },
        ],

        # 屋面坐标（卷棚顶）
        "roof_coords": {
            "ridge_line": [
                (0.0, 3.2, 6.0),
                (6.4, 3.2, 6.0),
            ],
            "eave_line_front": [
                (0.0, 0.0, 3.0),
                (6.4, 0.0, 3.0),
            ],
            "eave_line_back": [
                (0.0, 6.4, 3.0),
                (6.4, 6.4, 3.0),
            ],
            "roof_type": "roll_shed"
        }
    },

    # ----------------------------------------------------------
    # 层级（可直接与 Blender collections 对应）
    # ----------------------------------------------------------
    "levels": {
        "ground": 0.0,
        "pillar_height": 3.2,
        "beam_elevation": 3.2,
        "roof_elevation": 6.0
    },

    # ----------------------------------------------------------
    # 真实 Blender 中，这里将是 bpy.data.collections['前殿']
    # ----------------------------------------------------------
    "collection": "MainBuildingCollection"
}


    example()
