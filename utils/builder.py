import bpy


def create_cube(name: str, size: float = 1.0):
    """创建一个立方体"""
    bpy.ops.mesh.primitive_cube_add(size=size)
    obj = bpy.context.active_object
    obj.name = name
    return obj


# main
# from utils import create_cube

# create_cube("TestCube", size=2.0)
# bpy.ops.wm.save_as_mainfile(filepath="output/output_scene.blend")
