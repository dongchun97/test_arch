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

    bm = bmesh.new()

    radius_bottom = D / 2
    radius_top = (D * taper_ratio) / 2

    # 创建底部圆环（带边）
    bottom_circle = bmesh.ops.create_circle(
        bm,
        cap_ends=False,  # 创建圆环，有边界边
        segments=segments,
        radius=radius_bottom,
    )

    # 创建顶部圆环
    top_circle = bmesh.ops.create_circle(
        bm, cap_ends=False, segments=segments, radius=radius_top
    )

    # 移动顶部圆环到正确高度
    for vert in top_circle["verts"]:
        vert.co.z = H

    # 现在有边界边了，可以桥接
    bottom_edges = [
        e for e in bm.edges if e.is_boundary and all(v.co.z < 0.001 for v in e.verts)
    ]
    top_edges = [
        e
        for e in bm.edges
        if e.is_boundary and all(v.co.z > H - 0.001 for v in e.verts)
    ]

    if bottom_edges and top_edges:
        bmesh.ops.bridge_loops(bm, edges=bottom_edges + top_edges)

    # 封顶
    if cap_ends:
        bottom_boundary = [
            e
            for e in bm.edges
            if e.is_boundary and all(v.co.z < 0.001 for v in e.verts)
        ]
        top_boundary = [
            e
            for e in bm.edges
            if e.is_boundary and all(v.co.z > H - 0.001 for v in e.verts)
        ]

        if bottom_boundary:
            bmesh.ops.holes_fill(bm, edges=bottom_boundary)
        if top_boundary:
            bmesh.ops.holes_fill(bm, edges=top_boundary)

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
