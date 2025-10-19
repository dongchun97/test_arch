"""
geometry/pillar.py
------------------
定义柱子几何体的底层建模逻辑（纯 bmesh 操作，不涉及 object、collection）。
"""

import bmesh
import math
import bpy


def make_pillar_bmesh(
    D: float = 0.3,
    H: float = 3.0,
    segments: int = 16,
    cap_ends: bool = True,
    taper_ratio: float = 1.0,
) -> bmesh.types.BMesh:
    """
    创建柱子的 bmesh 对象。

    参数：
        D (float): 柱径（底部直径）
        H (float): 柱高
        segments (int): 圆柱分段数
        cap_ends (bool): 是否封顶
        taper_ratio (float): 顶端直径与底部直径之比（用于表示收分）

    返回：
        bmesh.types.BMesh: 柱子的 bmesh 对象
    """

    bm = bmesh.new()

    # 顶端与底端半径
    radius_bottom = D / 2
    radius_top = (D * taper_ratio) / 2

    # 创建底部圆
    circle_bottom = bmesh.ops.create_circle(
        bm, segments=segments, radius=radius_bottom
    )["verts"]

    # 复制并上移，创建顶部圆
    ret = bmesh.ops.duplicate(bm, geom=circle_bottom)
    circle_top = [v for v in ret["geom"] if isinstance(v, bmesh.types.BMVert)]
    for v in circle_top:
        v.co.z += H
        # 应用收分
        v.co.x *= taper_ratio
        v.co.y *= taper_ratio

    # 连接上下圆
    bmesh.ops.bridge_loops(bm, edges=[e for e in bm.edges if e.is_boundary])

    # 封顶与封底
    if cap_ends:
        bottom_edges = [e for e in bm.edges if all(v.co.z < 0.001 for v in e.verts)]
        top_edges = [e for e in bm.edges if all(v.co.z > H - 0.001 for v in e.verts)]
        if bottom_edges:
            bmesh.ops.holes_fill(bm, edges=bottom_edges)
        if top_edges:
            bmesh.ops.holes_fill(bm, edges=top_edges)

    # 统一法线方向
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    return bm


# 可选测试代码：直接在Blender中运行此脚本
if __name__ == "__main__":
    bm = make_pillar_bmesh(D=0.4, H=3.2, taper_ratio=0.97)

    mesh = bpy.data.meshes.new("TestPillarMesh")
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new("TestPillar", mesh)
    bpy.context.collection.objects.link(obj)
