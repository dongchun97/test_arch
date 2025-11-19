# -----------------------------------------------------------------------------
# file: structure/components/roof.py
# -----------------------------------------------------------------------------
import bpy
from structure.utils import get_or_create_mesh


def _build_roof_mesh(roof_type: str, params: dict):
    mesh_name = f"mesh_roof_{roof_type}"
    m = getattr(bpy.data, 'meshes', {}).get(mesh_name)
    if m:
        return m
    m = type('M', (), {'name': mesh_name, 'params': params})()
    bpy.data.meshes[mesh_name] = m
    return m


def create_roof(roof_type: str, params: dict):
    mesh_key = f"roof_{roof_type}"
    mesh = get_or_create_mesh(mesh_key, lambda: _build_roof_mesh(roof_type, params))
    try:
        obj = bpy.data_objects_new(mesh_key, mesh)
    except Exception:
        obj = type('O', (), {})()
        obj.name = mesh_key
        obj.data = mesh
    return obj