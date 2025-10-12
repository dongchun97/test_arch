import bpy
import bmesh
import math
from mathutils import Vector

bpy.ops.object.select_all(action="DESELECT")


def get_placeholder_mesh_obj_and_bm(context, name, center):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    scene = bpy.context.scene
    scene.collection.children["Collection"].objects.link(obj)

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")

    bm = bmesh.from_edit_mesh(mesh)
    return bm, obj


def select_edge_loops(bm, ref_edges, select_rings=False):
    """
    选择边循环或边环

    Args:
        bm: BMesh实例
        ref_edges: 参考边列表
        select_rings: 是否选择边环（False为边循环）

    Returns:
        list: 选中的边列表
    """
    bpy.ops.mesh.select_all(action="DESELECT")

    # 选择参考边
    for re in ref_edges:
        re.select = True

    # 执行循环选择
    bpy.ops.mesh.loop_multi_select(ring=select_rings)

    # 收集选中的边
    loop_edges = []
    for e in bm.edges:
        if e.select:
            loop_edges.append(e)

    return loop_edges


def create_arc_with_tangents(
    bm,
    radius,
    angle,
    segments,
    plane,
):
    """创建带切线的圆弧
    plane: "XZ" 或 "YZ"
    - 在 XZ 平面时，关于 Y 轴对称
    - 在 YZ 平面时，关于 X 轴对称
    - 所有顶点的 Z >= 0
    """

    # 角度区间以 pi/2 为中心，保证对称且 Z >= 0
    angle_rad = math.radians(angle)
    start_angle = math.pi / 2 - angle_rad / 2
    end_angle = math.pi / 2 + angle_rad / 2

    # 圆弧顶点
    arc_verts = []
    for i in range(segments + 1):
        theta = start_angle + (end_angle - start_angle) * i / segments
        x = radius * math.cos(theta)
        z = radius * math.sin(theta)

        if plane == "XZ":  # Z>0，关于 Y 轴对称
            arc_verts.append(bm.verts.new((x, 0, z)))
        elif plane == "YZ":  # Z>0，关于 X 轴对称
            arc_verts.append(bm.verts.new((0, x, z)))
        else:
            raise ValueError("plane 参数必须是 'XZ' 或 'YZ'")

    # 起点切线
    start_tangent_angle = start_angle + math.pi / 2
    tlen = radius * 1.0
    tx = radius * math.cos(start_tangent_angle)
    tz = radius * math.sin(start_tangent_angle)

    if plane == "XZ":
        start_tangent_vert = bm.verts.new(
            (arc_verts[0].co.x - tx, 0, arc_verts[0].co.z - tz)
        )
    else:  # YZ
        start_tangent_vert = bm.verts.new(
            (0, arc_verts[0].co.y - tx, arc_verts[0].co.z - tz)
        )

    # 终点切线
    end_tangent_angle = end_angle + math.pi / 2
    tx2 = radius * math.cos(end_tangent_angle)
    tz2 = radius * math.sin(end_tangent_angle)

    if plane == "XZ":
        end_tangent_vert = bm.verts.new(
            (arc_verts[-1].co.x + tx2, 0, arc_verts[-1].co.z + tz2)
        )
    else:  # YZ
        end_tangent_vert = bm.verts.new(
            (0, arc_verts[-1].co.y + tx2, arc_verts[-1].co.z + tz2)
        )

    # 创建圆弧边
    for i in range(len(arc_verts) - 1):
        bm.edges.new([arc_verts[i], arc_verts[i + 1]])

    # 创建切线边
    bm.edges.new([start_tangent_vert, arc_verts[0]])
    bm.edges.new([arc_verts[-1], end_tangent_vert])

    return arc_verts


def test_create_arc_with_tangents(
    context, name, radius, angle, segments, plane="XZ", center=Vector((0, 0, 0))
):
    # 1. 初始化 bm + obj
    bm, obj = get_placeholder_mesh_obj_and_bm(context, name, center)

    # 2. 生成圆弧 + 切线
    create_arc_with_tangents(bm, radius, angle, segments, plane)

    # 3. （可选）选择循环边
    if bm.edges:
        loop_edges = select_edge_loops(bm, ref_edges=[bm.edges[0]], select_rings=False)
    else:
        loop_edges = []

    # 4. 对整个网格做对称
    faces = bmesh.ops.symmetrize(
        bm,
        input=bm.verts[:],
        direction='X',
        dist=0.001,
    )

    # 5. 更新到界面
    bmesh.update_edit_mesh(obj.data)

    return obj, faces, loop_edges


test_create_arc_with_tangents(bpy.context, "arcXZ", 3, 120, 12, "XZ", Vector((0, 0, 0)))


# arc2 = create_arc_with_tangents(
#     bpy.context,
#     "arcYZ",
#     radius=3,
#     angle=120,
#     segments=12,
#     plane="YZ",
#     center=Vector((5, 0, 0)),
# )
