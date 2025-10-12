import bpy
import bmesh


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
