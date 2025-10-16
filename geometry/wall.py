# geometry/wall.py
import bpy, bmesh
from mathutils import Vector


class WallGeometry:
    """基于计算数据生成山墙几何体"""

    def __init__(self, params):
        self.params = params

    def build(self, base_data, body_data, roofjoint_data):
        # 创建一个新的网格对象
        mesh = bpy.data.meshes.new("WallMesh")
        bm = bmesh.new()

        # ========== 1. 基座 ==========
        bh = base_data["base_height"]
        wt = base_data["wall_thickness"]
        v1 = bmesh.ops.create_vert(bm, co=Vector((0, 0, 0)))
        v2 = bmesh.ops.create_vert(bm, co=Vector((self.params["span"], 0, 0)))
        v3 = bmesh.ops.create_vert(bm, co=Vector((self.params["span"], wt, bh)))
        v4 = bmesh.ops.create_vert(bm, co=Vector((0, wt, bh)))
        bmesh.ops.contextual_create(
            bm, geom=[v1["vert"], v2["vert"], v3["vert"], v4["vert"]]
        )

        # ========== 2. 墙身 ==========
        wh = body_data["wall_height"]
        top_z = bh + wh
        v5 = bmesh.ops.create_vert(bm, co=Vector((0, 0, top_z)))
        v6 = bmesh.ops.create_vert(bm, co=Vector((self.params["span"], 0, top_z)))
        bmesh.ops.contextual_create(
            bm, geom=[v2["vert"], v6["vert"], v5["vert"], v1["vert"]]
        )

        # ========== 3. 屋面线 ==========
        rh = roofjoint_data["roof_height"]
        roof_peak = top_z + rh
        peak = bmesh.ops.create_vert(
            bm, co=Vector((self.params["span"] / 2, wt / 2, roof_peak))
        )

        # 连接山墙三角面
        bmesh.ops.contextual_create(bm, geom=[v5["vert"], v6["vert"], peak["vert"]])

        bm.to_mesh(mesh)
        mesh.update()

        obj = bpy.data.objects.new("Wall", mesh)
        bpy.context.collection.objects.link(obj)
        return obj
