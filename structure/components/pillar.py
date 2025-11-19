# -----------------------------------------------------------------------------
# file: structure/components/pillar.py
# -----------------------------------------------------------------------------
import bpy
import math
from typing import Tuple
from structure.utils import get_or_create_mesh


def _build_pillar_mesh(diameter: float, height: float):
    """在真实 Blender 环境下，这里应创建 bmesh / mesh 对象。
    测试环境下返回一个简单的 MockMesh。
    """
    mesh_name = f"mesh_pillar_{diameter:.3f}_{height:.3f}"
    mesh = getattr(bpy.data, 'meshes', {}).get(mesh_name)
    if mesh:
        return mesh
    # Mock: 创建简单 mesh placeholder
    m = type('M', (), {'name': mesh_name})()
    bpy.data.meshes[mesh_name] = m
    return m


def create_pillar(diameter: float, height: float):
    mesh_key = f"pillar_{diameter:.3f}_{height:.3f}"
    mesh = get_or_create_mesh(mesh_key, lambda: _build_pillar_mesh(diameter, height))
    obj = None
    try:
        obj = bpy.data_objects_new(mesh_key, mesh)
    except Exception:
        # 兼容 Mock
        obj = type('O', (), {})()
        obj.name = mesh_key
        obj.data = mesh
    return obj