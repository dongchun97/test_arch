# -----------------------------------------------------------------------------
# file: structure/components/beam.py
# -----------------------------------------------------------------------------
import bpy
from structure.utils import get_or_create_mesh


def _build_beam_mesh(width: float, height: float, length: float):
    mesh_name = f"mesh_beam_{width:.3f}_{height:.3f}_{length:.3f}"
    m = getattr(bpy.data, 'meshes', {}).get(mesh_name)
    if m:
        return m
    m = type('M', (), {'name': mesh_name})()
    bpy.data.meshes[mesh_name] = m
    return m


def create_beam(width: float, height: float, length: float):
    mesh_key = f"beam_{width:.3f}_{height:.3f}_{length:.3f}"
    mesh = get_or_create_mesh(mesh_key, lambda: _build_beam_mesh(width, height, length))
    try:
        obj = bpy.data_objects_new(mesh_key, mesh)
    except Exception:
        obj = type('O', (), {})()
        obj.name = mesh_key
        obj.data = mesh
    return obj