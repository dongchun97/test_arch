# -----------------------------------------------------------------------------
# file: structure/frame/beam_frame.py
# -----------------------------------------------------------------------------
from typing import List


def build_beam_frame(beams: List[dict], beam_proto, collection):
    created = []
    for b in beams:
        start = getattr(b, 'start', None) or b.get('start')
        end = getattr(b, 'end', None) or b.get('end')
        inst = None
        try:
            inst = beam_proto.copy()
        except Exception:
            inst = type('O', (), {})()
            inst.name = beam_proto.name + "_inst"
            inst.data = beam_proto.data
        # 设定位置/长度/方向: 真实环境需计算变换矩阵
        inst.location = ((start[0]+end[0])/2.0, (start[1]+end[1])/2.0, (start[2]+end[2])/2.0)
        try:
            collection.objects_link(inst)
        except Exception:
            getattr(collection, 'objects', []).append(inst)
        created.append(inst)
    return created