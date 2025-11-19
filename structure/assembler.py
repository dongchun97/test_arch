# -----------------------------------------------------------------------------
# file: structure/assembler.py
# -----------------------------------------------------------------------------
from typing import Dict, Any
from structure.utils import ensure_collection
from structure.frames import build_pillar_frame
from structure.frames import build_beam_frame
from structure.frames import build_roof_system


def assemble_building(calc_result, components_objs: Dict[str, object], description_info: Dict[str, Any], name: str = None):
    """主组合函数：将 components 放置并按照 description_info 进行排列。
    calc_result: ComponentCalcResult 或 dict-like
    components_objs: {'pillar': obj, 'beam': obj, 'roof': obj}
    description_info: placement info
    name: collection name
    """
    collection_name = name or description_info.get('name') or 'building'
    coll = ensure_collection(collection_name)

    # 放置柱
    pillars = getattr(calc_result, 'pillars', None) or calc_result.get('pillars')
    beams = getattr(calc_result, 'beams', None) or calc_result.get('beams')
    roof = getattr(calc_result, 'roof', None) or calc_result.get('roof')

    pillar_proto = components_objs['pillar']
    beam_proto = components_objs['beam']
    roof_proto = components_objs['roof']

    created_pillars = build_pillar_frame(pillars, pillar_proto, coll)
    created_beams = build_beam_frame(beams, beam_proto, coll)
    created_roof = build_roof_system(roof, roof_proto, coll)

    # TODO: 根据 description_info 做更复杂的偏移、旋转和合并
    return {
        'collection': coll,
        'pillars': created_pillars,
        'beams': created_beams,
        'roof': created_roof,
    }