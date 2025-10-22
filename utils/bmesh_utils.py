import bpy
import bmesh



def get_placeholder_mesh_obj_and_bm(context, name,location=Vector((0, 0, 0))):
    mesh_placeholder = bpy.data.meshes.new(name=name)
    obj_placeholder = bpy.data.objects.new(name=name,
                                             object_data=mesh_placeholder)
    obj_placeholder.location = location
    context.collection.objects.link(obj_placeholder)
    for o in context.scene.objects:
        o.select_set(False)
    context.view_layer.objects.active = obj_placeholder
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(mesh_placeholder)
    return bm, obj_placeholder