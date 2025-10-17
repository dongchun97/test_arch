import bpy, bmesh

from mathutils import Vector


def create_pillars(result):

    result = FrameGeometryCalculator(**dimension)

    bm = bmesh.new()
    for x, y in result["pillar_coords"]:
        v = bmesh.ops.create_vert(bm, co=Vector((x, y, 0)))

    for beam in result["beam_data"]["x_beams"]:
        v1 = Vector((*beam["start"], 0))
        v2 = Vector((*beam["end"], 0))
        bmesh.ops.create_edge(bm, verts=[bm.verts.new(v1), bm.verts.new(v2)])

    name = "pillars"
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.data.collections["Collection"].objects.link(obj)
    bm.to_mesh(mesh)
    bm.free()


def get_placeholder_mesh_obj_and_bm(context, name, center):

    bm = bmesh.new()

    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.data.collections["Collection"].objects.link(obj)

    bm.to_mesh(mesh)
    return bm, obj


if __name__ == "__main__":
    import os, sys

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

    from core import DataLoader
    from core import FrameGeometryCalculator

    file_path = "data/data-2.csv"
    loader = DataLoader(file_path)
    data = loader.get_building_data(1)  # 加载数据行
    dimension = data["dimension_info"]
    print(dimension)

    result = FrameGeometryCalculator(**dimension)
    print(result.beams)
