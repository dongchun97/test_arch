# -----------------------------------------------------------------------------
# file: structure/frame/roof_system.py
# -----------------------------------------------------------------------------
from typing import Any, Dict


def build_roof_system(roof_spec: Any, roof_proto, collection):
    inst = None
    try:
        inst = roof_proto.copy()
    except Exception:
        inst = type('O', (), {})()
        inst.name = roof_proto.name + "_inst"
        inst.data = roof_proto.data
    # 真实 Blender 中需要对屋面网格进行拉伸/定位
    try:
        collection.objects_link(inst)
    except Exception:
        getattr(collection, 'objects', []).append(inst)
    return inst