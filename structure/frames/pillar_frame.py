# -----------------------------------------------------------------------------
# file: structure/frame/pillar_frame.py
# -----------------------------------------------------------------------------
from typing import List


def build_pillar_frame(pillars: List[dict], pillar_proto, collection):
    """pillars: list of PillarSpec-like dict or dataclass with .coord
    pillar_proto: object returned by components.create_pillar
    collection: bpy collection-like
    """
    created = []
    for p in pillars:
        coord = getattr(p, 'coord', None) or p.get('coord')
        inst = None
        try:
            inst = pillar_proto.copy()
        except Exception:
            inst = type('O', (), {})()
            inst.name = pillar_proto.name + "_inst"
            inst.data = pillar_proto.data
        # 设定位置
        try:
            inst.location = coord
        except Exception:
            inst.location = coord
        # 链接集合
        try:
            collection.objects_link(inst)
        except Exception:
            # Mock: append
            getattr(collection, 'objects', []).append(inst)
        created.append(inst)
    return created